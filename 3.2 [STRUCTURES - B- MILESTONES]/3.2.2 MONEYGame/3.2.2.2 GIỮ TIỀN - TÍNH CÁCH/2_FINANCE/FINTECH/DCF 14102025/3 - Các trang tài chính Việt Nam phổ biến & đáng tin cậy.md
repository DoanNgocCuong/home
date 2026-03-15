## 🏦 1. Các trang tài chính Việt Nam phổ biến & đáng tin cậy

|Trang|Loại dữ liệu|Cấu trúc HTML / API|Ưu điểm|Nhược điểm|
|---|---|---|---|---|
|**Cafef.vn** (thuộc VCCorp)|Báo cáo tài chính, lịch sử giá, chỉ số PE, EPS, dòng tiền|HTML có cấu trúc tương đối ổn (`div#divTableData`)|Có hầu hết công ty VN|Không có API, cần xử lý AJAX + rate limit|
|**Vietstock.vn**|Báo cáo tài chính chi tiết, phân tích, chỉ số, DCF|HTML và JS dynamic|Dữ liệu đầy đủ, cập nhật nhanh|JS render (phải dùng Selenium/Playwright)|
|**SSI iBoard / FiinTrade / FiinPro**|Real-time quotes, phân tích cơ bản|Có API riêng (cần key hoặc mua gói)|Ổn định, chuyên nghiệp|Trả phí, hạn chế request|
|**HNX / HOSE / UPCoM websites**|Báo cáo gốc (PDF, Excel)|File link cố định theo năm|Chính thức, nguồn xác thực|Khó parse, PDF thường là scan|
|**Company IR websites** (ví dụ: QTP.com.vn, POW.vn)|Báo cáo gốc (PDF)|Tên file có pattern|Đảm bảo chính xác|Cần crawl từng công ty riêng|
|**Investing.com / TradingView / Yahoo Finance (VN)**|Giá cổ phiếu, chỉ số, lịch sử|Có API ẩn / JSON endpoint|Dễ crawl, nhẹ|Không có dữ liệu dòng tiền chi tiết|
