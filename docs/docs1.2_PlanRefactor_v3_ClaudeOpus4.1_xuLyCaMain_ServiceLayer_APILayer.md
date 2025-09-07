
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

## 10. TIMELINE CẬP NHẬT

```
Day 1 (Morning):
  ✅ Phase 1 - Create utils_xp_level.py
  □ Phase 2 - Review utils_streak.py (no changes needed)

Day 1 (Afternoon):  
  □ Phase 3 - Create utils_folder.py
  □ Remove duplicate code from utils_folder_level.py

Day 2 (Morning):
  □ Phase 4.1 - Create config.py & models.py
  □ Phase 4.2 - Create service layer (domain, contribution, stats)

Day 2 (Afternoon):
  □ Phase 4.3 - Restructure API routes
  □ Phase 4.4 - Simplify main.py

Day 3:
  □ Phase 5 - Testing & Integration
  □ Phase 6 - Documentation & Deployment
```

## 11. FILE SIZE COMPARISON

### Before Refactor:

```
utils_folder_level.py:  661 lines (duplicated code)
utils_streak.py:        363 lines (good)
main.py:                843 lines (mixed concerns)
TOTAL:                1,867 lines
```

### After Refactor:

```
# Utils layer (clean, single responsibility)
utils_xp_level.py:      250 lines (new, focused)
utils_streak.py:        363 lines (unchanged)
utils_folder.py:        450 lines (cleaned)

# Config & Models
config.py:               50 lines (new)
models.py:               80 lines (extracted)

# Service layer (business logic)
services/domain_service.py:        150 lines
services/contribution_service.py:   80 lines
services/stats_service.py:         100 lines

# API layer
api/routes/domains.py:              120 lines
api/routes/streak.py:                60 lines
api/routes/stats.py:                 80 lines

# Main application
main.py:                            100 lines (simplified)

TOTAL:                            1,883 lines
```

## 12. SUCCESS METRICS CẬP NHẬT

### Code Quality Metrics

* ✅ **Zero code duplication** between modules
* ✅  **Single Responsibility** : Mỗi module < 500 lines
* ✅  **Cyclomatic Complexity** : < 10 per function
* ✅  **Test Coverage** : > 85%
* ✅  **Documentation** : 100% public functions documented

### Performance Metrics

* ✅  **Import time** : < 100ms per module
* ✅  **API response time** : < 200ms (with caching)
* ✅  **Memory usage** : Reduced by ~30%
* ✅  **Scan performance** : Parallel processing option

### Maintainability Metrics

* ✅  **Module coupling** : Loose (dependency injection)
* ✅  **Code reusability** : 90% of utils reusable
* ✅  **Change impact** : Isolated to single module
* ✅  **Debug time** : Reduced by clear separation

## 13. CHECKLIST TỔNG HỢP

### ✅ Completed

* [X] Phân tích hiện trạng
* [X] Lập kế hoạch refactor
* [X] Tạo utils_xp_level.py
* [X] Review utils_streak.py

### 🔄 In Progress

* [ ] Tạo utils_folder.py
* [ ] Extract config & models
* [ ] Create service layer
* [ ] Restructure API routes

### 📋 Todo

* [ ] Integration testing
* [ ] Performance benchmarks
* [ ] Update documentation
* [ ] Deploy to production

---

## NEXT IMMEDIATE STEPS

### Bước tiếp theo: Tạo utils_folder.py

1. **Import dependencies đúng**
2. **Remove duplicate functions**
3. **Test thoroughly**
4. **Update imports in main.py**

 **Current Status** : 🚧 REFACTORING IN PROGRESS
 **Phase Completed** : 1/6
 **Estimated Completion** : 3 days
 **Risk Level** : LOW (incremental changes)


---



# GIẢI THÍCH VỀ SERVICE LAYER VÀ API LAYER trong đợt REFACTOR

Service layer là một **tầng xử lý business logic** riêng biệt, tách khỏi API routes. Đây là pattern phổ biến trong kiến trúc phần mềm.

### 🎯 TẠI SAO CẦN SERVICE LAYER?

Hiện tại trong main.py, bạn có code như này:

```python
# main.py HIỆN TẠI - Business logic lẫn lộn với API
@app.get("/api/domains")
async def get_domains():
    # BUSINESS LOGIC ngay trong route handler 😰
    domains = {}
    for item in os.listdir(DATA_SCIENCE_PATH):
        # ... 60 lines xử lý logic scan folder...
    return domains
```

### 🏗️ SERVICE LAYER LÀ GÌ?

Service layer tách riêng business logic ra khỏi API:

```python
# services/domain_service.py - LOGIC TẬP TRUNG
class DomainService:
    def scan_all(self):
        """Toàn bộ logic scan folder ở đây"""
        # 60 lines logic...
        return domains

# main.py - CHỈ GỌI SERVICE
@app.get("/api/domains")
async def get_domains():
    service = DomainService()
    return service.scan_all()  # Simple! 
```

### 📁 CHI TIẾT 3 SERVICES:

#### 1️⃣ **domain_service.py** (150 lines)

```python
class DomainService:
    """Xử lý mọi thứ liên quan đến Domain scanning"""
  
    def scan_all(self):
        # Logic từ scan_all_domains() hiện tại
    
    def scan_single(self, path):
        # Scan 1 domain cụ thể
    
    def get_tree_structure(self):
        # Build tree structure
```

#### 2️⃣ **contribution_service.py** (80 lines)

```python
class ContributionService:
    """Xử lý contribution dates và streaks"""
  
    def collect_dates(self):
        # Logic từ _collect_all_contribution_dates()
    
    def get_global_streak(self):
        # Tính global streak
```

#### 3️⃣ **stats_service.py** (100 lines)

```python
class StatsService:
    """Tính toán thống kê"""
  
    def calculate_totals(self, domains):
        # Tổng XP, levels, articles
    
    def get_rankings(self):
        # Top domains, best streaks
```

### ✅ LỢI ÍCH:

1. **Dễ test** : Test service độc lập, không cần FastAPI
2. **Reusable** : Có thể dùng service trong CLI, scripts khác
3. **Clean code** : API routes ngắn gọn, dễ đọc
4. **Maintainable** : Logic tập trung 1 chỗ
5. **Scalable** : Dễ thêm features mới

### 🤔 CÓ CẦN THIẾT KHÔNG?

**Không bắt buộc** cho project nhỏ! Nhưng sẽ giúp nếu bạn muốn:

* Code dễ maintain hơn
* Dễ test hơn
* Có thể mở rộng sau này

### 💡 ĐỀ XUẤT CHO BẠN:

Có 2 options:

**Option A: Simple Refactor** (Đề xuất cho bạn)

* Chỉ tách utils modules (đang làm)
* Giữ main.py như cũ (chỉ update imports)
* Đủ tốt cho project hiện tại

**Option B: Full Refactor** (Nếu muốn scale)

* Tách utils modules
* Thêm service layer
* Clean up main.py
* Tốt cho long-term

Bạn muốn chọn option nào? Tôi sẽ điều chỉnh kế hoạch theo lựa chọn của bạn!


---

# MODEL PYDANTIC DATA



## 📦 MODELS.PY - DATA MODELS (PYDANTIC)

Models.py chứa các **Pydantic models** - là các class định nghĩa cấu trúc dữ liệu.

### HIỆN TẠI TRONG MAIN.PY:

```python
# Các Pydantic models đang nằm trong main.py
class DomainData(BaseModel):
    xp: int
    level: int
    color: str
    taskCount: int
    streakDays: int
    maxStreakDays: int
    totalDays: int
    lastTaskDate: str

class DomainsResponse(BaseModel):
    success: bool
    domains: Dict[str, DomainData]
    count: int
    last_scan: str

class StatsResponse(BaseModel):
    success: bool
    stats: Dict[str, Any]
    last_scan: str

class ErrorResponse(BaseModel):
    success: bool
    error: str
```

### MODELS.PY SAU KHI REFACTOR:## 📊 MODELS LÀ GÌ?

Models là các **class định nghĩa cấu trúc dữ liệu** - giống như "bản thiết kế" cho data.

### 🎯 VÍ DỤ ĐƠN GIẢN:

```python
# Không có model - data lộn xộn
domain = {
    'xp': 1000,
    'lvl': 2,      # inconsistent naming
    'COLOR': 'red'  # inconsistent case
}

# Có model - data chuẩn hóa
class DomainData(BaseModel):
    xp: int         # Phải là số nguyên
    level: int      # Naming nhất quán
    color: str      # Type checking
  
domain = DomainData(xp=1000, level=2, color='red')
# ✅ Auto validation, consistent structure
```

### 📦 MODELS.PY BAO GỒM:

Tôi đã tạo file models.py mẫu ở trên với:

1. **Core Models** (từ main.py hiện tại):
   * `DomainData` - Cấu trúc 1 domain
   * `FolderNode` - Node trong tree structure
2. **Response Models** (API responses):
   * `DomainsResponse` - Trả về list domains
   * `StatsResponse` - Trả về statistics
   * `TreeResponse` - Trả về folder tree
   * `ErrorResponse` - Xử lý errors
3. **Streak Models** (mới thêm):
   * `StreakData` - GitHub-style streak
   * `ContributionDay` - 1 ngày trong calendar
   * `ContributionCalendar` - Full calendar
4. **Request Models** (validate input):
   * `ScanRequest` - Yêu cầu scan folders
   * `CalendarRequest` - Yêu cầu calendar data

### ✅ LỢI ÍCH CỦA PYDANTIC MODELS:

```python
# Automatic validation
domain = DomainData(xp=-100)  # ❌ Error: xp must be >= 0

# Type hints
def process(domain: DomainData):  # IDE autocomplete!
    print(domain.xp)  # ✅ IDE knows .xp exists

# JSON serialization
json_data = domain.json()  # Auto convert to JSON

# Documentation
# FastAPI tự động generate docs từ models
```

### 🤔 CÓ CẦN THIẾT KHÔNG?

 **Với project của bạn** : Models đã có sẵn trong main.py, chỉ cần:

1. **Move ra file riêng** → Dễ maintain
2. **Thêm validation** → Tránh bugs
3. **Consistent naming** → Code clean hơn

### 💡 SIMPLE VERSION CHO BẠN:

```python
# models.py (30 lines - simplified)
from pydantic import BaseModel
from typing import Dict

class DomainData(BaseModel):
    """Chỉ giữ fields cần thiết"""
    name: str
    xp: int
    level: int
    taskCount: int
    streakDays: int

class DomainsResponse(BaseModel):
    domains: Dict[str, DomainData]
    count: int
```

Bạn có thể:

* **Option A** : Giữ models trong main.py (OK cho project nhỏ)
* **Option B** : Move ra models.py (cleaner, recommended)

Bạn muốn làm option nào?
