WITH fare_base AS (
    SELECT
        t.driver_id,
        DATE_TRUNC('week', t.completed_at)              AS week_start,
        ROUND(SUM(t.fare_amount + t.tip_amount), 2)     AS weekly_earnings
    FROM trips t
    WHERE t.status = 'completed'
      AND t.completed_at >= DATE_TRUNC('week', CURRENT_DATE) - INTERVAL '12 weeks'
    GROUP BY t.driver_id, DATE_TRUNC('week', t.completed_at)
),
aggregated AS (
    SELECT
        driver_id,
        week_start,
        weekly_earnings,
        LAG(weekly_earnings) OVER (
            PARTITION BY driver_id
            ORDER BY week_start
        )                                               AS prev_week_earnings
    FROM fare_base
)
SELECT
    driver_id,
    week_start,
    weekly_earnings,
    prev_week_earnings,
    weekly_earnings - prev_week_earnings                AS earnings_change,
    CASE
        WHEN prev_week_earnings IS NULL              THEN NULL
        WHEN weekly_earnings > prev_week_earnings    THEN 'up'
        WHEN weekly_earnings < prev_week_earnings    THEN 'down'
        ELSE 'flat'
    END                                                 AS change_direction
FROM aggregated
ORDER BY driver_id, week_start;