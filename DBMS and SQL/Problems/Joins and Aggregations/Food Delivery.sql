-- Note : city comes from couriers, not restaurants — a courier's home city is stable, restaurant city would shift if 
-- they delivered across city lines.
WITH base_stats AS (
    SELECT
        c.courier_id,
        c.name                                      AS courier_name,
        c.city,
        o.order_total + o.tip_amount                AS order_value
    FROM orders o
    JOIN couriers c ON o.courier_id = c.courier_id
    WHERE o.status = 'delivered'
      AND o.created_at >= CURRENT_DATE - INTERVAL '90 days'
),
summarised AS (
    SELECT
        city,
        courier_id,
        courier_name,
        SUM(order_value)                            AS total_delivered_value,
        COUNT(*)                                    AS order_count,
        ROUND(AVG(order_value), 2)                  AS avg_order_value
    FROM base_stats
    GROUP BY city, courier_id, courier_name
),
ranked AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY city
            ORDER BY total_delivered_value DESC,
                     order_count DESC,
                     courier_id ASC
        ) AS city_rank
    FROM summarised
)
SELECT
    city,
    courier_name,
    total_delivered_value,
    order_count,
    avg_order_value,
    city_rank
FROM ranked
WHERE city_rank <= 3
ORDER BY city, city_rank;