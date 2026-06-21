/*You're a data engineer at DoorDash. The growth team wants to understand courier efficiency — specifically, 
which couriers are carrying the most value per trip and how that compares to their peers. This will feed
a tiering model for bonus payouts.

Schema : 
orders
order_id PK bigint
courier_id bigint
restaurant_id bigint
order_total decimal
tip_amount decimal
status varchar
created_at timestamp
delivered_at timestamp

couriers
courier_id PK bigint 
name varchar 
city varchar 
vehicle_type varchar 
joined_at date

restaurants
restaurant_id PK bigint 
name varchar 
city varchar 
cuisine_type varchar

Write a query that returns, for each city, the top 3 couriers by total delivered order value (order_total + tip_amount) 
in the last 90 days.
Include only delivered orders. For each courier return:
city
courier_name
total_delivered_value
order_count
avg_order_value — rounded to 2 decimal places
city_rank — their rank within the city
Tie-break: if two couriers have the same total value, rank by order_count descending, then by courier_id ascending. 
*/


with base_stats as (
    select c.courier_id, c.city, c.name, 
    o.order_total + o.tip_amount as total_order_values
    from orders o 
    -- decide joining condition properly inner join not left | nulls for unmatched records
    inner join couriers c 
    on o.courier_id = c.courier_id
    where o.status = 'delivered'
    -- learn to use date filters, ANSI
    AND o.created_at >= CURRENT_DATE - INTERVAL '90 days'
),
summarised as (
    select courier_id, city, name, 
    sum(total_order_values) as total_delivered_value, 
    count(*) as order_count,
    round(avg(total_order_values), 2) as avg_order_value
    from base_stats
    group by city, name, courier_id
),
ranked_stats as (
    select city, 
    name as courier_name, 
    total_delivered_value, 
    order_count, 
    avg_order_value,
    -- ranking properly, re-read the problem — the full tie-break chain.
    row_number() over(partition by city order by total_delivered_value desc, order_count desc, courier_id asc) as city_rank
    from summarised
)
select city, 
    courier_name, 
    total_delivered_value, 
    order_count, 
    avg_order_value, 
    city_rank
from ranked_stats
where city_rank <= 3
order by cuty, city_rank;

-- Note : city comes from couriers, not restaurants — a courier's home city is stable, restaurant city would shift if 
-- they delivered across city lines.