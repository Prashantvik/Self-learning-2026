# Git Log Cheat Sheet (General Purpose)

A practical, end-to-end reference for using `git log` in day-to-day development, debugging, audits, and release management.

---

## 1. Basic Usage

Show full commit history:
```bash
git log
```

Readable compact view (most commonly used):
```bash
git log --oneline --decorate --graph
```

Limit number of commits:
```bash
git log -5
git log -10 --oneline
```

---

## 2. Time-Based Filtering

### Since a specific date or time
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

## 3. File and Path History

### Single file
```bash
git log path/to/file.py
```

### Multiple files
```bash
git log file1.py file2.sql
```

### Directory
```bash
git log src/
```

> Use `--` to separate paths from options
```bash
git log -- path/to/file.py
```

---

## 4. Show Code Changes (Diffs)

Show patch for each commit:
```bash
git log -p
```

Limit diff context:
```bash
git log -p -1
```

Stats only (files changed, insertions, deletions):
```bash
git log --stat
```

---

## 5. Search by Commit Message

Search by keyword:
```bash
git log --grep="bugfix"
git log --grep="hotfix"
```

Case-insensitive:
```bash
git log --grep="schema" -i
```

Multiple keywords (AND):
```bash
git log --grep="auth" --grep="token" --all-match
```

---

## 6. Search by Code Change (Very Powerful)

### When a string was added or removed
```bash
git log -S "function_name"
```

### Regex search in diffs
```bash
git log -G "TODO|FIXME"
```

### Search within a path
```bash
git log -S "config_key" -- config/
```

---

## 7. Filter by Author

```bash
git log --author="Alice"
git log --author="bob@example.com"
```

Exclude an author:
```bash
git log --author="^(?!Alice)"
```

---

## 8. Branch and Revision Comparison

### Commits in branchB not in branchA
```bash
git log branchA..branchB
```

### Symmetric difference
```bash
git log branchA...branchB
```

### Current branch vs main
```bash
git log main..HEAD
```

---

## 9. Pretty Formats (Custom Output)

One-line with author and date:
```bash
git log --pretty=format:"%h | %an | %ad | %s" --date=short
```

Useful placeholders:
- `%h` short hash
- `%H` full hash
- `%an` author name
- `%ae` author email
- `%ad` author date
- `%s` subject

---

## 10. Sorting and Order

Oldest → newest:
```bash
git log --reverse
```

By commit date (default):
```bash
git log --date-order
```

---

## 11. Combining Filters (Real-World Use)

```bash
git log --since="1 week ago" --author="Alice" --grep="fix" --oneline
```

```bash
git log -S "password" --since="2023-01-01" -- src/
```

---

## 12. Helpful Aliases (Recommended)

Create a global alias:
```bash
git config --global alias.lg "log --oneline --decorate --graph --all"
```

Usage:
```bash
git lg
git lg --since="2 weeks ago"
```

---

## Mental Model

```text
git log
  [range / branches]
  [time filters]
  [author / grep / search]
  --
  [file / directory]
```

---

**Use this cheat sheet for debugging, audits, incident analysis, and release reviews across any Git repository.**

