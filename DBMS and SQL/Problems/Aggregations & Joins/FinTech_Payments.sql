/* You're a data engineer at Stripe. The risk team has flagged an uptick in payment failures and wants to understand failure patterns by merchant and payment method. They need a clean breakdown to prioritize outreach — merchants with high failure rates on specific methods should be contacted first.

merchants
merchant_id PK bigint 
name varchar 
country varchar 
industry varchar 
created_at timestamp

payments
payment_id PK bigint 
merchant_id bigint 
payment_method varchar 
amount decimal 
currency varchar 
status varchar 
failure_reason varchar 
created_at timestamp

Write a query that returns, for each merchant and payment method, a failure rate summary over the last 60 days.
Only include combinations where there were at least 10 total payments. For each row return:
merchant_id
merchant_name
payment_method
total_payments
failed_payments
failure_rate — as a percentage, rounded to 2 dp (e.g. 23.45)
most_common_failure_reason — the single most frequent failure_reason among failed payments; NULL if no failures

The status column values are 'succeeded', 'failed', and 'pending'. Sort output by failure_rate descending.
*/

