/*You're on the growth analytics team at Spotify. The re-engagement team wants to identify lapsed listeners — users who were active in a prior period but have gone silent recently. Before building a model, they need a clean aggregation to understand listening behaviour across two windows.

users 
user_id PK bigint 
country varchar 
plan_type varchar 
created_at timestamp

streams
stream_id PK bigint 
user_id bigint 
track_id bigint 
streamed_at timestamp 
duration_ms bigint 
completed boolean

tracks
track_id PK bigint 
artist_id bigint 
genre varchar 
duration_ms bigint


Write a query that returns one row per user showing their listening behaviour across two non-overlapping 30-day windows:
Recent window: last 30 days
Prior window: 31-60 days ago

For each user return:
user_id
plan_type
recent_streams — stream count in the last 30 days
prior_streams — stream count 31-60 days ago
recent_listen_mins — total minutes streamed in last 30 days, rounded to 2 dp
prior_listen_mins — total minutes streamed 31-60 days ago, rounded to 2 dp
is_lapsed — 1 if prior_streams > 0 and recent_streams = 0, else 0
Include all users who had at least one stream in either window. Users active in both, only recent, or only prior should all appear. Do not include users with zero activity in both windows.
*/
with current_window as (
    select u.user_id, u.plan_type, count(*) as recent_streams, sum(s.duration_ms) as recent_listen_ms
    from streams s
    inner join users u 
    on u.user_id = s.user_id
    where s.streamed_at >= CURRENT_DATE - INTERVAL '30 days'
    group by u.user_id, u.plan_type
),
prior_window as (
    select u.user_id, u.plan_type, count(*) as prior_streams, sum(s.duration_ms) as prior_listen_ms
    from streams s
    inner join users u 
    on u.user_id = s.user_id
    where s.streamed_at >= CURRENT_DATE - INTERVAL '60 days' 
    and s.streamed_at <= CURRENT_DATE - INTERVAL '30 days'
    group by u.user_id, u.plan_type
),
listening_behaviour as (
    select c.user_id, c.plan_type, 
    c.recent_streams, round(c.recent_listen_ms/(1000 * 60), 2) as recent_listen_mins,
    p.prior_streams, round(p.prior_listen_ms/(1000 * 60), 2) as prior_listen_mins,
    case when p.prior_streams > 0 and c.recent_streams = 0 then 1 else 0 end as is_lapsed
    from current_window c 
    full outer join prior_window p 
    on c.user_id = p.user_id
    and c.plan_type = p.plan_type
    where recent_listen_ms != 0 and prior_listen_ms != 0
)
select user_id,
    plan_type,
    recent_streams,
    recent_listen_mins,
    prior_streams,
    prior_listen_mins,
    is_lapsed
from listening_behaviour
order by user_id;


/* Some bugs that would silently corrupt results in production.
Bug 1 — Prior window boundary includes day 30 (overlap with recent window)
streamed_at <= CURRENT_DATE - INTERVAL '30 days' means day-30 rows fall into both windows. Use < not <= for a clean boundary, or use CURRENT_DATE - INTERVAL '31 days' as the upper bound. Windows must be strictly non-overlapping.

Bug 2 — WHERE clause drops users active in only one window
WHERE recent_listen_ms != 0 AND prior_listen_ms != 0 — after a FULL OUTER JOIN, users only in the recent window have prior_listen_ms = NULL, and users only in the prior window have recent_listen_ms = NULL. NULL != 0 evaluates to NULL (not TRUE), so both get filtered out. This removes exactly the lapsed users you're trying to find. Remove this WHERE entirely — the spec's inclusion rule is handled by the FULL OUTER JOIN itself.

Bug 4 — NULL handling in is_lapsed and ROUND after FULL OUTER JOIN
After the FULL OUTER JOIN, c.recent_streams is NULL (not 0) for prior-only users. So c.recent_streams = 0 evaluates to NULL, not TRUE — the CASE returns 0 instead of 1 for lapsed users. Wrap with COALESCE(c.recent_streams, 0). Same issue for ROUND(NULL / ..., 2) — returns NULL cleanly, which is fine, but only if you handle it intentionally.

Warning — joining on plan_type in the FULL OUTER JOIN
Joining on both user_id and plan_type means a user who changed plans between windows gets two rows. A user_id should be unique — join only on user_id and pull plan_type from a single source (the users table, or COALESCE(c.plan_type, p.plan_type)).*/


WITH current_window AS (
    SELECT
        user_id,
        COUNT(*)                                        AS recent_streams,
        SUM(duration_ms)                                AS recent_listen_ms
    FROM streams
    WHERE streamed_at >= CURRENT_DATE - INTERVAL '30 days'
    GROUP BY user_id
),
prior_window AS (
    SELECT
        user_id,
        COUNT(*)                                        AS prior_streams,
        SUM(duration_ms)                                AS prior_listen_ms
    FROM streams
    WHERE streamed_at >= CURRENT_DATE - INTERVAL '60 days'
      AND streamed_at <  CURRENT_DATE - INTERVAL '30 days'
    GROUP BY user_id
),
combined AS (
    SELECT
        COALESCE(c.user_id, p.user_id)                 AS user_id,
        COALESCE(c.recent_streams, 0)                  AS recent_streams,
        COALESCE(p.prior_streams, 0)                   AS prior_streams,
        ROUND(COALESCE(c.recent_listen_ms, 0) / (1000.0 * 60), 2) AS recent_listen_mins,
        ROUND(COALESCE(p.prior_listen_ms, 0) / (1000.0 * 60), 2)  AS prior_listen_mins
    FROM current_window c
    FULL OUTER JOIN prior_window p ON c.user_id = p.user_id
)
SELECT
    cb.user_id,
    u.plan_type,
    cb.recent_streams,
    cb.prior_streams,
    cb.recent_listen_mins,
    cb.prior_listen_mins,
    CASE WHEN cb.prior_streams > 0 AND cb.recent_streams = 0 THEN 1 ELSE 0 END AS is_lapsed
FROM combined cb
JOIN users u ON cb.user_id = u.user_id
ORDER BY cb.user_id;