```
@utils_streak.py @utils_folder_level.py
# Phân tích code hiện tại
# Dự kiến refactor
* utils_xp_level.py
* utils_streak.py
* utils_folder.py
(chưa code vội nhé)
viết kế hoạch vào file @docs1.2_PlanRefactor.md

HƯỚNG DẪN TÔI VÀ CHO TÔI CODE TỪNG BƯỚC REFACTOR 

start
```


---



# Kế hoạch Refactor Utils Modules

## Ngày: 07/09/2025

## 1. PHÂN TÍCH HIỆN TRẠNG

### 1.1 Vấn đề hiện tại

* **Code duplication** : Các hàm streak bị duplicate giữa `utils_streak.py` và `utils_folder_level.py`
* **Single Responsibility Violation** : `utils_folder_level.py` chứa quá nhiều responsibilities khác nhau
* **Tight coupling** : Các chức năng không được tách biệt rõ ràng
* **Import complexity** : Khó quản lý dependencies giữa các modules

### 1.2 Code hiện tại

#### utils_streak.py (363 lines)

```
✅ Core streak functions:
   - calculate_streak_days()
   - calculate_max_historical_streak() 
   - calculate_total_days()

✅ GitHub-style features:
   - calculate_github_like_streak()
   - build_contribution_calendar()
   
✅ Helper functions:
   - _parse_to_date()
   - _normalize_date_list()
   - _count_by_date()
```

#### utils_folder_level.py (661 lines)

```
❌ DUPLICATED from utils_streak:
   - calculate_streak_days() [lines 137-216]
   - calculate_max_historical_streak() [lines 218-282]
   - calculate_total_days() [lines 284-305]

📊 XP/Level functions:
   - calculate_xp_from_articles()
   - calculate_level_from_xp()
   
🎨 UI/Display:
   - get_domain_color()
   
📁 File processing:
   - estimate_word_count()
   
📂 Folder scanning:
   - scan_single_folder()
   - scan_folder_with_subfolders()
   - scan_folder_tree_recursive()
   - build_complete_folder_tree()
   
📈 Analytics:
   - get_top_subfolders_by_level()
   - format_tree_display()
```

## 2. MỤC TIÊU REFACTOR

### 2.1 Separation of Concerns

* **utils_xp_level.py** : Chỉ xử lý logic tính XP và Level
* **utils_streak.py** : Chỉ xử lý logic liên quan đến streak/timeline
* **utils_folder.py** : Chỉ xử lý scan folder và aggregate data

### 2.2 Principles

* ✅ DRY (Don't Repeat Yourself)
* ✅ Single Responsibility Principle
* ✅ Loose Coupling
* ✅ High Cohesion
* ✅ Easy Testing

## 3. THIẾT KẾ MỚI

### 3.1 Module Structure

```
utils/
├── utils_xp_level.py     (~ 100 lines)
│   ├── calculate_xp_from_articles()
│   ├── calculate_level_from_xp()
│   ├── get_xp_for_next_level()
│   └── get_level_progress()
│
├── utils_streak.py        (~ 400 lines) 
│   ├── calculate_streak_days()
│   ├── calculate_max_historical_streak()
│   ├── calculate_total_days()
│   ├── calculate_github_like_streak()
│   ├── build_contribution_calendar()
│   └── [helper functions]
│
└── utils_folder.py        (~ 450 lines)
    ├── estimate_word_count()
    ├── get_domain_color()
    ├── scan_single_folder()
    ├── scan_folder_with_subfolders()
    ├── scan_folder_tree_recursive()
    ├── build_complete_folder_tree()
    ├── get_top_subfolders_by_level()
    └── format_tree_display()
```

### 3.2 Dependencies Flow

```
utils_folder.py
    ↓ imports
    ├── utils_xp_level.py (for XP/Level calculation)
    └── utils_streak.py   (for streak calculation)

utils_xp_level.py (no dependencies)
utils_streak.py   (no dependencies)
```

## 4. KẾ HOẠCH THỰC HIỆN

### Phase 1: Tạo utils_xp_level.py ✨

 **Mục tiêu** : Tách riêng logic XP/Level

1. Extract các hàm từ utils_folder_level.py:
   * `calculate_xp_from_articles()`
   * `calculate_level_from_xp()`
2. Thêm các hàm utility mới:
   * `get_xp_for_next_level()` - Tính XP cần cho level tiếp theo
   * `get_level_progress()` - Tính % tiến độ của level hiện tại
3. Add constants:
   * `BASE_XP_PER_ARTICLE = 100`
   * `WORDS_PER_XP = 10`
   * `BASE_LEVEL_XP = 1000`
   * `LEVEL_XP_MULTIPLIER = 1.5`

### Phase 2: Clean up utils_streak.py 🧹

 **Mục tiêu** : Giữ nguyên, chỉ improve documentation

1. Giữ tất cả functions hiện tại
2. Add type hints đầy đủ
3. Improve docstrings
4. Add unit tests

### Phase 3: Tạo utils_folder.py 📁

 **Mục tiêu** : Tách riêng logic folder scanning

1. Extract từ utils_folder_level.py:
   * Tất cả hàm scan folder
   * `estimate_word_count()`
   * `get_domain_color()`
2. Remove duplicate streak functions
3. Import và sử dụng:
   ```python
   from utils_xp_level import calculate_xp_from_articles, calculate_level_from_xpfrom utils_streak import calculate_streak_days, calculate_max_historical_streak, calculate_total_days
   ```

### Phase 4: Update main.py 🔄

 **Mục tiêu** : Update imports

1. Thay đổi imports từ:

   ```python
   from utils_folder_level import ...
   ```

   Thành:

   ```python
   from utils_folder import ...from utils_xp_level import ...from utils_streak import ...
   ```

### Phase 5: Testing & Validation ✅

1. Unit tests cho từng module
2. Integration tests
3. Performance testing
4. Documentation update

## 5. BENEFITS SAU REFACTOR

### 5.1 Code Quality

* ✅ Không còn code duplication
* ✅ Mỗi module có single responsibility rõ ràng
* ✅ Dễ maintain và extend
* ✅ Dễ test từng phần độc lập

### 5.2 Performance

* ✅ Import nhanh hơn (module nhỏ hơn)
* ✅ Memory footprint giảm
* ✅ Có thể optimize từng module độc lập

### 5.3 Developer Experience

* ✅ Code dễ đọc và hiểu hơn
* ✅ Dễ tìm kiếm function cần thiết
* ✅ Dễ debug và trace issues
* ✅ Có thể reuse trong các projects khác

## 6. RISKS & MITIGATION

### 6.1 Risks

* Breaking changes với code hiện tại
* Import errors nếu miss dependencies
* Test coverage có thể giảm trong quá trình chuyển đổi

### 6.2 Mitigation

* Backup code trước khi refactor
* Refactor từng phase, test sau mỗi phase
* Maintain backward compatibility trong phase chuyển tiếp
* Viết tests trước khi refactor (TDD approach)

## 7. TIMELINE

```
Day 1: Phase 1 - Create utils_xp_level.py
Day 1: Phase 2 - Clean utils_streak.py  
Day 2: Phase 3 - Create utils_folder.py
Day 2: Phase 4 - Update main.py
Day 3: Phase 5 - Testing & Documentation
```

## 8. SUCCESS METRICS

* ✅ Zero code duplication
* ✅ Tất cả tests pass
* ✅ Performance không giảm (benchmark)
* ✅ Code coverage > 80%
* ✅ Documentation đầy đủ cho mỗi module

---

## NEXT STEPS

1. Review và approve kế hoạch
2. Bắt đầu Phase 1: Tạo utils_xp_level.py
3. Proceed từng phase theo timeline

 **Status** : 📝 PLANNING
 **Assignee** : Development Team
 **Priority** : HIGH
