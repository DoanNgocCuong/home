# Kiến Trúc Dự Án

## Cấu Trúc Thư Mục

```
src/
├── assets/         # Tài nguyên tĩnh (hình ảnh, fonts, etc.)
│   └── README.md   # Hướng dẫn quản lý tài nguyên
├── components/     # Các component tái sử dụng
│   ├── Charts.tsx          # Component biểu đồ thống kê
│   ├── ExperienceOverview.tsx  # Trang tổng quan kinh nghiệm
│   ├── GameDashboard.jsx   # Dashboard chính của game
│   ├── Notification.tsx    # Component thông báo
│   ├── TagLevels.tsx       # Hiển thị cấp độ của tags
│   ├── TaskForm.tsx        # Form tạo/sửa task
│   ├── TaskList.tsx        # Danh sách tasks
│   └── README.md           # Hướng dẫn sử dụng components
├── features/       # Các tính năng chính của ứng dụng
│   └── README.md   # Mô tả các tính năng
├── hooks/          # Custom React hooks
│   └── README.md   # Hướng dẫn sử dụng hooks
├── layouts/        # Các layout template
│   └── README.md   # Hướng dẫn về layouts
├── pages/          # Các trang chính của ứng dụng
│   └── README.md   # Mô tả các trang
├── routes/         # Cấu hình routing
│   └── README.md   # Hướng dẫn routing
├── services/       # Các service gọi API
│   └── README.md   # Hướng dẫn sử dụng services
├── store/          # State management (Redux)
│   ├── slices/     # Redux slices
│   │   ├── taskSlice.ts  # Quản lý state của tasks
│   │   └── tagSlice.ts   # Quản lý state của tags
│   ├── index.ts    # Store configuration
│   └── README.md   # Hướng dẫn quản lý state
├── utils/          # Các hàm tiện ích
│   └── README.md   # Hướng dẫn sử dụng utils
├── App.tsx         # Component gốc của ứng dụng
├── main.tsx        # Entry point của ứng dụng
└── index.css       # Global styles
```

## Mô Tả Chi Tiết

### Components
- `Charts.tsx`: Component hiển thị biểu đồ thống kê
  - Sử dụng Chart.js để vẽ biểu đồ
  - Hiển thị dữ liệu theo ngày/tháng/năm
  - Tương tác với Redux store để lấy dữ liệu
  - Hiển thị phân bố XP theo tag

- `ExperienceOverview.tsx`: Trang tổng quan kinh nghiệm
  - Tích hợp các biểu đồ thống kê
  - Hiển thị tổng quan về tiến độ
  - Tương tác với Redux store để lấy dữ liệu

- `GameDashboard.jsx`: Dashboard chính của game
  - Giao diện chính của ứng dụng
  - Tích hợp các component con
  - Quản lý layout và navigation

- `Notification.tsx`: Component thông báo
  - Hiển thị thông báo cho người dùng
  - Hỗ trợ nhiều loại thông báo (success, error, warning)
  - Tự động ẩn sau một khoảng thời gian

- `TagLevels.tsx`: Hiển thị cấp độ của tags
  - Hiển thị tiến trình level của từng tag
  - Tính toán và hiển thị XP cần thiết cho level tiếp theo
  - Tương tác với Redux store để lấy dữ liệu tags

- `TaskForm.tsx`: Form tạo/sửa task
  - Form nhập liệu cho task mới
  - Chỉnh sửa task hiện có
  - Validation và xử lý submit

- `TaskList.tsx`: Danh sách tasks
  - Hiển thị danh sách tasks
  - Hỗ trợ sắp xếp và lọc
  - Tương tác với Redux store để CRUD tasks

### Store
- `taskSlice.ts`: Quản lý state của tasks
  - CRUD operations cho tasks
  - Tính toán kinh nghiệm (XP)
  - Lọc và sắp xếp tasks

- `tagSlice.ts`: Quản lý state của tags
  - CRUD operations cho tags
  - Quản lý màu sắc và thuộc tính của tags
  - Tính toán XP theo tag

### Pages
- `ExperienceOverview.tsx`: Trang tổng quan kinh nghiệm
  - Hiển thị biểu đồ thống kê
  - Tổng hợp kinh nghiệm theo thời gian
  - Phân tích phân bố theo tag

### Services
- Các service gọi API để tương tác với backend
- Xử lý authentication và authorization
- Quản lý các request/response

### Utils
- Các hàm tiện ích dùng chung
- Format dữ liệu
- Xử lý ngày tháng
- Tính toán XP

## Luồng Dữ Liệu

1. Người dùng tương tác với UI
2. Actions được dispatch đến Redux store
3. Reducers cập nhật state
4. Components re-render với dữ liệu mới
5. Biểu đồ tự động cập nhật

## Công Nghệ Sử Dụng

- React + TypeScript
- Redux Toolkit cho state management
- Chart.js cho biểu đồ
- Tailwind CSS cho styling
- Vite cho build tool 

## Tài Liệu Hướng Dẫn

Mỗi thư mục chính đều có file README.md riêng để cung cấp thông tin chi tiết về:

### assets/README.md
- Cấu trúc thư mục tài nguyên
- Quy tắc đặt tên file
- Cách sử dụng assets trong dự án

### components/README.md
- Danh sách các component
- Cách sử dụng từng component
- Props và events của components
- Ví dụ sử dụng

### features/README.md
- Mô tả các tính năng chính
- Cách tích hợp tính năng mới
- Quy trình phát triển tính năng

### hooks/README.md
- Danh sách custom hooks
- Cách sử dụng hooks
- Best practices

### layouts/README.md
- Các layout template có sẵn
- Cách tạo layout mới
- Quy tắc responsive design

### pages/README.md
- Danh sách các trang
- Cấu trúc trang
- Quy tắc routing

### services/README.md
- Các API endpoints
- Cách gọi API
- Xử lý errors
- Authentication

### store/README.md
- Cấu trúc Redux store
- Các actions và reducers
- Cách thêm state mới
- Best practices

### utils/README.md
- Danh sách các utility functions
- Cách sử dụng
- Ví dụ minh họa 