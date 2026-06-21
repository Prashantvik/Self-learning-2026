## Daily SQL learnings 

### 20th June 2026 
#### Aggregation & Joins
1. This query will be run daily by a BI dashboard for every city DoorDash operates in. At 500M rows in orders, what index or partition strategy would you recommend, and where does this query break down first?
500M rows — indexing & where the query breaks
* Your answer : 
Correct Index on created_at is the right instinct — it enables range scan instead of full table scan.
Incomplete A bare index on created_at still reads the whole 90-day slice row by row and filters status after. You want a composite index: (status, created_at) — filter the cheap column first (status is low cardinality), then range on time.
Where it actually breaks at 500M rows
Shuffle / sort cost in the window function. PARTITION BY city ORDER BY total_delivered_value forces the engine to redistribute all rows by city, then sort within each partition. On 500M orders with hundreds of cities, this is an expensive global sort. This is the first thing to fail at scale.
No partition pruning on orders. At this scale, orders should be partitioned by month (or week) on created_at. Without it, even with an index, the engine scans the full table and discards 90%+ of rows.
The JOIN to couriers is a broadcast join risk. If couriers is small (it usually is — maybe 1M rows), most engines broadcast it to all nodes and it's fine. But if you had a very large dimension table, the join would cause data skew.
What you'd actually do in production: partition orders by created_at month, cluster/sort by courier_id, pre-aggregate a daily summary table so the dashboard never touches raw orders.
Senior answer = index + partitioning + pre-aggregation. Not just "add an index."

2. Right now city comes from the couriers table. A PM argues it should come from restaurants instead — "we care about where the food is being picked up, not where the courier lives." Walk me through how that changes the query and whether it changes the results.
* Your answer
Correct Join restaurants on restaurant_id and pull r.city — mechanics right.
Shallow You said "records may change" — true, but you didn't explain why or what it means semantically. An interviewer wants the business impact, not just the join behaviour.
What actually changes and why it matters
Same courier, different city buckets. A courier based in Austin who delivers for a San Antonio restaurant on a busy weekend gets attributed to San Antonio in the restaurant-city model. Their Austin rank is unaffected, their San Antonio rank appears from nowhere. This makes ranking unstable and hard to action (you can't pay out a bonus by city if the courier's city keeps shifting).
Record count doesn't change from the join itself (assuming every order has a valid restaurant_id). What changes is the GROUP BY city — same courier now appears in multiple cities instead of one.
This is a data modeling decision, not a SQL decision. The right answer is: courier city for payout logic (stable identity), restaurant city for demand/supply analysis (where the food originates). The question you should ask your PM is: "what is this ranking used for?"
Interviewers reward candidates who push back with a business question rather than just switching the JOIN column.

3. The growth team now wants this to be a rolling 90-day metric updated hourly, not a nightly batch. How does your approach change? What would you materialize, and at what granularity?
* No answer : The core problem
Running your raw query hourly against 500M rows = full table scan every hour. Extremely expensive. This is why you need incremental + pre-aggregation.
The production pattern
Step 1 — Daily summary table. Each night, aggregate orders into a courier_daily_stats table: one row per (courier_id, city, date) with total_value, order_count. This compresses 500M rows into maybe 5M rows/day.
Step 2 — Hourly incremental. Every hour, append today's new orders (since last run) into courier_daily_stats for today's date partition. Only touch today's data — never rescan history.
Step 3 — Rolling window on the summary table. Your ranking query now hits courier_daily_stats and sums 90 rows per courier (one per day) instead of millions of order rows. Extremely fast.
The tradeoff: you lose sub-day granularity in history. But for a bonus dashboard, daily precision is fine. If you needed real-time, you'd use a streaming pipeline (Kafka → Flink → a materialized view) — but that's a different system.
Pattern to memorize: never rescan raw fact tables for dashboards. Pre-aggregate to a daily grain, then query the aggregate.

#### Notes to take from this problem:
* BETWEEN — always smaller value first, or use >= / <= instead. Safer and more explicit.  
* INTERVAL '90 days' not - 90 — subtracting an integer from a date is dialect-specific and fragile. Use interval literals.  
* Window function ORDER BY — re-read it against the spec every time. It's the most common ranking bug in interviews.  
* INNER JOIN vs LEFT JOIN — left join is not a "safe default." Use it only when you explicitly want NULLs to pass through. On dimension tables like couriers, inner join is almost always correct.  
* Composite index (status, created_at) — low-cardinality filter column first, then range column. This is a standard pattern for time-series filtering.  
* Pre-aggregation pattern — raw fact table → daily summary table → hourly incremental append → dashboard queries the summary. This is the answer to almost every "how would you scale this" question on reporting workloads.  


#### Aggregation & Joins - Streaming
1. The re-engagement team now wants is_lapsed broken out by genre — they want to know which genres lapsed users were listening to in their prior window. How does your query change, and what does that do to the grain of your output?
```
WITH base AS (
    -- join tracks once, branch into windows from here
    SELECT
        s.user_id,
        t.genre,
        s.duration_ms,
        s.completed,
        s.streamed_at
    FROM streams s
    JOIN tracks t ON s.track_id = t.track_id
),
current_window AS (
    SELECT user_id, genre, COUNT(*) AS recent_streams, SUM(duration_ms) AS recent_listen_ms
    FROM base
    WHERE streamed_at >= CURRENT_DATE - INTERVAL '30 days'
    GROUP BY user_id, genre
),
prior_window AS (
    SELECT user_id, genre, COUNT(*) AS prior_streams, SUM(duration_ms) AS prior_listen_ms
    FROM base
    WHERE streamed_at >= CURRENT_DATE - INTERVAL '60 days'
      AND streamed_at <  CURRENT_DATE - INTERVAL '30 days'
    GROUP BY user_id, genre
),
combined AS (
    SELECT
        COALESCE(c.user_id, p.user_id)                              AS user_id,
        COALESCE(c.genre, p.genre)                                  AS genre,
        COALESCE(c.recent_streams, 0)                               AS recent_streams,
        COALESCE(p.prior_streams, 0)                                AS prior_streams,
        ROUND(COALESCE(c.recent_listen_ms, 0) / (1000.0 * 60), 2)  AS recent_listen_mins,
        ROUND(COALESCE(p.prior_listen_ms, 0) / (1000.0 * 60), 2)   AS prior_listen_mins
    FROM current_window c
    FULL OUTER JOIN prior_window p
        ON c.user_id = p.user_id AND c.genre = p.genre  -- grain is (user, genre)
)
SELECT
    cb.user_id,
    u.plan_type,
    cb.genre,                                                       -- from combined, not users
    cb.recent_streams,
    cb.prior_streams,
    cb.recent_listen_mins,
    cb.prior_listen_mins,
    CASE WHEN cb.prior_streams > 0 AND cb.recent_streams = 0 THEN 1 ELSE 0 END AS is_lapsed
FROM combined cb
JOIN users u ON cb.user_id = u.user_id
ORDER BY cb.user_id, cb.genre;
```

2. This query defines lapsed as "zero streams in the last 30 days." A PM argues that's too strict — a user who streamed once for 30 seconds shouldn't count as active. How would you add a minimum engagement threshold, and what column would you use?
* completed = TRUE is a clean, defensible threshold, this condition will go into the base cte we'll exclude the records during the base table

3. You're asked to schedule this query to populate a lapsed_users table daily. Two days later, a user who was lapsed streams again — they're no longer lapsed. How do you handle that in the table?
* Daily summary + hourly incremental is the right architecture. But the interviewer is asking specifically about the lapsed_users table — a user was marked lapsed, then came back. How does the row change?    
Missing — the SCD/upsert answer  : The complete answer: on each daily run, re-evaluate is_lapsed for all users and upsert (UPDATE if exists, INSERT if new). A re-activated user gets is_lapsed = 0 overwritten. If you need history (when did they lapse, when did they return), you'd use an SCD Type 2 pattern — add a row with the new state and a valid_from/valid_to timestamp. This is Phase 7 territory, but knowing the term earns points.


#### Notes to take from this problem:
* FULL OUTER JOIN NULL discipline — after any FULL OUTER JOIN, every column from both sides can be NULL for unmatched rows. Audit every WHERE, CASE, and arithmetic expression that touches those columns. COALESCE to 0 before math, not after.
* Window boundary operators — use >= on the lower bound and < on the upper bound. BETWEEN and <= cause off-by-one overlaps on time windows. Make it a habit: >= start AND < end.
* Join late, join once — pull dimension attributes (plan_type, name, city) in the final SELECT, not inside aggregation CTEs. Joining early means the engine drags extra columns through GROUP BY and potentially scans the dimension table multiple times.
* Integer division — whenever dividing by a constant, make at least one operand a float literal (1000.0, not 1000). Silent truncation is one of the hardest bugs to spot in output.
* The right structural instincts — the gaps are mostly NULL discipline and keeping JOIN keys consistent with GROUP BY grain


### 21st June 2026 
#### 