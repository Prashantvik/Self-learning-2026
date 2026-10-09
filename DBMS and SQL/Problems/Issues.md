
### Syntax — always costs points, never should : 

#### Trailing comma before FROM
SUM(x) AS col,  ← FROM table — syntax error in all dialects. Hit this on Day 1, Day 3, Day 4. Fix: read the last column before FROM every time you write a SELECT.

#### CTE syntax: missing AS
WITH cte_name(SELECT ...) is invalid. Must be WITH cte_name AS (SELECT ...). Parentheses wrap the SELECT; AS connects the name to them.

#### Wrong alias in final SELECT
Referencing A.SELLER_ID when the alias in scope is S. Copy-paste error — always verify alias names match the FROM/JOIN they reference.

#### ORDER BY inside a CTE
Not valid in most dialects. ORDER BY belongs only in the outermost SELECT. Inside a CTE it is either ignored or throws an error.

### Logic — silent failures, hardest to catch
#### BETWEEN with inverted bounds
BETWEEN current_date AND current_date - 90 — returns zero rows because the range is empty. BETWEEN requires lower bound first. Use >= start AND < end instead — explicit and safe.

#### Integer division truncates silently
completed / total * 100 — if both are integers, division happens first and truncates to 0. Always multiply by 100.0 before dividing, or cast: completed * 100.0 / NULLIF(total, 0).

#### Wrong denominator in rate calculations
large_order_rate used total_orders instead of completed_orders. Always re-read "% of X" — X is your denominator, not whatever is convenient.

#### Wrong metric in ORDER BY of window function
Day 1: ranked by order_count when spec said rank by total_value. Re-read the window ORDER BY against the spec before submitting — this is the most common ranking bug.

#### Window boundary overlap
streamed_at <= CURRENT_DATE - INTERVAL '30 days' — day 30 falls in both windows. Always use < for the upper bound of a window to keep boundaries strictly non-overlapping.

#### ELSE NULL in CASE is redundant
CASE WHEN x THEN 1 ELSE NULL END — NULL is the default. Write CASE WHEN x THEN 1 END. Signals SQL fluency.

#### Interval arithmetic: use INTERVAL, not integers
CURRENT_DATE - 90 subtracts 90 from the date integer in some dialects and errors in others. Always write CURRENT_DATE - INTERVAL '90 days' for portability.


Five tabs — work through all of them. The checklist tab is the one to run before submitting any query in a real interview.

**The three patterns that tripped you most across Phase 1 and 2, in order of frequency:**

First — NULL discipline after joins. It came up in almost every problem. The fix is mechanical: after every JOIN, write down which columns can be NULL and trace each through every CASE, WHERE, and arithmetic expression below it. Takes 10 seconds and saves every time.

Second — syntax under pressure. Trailing commas, wrong aliases, missing AS in CTEs. These aren't knowledge gaps — they're execution gaps. The fix: write the CTE skeleton first (name, FROM, WHERE, GROUP BY), verify it compiles in your head, then fill in expressions. Never write SELECT and GROUP BY in separate passes.

Third — denominator and window ORDER BY. Both require re-reading the spec definition literally before writing the expression. "% of X" → X is the denominator. "Rank by Y" → Y is the ORDER BY. Two seconds of re-reading prevents the most common correctness bugs.
