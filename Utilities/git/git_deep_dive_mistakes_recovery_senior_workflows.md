# Git Deep Dive: Mistakes, Recovery & Senior Engineer Workflows

This document is designed for **real-world engineering teams**. It covers common Git failure patterns, how to recover safely, how senior engineers should use Git, and a clear learning path from beginner to advanced.

---

## 1. Git Mistakes & Recovery (Real Incident Patterns)

### Mistake 1: Committed to the Wrong Branch (e.g. `main`)

**Scenario**: You accidentally committed directly to `main`.

**Recovery (commit not pushed)**:
```bash
git checkout -b fix/my-branch
git checkout main
git reset --hard HEAD~1
```

**Recovery (commit already pushed)**:
```bash
git revert <commit_hash>
```
> Never rewrite shared history.

---

### Mistake 2: Forgot to Pull Before Committing

**Symptom**: Push rejected, branch behind remote.

**Recovery (preferred)**:
```bash
git pull --rebase
```

If conflicts occur:
```bash
git rebase --continue
git rebase --abort
```

---

### Mistake 3: Bad Commit Message / Missing File

```bash
git commit --amend
```
> Safe only if commit is **not pushed**.

---

### Mistake 4: Lost Work After Reset / Checkout

```bash
git reflog
```

Restore:
```bash
git checkout <reflog_hash>
```

> `reflog` is your last line of defense.

---

### Mistake 5: Messy Commits (Too Many WIPs)

```bash
git rebase -i HEAD~5
```
Actions:
- `s` → squash
- `r` → reword
- `d` → drop

---

### Mistake 6: Merge Conflict Panic

Correct approach:
1. Understand conflict markers
2. Fix code
3. `git add <file>`
4. Continue:
```bash
git rebase --continue
# or
git merge --continue
```

---

## 2. Senior Engineer Git Workflow (Rules That Scale)

### Golden Rules

- Never force-push to shared branches (`main`, `release/*`)
- Rebase **feature branches only**
- Keep `main` always releasable
- One logical change per commit

---

### Rebase vs Merge (When to Use What)

| Scenario | Use | Why |
|-------|-----|-----|
| Feature branch sync | Rebase | Clean history |
| Long-lived branch | Merge | Preserve context |
| Release to main | Merge (no-ff) | Auditability |
| Shared branch | Never rebase | Avoid history rewrite |

---

### Recommended Flow

```bash
# Start work
git checkout main
git pull
git checkout -b feature/x

# Keep branch updated
git fetch origin
git rebase origin/main

# Final cleanup
git rebase -i origin/main

# Push
git push -u origin feature/x
```

---

## 3. Learning Path: Beginner → Advanced

### Beginner (Must Know)

- `clone`, `status`, `add`, `commit`
- `push`, `pull`
- `branch`, `checkout`, `switch`
- `diff`

---

### Intermediate (Team-Ready)

- `merge` vs `rebase`
- `stash`
- Conflict resolution
- `reset --soft / --hard`
- `revert`
- `tag`

---

### Advanced (Senior Level)

- Interactive rebase
- `reflog` recovery
- Cherry-pick
- Release branching
- History hygiene
- Incident recovery without force-push

---

## 4. Visual Git Workflow (Onboarding Friendly)

```
Working Directory
       ↓ git add
Staging Area
       ↓ git commit
Local Repository
       ↓ git push
Remote Repository
```

### Feature Workflow

```
main ──────●──────●─────────
            \        \
feature/x    ●──●──●  (rebase + squash)
```

### Release Workflow

```
main ──●────●────●─────
         \         \
release   ●──●──●   (merge back)
```

---

## 5. Mental Model (Senior Engineer)

```text
Local safety → Clean history → Shared branch stability

If shared → revert
If local  → reset / rebase
If lost   → reflog
```

---

**This document is suitable for onboarding, internal wikis, and senior-level interviews.**

