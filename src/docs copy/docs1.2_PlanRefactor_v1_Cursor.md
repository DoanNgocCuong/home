
```
@utils_streak.py @utils_folder_level.py 

# Phân tích code hiện tại 
# Dự kiến refactor 
* utils_xp_level.py
* utils_streak.py
* utils_folder.py

(chưa code vội nhé) 

viết kế hoạch vào file @docs1.2_PlanRefactor.md 
```

# Kế hoạch refactor các tiện ích tính XP/Level, Streak và Folder Scan

Mục tiêu: tách rõ trách nhiệm, giảm lặp lại, dễ bảo trì và mở rộng, đồng thời giữ nguyên hành vi API hiện tại.

---

## 1) Phân tích code hiện tại

- `backend/utils_folder_level.py`

  - Vừa scan folder (files + subfolders), vừa tính toán XP/Level, vừa tính Streak/Max streak/Total days, đồng thời gộp số liệu cho toàn bộ cây con.
  - Ưu điểm: một file làm được tất cả; logic đang chạy ổn với tree view.
  - Nhược điểm:
    - Trách nhiệm lẫn lộn (scan + tính toán XP + tính toán Streak).
    - Khó tái sử dụng riêng lẻ từng phần (ví dụ muốn dùng lại hàm streak cho luồng khác).
    - Khó test unit theo từng mảng.
- `backend/utils_streak.py`

  - Chứa các hàm streak dùng cho API `/api/streak/global` và `/api/streak/calendar` (GitHub-like):
    - `calculate_github_like_streak`
    - `build_contribution_calendar`
    - Các helper chuẩn hoá ngày, đếm ngày, v.v.
  - Bản hiện tại không được `utils_folder_level.py` dùng; hai nhánh tính streak khác nhau đang sống tách biệt.
- Các vấn đề kỹ thuật đã khắc phục gần đây

  - Tính streak/longest streak/total days cho folder cha dựa trên TỔNG ngày hoạt động của chính nó + mọi con (nếu không có file leaf ở cha vẫn có streak đúng nhờ con).
  - Tổng XP của cha đã gộp `totalXpWithChildren` đúng (không chỉ cộng `xp` trực tiếp của con).

Kết luận: cần tách phần “tính” (XP/Level, Streak) ra khỏi “scan” để tái sử dụng và kiểm thử tốt hơn.

---

## 2) Dự kiến refactor (chưa code)

Sẽ tạo 3 module rõ trách nhiệm:

### 2.1 `backend/utils_xp_level.py`

- Trách nhiệm: toàn bộ logic XP/Level.
- Hàm dự kiến:
  - `estimate_word_count(file_path: str, file_ext: str) -> int`Ước tính số từ (giữ logic cũ: .txt/.md đếm trực tiếp, .html bỏ tag, khác thì rule dựa trên size).
  - `calculate_xp_from_articles(articles_count: int, total_words: int) -> int`Công thức XP = 100/article + 1/10 words.
  - `calculate_level_from_xp(xp: int) -> int`Lộ trình level (base 1000, nhân 1.5 theo từng cấp).
  - (Optional) `sum_child_totals(total_xps: list[int], total_files: list[int]) -> tuple[int,int]`
    Helper gộp số liệu tổng của con cho cha (đỡ lặp).
- Docstring tiếng Việt giải thích công thức, ví dụ, trade-off hiệu năng.

### 2.2 `backend/utils_streak.py`

- Trách nhiệm: TOÀN BỘ logic Streak (cho cả API và tree).
- Hàm công khai dự kiến (giữ lại + thống nhất):
  - `calculate_streak_days(article_dates: Iterable[datetime|date|str]) -> int`
  - `calculate_max_historical_streak(article_dates: Iterable[datetime|date|str]) -> int`
  - `calculate_total_days(article_dates: Iterable[datetime|date|str]) -> int`
  - `normalize_to_dates(values: Iterable[datetime|date|str]) -> set[date]`
  - `merge_dates(*date_sets: Iterable[datetime|date|str]) -> set[date]`Hợp nhất tất cả ngày hoạt động; dùng cho bài toán “folder cha = tổng hoạt động của cả cây con”.
  - (Giữ) `calculate_github_like_streak` và `build_contribution_calendar` cho global view.
- Docstring tiếng Việt: định nghĩa “Streak GitHub-like”, ví dụ minh hoạ, giải thích các edge cases (không bắt buộc có hôm nay, flexible mode, …).

### 2.3 `backend/utils_folder.py`

- Trách nhiệm: chỉ SCAN và tổng hợp cây thư mục.
- Hành vi sau refactor (giữ nguyên output):
  - Tách phần tính XP/Level sang gọi `utils_xp_level.py`.
  - Tách phần tính Streak/Max/Days sang gọi `utils_streak.py` (dùng `merge_dates` để gộp ngày của con + cha).
  - Vẫn sử dụng `_dates_set` nội bộ trong quá trình đệ quy để truyền ngày lên cha, và strip trước khi trả JSON.
  - Vẫn trả về cấu trúc tree với các key: `xp`, `level`, `taskCount`, `streakDays`, `maxStreakDays`, `totalDays`, `totalXpWithChildren`, `totalArticlesWithChildren`, `maxLevelInTree`, `children`, …
- Docstring tiếng Việt: mô tả flow scan, giới hạn depth, vì sao dùng `_dates_set`, cách strip, độ phức tạp.

---

## 3) Lộ trình triển khai (đảm bảo không phá API)

1. Tạo file `utils_xp_level.py` và `utils_streak.py` với docstring VN đầy đủ; copy/di chuyển các hàm gốc tương ứng, thống nhất kiểu dữ liệu input (datetime|date|str đều normalize về date).
2. Tạo file `utils_folder.py` từ việc rút gọn `utils_folder_level.py`: giữ code scan/aggregate, thay các lời gọi tính toán sang import từ 2 file mới. Tách nhỏ các khối lớn thành hàm private (_scan_current_folder, _aggregate_child, …) để dễ đọc.
3. Cập nhật `main.py` (import mới) nhưng không đổi schema API.
4. Kiểm thử thủ công:
   - `/api/domains/tree` hiển thị đủ domain, streak của domain cha > 0 khi con có hoạt động.
   - `/api/streak/global`, `/api/streak/calendar` vẫn chạy bình thường.
   - Frontend Tree Structure:
     - Bar tiến độ dùng `totalXpWithChildren` cho cha;
     - Hiển thị `leaf xp` cho cha.
5. Xoá các hàm trùng lặp còn sót trong `utils_folder_level.py` (nếu giữ file cũ thì chuyển thành stub hoặc đổi tên sang `utils_folder.py`).

---

## 4) Nguyên tắc code & chất lượng

- Không thay đổi output JSON hiện có; chỉ đổi chỗ tính toán.
- Tất cả hàm public có docstring tiếng Việt rõ ràng + ví dụ.
- Chuẩn hoá ngày: luôn convert về `date` sớm nhất có thể.
- Không để circular import: `utils_folder.py` chỉ import từ `utils_xp_level.py` và `utils_streak.py` (một chiều).
- Lint sạch; không thêm dependency mới.

---

## 5) Rủi ro và cách giảm thiểu

- Khác biệt nhỏ trong normalize ngày → Viết unit sample mini để so sánh trước/sau bằng các bộ ngày (bao gồm duplicate, string ISO, future date).
- Sai lệch total XP ở cha → Dùng helper gộp totals, không cộng thủ công nhiều nơi.
- Thiếu sót strip `_dates_set` → Viết helper `_strip_internal(node)` gọi đệ quy trước khi trả tree.

---

## 6) Kết quả mong đợi

- Mã nguồn rõ ràng: scan tách khỏi tính toán.
- Dễ tái sử dụng streak/XP cho các luồng khác (report, thống kê,…).
- Dễ mở rộng (ví dụ thêm công thức level mới, hay thêm kiểu streak khác) mà không ảnh hưởng phần scan.
