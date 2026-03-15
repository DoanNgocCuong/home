# Branching Strategies — Chọn model phù hợp

## Table of Contents
1. [Decision Matrix](#1-decision-matrix)
2. [Trunk-Based Development](#2-trunk-based-development)
3. [Git Flow](#3-git-flow)
4. [GitHub Flow](#4-github-flow)
5. [GitLab Flow](#5-gitlab-flow)
6. [Release Branch Model](#6-release-branch-model)
7. [Hybrid Patterns](#7-hybrid-patterns)

---

## 1. Decision Matrix

| Yếu tố | Trunk-based | Git Flow | GitHub Flow | GitLab Flow |
|---|---|---|---|---|
| Team size | Mọi size (cần CI tốt) | Medium-Large | Small-Medium | Medium-Large |
| Release cycle | Continuous | Scheduled | On-merge | Environment-based |
| CI/CD maturity | Cao (bắt buộc) | Thấp-Trung bình | Trung bình | Trung bình-Cao |
| Versioned product | Không phù hợp | ✅ Tốt nhất | Không phù hợp | Khá tốt |
| Hotfix speed | Nhanh nhất | Chậm (qua process) | Nhanh | Nhanh |
| Learning curve | Thấp | Cao | Thấp nhất | Trung bình |
| Long-lived branches | Không | Có (develop, release) | Không | Có (env branches) |

### Quick pick:
- **SaaS, deploy liên tục, CI mạnh** → Trunk-based
- **Mobile app, firmware, versioned releases** → Git Flow
- **Small team, PR-based, simple** → GitHub Flow
- **Multiple environments (staging, prod)** → GitLab Flow

---

## 2. Trunk-Based Development

### Mô hình

```
main ─────●────●────●────●────●────●──── (deploy liên tục)
           \  /      \  /
            \/        \/
         short-lived feature branches (< 2 days)
```

### Rules
- `main` luôn deployable
- Feature branches sống **< 2 ngày**, merge bằng PR
- Không có `develop` branch
- Feature flags thay vì long-lived branches
- CI chạy trên mọi PR, block merge nếu fail

### Commands

```bash
# Start feature
git checkout -b feat/user-auth main
# ... code 1-2 ngày ...
git push -u origin feat/user-auth
# Tạo PR → Review → Squash merge → Delete branch

# Hotfix = cũng là short-lived branch
git checkout -b fix/critical-bug main
```

### Khi nào dùng worktree
- Ít cần — vì branches rất ngắn, switch nhanh
- Có thể dùng 1 worktree cho "đang review PR" trong khi code feature

---

## 3. Git Flow

### Mô hình

```
main     ─────●──────────────────●─────── (chỉ release tags)
               \                /
hotfix    ──────●──────────────/
                              /
release   ───────────●───────●
                    /
develop  ────●────●────●────●────●──────── (integration)
              \  /      \  /
               \/        \/
            feature branches (có thể dài)
```

### Branches

| Branch | Mục đích | Lifetime | Merge vào |
|---|---|---|---|
| `main` | Production code, chỉ tag releases | Permanent | — |
| `develop` | Integration branch | Permanent | main (via release) |
| `feature/*` | Phát triển tính năng | Temporary | develop |
| `release/*` | Chuẩn bị release (QA, bugfix) | Temporary | main + develop |
| `hotfix/*` | Fix lỗi production gấp | Temporary | main + develop |

### Commands

```bash
# Feature
git checkout -b feature/payment develop
# ... code ...
git checkout develop && git merge --no-ff feature/payment

# Release
git checkout -b release/v2.1 develop
# ... QA, fix bugs ...
git checkout main && git merge --no-ff release/v2.1
git tag -a v2.1.0 -m "Release v2.1.0"
git checkout develop && git merge --no-ff release/v2.1

# Hotfix
git checkout -b hotfix/v2.1.1 main
# ... fix ...
git checkout main && git merge --no-ff hotfix/v2.1.1
git tag -a v2.1.1
git checkout develop && git merge --no-ff hotfix/v2.1.1
```

### Khi nào dùng worktree
- **Rất phù hợp** — thường cần làm feature + hotfix đồng thời
- Recommended setup:

```bash
git worktree add .worktrees/develop develop
git worktree add .worktrees/hotfix  hotfix/current
git worktree add .worktrees/release release/v2.1
# main ở root
```

---

## 4. GitHub Flow

### Mô hình

```
main ─────●────●────●────●────●────── (auto-deploy on merge)
           \  /      \  /      \  /
            PR        PR        PR
           /          /          /
        feature    bugfix     feature
```

### Rules
- `main` = production, luôn deployable
- Mọi thay đổi qua PR
- Review → Merge → Auto-deploy
- Không có release/develop branch

### Commands

```bash
git checkout -b feat/new-dashboard main
# ... code ...
git push -u origin feat/new-dashboard
# Tạo PR trên GitHub → Review → Merge → Auto-deploy
```

### Khi nào dùng worktree
- Dùng khi cần review PR mà không muốn stash:

```bash
git worktree add .worktrees/review-pr-42 origin/feat/new-dashboard
# Review xong → remove
```

---

## 5. GitLab Flow

### Mô hình

```
main ──────●────●────●──── (development)
            \         \
staging ─────●─────────●── (auto-deploy to staging)
              \         \
production ────●─────────● (manual promote)
```

### Rules
- `main` = development branch
- Environment branches (`staging`, `production`) = deploy targets
- Merge downstream: main → staging → production
- Không merge ngược

### Khi nào dùng worktree
- Dùng worktree cho mỗi environment branch để debug:

```bash
git worktree add .worktrees/staging staging
git worktree add .worktrees/prod production
```

---

## 6. Release Branch Model

Variant đơn giản hơn Git Flow, phù hợp cho team cần versioned releases nhưng không muốn complexity:

```
main ────●────●────●────●────●──── (ongoing dev)
          \              \
release/v1 ──●──●        release/v2 ──●──
             (backport)                (backport)
```

- Mỗi release tạo branch riêng từ main
- Bugfix cherry-pick vào release branch
- Không có `develop` branch

---

## 7. Hybrid Patterns

### Pattern: Git Flow + Worktree (recommended cho team vừa)

```bash
# Main worktree = main (production)
# Worktrees cho concurrent work:
git worktree add .worktrees/develop develop
git worktree add .worktrees/current-feature feature/payment
git worktree add .worktrees/hotfix-slot       # reuse cho hotfixes
```

### Pattern: Trunk-based + Worktree (cho review)

```bash
# Main worktree = main (trunk)
# 1 worktree dành riêng cho reviewing PRs:
git worktree add .worktrees/review
# Khi cần review PR #42:
cd .worktrees/review
git checkout origin/feat/pr-42
```

### Pattern: Monorepo + Worktree

```bash
# Mỗi worktree focus 1 service:
git worktree add .worktrees/api-service   -b feature/api-refactor
git worktree add .worktrees/web-frontend  -b feature/new-ui
# Cùng monorepo nhưng làm việc độc lập
```
