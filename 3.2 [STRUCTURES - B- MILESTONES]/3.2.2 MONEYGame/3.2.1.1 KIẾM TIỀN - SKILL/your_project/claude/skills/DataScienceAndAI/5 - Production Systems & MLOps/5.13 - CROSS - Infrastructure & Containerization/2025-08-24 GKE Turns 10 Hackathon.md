**GKE Turns 10 Hackathon** là một cuộc thi hackathon do Google tổ chức nhân dịp dịch vụ Google Kubernetes Engine (GKE) tròn 10 tuổi. Đây không phải “game” mà là cuộc thi kỹ năng lập trình với tổng giải thưởng 50.000 USD. Theo quy định chính thức, đây là cuộc thi kỹ năng; người tham gia phải trên độ tuổi thành niên tại nơi cư trú và không thuộc các vùng bị cấm như Ý, Quebec, Cuba, Iran, v.v.. Mục tiêu của hackathon là “nâng cấp” một ứng dụng microservice có sẵn (Bank of Anthos hoặc Online Boutique) bằng cách xây dựng các thành phần container hóa mới để giao tiếp với API hiện có mà không sửa code gốc, đồng thời triển khai toàn bộ trên GKE và tận dụng mô hình AI của Google như Gemini.

### Yêu cầu nộp bài

Theo phần “What to Submit” trong quy định, bài dự thi cần có:

- **Dự án được triển khai** với công nghệ yêu cầu (GKE, mô hình AI) đáp ứng đầy đủ yêu cầu.
    
- **Lựa chọn khu vực** phù hợp (Bắc Mỹ, Châu Âu–Trung Đông–Châu Phi, Châu Á–Thái Bình Dương, v.v.) để tính giải khu vực.
    
- **URL sản phẩm chạy thực tế** (web UI, ứng dụng di động, v.v.) – khuyến khích mạnh.
    
- **Mô tả chi tiết bằng tiếng Anh**: tóm tắt tính năng, công nghệ dùng (GKE, ADK, MCP, A2A…), nguồn dữ liệu và bài học trong quá trình làm.
    
- **Link kho mã nguồn công khai** và **sơ đồ kiến trúc** minh họa các thành phần và cách chúng giao tiếp.
    
- **Video demo ≤ 3 phút** cho thấy dự án hoạt động trên nền tảng mục tiêu, đăng công khai (YouTube/Vimeo) và có phụ đề tiếng Anh nếu cần.
    
- **Tuân thủ pháp luật và không sử dụng nội dung sở hữu trí tuệ của bên thứ ba**.
    
- Có thể nhận thêm điểm thưởng nếu bạn: (1) đăng bài blog/podcast/video công khai mô tả cách bạn xây dựng dự án trên GKE (cộng thêm tối đa 0,4 điểm) và (2) đăng bài quảng bá dự án trên mạng xã hội (X, LinkedIn…) với hashtag #GKEHackathon hoặc #GKETurns10 (tối đa 0,4 điểm).
    

### Tiêu chí chấm điểm

Các bài nộp vượt qua vòng sơ tuyển sẽ được chấm theo ba tiêu chí có trọng số:

1. **Triển khai kỹ thuật – 40 %**: Mức độ sạch sẽ, tối ưu và có tài liệu của code; khả năng triển khai ứng dụng và agent trên GKE và giao tiếp qua framework agent.
    
2. **Demo & trình bày – 40 %**: Bài nộp phải xác định vấn đề rõ ràng, trình bày giải pháp qua mô tả, sơ đồ kiến trúc và video; giải thích cách sử dụng GKE, framework agent và công cụ liên quan.
    
3. **Đổi mới & sáng tạo – 20 %**: Mức độ độc đáo và khả năng giải quyết vấn đề mới; ý tưởng vượt ra ngoài các ứng dụng AI cơ bản.
    

Điểm cao nhất tối đa là 5,8 (nhờ phần thưởng tùy chọn). Bài có điểm cao nhất trong mỗi khu vực sẽ nhận giải khu vực; bài có điểm cao nhất toàn cầu sẽ nhận giải Grand Prize.

### Cách để có cơ hội giành TOP 1

- **Chọn bài toán hấp dẫn**: Phân tích Bank of Anthos hoặc Online Boutique và xác định vấn đề thực tế (ví dụ, tối ưu hóa quy trình thanh toán, cá nhân hóa sản phẩm, quản lý rủi ro…). Sử dụng mô hình AI của Google (như Gemini) để xây dựng agent giải quyết vấn đề đó.
    
- **Thiết kế kiến trúc rõ ràng**: Tách agent ra khỏi ứng dụng gốc, triển khai lên GKE và giao tiếp qua API hoặc các giao thức MCP/A2A; mô tả kỹ sơ đồ kiến trúc trong tài liệu.
    
- **Viết code sạch và có tài liệu**: Tuân thủ best practices về container, Kubernetes (Helm, CI/CD), bảo mật, logging; cung cấp README và hướng dẫn triển khai.
    
- **Chuẩn bị demo chuyên nghiệp**: Video ≤ 3 phút cần có kịch bản mạch lạc: giới thiệu bài toán, mô tả kiến trúc, demo trực tiếp, nêu kết quả và lợi ích; phụ đề tiếng Anh nếu nói tiếng khác.
    
- **Tăng cường yếu tố sáng tạo**: Kết hợp nhiều agent chuyên biệt và giao tiếp phức tạp; sử dụng ADK/MCP/A2A để tạo workflow thông minh; thử nghiệm các tính năng mới của GKE (auto‑scaling, GPU) để chạy mô hình AI hiệu quả.
    
- **Điểm thưởng**: Đăng bài blog hoặc video chia sẻ chi tiết quy trình xây dựng dự án trên Medium, dev.to, YouTube, v.v., và đăng bài mạng xã hội với hashtag theo yêu cầu để tăng điểm.
    
- **Tuân thủ thời hạn và vùng**: Deadline trên trang Devpost là 22 Tháng 9 2025 5:00 pm PDT (tương đương 23 Tháng 9 2025 7:00 am GMT+7). Hoàn thành bài và nộp trước thời hạn. Lựa chọn khu vực “Asia Pacific” nếu bạn ở Việt Nam.
    

Tóm lại, GKE Turns 10 Hackathon là cơ hội để xây dựng microservice tích hợp AI trên nền tảng GKE. Để đạt giải cao nhất, bạn cần đáp ứng đầy đủ yêu cầu kỹ thuật, trình bày và demo rõ ràng, đồng thời tạo ra giải pháp sáng tạo giải quyết vấn đề thực tế.