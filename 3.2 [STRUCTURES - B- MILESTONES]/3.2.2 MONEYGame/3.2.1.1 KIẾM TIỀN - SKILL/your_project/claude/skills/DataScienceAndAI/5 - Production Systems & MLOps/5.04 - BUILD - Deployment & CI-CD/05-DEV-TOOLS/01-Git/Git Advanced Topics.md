# Git Advanced Topics

## 1. Git Submodule

[MiniProd_Agent2_WorkflowAgents_T5_2025/docs/docs1_submodules.md at main · DoanNgocCuong/MiniProd_Agent2_WorkflowAgents_T5_2025](https://github.com/DoanNgocCuong/MiniProd_Agent2_WorkflowAgents_T5_2025/blob/main/docs/docs1_submodules.md)

---

## 2. Cách thức lưu trữ Checkpoint (CKP) của code

1. Hạn chế lưu trong code hiện tại 
2. Sẽ lưu trữ ở trong branch hoặc gắn tag hoặc lịch sử nó tự có

---

## 3. Quản lý Version Code trên GitHub

### 3.1. Thói quen lưu các bản v1, v2, v3, v4...

- Nếu bạn **tạo folder hoặc copy code** cho mỗi version thì sẽ rất khó kiểm soát, dễ loạn, tốn dung lượng, và khó làm việc nhóm.
- Git vốn sinh ra để quản lý lịch sử, nên việc bạn tự lưu các bản copy là **không cần thiết**. Chỉ cần commit cẩn thận thì toàn bộ lịch sử đã được giữ lại.

### 3.2. Quản lý version bằng Git

Có 2 cách phổ biến:

#### **a. Dùng Tag (phổ biến, chuẩn)**

- Khi sản phẩm đạt một mốc quan trọng (ví dụ: release v1.0.0), bạn gắn tag:
    
    ```bash
    git tag -a v1.0.0 -m "Release version 1.0.0"
    git push origin v1.0.0
    ```
    
- Sau này chỉ cần checkout về tag đó:
    
    ```bash
    git checkout v1.0.0
    ```
    
👉 Đây là cách chuẩn để quản lý version release.

#### **b. Dùng Branch**

- Branch thường dùng cho **song song phát triển** (feature, hotfix, release).
- Ví dụ:
    - `main` (ổn định, code production)
    - `develop` (tích hợp code mới, chưa release)
    - `feature/...` (branch tạm thời cho từng tính năng)
    - `release/v1.0.0` (chuẩn bị release, test)
- Sau khi release xong, branch đó có thể merge vào `main` rồi xóa.

👉 Không ai tạo branch cho từng version kiểu `main_v1`, `main_v2` vì như vậy rất loạn. Thay vào đó, **tag + release branch** là chuẩn.

### 3.3. Cách xem và so sánh code của version cũ

#### Check code của version cũ bằng tag

- Đúng là muốn _trở lại toàn bộ repo_ ở trạng thái version đó thì phải:
    
    ```bash
    git checkout v1.0.0
    ```
    
    Nhưng lúc này bạn sẽ ở chế độ _detached HEAD_ → có thể xem, đọc code thoải mái.

👉 Nếu chỉ muốn "học hỏi code cũ" thì cách này vẫn ổn.

#### Xem diff giữa các version

Bạn không cần phải checkout nhiều lần để "soi". Git có sẵn diff:

```bash
git diff v1.0.0 v2.0.0
```

→ Nó sẽ highlight **những đoạn code thay đổi** giữa 2 version, giống như tool so sánh folder của bạn nhưng mạnh hơn.

#### Xem file cụ thể ở version cũ

Không cần checkout toàn repo, chỉ cần:

```bash
git show v1.0.0:path/to/file.py
```

→ Mở ngay file ở version đó để học.

#### Nếu muốn giữ kiểu "nhiều folder để học hỏi"

Bạn hoàn toàn có thể:

```bash
git clone repo repo_v1
cd repo_v1
git checkout v1.0.0
```

Rồi clone thêm cho `repo_v2`, `repo_v3`…  
👉 Giống hệt cách bạn copy folder, nhưng vẫn dựa trên Git nên sạch sẽ và dễ quản lý hơn.

### 3.4. Cách luyện Git để chuyên nghiệp hơn

- **Thực hành workflow chuẩn**: Gitflow hoặc Trunk-based development.
- **Học thao tác nâng cao**:
    - `git rebase` (gọn lịch sử commit)
    - `git cherry-pick` (lấy commit lẻ từ branch khác)
    - `git stash` (lưu tạm thay đổi)
    - `git bisect` (debug commit gây lỗi)
- **Luôn viết commit message rõ ràng** (theo convention, ví dụ [Conventional Commits](https://www.conventionalcommits.org/)).
- **Tập làm việc nhóm**: fork, pull request (PR), code review.
- **Tạo repo phụ** để luyện tình huống "merge conflict", "rollback", "release version".

👉 Tóm lại:
- Không cần copy `v1, v2, v3`. Hãy commit & dùng **tag**.
- Branch thì chia theo feature, release, hotfix, không theo version.
- Muốn chuyên nghiệp thì học thêm rebase, stash, cherry-pick, commit convention, và workflow Gitflow.

---

## 4. Commit và Tag Management

### 4.1. Tạo Annotated Tag với comment chi tiết

Bạn đang muốn viết một **annotated tag** trong Git có kèm comment/document chi tiết cho version. Mình gợi ý format comment cho tag như sau, vừa rõ ràng vừa dễ đọc khi người khác checkout hoặc xem log:

#### Cách tạo annotated tag với comment

```bash
git tag -a "v3.1_Search=QueryDB_P95P99=200ms_T7T82025" -m "
🚀 v3.1 SEARCH: Query DB - 200ms siêu nhanh

Tính năng:
1. Hỗ trợ ĐÚNG (MATCH), sai chính tả nhẹ (FUZZY) và ELASTIC SEARCH
2. Tên gọi khác: Table Mapping
3. Sai nhiều: chưa có giải pháp
4. Mix nhiều Job Roles

⚠️ Giới hạn:
- Chưa xử lý tốt khi sai nhiều hoặc khi mix nhiều Job Roles

🔮 Định hướng v3.2:
- SEARCH = RETRIEVAL of RAG
- Đáp ứng 3p95, P99 ~2–5s
- Dùng model siêu nhanh (oss-20b, host trên Groq)
"
```

#### Kết quả

- Khi chạy `git show v3.1_Search=QueryDB_P95P99=200ms_T7T82025` bạn sẽ thấy ngay toàn bộ ghi chú chi tiết này.
- Dễ cho bạn hoặc team sau này đọc lại, biết rõ **tính năng đạt được – giới hạn – định hướng tiếp theo**.

### 4.2. Tạo tag cho commit cụ thể

Bạn muốn tạo tag cho commit `8b963b09fafa971364f3bc79b8957940c6caf87f`. Có 2 kiểu tag trong Git:

#### 1. **Lightweight tag** (chỉ đánh dấu commit, không có message)

```bash
git tag v3.1_Search=QueryDB_P95P99=200ms_T7T82025 8b963b09fafa971364f3bc79b8957940c6caf87f
```

#### 2. **Annotated tag** (chuẩn, có comment như bạn vừa viết)

```bash
git tag -a "v3.1_Search=QueryDB_P95P99=200ms_T7T82025" 8b963b09fafa971364f3bc79b8957940c6caf87f -m "
🚀 v3.1 SEARCH: Query DB - 200ms siêu nhanh

Tính năng:
1. Hỗ trợ ĐÚNG (MATCH), sai chính tả nhẹ (FUZZY) và ELASTIC SEARCH
2. Tên gọi khác: Table Mapping
3. Sai nhiều: chưa có giải pháp
4. Mix nhiều Job Roles

⚠️ Giới hạn:
- Chưa xử lý tốt khi sai nhiều hoặc khi mix nhiều Job Roles

🔮 Định hướng v3.2:
- SEARCH = RETRIEVAL of RAG
- Đáp ứng 3p95, P99 ~2–5s
- Dùng model siêu nhanh (oss-20b, host trên Groq)
"
```

#### 3. Push tag lên remote

Sau khi tạo xong local tag, bạn cần push lên remote để mọi người cùng thấy:

```bash
git push origin v3.1_Search=QueryDB_P95P99=200ms_T7T82025
```

---

## 5. Server Configuration

_(Nội dung về cấu hình server Git sẽ được bổ sung sau)_

---

## Tài liệu tham khảo

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Submodule Documentation](https://github.com/DoanNgocCuong/MiniProd_Agent2_WorkflowAgents_T5_2025/blob/main/docs/docs1_submodules.md)










