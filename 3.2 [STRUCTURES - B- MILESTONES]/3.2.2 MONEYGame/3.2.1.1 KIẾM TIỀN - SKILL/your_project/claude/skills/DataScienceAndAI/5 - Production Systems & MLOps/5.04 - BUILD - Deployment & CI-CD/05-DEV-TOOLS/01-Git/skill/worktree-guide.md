# Worktree Guide — Hướng dẫn chi tiết

## Table of Contents
1. [Concepts](#1-concepts)
2. [Setup Patterns](#2-setup-patterns)
3. [Deployment Use Case](#3-deployment-use-case)
4. [Sync & Merge Workflow](#4-sync--merge-workflow)
5. [Cleanup](#5-cleanup)
6. [Troubleshooting](#6-troubleshooting)

---

## 1. Concepts

### Worktree là gì?

`git worktree` cho phép checkout nhiều branch **đồng thời** vào các thư mục khác nhau,
chia sẻ cùng 1 `.git` directory. Không cần clone riêng, không tốn disk cho `.git`.

```
.git/           ← shared giữa tất cả worktrees
repo/           ← main worktree (thường là main/master branch)
repo/.worktrees/feature/  ← linked worktree (feature branch)
```

### Ràng buộc quan trọng

- **Mỗi branch chỉ checkout được ở 1 worktree**. Không thể checkout `main` ở 2 nơi.
- Worktree **share reflog, stash, remote** — push/pull từ worktree nào cũng được.
- `.git` trong linked worktree là file (pointer), không phải folder.

---

## 2. Setup Patterns

### Pattern A: Flat layout (recommended cho dự án nhỏ-vừa)

```bash
# Từ repo gốc
cd ~/projects/my-app

# Tạo worktree cùng cấp
git worktree add ../my-app-hotfix -b hotfix/critical-bug
git worktree add ../my-app-review -b review/pr-42

# Kết quả:
# ~/projects/my-app/          ← main
# ~/projects/my-app-hotfix/   ← hotfix
# ~/projects/my-app-review/   ← review
```

### Pattern B: Nested layout (recommended cho dự án lớn, CI/CD)

```bash
cd ~/projects/my-app

# Tạo worktree trong subfolder
git worktree add .worktrees/deploy-test -b worktree/deploy-test
git worktree add .worktrees/feature-x   -b feature/x

# Kết quả:
# ~/projects/my-app/                      ← main
# ~/projects/my-app/.worktrees/deploy-test/ ← test env
# ~/projects/my-app/.worktrees/feature-x/   ← feature dev
```

**Tip:** Thêm `.worktrees/` vào `.gitignore` để không track worktree directories.

### Pattern C: Bare repo + worktrees (advanced — cho power users)

```bash
# Clone bare repo (chỉ .git, không có working files)
git clone --bare git@github.com:org/repo.git repo.git
cd repo.git

# Tạo worktrees cho mỗi branch
git worktree add ../repo-main main
git worktree add ../repo-dev  develop
git worktree add ../repo-hotfix hotfix/v2.1
```

Ưu điểm: Không có "main worktree" nào đặc biệt hơn — tất cả worktree bình đẳng.

---

## 3. Deployment Use Case

### Scenario: Test deployment trên port riêng

Đây là use case điển hình khi cần chạy song song production + test env từ cùng 1 repo.

**Bước 1: Tạo worktree**

```bash
cd /home/ubuntu/my-project
git worktree add .worktrees/deploy-test-30002 -b worktree-deploy-test-30002
```

**Bước 2: Config riêng cho worktree**

```yaml
# .worktrees/deploy-test-30002/docker-compose.yml
services:
  api:
    ports:
      - "30002:8000"    # Port riêng, không conflict với main (30001)
    container_name: my-project-api-test  # Tên riêng
```

```bash
# Copy và sửa .env
cp .env .worktrees/deploy-test-30002/.env
# Sửa PORT, DB name nếu cần tránh conflict
```

**Bước 3: Deploy & test**

```bash
cd .worktrees/deploy-test-30002
docker compose build api
docker compose up -d api
curl http://localhost:30002/v1/health
```

**Port mapping convention:**

| Environment | Port | Branch |
|---|---|---|
| Production | 30001 | main |
| Test | 30002 | worktree-deploy-test |
| Staging | 30003 | staging |

---

## 4. Sync & Merge Workflow

### Từ worktree vào main (quy trình khuyến nghị)

```bash
# 1. Trong worktree: commit changes
cd .worktrees/deploy-test-30002
git add .
git commit -m "feat: implement new endpoint"

# 2. Về main worktree
cd /home/ubuntu/my-project

# 3. Option A: Merge (giữ history)
git merge worktree-deploy-test-30002

# 3. Option B: Cherry-pick (chọn commit cụ thể)
git cherry-pick <commit-hash>

# 3. Option C: Rebase (linear history)
git checkout worktree-deploy-test-30002
git rebase main
git checkout main
git merge --ff-only worktree-deploy-test-30002
```

### Giữ worktree đồng bộ với main

```bash
# Trong worktree, pull changes từ main
cd .worktrees/deploy-test-30002
git rebase main
# hoặc
git merge main
```

### Quy tắc merge

| Tình huống | Strategy |
|---|---|
| Feature hoàn thành, muốn history rõ | `merge --no-ff` |
| Hotfix nhỏ, muốn linear | `rebase` + `merge --ff-only` |
| Chỉ lấy 1-2 commit | `cherry-pick` |
| Test thất bại, bỏ worktree | `worktree remove` + `branch -D` |

---

## 5. Cleanup

```bash
# Stop services nếu có
cd .worktrees/deploy-test-30002
docker compose down

# Xóa worktree
cd /home/ubuntu/my-project
git worktree remove .worktrees/deploy-test-30002

# Xóa branch nếu đã merge
git branch -d worktree-deploy-test-30002   # safe delete (chỉ xóa nếu đã merge)
git branch -D worktree-deploy-test-30002   # force delete

# Dọn stale worktrees
git worktree prune
```

### Kiểm tra worktree hiện tại

```bash
git worktree list
# /home/ubuntu/my-project                    abc1234 [main]
# /home/ubuntu/my-project/.worktrees/test    def5678 [worktree-deploy-test-30002]
```

---

## 6. Troubleshooting

### "fatal: 'branch-name' is already checked out"

Branch đang được checkout ở worktree khác. Mỗi branch chỉ ở 1 worktree.

```bash
git worktree list  # Xem branch nào ở đâu
```

### Port conflict

```bash
lsof -i :30002          # Ai đang dùng port
kill -9 <PID>           # Hoặc đổi port trong docker-compose.yml
```

### Worktree bị "orphan" (thư mục đã xóa nhưng git vẫn track)

```bash
git worktree prune      # Dọn references tới worktrees đã xóa
```

### Database conflict khi chạy song song

- Dùng DB name riêng cho mỗi worktree trong `.env`
- Hoặc dùng separate Docker network
- Hoặc mount volume riêng
