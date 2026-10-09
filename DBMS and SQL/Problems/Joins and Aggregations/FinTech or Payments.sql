WITH payment_stats AS (
    SELECT
        p.merchant_id,
        p.payment_method,
        COUNT(*)                                                        AS total_payments,
        COUNT(*) FILTER (WHERE p.status = 'failed')                     AS failed_payments,
        -- exclude pending from denominator
        COUNT(*) FILTER (WHERE p.status IN ('succeeded', 'failed'))     AS settled_payments
    FROM payments p
    WHERE p.created_at >= CURRENT_DATE - INTERVAL '60 days'
    GROUP BY p.merchant_id, p.payment_method
    HAVING COUNT(*) >= 10
),
failure_reasons AS (
    -- rank failure reasons per (merchant, method) by frequency
    SELECT
        merchant_id,
        payment_method,
        failure_reason,
        ROW_NUMBER() OVER (
            PARTITION BY merchant_id, payment_method
            ORDER BY COUNT(*) DESC
        )                                                               AS reason_rank
    FROM payments
    WHERE status = 'failed'
      AND created_at >= CURRENT_DATE - INTERVAL '60 days'
    GROUP BY merchant_id, payment_method, failure_reason
)
SELECT
    ps.merchant_id,
    m.name                                                              AS merchant_name,
    ps.payment_method,
    ps.total_payments,
    ps.failed_payments,
    ROUND(
        ps.failed_payments * 100.0 / NULLIF(ps.settled_payments, 0),
    2)                                                                  AS failure_rate,
    fr.failure_reason                                                   AS most_common_failure_reason
FROM payment_stats ps
JOIN merchants m ON ps.merchant_id = m.merchant_id
LEFT JOIN failure_reasons fr
    ON ps.merchant_id = fr.merchant_id
    AND ps.payment_method = fr.payment_method
    AND fr.reason_rank = 1
ORDER BY failure_rate DESC;