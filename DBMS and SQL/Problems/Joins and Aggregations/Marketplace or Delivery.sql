WITH order_stats AS (
    SELECT
        o.shopper_id,
        COUNT(*)                                                            AS total_orders,
        COUNT(CASE WHEN o.status = 'completed' THEN 1 END)                 AS completed_orders,
        COUNT(CASE WHEN o.status = 'completed' AND o.item_count > 20 THEN 1 END) AS large_orders
    FROM orders o
    WHERE o.created_at >= CURRENT_DATE - INTERVAL '90 days'
    GROUP BY o.shopper_id
    HAVING COUNT(CASE WHEN o.status = 'completed' THEN 1 END) >= 20
),
rating_stats AS (
    -- only rate completed orders; left join so NULL avg is preserved for unrated shoppers
    SELECT
        r.shopper_id,
        ROUND(AVG(r.score), 2)                                              AS avg_rating
    FROM ratings r
    JOIN orders o ON r.order_id = o.order_id
    WHERE o.created_at >= CURRENT_DATE - INTERVAL '90 days'
      AND o.status = 'completed'
    GROUP BY r.shopper_id
),
ranked AS (
    SELECT
        s.shopper_id,
        s.name                                                              AS shopper_name,
        s.city,
        os.total_orders,
        os.completed_orders,
        ROUND(os.completed_orders * 100.0 / NULLIF(os.total_orders, 0), 2) AS completion_rate,
        rs.avg_rating,
        ROUND(os.large_orders * 100.0 / NULLIF(os.completed_orders, 0), 2) AS large_order_rate,
        DENSE_RANK() OVER (
            PARTITION BY s.city
            ORDER BY os.completed_orders DESC
        )                                                                   AS city_rank
    FROM order_stats os
    JOIN shoppers s ON os.shopper_id = s.shopper_id
    LEFT JOIN rating_stats rs ON os.shopper_id = rs.shopper_id
)
SELECT *
FROM ranked
ORDER BY city, city_rank;