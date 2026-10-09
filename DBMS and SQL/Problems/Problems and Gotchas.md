# Problem Statements
- https://docs.google.com/document/d/1lgiPto2Q4XbT7gm559sR8YXphUKxGTF64kyv-5FhfhI/edit

# Learnings and gotchas
- Read problem statement with focus, re-read and cross check before submitting  

## Problem 1 : Food Delivery | Notes to take
- Use of filtering created_at >= CURRENT_DATE - INTERVAL '90 days'
- The full tie-break chain in case of ordering 
- BETWEEN — always smaller value first, or use >= / <= instead. Safer and more explicit.
- INTERVAL '90 days' not - 90 — subtracting an integer from a date is dialect-specific and fragile. Use interval literals.
- Window function ORDER BY — re-read it against the spec every time. It's the most common ranking bug in interviews.
- INNER JOIN vs LEFT JOIN — left join is not a "safe default." Use it only when you explicitly want NULLs to pass through. On dimension tables like couriers, inner join is almost always correct.
- Composite index (status, created_at) — low-cardinality filter column first, then range column. This is a standard pattern for time-series filtering.
- Pre-aggregation pattern — raw fact table → daily summary table → hourly incremental append → dashboard queries the summary. This is the answer to almost every "how would you scale this" question on reporting workloads.

### Follow-up Questions:
#### 1. This query will be run daily by a BI dashboard for every city DoorDash operates in. At 500M rows in orders, what index or partition strategy would you recommend, and where does this query break down first?
Ans. Shuffle / sort cost in the window function. PARTITION BY city ORDER BY total_delivered_value forces the engine to redistribute all rows by city, then sort within each partition. On 500M orders with hundreds of cities, this is an expensive global sort. This is the first thing to fail at scale.  
No partition pruning on orders. At this scale, orders should be partitioned by month (or week) on created_at. Without it, even with an index, the engine scans the full table and discards 90%+ of rows.  
The JOIN to couriers is a broadcast join risk. If couriers is small (it usually is — maybe 1M rows), most engines broadcast it to all nodes and it's fine. But if you had a very large dimension table, the join would cause data skew.
What you'd actually do in production: partition orders by created_at month, cluster/sort by courier_id, pre-aggregate a daily summary table so the dashboard never touches raw orders.  
Senior answer = index + partitioning + pre-aggregation. Not just "add an index."  

#### 2. Right now city comes from the couriers table. A PM argues it should come from restaurants instead — "we care about where the food is being picked up, not where the courier lives." Walk me through how that changes the query and whether it changes the results.  
Ans. Same courier, different city buckets. A courier based in Austin who delivers for a San Antonio restaurant on a busy weekend gets attributed to San Antonio in the restaurant-city model. Their Austin rank is unaffected, their San Antonio rank appears from nowhere. This makes ranking unstable and hard to action (you can't pay out a bonus by city if the courier's city keeps shifting).  
Record count doesn't change from the join itself (assuming every order has a valid restaurant_id). What changes is the GROUP BY city — same courier now appears in multiple cities instead of one.  
This is a data modeling decision, not a SQL decision. The right answer is: courier city for payout logic (stable identity), restaurant city for demand/supply analysis (where the food originates). The question you should ask your PM is: "what is this ranking used for?"  
Interviewers reward candidates who push back with a business question rather than just switching the JOIN column.  

#### 3. The growth team now wants this to be a rolling 90-day metric updated hourly, not a nightly batch. How does your approach change? What would you materialize, and at what granularity?
Ans. 
Step 1 — Daily summary table. Each night, aggregate orders into a courier_daily_stats table: one row per (courier_id, city, date) with total_value, order_count. This compresses 500M rows into maybe 5M rows/day.  
Step 2 — Hourly incremental. Every hour, append today's new orders (since last run) into courier_daily_stats for today's date partition. Only touch today's data — never rescan history.  
Step 3 — Rolling window on the summary table. Your ranking query now hits courier_daily_stats and sums 90 rows per courier (one per day) instead of millions of order rows. Extremely fast.  
The tradeoff: you lose sub-day granularity in history. But for a bonus dashboard, daily precision is fine. If you needed real-time, you'd use a streaming pipeline (Kafka → Flink → a materialized view) — but that's a different system.  
Pattern to memorize: never rescan raw fact tables for dashboards. Pre-aggregate to a daily grain, then query the aggregate.  


## Problem 2 : Streaming | Notes to take
- FULL OUTER JOIN NULL discipline — after any FULL OUTER JOIN, every column from both sides can be NULL for unmatched rows. Audit every WHERE, CASE, and arithmetic expression that touches those columns. COALESCE to 0 before math, not after.
- Window boundary operators — use >= on the lower bound and < on the upper bound. BETWEEN and <= cause off-by-one overlaps on time windows. Make it a habit: >= start AND < end.
- Join late, join once — pull dimension attributes (plan_type, name, city) in the final SELECT, not inside aggregation CTEs. Joining early means the engine drags extra columns through GROUP BY and potentially scans the dimension table multiple times.
- Integer division — whenever dividing by a constant, make at least one operand a float literal (1000.0, not 1000). Silent truncation is one of the hardest bugs to spot in output. 

### Follow-up Questions:
#### 1. The re-engagement team now wants is_lapsed broken out by genre — they want to know which genres lapsed users were listening to in their prior window. How does your query change, and what does that do to the grain of your output?
Correct — joined tracks to get genre, added to GROUP BY
Right instinct. Genre lives in tracks, so joining it in both window CTEs is the correct approach. Adding it to GROUP BY user_id, genre correctly changes the grain.  
Bug 1 — FULL OUTER JOIN still only on user_id (genre gets crossed)
You join ON c.user_id = p.user_id but the grain is now (user_id, genre). A user who listened to Pop in the recent window and Jazz in the prior window will get a cross-match — Pop row joins to Jazz row because user_id matches. You need ON c.user_id = p.user_id AND c.genre = p.genre.  
Bug 2 — SELECT references u.genre which doesn't exist on users table
users has no genre column — genre comes from combined via tracks. Should be cb.genre, not u.genre.  
Warning — tracks joined twice, scanning it in both CTEs  
At scale you're joining tracks twice. A cleaner approach: pre-join streams to tracks once in a base CTE, then branch into the two windows from there. Halves the join cost.  
Warning — is_lapsed at genre grain needs rethinking
is_lapsed now fires per (user_id, genre) — a user is "lapsed in Jazz" but active in Pop. That's a valid product metric, but you should flag to the interviewer that the definition has changed and confirm if that's intended.  

#### 2. This query defines lapsed as "zero streams in the last 30 days." A PM argues that's too strict — a user who streamed once for 30 seconds shouldn't count as active. How would you add a minimum engagement threshold, and what column would you use?  
completed = TRUE is a clean, defensible threshold. Good instinct. But the answer needs to say where this filter goes — a WHERE clause in the window CTEs: WHERE completed = TRUE, so only completed streams count toward active status. One sentence of placement is what separates a complete answer from a vague one

#### 3. You're asked to schedule this query to populate a lapsed_users table daily. Two days later, a user who was lapsed streams again — they're no longer lapsed. How do you handle that in the table?
Daily summary + hourly incremental is the right architecture. But the interviewer is asking specifically about the lapsed_users table — a user was marked lapsed, then came back. How does the row change?  
Missing — the SCD/upsert answer  
The complete answer: on each daily run, re-evaluate is_lapsed for all users and upsert (UPDATE if exists, INSERT if new). A re-activated user gets is_lapsed = 0 overwritten. If you need history (when did they lapse, when did they return), you'd use an SCD Type 2 pattern — add a row with the new state and a valid_from/valid_to timestamp. This is Phase 7 territory, but knowing the term earns points.


## Problem 3 : FinTech/Payments | Notes to take
- Pattern: MODE() — simplest where supported
Some dialects (PostgreSQL) have MODE() WITHIN GROUP (ORDER BY failure_reason) — returns the most frequent value in a group directly. Cleanest syntax, but not ANSI and not available in BigQuery/Snowflake/Redshift.
- Pattern: Window function inside a subquery (most portable)
In a subquery, rank failure_reasons per (merchant_id, payment_method) by count descending using ROW_NUMBER(), then join back and filter where rank = 1. Works in every major dialect.
- Common mistake — nesting aggregates (illegal in SQL)
MAX(COUNT(failure_reason)) is not valid SQL. You cannot aggregate an aggregate in a single SELECT. You must use a subquery or CTE to pre-count, then take the max.
- HAVING filters aggregated results — WHERE filters raw rows. Never try to put a COUNT() condition in a WHERE clause. This comes up in nearly every interview.
- Most-frequent-value-per-group pattern — pre-count in a CTE, apply ROW_NUMBER() OVER (PARTITION BY ... ORDER BY COUNT(*) DESC), join back filtering rank = 1. Memorize this shape.
- NULLIF(denominator, 0) — standard guard against division-by-zero. Always wrap dynamic denominators with it.
- LEFT JOIN to bring in optional enrichment — when a subquery or CTE may have no matching row for some groups (zero failures, no activity), use LEFT JOIN to preserve the parent row with NULLs rather than silently dropping it.
- Denominator decisions are business decisions — always state your assumption about what counts as the denominator (all payments? only settled? only attempts?). Interviewers reward candidates who flag this rather than silently picking one.

### Follow-up Questions : 
#### - 



## Problem 4 : Marketplace/Delivery | Notes to take
- ROW_NUMBER vs RANK vs DENSE_RANK — commit this to memory permanently:
- ROW_NUMBER() → always unique, no ties (1, 2, 3, 4)
- RANK() → ties get same number, next rank skips (1, 2, 2, 4)
- DENSE_RANK() → ties get same number, no gaps (1, 2, 2, 3)
"No gaps" in the spec = DENSE_RANK. Every time.
- Aggregate CTEs should not carry dimension columns — group only on the key (shopper_id), join dimension tables (shoppers) at the final step. This keeps aggregation CTEs reusable and avoids GROUP BY bloat.
- Separate enrichment CTEs — when a metric comes from a different table (ratings vs orders), give it its own CTE. Don't try to join everything in one pass. Clean separation = easier to debug and extend.
- Denominator discipline — completion_rate denominator is total_orders; large_order_rate denominator is completed_orders. Always re-read the spec definition before writing the division. Wrap every denominator in NULLIF(..., 0).
- Multiply before dividing for percentages — value * 100.0 / denominator, not value / denominator * 100.0. Integer division truncates silently.


## Problem 5 : Marketplace/Delivery | Notes to take
- LAG(col, 1) and LAG(col) are identical — the offset defaults to 1. Knowing this signals fluency.
- CASE branch order matters for NULLs — always put WHEN col IS NULL THEN NULL first if NULL is a meaningful distinct state from the other conditions.
- DATE_TRUNC('week', ...) snaps to Monday in PostgreSQL/Snowflake/BigQuery. In Redshift, DATE_TRUNC('week', date) also returns Monday. In SQL Server you'd use DATETRUNC or a DATEADD/DATEDIFF trick. Know the dialect.
- LAG across sparse data — LAG() looks at the previous row in the result set, not the previous calendar period. If week 2 is missing, week 3's LAG returns week 1. This is correct when sparse data is intentional; when you need true week-over-week comparisons including zero-earning weeks, you need a calendar spine joined in — a Phase 3 pattern.
- 12-week boundary — DATE_TRUNC('week', CURRENT_DATE) - INTERVAL '12 weeks' anchors to the start of the window week, not mid-week. Using CURRENT_DATE - INTERVAL '84 days' would give a ragged start depending on today's day of week. Always truncate to the period boundary first.

### Follow-up Questions : 
#### 1. A driver who earned $800 in week 1 then had zero trips in weeks 2 and 3, then earned $600 in week 4 — what does your query return for week 4's prev_week_earnings and earnings_change? Is that the right behaviour for the churn model?
Two ways to fix it: Option 1 — fill missing weeks with a calendar spine and COALESCE(earnings, 0), so the gap weeks show as $0 and the model sees the true drop.  
Option 2 — add a weeks_since_last_active column using DATEDIFF(week_start, LAG(week_start)), and let the model treat gaps > 1 week differently. Which fix is right depends on the model — flag both to the interviewer.  
Senior answer = mechanics + business consequence + two remediation options.

#### 2. The team now wants a 3-week rolling average of earnings alongside the weekly figure. How does your query change, and which window function do you reach for?

Exactly right. AVG(weekly_earnings) OVER (PARTITION BY driver_id ORDER BY week_start ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) is the correct frame.  
The frame syntax — know all variants  
- ROWS BETWEEN 2 PRECEDING AND CURRENT ROW -- 3-row rolling (current + 2 back)  
- ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING -- centred 3-row window  
- ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW -- running total/avg  
- RANGE BETWEEN INTERVAL '7' DAY PRECEDING AND CURRENT ROW time-based

ROWS vs RANGE: ROWS counts physical rows — always use this for rolling metrics. RANGE includes all rows with the same ORDER BY value as the current row — dangerous with ties, can silently include more rows than expected.  
Sparse data caveat: on a driver missing week 2, ROWS BETWEEN 2 PRECEDING averages weeks 1 and 3 — not a true 3-week average. If you need calendar-accurate rolling windows, you need the spine first.  
Perfect answer. The ROWS vs RANGE distinction is a common senior-level follow-up — keep it in your notes.

#### 3. At 50M drivers each with 52 weeks of data, the window function sorts 2.6B rows. What does the execution plan look like and what would you do to make this faster in a warehouse like Snowflake or BigQuery?
What the execution plan actually looks like : 
- Step 1 — Partition scan. Filter completed_at for 12 weeks. With clustering on completed_at, the engine prunes micro-partitions and scans maybe 5–10% of the table instead of all 2.6B rows. Without clustering, full scan.
- Step 2 — Shuffle by driver_id. PARTITION BY driver_id forces the engine to redistribute all rows so each driver's rows land on the same node. At 50M drivers this is a massive shuffle — the most expensive step.
- Step 3 — Sort within partition. ORDER BY week_start sorts each driver's rows. At ~52 rows per driver this is cheap per partition, but it's still 2.6B row-sorts total.

What you'd actually do : 
- Pre-aggregate to a daily/weekly summary table. Instead of running this against raw trips (2.6B rows), pre-aggregate to a driver_weekly_earnings table (~50M drivers × 52 weeks = 2.6B → compressed to ~2.6B rows pre-aggregated, but each row is far cheaper to shuffle since there's no fare/tip detail). Window functions on the summary table are dramatically faster.
- Cluster on (driver_id, completed_at) in Snowflake — co-locates a driver's trips in the same micro-partitions, reducing shuffle distance. In BigQuery, partition on DATE(completed_at) and cluster on driver_id.
- Materialise the window function output. The rolling avg and LAG results don't change for past weeks — only the most recent week is new. Incremental append: compute the new week, append to the materialised table, never recompute history. 

##### The pattern: scan cost → clustering. Shuffle cost → pre-aggregation + incremental. Sort cost → pre-aggregate to reduce row count before the window. All three levers together

## Problem 5 : Marketplace/Delivery | Notes to take
- Stacking window functions across CTEs — the pattern is: aggregate in CTE 1 → apply ranking windows in CTE 2 → apply LAG/LEAD on those ranks in CTE 3 → apply running totals in the final SELECT. You can't compute LAG on a rank in the same CTE where the rank is defined — the window functions execute at the same logical step.
- Running SUM default frame — SUM(x) OVER (PARTITION BY ... ORDER BY ...) without an explicit frame defaults to ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW in all major dialects. This is the running total behaviour. You don't need to write the frame explicitly, but knowing the default prevents surprises.
- Rank direction convention — lower number = better rank. prev - current = positive means rank number decreased = moved up. Always re-read "positive = moved up" against the subtraction direction before writing it.
- Alias discipline under pressure — when copying CTE names, always verify the alias in scope matches what you reference. A single wrong alias letter fails at runtime silently until execution.

### Follow-up Questions : 
Note : Good instincts on both — but both have implementation gaps that would trip you up in a real interview

#### 1. A seller who was ranked #2 in Electronics in January but had zero completed orders in February — do they appear in February's output? Should they? How would you change the query if the team wants to show them with NULL revenue and their January rank carried forward?
Term : Calendar spine for missing months  

- Join is backwards. You wrote FROM SERIES_MONTH LEFT JOIN ORDERS then immediately filter WHERE O.STATUS = 'completed'. A WHERE clause on the right-side table of a LEFT JOIN converts it to an INNER JOIN — the NULLs you want for missing months get filtered out. The status filter must move to the JOIN condition: LEFT JOIN ORDERS O ON ... AND O.STATUS = 'completed'.
- Spine only gives you months — not (seller, category, month) combinations. If you join the spine to orders, months where a seller had zero orders produce no seller_id or category — you GROUP BY O.SELLER_ID which is NULL, collapsing all absent sellers into one NULL row. You need a seller_category spine too: cross join all distinct (seller_id, category) pairs with all months, then left join orders onto that three-column key.
- SUM(O.REVENUE) on NULLs returns NULL, not 0. Wrap with COALESCE(ROUND(SUM(O.REVENUE), 2), 0) for months with no orders.

**Build the spine as (seller, category) x month**
```
WITH seller_categories AS (
    SELECT DISTINCT seller_id, category FROM orders
    WHERE EXTRACT(YEAR FROM created_at) = EXTRACT(YEAR FROM CURRENT_DATE)
),
month_spine AS (
    SELECT DATE_TRUNC('month', created_at) AS month
    FROM orders
    WHERE EXTRACT(YEAR FROM created_at) = EXTRACT(YEAR FROM CURRENT_DATE)
    GROUP BY 1
),
spine AS (
    SELECT sc.seller_id, sc.category, ms.month
    FROM seller_categories sc
    CROSS JOIN month_spine ms
)
SELECT sp.seller_id, sp.category, sp.month,
    COALESCE(ROUND(SUM(o.revenue), 2), 0) AS monthly_revenue
FROM spine sp
LEFT JOIN orders o
    ON  sp.seller_id = o.seller_id
    AND sp.category  = o.category
    AND sp.month     = DATE_TRUNC('month', o.created_at)
    AND o.status     = 'completed'
GROUP BY sp.seller_id, sp.category, sp.month
```

Key rule: filters on the right-side table of a LEFT JOIN always go in the ON clause, never in WHERE. WHERE runs after the join and kills your NULLs.

#### 2. The promoted listings algorithm wants to weight sellers who have been consistently in the top 3 for at least 3 consecutive months. How would you identify those sellers using what you already have here?
Note : Pattern: compute window functions in a CTE, filter in the outer query. Never filter on a column alias defined in the same SELECT.

```
WITH TOP_SELLERS AS (
SELECT 
    SELLER_ID,
    SELLER_NAME,
    CATEGORY,
    MONTH,
    CATEGORY_RANK,
    LAG(CATEGORY_RANK, 1) OVER(PARTITION BY SELLER_ID, CATEGORY ORDER BY MONTH) AS PREV_MONTH_RANK,
    LAG(CATEGORY_RANK, 2) OVER(PARTITION BY SELLER_ID, CATEGORY ORDER BY MONTH) AS SECOND_PREV_MONTH_RANK
FROM AGGREGATED_RANKED_TABLE
)
SELECT 
    SELLER_ID,
    SELLER_NAME,
    CATEGORY
FROM TOP_SELLERS
WHERE CATEGORY_RANK <= 3
AND PREV_MONTH_RANK <= 3
AND SECOND_PREV_MONTH_RANK <= 3
AND PREV_MONTH_RANK IS NOT NULL   -- ensures 3 months of data exist
AND SECOND_PREV_MONTH_RANK IS NOT NULL;
```

## Problem 6 : SaaS/Marketplace | Notes to take
- 




