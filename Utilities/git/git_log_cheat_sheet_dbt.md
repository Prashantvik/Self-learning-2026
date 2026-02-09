# Git Log Cheat Sheet (dbt-focused)

A concise, production-ready reference for using `git log` effectively—especially useful for dbt models, debugging data issues, and managing UAT → PROD releases.

User >> results.json to save the output in a file for easy access during incidents.

---

## 1. Basic `git log`

```bash
git log
```

Most-used readable format:
```bash
git log --oneline --decorate --graph
```

---

## 2. Time-Based Filters

### Since a date or time
```bash
git log --since="2024-01-01"
git log --since="2 weeks ago"
git log --since="3 days ago"
```

### Before a date
```bash
git log --before="2024-02-01"
```

### Between two dates
```bash
git log --since="2024-01-01" --before="2024-02-01"
```

### Today / Yesterday
```bash
git log --since=midnight
git log --since="yesterday"
```

---

## 3. File-Level History (Single dbt Model)

```bash
git log models/marts/sales/fct_orders.sql
```

Compact:
```bash
git log --oneline models/marts/sales/fct_orders.sql
```

With diffs per commit:
```bash
git log -p models/marts/sales/fct_orders.sql
```

---

## 4. Folder-Level History (dbt Layers)

### Entire staging layer
```bash
git log models/staging/
```

### One mart
```bash
git log models/marts/finance/
```

---

## 5. Prefix-Based History (Facts / Dimensions)

> Use `--` to separate paths from options

### All fact models
```bash
git log -- models/**/fct_*.sql
```

### All dimension models
```bash
git log -- models/**/dim_*.sql
```

---

## 6. Time + Path (Most Common in Prod Debugging)

### One model, last 2 weeks
```bash
git log --since="2 weeks ago" --oneline models/marts/sales/fct_orders.sql
```

### All fact models this month
```bash
git log --since="2024-02-01" -- models/**/fct_*.sql
```

---

## 7. Search by Commit Message

```bash
git log --grep="backfill"
git log --grep="hotfix"
```

Case-insensitive:
```bash
git log --grep="schema" -i
```

---

## 8. Search by Code Change (Very Powerful)

### When a column was added/removed
```bash
git log -S customer_id -- models/marts/sales/fct_orders.sql
```

### Regex search in code
```bash
git log -G "order_status" -- models/
```

---

## 9. Filter by Author

```bash
git log --author="Prashant"
git log --author="john.doe"
```

---

## 10. Custom Pretty Formats

```bash
git log --pretty=format:"%h | %an | %ad | %s" --date=short
```

Last N commits:
```bash
git log -5 --oneline
```

---

## 11. Branch Comparison (UAT ↔ PROD)

### In UAT but not PROD
```bash
git log prod..uat --oneline
```

### In PROD but not UAT
```bash
git log uat..prod --oneline
```

---

## 12. Oldest → Newest Changes (Bug Tracing)

```bash
git log --reverse -- models/marts/sales/fct_orders.sql
```

---

## 13. Recommended Alias (Highly Useful)

```bash
git config --global alias.lg "log --oneline --decorate --graph --all"
```

Usage:
```bash
git lg --since="2 weeks ago" -- models/**/fct_*.sql
```

---

## Mental Model

```text
git log
  [time filters]
  [search / author]
  --
  [file / folder / glob]
```

---

**Use this file as a quick reference during production incidents, dbt model debugging, and release audits.**

