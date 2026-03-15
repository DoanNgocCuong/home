# Git LFS - Xử lý File Lớn (Large File Storage)

## 📚 Mục lục
1. [Git LFS là gì?](#git-lfs-là-gì)
2. [Khi nào cần dùng Git LFS?](#khi-nào-cần-dùng-git-lfs)
3. [Cài đặt Git LFS](#cài-đặt-git-lfs)
4. [Cách sử dụng Git LFS](#cách-sử-dụng-git-lfs)
5. [Các lỗi thường gặp](#các-lỗi-thường-gặp)
6. [Best Practices](#best-practices)

---

## 🤔 Git LFS là gì?

**Git Large File Storage (LFS)** là một extension của Git giúp quản lý các file lớn hiệu quả hơn.

### Vấn đề Git gặp phải với file lớn:
- ❌ Git lưu toàn bộ lịch sử của mọi file
- ❌ Mỗi lần clone phải tải về toàn bộ history → Rất chậm
- ❌ Repo size tăng nhanh chóng → GitHub giới hạn file 100MB
- ❌ Push/pull chậm

### Git LFS giải quyết như thế nào:
- ✅ Chỉ lưu **pointer** (văn bản nhỏ) trong Git
- ✅ File thật được lưu ở **LFS server** riêng
- ✅ Chỉ tải file khi thực sự cần
- ✅ Clone nhanh hơn nhiều

```
┌─────────────────────────────────────────────┐
│          Git Repository                      │
│  ┌──────────────────────────────────────┐   │
│  │  model.pkl (pointer)                 │   │
│  │  version 3b8f9a1...                  │   │
│  │  size 500MB                          │   │
│  │  oid sha256:abc123...                │   │
│  └──────────────────────────────────────┘   │
│                    ↓                         │
│         Khi checkout/pull                    │
│                    ↓                         │
│  ┌──────────────────────────────────────┐   │
│  │     Git LFS Server                   │   │
│  │  Lưu file thật 500MB                 │   │
│  └──────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

---

## 📌 Khi nào cần dùng Git LFS?

### ✅ NÊN DÙNG cho:

| Loại File | Ví dụ | Lý do |
|-----------|-------|-------|
| **Model AI/ML** | `*.pkl`, `*.h5`, `*.pth`, `*.onnx` | Thường >100MB |
| **Dataset** | `*.csv`, `*.parquet`, `*.arrow` | File data lớn |
| **Media** | `*.mp4`, `*.mov`, `*.wav` | Video/audio lớn |
| **Binary** | `*.zip`, `*.tar.gz`, `*.exe` | File nén, executable |
| **3D Assets** | `*.fbx`, `*.blend`, `*.obj` | Game/3D models |
| **Documents** | `*.pdf`, `*.psd`, `*.ai` | File design lớn |

### ❌ KHÔNG NÊN DÙNG cho:

| Loại File | Lý do |
|-----------|-------|
| **Code files** (`.py`, `.js`, `.java`) | Cần track changes chi tiết |
| **Text files** (`.txt`, `.md`, `.json`) | Git xử lý tốt |
| **Config files** (`.yaml`, `.toml`, `.env`) | Nhỏ, cần version control |
| **Git special files** (`.gitignore`, `.gitkeep`) | **BỊ CẤM** bởi Git LFS |

---

## 🔧 Cài đặt Git LFS

### **Bước 1: Cài đặt Git LFS**

#### Windows:
```powershell
# Cách 1: Dùng chocolatey
choco install git-lfs

# Cách 2: Dùng scoop
scoop install git-lfs

# Cách 3: Tải từ trang chủ
# https://git-lfs.github.com/
```

#### macOS:
```bash
brew install git-lfs
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt-get install git-lfs
```

### **Bước 2: Khởi tạo Git LFS trong repo**

```bash
# Di chuyển vào thư mục repo
cd your-repo

# Khởi tạo Git LFS (chỉ cần làm 1 lần)
git lfs install

# Output:
# Updated git hooks.
# Git LFS initialized.
```

**Giải thích:**
- Lệnh này cài đặt các **git hooks** cần thiết
- Chỉ cần chạy **1 lần** cho mỗi user trên máy
- Nếu đã chạy rồi, chạy lại không sao

---

## 🚀 Cách sử dụng Git LFS

### **Phương pháp 1: Track theo extension (ĐỀ XUẤT)**

```bash
# Track tất cả file .pkl
git lfs track "*.pkl"

# Track tất cả file .h5
git lfs track "*.h5"

# Track tất cả file .pth và .onnx
git lfs track "*.pth"
git lfs track "*.onnx"

# Track tất cả file .mp4 trong thư mục videos/
git lfs track "videos/*.mp4"
```

**Kết quả:** File `.gitattributes` được tạo/cập nhật:
```
*.pkl filter=lfs diff=lfs merge=lfs -text
*.h5 filter=lfs diff=lfs merge=lfs -text
*.pth filter=lfs diff=lfs merge=lfs -text
*.onnx filter=lfs diff=lfs merge=lfs -text
videos/*.mp4 filter=lfs diff=lfs merge=lfs -text
```

### **Phương pháp 2: Track file cụ thể**

```bash
# Track 1 file cụ thể
git lfs track "models/bert-large.pkl"
git lfs track "data/train_dataset.csv"
```

### **Phương pháp 3: Track theo thư mục**

```bash
# Track tất cả file trong thư mục models/
git lfs track "models/**"

# Track tất cả file trong data/ và subdirectories
git lfs track "data/**/*"
```

### **Commit và Push file LFS**

```bash
# Bước 1: Add .gitattributes (QUAN TRỌNG!)
git add .gitattributes

# Bước 2: Add file lớn
git add models/large-model.pkl

# Bước 3: Commit
git commit -m "Add large model with Git LFS"

# Bước 4: Push (file sẽ tự động upload lên LFS server)
git push origin main
```

**Giải thích:**
1. `.gitattributes` phải được commit trước
2. Git LFS tự động detect file dựa trên `.gitattributes`
3. Khi push, file thật upload lên LFS server, Git chỉ lưu pointer

---

## ❌ Các lỗi thường gặp

### **Lỗi 1: Track "**" - FORBIDDEN FILES**

```powershell
PS> git lfs track "**"
Pattern '**' matches forbidden file '.gitignore'
Pattern '**' matches forbidden file '.gitkeep'
```

**Nguyên nhân:**
- `"**"` track TẤT CẢ files
- Git LFS **CẤM** track các file đặc biệt:
  - `.gitignore`
  - `.gitkeep`
  - `.gitattributes`
  - Các file Git config khác

**Giải pháp:**
```bash
# ❌ ĐỪNG LÀM THẾ NÀY:
git lfs track "**"

# ✅ THAY VÀO ĐÓ, track cụ thể:
git lfs track "*.pkl"
git lfs track "*.h5"
git lfs track "*.pth"
# ... hoặc
git lfs track "models/**/*.pkl"  # Chỉ .pkl trong models/
```

### **Lỗi 2: File đã commit trước khi track**

```bash
# Lỗi: File đã trong Git history nhưng chưa dùng LFS
error: file 'model.pkl' is too large (200MB > 100MB limit)
```

**Giải pháp:**
```bash
# Bước 1: Track file type
git lfs track "*.pkl"
git add .gitattributes

# Bước 2: Migrate file đã commit vào LFS
git lfs migrate import --include="*.pkl"

# Bước 3: Push lại (có thể cần force)
git push --force-with-lease origin main
```

⚠️ **LƯU Ý:** Force push sẽ **GHI ĐÈ HISTORY**!

### **Lỗi 3: LFS bandwidth limit exceeded**

```
Error: Your LFS bandwidth limit has been exceeded
```

**Giải thích:**
- GitHub Free: 1GB bandwidth/tháng
- GitHub Pro: 50GB bandwidth/tháng

**Giải pháp:**
1. Upgrade GitHub plan
2. Dùng alternative LFS server (GitLab, Bitbucket)
3. Giảm số lần clone/pull không cần thiết

### **Lỗi 4: Git LFS không hoạt động sau khi clone**

```bash
# File pointer không được download
$ cat model.pkl
version https://git-lfs.github.com/spec/v1
oid sha256:abc123...
size 524288000
```

**Nguyên nhân:** Git LFS chưa được cài đặt trên máy mới

**Giải pháp:**
```bash
# Bước 1: Cài đặt Git LFS
git lfs install

# Bước 2: Pull file thật
git lfs pull

# Hoặc pull specific file
git lfs pull --include="models/model.pkl"
```

---

## 💡 Best Practices

### ✅ **DO (Nên làm)**

1. **Track sớm:**
   ```bash
   # Khi bắt đầu project, setup ngay
   git lfs install
   git lfs track "*.pkl"
   git lfs track "*.h5"
   git add .gitattributes
   git commit -m "Setup Git LFS"
   ```

2. **Commit .gitattributes trước:**
   ```bash
   # Đúng thứ tự:
   git add .gitattributes
   git commit -m "Add LFS tracking"
   git add model.pkl
   git commit -m "Add model"
   ```

3. **Document trong README:**
   ```markdown
   ## Setup
   1. Install Git LFS: `git lfs install`
   2. Clone repo: `git clone ...`
   3. Pull LFS files: `git lfs pull`
   ```

4. **Kiểm tra trước khi commit:**
   ```bash
   # Xem file nào đang được track
   git lfs ls-files
   
   # Xem status
   git lfs status
   ```

### ❌ **DON'T (Không nên)**

1. **Đừng track "**":**
   ```bash
   # ❌ ĐỪNG LÀM:
   git lfs track "**"
   ```

2. **Đừng track code files:**
   ```bash
   # ❌ ĐỪNG track code
   git lfs track "*.py"
   git lfs track "*.js"
   ```

3. **Đừng track file nhỏ:**
   ```bash
   # ❌ Không cần LFS cho file <10MB
   git lfs track "small-config.json"  # 1KB
   ```

4. **Đừng commit rồi mới track:**
   ```bash
   # ❌ SAI THỨ TỰ:
   git add model.pkl
   git commit -m "Add model"
   git lfs track "*.pkl"  # Đã muộn!
   ```

---

## 📊 So sánh: Git vs Git LFS

| Tính năng | Git thông thường | Git LFS |
|-----------|------------------|---------|
| **Clone speed** | Chậm với file lớn | Nhanh, chỉ tải pointer |
| **Repo size** | Lớn | Nhỏ (chỉ pointer) |
| **Bandwidth** | Cao | Thấp hơn |
| **File limit** | 100MB (GitHub) | 2GB/file (GitHub) |
| **Version control** | Full history | Full history |
| **Diffs** | Line-by-line | Binary (không diff được) |

---

## 🔍 Các lệnh Git LFS hữu ích

### Xem thông tin
```bash
# Xem file nào đang được track
git lfs ls-files

# Xem pattern nào đang được track
git lfs track

# Xem LFS status
git lfs status

# Xem LFS environment
git lfs env
```

### Quản lý file
```bash
# Pull tất cả LFS files
git lfs pull

# Pull specific file
git lfs pull --include="models/*.pkl"

# Fetch nhưng không checkout (tiết kiệm bandwidth)
git lfs fetch

# Xem file info
git lfs ls-files --size
```

### Migration
```bash
# Migrate file vào LFS (cho file đã commit)
git lfs migrate import --include="*.pkl"

# Export từ LFS về Git thông thường
git lfs migrate export --include="*.pkl"

# Kiểm tra migration
git lfs migrate info
```

### Untrack file
```bash
# Bước 1: Untrack
git lfs untrack "*.pkl"

# Bước 2: Update .gitattributes
git add .gitattributes

# Bước 3: Commit
git commit -m "Stop tracking .pkl with LFS"
```

---

## 🎯 Kịch bản thực tế

### **Scenario 1: Project mới với ML models**

```bash
# Bước 1: Init repo
git init
git lfs install

# Bước 2: Setup LFS tracking
git lfs track "*.pkl"
git lfs track "*.h5"
git lfs track "*.pth"
git lfs track "data/*.csv"

# Bước 3: Commit .gitattributes
git add .gitattributes
git commit -m "Setup Git LFS for ML files"

# Bước 4: Add và commit model
git add models/bert-base.pkl
git commit -m "Add BERT base model"

# Bước 5: Push
git push origin main
```

### **Scenario 2: Migrate project đã có file lớn**

```bash
# Hiện tại: model.pkl đã commit, GitHub reject vì >100MB

# Bước 1: Setup LFS
git lfs install
git lfs track "*.pkl"
git add .gitattributes

# Bước 2: Migrate file vào LFS
git lfs migrate import --include="*.pkl" --everything

# Bước 3: Force push (vì history thay đổi)
git push --force-with-lease origin main
```

### **Scenario 3: Clone project có LFS**

```bash
# Bước 1: Clone như bình thường
git clone https://github.com/user/repo.git
cd repo

# Bước 2: Cài đặt LFS (nếu chưa có)
git lfs install

# Bước 3: Pull LFS files (tự động trong Git 2.3+)
# Hoặc pull manual:
git lfs pull
```

---

## 📖 Tham khảo

- **Docs chính thức:** https://git-lfs.github.com/
- **GitHub LFS:** https://docs.github.com/en/repositories/working-with-files/managing-large-files
- **Tutorial:** https://www.atlassian.com/git/tutorials/git-lfs

---

## ⚠️ Lưu ý quan trọng

1. **Git LFS ≠ Giải pháp cho mọi file lớn:**
   - Nếu file >2GB, xem xét dùng:
     - Cloud storage (S3, GCS, Azure Blob)
     - DVC (Data Version Control)
     - Git Annex

2. **Bandwidth limits:**
   - GitHub Free: 1GB/tháng
   - Cân nhắc upgrade nếu team lớn

3. **Không phải giải pháp cho secret scanning:**
   - Git LFS chỉ xử lý file lớn
   - Secret scanning vẫn quét cả pointer files

4. **Backup LFS files:**
   - LFS server riêng biệt với Git
   - Cần backup cả 2 nơi

---

**Tác giả:** Đoàn Ngọc Cường  
**Ngày tạo:** 11/10/2025  
**Phiên bản:** 1.0

