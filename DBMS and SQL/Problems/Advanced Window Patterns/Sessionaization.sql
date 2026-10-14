with events_base as (
    select 
        user_id,
        event_id,
        occured_at as occurred_at,
        lag(occurred_at) over (partition by user_id order by occurred_at) as prev_occurred_at
    from events
),
-- Note: we consider a new session to start if the gap between consecutive events is more than 30 minutes
session_flags as (
    select 
            user_id, 
            event_id, 
            occurred_at, 
            prev_occurred_at,
            case when prev_occurred_at is null then 1
                 when extract(epoch from (occurred_at - prev_occurred_at)) / 60 > 30 
            then 1 else 0 
            end as is_session_start
    from events_base
),
-- In the sessionaization cte, we determine the actual session start and end times based on the identified gaps
-- Session assignment and aggregation steps had fundamental issues | Forgot this step altogether in the original solution. 
-- Step 3: running sum of flags assigns session number — increments exactly at each session boundary
session_labeled as (
    select
        user_id,
        event_id,
        event_type,
        occurred_at,
        sum(is_session_start) over (
            partition by user_id
            order by occurred_at
            rows between unbounded preceding and current row
        ) as session_num
    from session_flags
),
-- Step 4: aggregate to session grain
sessions as (
    select
        user_id,
        session_num                                     as session_id,
        min(occurred_at)                                as session_start,
        max(occurred_at)                                as session_end,
        count(*)                                        as event_count,
        count(distinct event_type)                      as unique_event_types
    from session_labeled
    group by user_id, session_num
)
select
    user_id,
    session_id,
    session_start,
    session_end,
    round(extract(epoch from (session_end - session_start)) / 60, 1) as session_duration_mins,
    event_count,
    unique_event_types
from sessions
order by user_id, session_id;