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