# Git Cheat Sheet (General Purpose)

A practical, everyday Git reference covering the commands you actually use while developing, reviewing code, fixing mistakes, and releasing software.

> This cheat sheet intentionally **excludes `git log`** (covered separately).

---

## 1. Repository Setup & Basics

Initialize a repo:
```bash
git init
```

Clone a repo:
```bash
git clone <repo_url>
```

Check repo status:
```bash
git status
```

Show current branch:
```bash
git branch --show-current
```

---

## 2. Staging & Committing

Stage files:
```bash
git add file.py
git add .
```

Unstage file:
```bash
git restore --staged file.py
```

Commit changes:
```bash
git commit -m "Meaningful message"
```

Amend last commit:
```bash
git commit --amend
```

---

## 3. Branching

List branches:
```bash
git branch
git branch -a
```

Create a branch:
```bash
git branch feature-x
```

Create and switch:
```bash
git checkout -b feature-x
# or
git switch -c feature-x
```

Switch branches:
```bash
git checkout main
# or
git switch main
```

Delete branch:
```bash
git branch -d feature-x
git branch -D feature-x  # force
```

---

## 4. Merging & Rebasing

Merge branch:
```bash
git merge feature-x
```

Rebase current branch on main:
```bash
git rebase main
```

Abort merge/rebase:
```bash
git merge --abort
git rebase --abort
```

Continue after conflict resolution:
```bash
git merge --continue
git rebase --continue
```

---

## 5. Remote Repositories

List remotes:
```bash
git remote -v
```

Add remote:
```bash
git remote add origin <repo_url>
```

Fetch updates:
```bash
git fetch
git fetch origin
```

Pull (fetch + merge):
```bash
git pull
git pull --rebase
```

Push changes:
```bash
git push
git push origin feature-x
```

Set upstream:
```bash
git push -u origin feature-x
```

---

## 6. Undoing & Fixing Mistakes (Very Important)

Discard local changes (unstaged):
```bash
git restore file.py
```

Discard all local changes:
```bash
git restore .
```

Reset commit but keep changes:
```bash
git reset --soft HEAD~1
```

Reset commit and changes:
```bash
git reset --hard HEAD~1
```

Revert a commit (safe for shared branches):
```bash
git revert <commit_hash>
```

---

## 7. Stashing (Context Switching)

Stash changes:
```bash
git stash
git stash push -m "WIP"
```

List stashes:
```bash
git stash list
```

Apply stash:
```bash
git stash apply
git stash pop
```

Drop stash:
```bash
git stash drop
```

---

## 8. Diffing (Before You Commit)

Unstaged changes:
```bash
git diff
```

Staged changes:
```bash
git diff --staged
```

Between branches:
```bash
git diff main..feature-x
```

Between commits:
```bash
git diff commit1 commit2
```

---

## 9. Tags & Releases

Create tag:
```bash
git tag v1.0.0
```

Annotated tag:
```bash
git tag -a v1.0.0 -m "Release v1.0.0"
```

Push tags:
```bash
git push origin --tags
```

Delete tag:
```bash
git tag -d v1.0.0
git push origin :refs/tags/v1.0.0
```

---

## 10. Cleaning & Maintenance

Remove untracked files:
```bash
git clean -f
```

Remove untracked files and dirs:
```bash
git clean -fd
```

Dry run:
```bash
git clean -n
```

---

## 11. Inspection & Info

Show commit details:
```bash
git show <commit_hash>
```

Show file from another branch:
```bash
git show main:file.py
```

Who changed what (line-level):
```bash
git blame file.py
```

---

## Mental Model

```text
Working Directory → Staging Area → Commit → Remote

restore → add → commit → push
```

---

**Use this cheat sheet as a daily reference for development, debugging, collaboration, and releases across any Git-based project.**

