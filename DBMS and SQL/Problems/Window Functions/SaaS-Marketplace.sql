with applications_base as (
    select job_id, application_id, applied_at, 
    lead(applied_at) over(partition by job_id order by applied_at) as next_application_at
    from applications
),
summarised_applications as (
    select job_id, application_id, applied_at, next_application_at,
    round(extract(epoch from (next_application_at - applied_at)) / 60, 1) as mins_to_next_application,
    row_number() over(partition by job_id order by applied_at ) as application_number,
    -- Concept here is to use window functions to get the running total of applications for each job, and the total number of applications for each job.
    count(*) over(partition by job_id order by applied_at ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as running_total_applications,
    count(*) over(partition by job_id) as total_job_applications
    from applications_base
),
-- percentile must be at job grain — one row per job
job_posting_base as (
    select pos.job_id, pos.category, count(app.application_id) as total_job_applications,
    -- granularity of percentile is at the job level, so we can use percent_rank() to get the percentile of each job's total applications within its category
    round(percent_rank() over(partition by pos.category order by count(app.application_id)) * 100, 1) as category_percentile
    from job_postings pos
    inner join applications app
    on pos.job_id = app.job_id
    group by pos.job_id, pos.category
)
select 
sap.job_id,
pos.category,
sap.application_id,
sap.applied_at,
sap.next_application_at,
sap.mins_to_next_application,
sap.application_number,
sap.running_total_applications,
sap.total_job_applications,
pos.category_percentile
from summarised_applications sap
left join job_posting_base pos
on pos.job_id = sap.job_id
order by sap.job_id, sap.applied_at;