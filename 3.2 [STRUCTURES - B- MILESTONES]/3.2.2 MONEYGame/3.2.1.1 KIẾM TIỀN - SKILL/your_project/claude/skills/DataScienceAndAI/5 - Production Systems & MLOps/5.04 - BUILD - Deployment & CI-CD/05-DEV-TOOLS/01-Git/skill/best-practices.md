# Git Best Practices — MECE Checklist

Tổ chức theo 6 category MECE (Mutually Exclusive, Collectively Exhaustive),
cover toàn bộ lifecycle của Git usage trong production project.

## Table of Contents
1. [Commit Hygiene](#1-commit-hygiene)
2. [Branch Management](#2-branch-management)
3. [Merge & Integration](#3-merge--integration)
4. [Worktree Operations](#4-worktree-operations)
5. [Security & Safety](#5-security--safety)
6. [Collaboration & CI/CD](#6-collaboration--cicd)

---

## 1. Commit Hygiene

_Mọi thứ liên quan đến việc tạo commit chất lượng._

### ✅ DO

- **Atomic commits**: Mỗi commit = 1 thay đổi logic hoàn chỉnh
  - Tốt: `fix: resolve null pointer in payment handler`
  - Xấu: `fix stuff and also add new feature and refactor`
- **Conventional Commits format**:
  ```
  <type>(<scope>): <description>
  
  [optional body]
  [optional footer]
  ```
  Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `ci`, `chore`
- **Commit message tiếng Anh** cho codebase shared, tiếng Việt OK cho internal/solo
- **Sign commits** (`git commit -S`) cho production repos
- **Viết body cho commit phức tạp**: Giải thích WHY, không chỉ WHAT

### ❌ DON'T

- Commit file generated (build artifacts, node_modules, .env)
- Commit với message vô nghĩa: `fix`, `update`, `wip`, `asdf`
- Squash tất cả thành 1 commit khổng lồ (mất history)
- Commit secrets/credentials (dù xóa sau vẫn còn trong history)

### .gitignore checklist

```gitignore
# Build & Dependencies
node_modules/
dist/
build/
*.pyc
__pycache__/
.venv/
target/

# Environment & Secrets
.env
.env.local
*.pem
*.key

# IDE
.idea/
.vscode/
*.swp

# OS
.DS_Store
Thumbs.db

# Worktrees
.worktrees/

# Docker
docker-compose.override.yml
```

---

## 2. Branch Management

_Mọi thứ liên quan đến tạo, đặt tên, và quản lý lifecycle của branch._

### Naming Convention

```
<type>/<ticket-or-short-desc>

Ví dụ:
feature/PIKA-123-emotion-model
fix/PIKA-456-websocket-timeout
hotfix/critical-db-connection
release/v2.1.0
chore/update-dependencies
docs/api-reference
worktree/deploy-test-30002
```

| Prefix | Mục đích | Lifetime |
|---|---|---|
| `feature/` | Tính năng mới | Days-Weeks |
| `fix/` | Bug fix không gấp | Days |
| `hotfix/` | Fix production gấp | Hours-Days |
| `release/` | Chuẩn bị release | Days |
| `chore/` | Maintenance, cleanup | Days |
| `docs/` | Documentation only | Days |
| `worktree/` | Worktree-specific branch | Temporary |
| `experiment/` | Thử nghiệm, có thể bỏ | Variable |

### Lifecycle rules

- **Feature branches**: Merge hoặc close trong < 2 tuần (trunk-based: < 2 ngày)
- **Hotfix branches**: Merge trong < 1 ngày
- **Release branches**: Tồn tại đến khi release xong → delete
- **Stale branches**: Xóa sau 30 ngày inactive (dùng script tự động)

### Cleanup commands

```bash
# Xóa branches đã merge
git branch --merged main | grep -v 'main\|develop' | xargs git branch -d

# Xóa remote tracking branches đã xóa trên remote
git fetch --prune

# Liệt kê branches cũ (> 30 ngày)
git for-each-ref --sort=committerdate --format='%(committerdate:short) %(refname:short)' refs/heads/
```

---

## 3. Merge & Integration

_Mọi thứ liên quan đến merge strategy, conflict resolution, và integration._

### Merge Strategy Decision

| Tình huống | Strategy | Command |
|---|---|---|
| Feature → develop/main (giữ history) | Merge commit | `git merge --no-ff feature/x` |
| Feature → main (clean history) | Squash merge | `git merge --squash feature/x` |
| Rebase trước merge (linear) | Rebase + FF | `git rebase main` → `git merge --ff-only` |
| Lấy 1-2 commit cụ thể | Cherry-pick | `git cherry-pick <hash>` |
| Hotfix vào cả main + develop | Merge vào cả hai | merge vào main → merge vào develop |

### Conflict Resolution

```bash
# 1. Merge và gặp conflict
git merge feature/x
# CONFLICT in file.py

# 2. Xem conflict
git diff --name-only --diff-filter=U   # List conflicted files

# 3. Resolve
# Edit files, chọn version đúng
git add <resolved-files>
git merge --continue

# 4. Nếu muốn abort
git merge --abort
```

### Rebase rules

- **Rebase local branches** chưa push: OK
- **KHÔNG rebase branches đã push** mà người khác dùng
- **Interactive rebase** để clean up trước khi PR:
  ```bash
  git rebase -i HEAD~5   # Squash/reorder/edit last 5 commits
  ```

### PR/MR checklist

- [ ] Branch name đúng convention
- [ ] Commit messages clear
- [ ] Tests pass
- [ ] No merge conflicts
- [ ] Reviewers assigned
- [ ] Linked to ticket/issue
- [ ] No secrets/credentials
- [ ] Documentation updated (nếu cần)

---

## 4. Worktree Operations

_Mọi thứ riêng cho worktree lifecycle._

### Setup best practices

- **Đặt worktrees trong `.worktrees/`** (nested pattern) hoặc cùng cấp (flat pattern)
- **Thêm `.worktrees/` vào `.gitignore`**
- **Đặt tên branch worktree rõ ràng**: `worktree/<mục-đích>`
- **Giới hạn 3-5 worktrees** — nhiều hơn dễ mất track

### Recommended worktree layout

```bash
# Cho team dùng Git Flow:
repo/                               # main (production)
├── .worktrees/
│   ├── develop/                    # develop branch
│   ├── current-feature/            # feature đang làm
│   └── hotfix/                     # slot cho hotfix khi cần

# Cho solo dev / small team:
repo/                               # main
├── .worktrees/
│   ├── work/                       # feature/task đang làm
│   ├── review/                     # review PR
│   └── scratch/                    # thử nghiệm
```

### Worktree + Docker/Service isolation

Khi mỗi worktree chạy service riêng:

```yaml
# Convention: Port = base_port + worktree_id
# main:     30001
# test:     30002
# staging:  30003
```

Checklist cho mỗi worktree service:
- [ ] Port riêng (không conflict)
- [ ] Container name riêng
- [ ] `.env` riêng (copy + sửa)
- [ ] DB name/schema riêng (nếu dùng chung DB server)
- [ ] Docker network riêng (optional)

### Worktree lifecycle

```
Create → Configure → Work → Commit → Merge → Cleanup
  │         │         │       │        │        │
  │         │         │       │        │        └── git worktree remove + branch -d
  │         │         │       │        └── merge/cherry-pick/rebase vào target
  │         │         │       └── git add + commit (thường xuyên)
  │         │         └── code, test, debug
  │         └── .env, docker-compose, port mapping
  └── git worktree add .worktrees/<name> -b <branch>
```

### ❌ Worktree anti-patterns

- Để worktree sống > 2 tuần mà không sync với main
- Quên cleanup → disk space leak
- Direct commit vào main từ worktree (bypass review)
- Chạy chung port/DB với main worktree
- Tạo quá nhiều worktrees (> 5) → confusion

---

## 5. Security & Safety

_Mọi thứ liên quan đến bảo vệ repo và tránh mất dữ liệu._

### Bảo vệ branch

```bash
# GitHub: Settings → Branches → Branch protection rules
# Require:
# - PR reviews before merge
# - Status checks pass
# - No force push
# - No deletion
```

### Pre-commit hooks

```bash
# .git/hooks/pre-commit hoặc dùng pre-commit framework
# Kiểm tra:
# - Không commit secrets (.env, *.pem, API keys)
# - Lint pass
# - Tests pass
# - Commit message format đúng

# Tool recommended: https://pre-commit.com
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: detect-private-key
      - id: check-added-large-files
      - id: trailing-whitespace
```

### Secret scanning

```bash
# Nếu đã commit secrets:
# 1. Rotate secret NGAY LẬP TỨC
# 2. Dùng git-filter-repo để xóa khỏi history
pip install git-filter-repo
git filter-repo --invert-paths --path .env

# 3. Force push (chỉ khi đã coordinate với team)
git push --force-with-lease
```

### Backup & Recovery

```bash
# Reflog = safety net (giữ 90 ngày)
git reflog                        # Xem history của HEAD
git checkout HEAD@{5}             # Recovery tới state trước đó

# Stash recovery
git stash list
git stash apply stash@{0}

# Tag important states
git tag -a backup/before-refactor -m "State before major refactor"
```

### Force push rules

- **KHÔNG BAO GIỜ** force push lên `main` hoặc `develop`
- Dùng `--force-with-lease` thay vì `--force` (kiểm tra remote chưa thay đổi)
- Chỉ force push trên personal branches chưa ai dùng

---

## 6. Collaboration & CI/CD

_Mọi thứ liên quan đến làm việc nhóm và tích hợp CI/CD._

### Git workflow cho CI/CD

```
Developer → Push → CI Pipeline → Tests → Build → Deploy
    │                  │
    │                  ├── Lint + Unit tests (mọi push)
    │                  ├── Integration tests (PR to main)
    │                  ├── Build Docker image (merge to main)
    │                  └── Deploy (tag/release)
    │
    └── Worktree: test locally trước khi push
```

### Commit message cho CI

```bash
# Trigger specific CI jobs:
git commit -m "feat: add payment [deploy:staging]"
git commit -m "ci: update pipeline config"
git commit -m "docs: update README [skip ci]"      # Skip CI cho docs-only
```

### Tag & Release

```bash
# Semantic versioning: MAJOR.MINOR.PATCH
git tag -a v2.1.0 -m "Release v2.1.0: Payment integration"
git push origin v2.1.0

# List tags
git tag -l "v2.*"

# CI trigger on tag push → build + deploy production
```

### Monorepo considerations

```bash
# Path-based CI triggers (GitHub Actions example):
# .github/workflows/api.yml
on:
  push:
    paths:
      - 'services/api/**'
      - 'shared/**'

# Worktree per service:
git worktree add .worktrees/api-work -b feature/api-refactor
git worktree add .worktrees/web-work -b feature/web-redesign
```

### Team conventions checklist

- [ ] Branching model documented và team đồng thuận
- [ ] Commit message format enforced (commitlint hoặc hook)
- [ ] PR template có sẵn
- [ ] Branch protection rules enabled
- [ ] CI/CD pipeline chạy trên mọi PR
- [ ] Stale branch cleanup automated
- [ ] Worktree convention documented (nếu dùng)
- [ ] Secret scanning enabled
- [ ] Release process documented
- [ ] Hotfix process documented
