-- step 1: assign every user their cohort week
with cohort_base as (
    select
        user_id,
        date_trunc('week', created_at)::date as cohort_week
    from users
),

-- step 2: count users per cohort — denominator for retention rate
cohort_sizes as (
    select
        cohort_week,
        count(*) as cohort_size
    from cohort_base
    group by cohort_week
),

-- step 3: all real activity rows, mapped to (cohort_week, week_number)
activity_mapped as (
    select
        cb.cohort_week,
        cb.user_id,
        date_trunc('week', a.occurred_at)::date as activity_week,
        (date_trunc('week', a.occurred_at)::date - cb.cohort_week) / 7 as week_number
    from cohort_base cb
    join activity a on cb.user_id = a.user_id
    where a.occurred_at >= cb.cohort_week::timestamp   -- no activity before signup
),

-- step 4: guarantee week 0 for every user (signup = active by definition)
-- union with real activity so week 0 never drops below 100%
all_activity as (
    select cohort_week, user_id, 0 as week_number
    from cohort_base                                   -- synthetic week 0 rows
    union                                              -- union deduplicates
    select cohort_week, user_id, week_number
    from activity_mapped
),

-- step 5: count distinct active users per cohort + week offset
retention as (
    select
        cohort_week,
        week_number,
        count(distinct user_id) as active_users
    from all_activity
    group by cohort_week, week_number
)

-- step 6: join cohort sizes and compute retention rate
select
    r.cohort_week,
    r.week_number,
    cs.cohort_size,
    r.active_users,
    round(r.active_users * 100.0 / cs.cohort_size, 1) as retention_rate
from retention r
join cohort_sizes cs on r.cohort_week = cs.cohort_week
order by r.cohort_week, r.week_number;