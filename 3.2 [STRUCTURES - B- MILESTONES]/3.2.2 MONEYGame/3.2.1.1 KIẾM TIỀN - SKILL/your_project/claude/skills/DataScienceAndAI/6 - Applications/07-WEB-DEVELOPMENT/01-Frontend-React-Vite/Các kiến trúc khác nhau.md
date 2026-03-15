
**1. Event-Driven Architecture (EDA) – Kiến Trúc Hướng Sự Kiện**

Mô hình này hoạt động dựa trên các sự kiện, khi một sự kiện xảy ra, nó sẽ kích hoạt một hành động khác, giống như hiệu ứng domino.

 ![💡](https://static.xx.fbcdn.net/images/emoji.php/v9/t3c/1/16/1f4a1.png) **Ứng dụng thực tế:**  
![✅](https://static.xx.fbcdn.net/images/emoji.php/v9/t33/1/16/2705.png) Marketplace trực tuyến: Gửi thông báo cho người dùng về khuyến mãi hoặc sản phẩm mới.  
![✅](https://static.xx.fbcdn.net/images/emoji.php/v9/t33/1/16/2705.png) Thiết bị IoT: Cảm biến phát hiện chuyển động và tự động bật đèn.

**Thành phần chính:**

- **Sự kiện (Event):** Tương tác của người dùng hoặc tín hiệu từ cảm biến.
    

- **Bộ xử lý sự kiện (Event Handlers):** Nhận và xử lý sự kiện.
    

- **Bus sự kiện (Event Bus):** Truyền tải sự kiện giữa các thành phần hệ thống.
    

**2. Layered Architecture – Kiến Trúc Phân Tầng**

Chia hệ thống thành nhiều tầng logic khác nhau, mỗi tầng đảm nhiệm một chức năng riêng biệt. Giống như một ngôi nhà có các tầng với mục đích khác nhau.

 ![💡](https://static.xx.fbcdn.net/images/emoji.php/v9/t3c/1/16/1f4a1.png) **Ứng dụng thực tế:**  
![✅](https://static.xx.fbcdn.net/images/emoji.php/v9/t33/1/16/2705.png) Hệ thống ngân hàng: Phân tách giao diện, xử lý nghiệp vụ và truy xuất dữ liệu.  
![✅](https://static.xx.fbcdn.net/images/emoji.php/v9/t33/1/16/2705.png) Mạng xã hội: Tách biệt các tính năng như hồ sơ, bảng tin, thông báo.

**Thành phần chính:**

- **Presentation Layer:** Giao diện người dùng.
    

- **Business Logic Layer:** Xử lý dữ liệu và nghiệp vụ.
    

- **Data Access Layer:** Tương tác với cơ sở dữ liệu.
    

**3. Monolithic Architecture – Kiến Trúc Nguyên Khối**

Toàn bộ ứng dụng được phát triển trong một khối duy nhất, các thành phần liên kết chặt chẽ với nhau.

 ![💡](https://static.xx.fbcdn.net/images/emoji.php/v9/t3c/1/16/1f4a1.png) **Ứng dụng thực tế:**  
![✅](https://static.xx.fbcdn.net/images/emoji.php/v9/t33/1/16/2705.png) Hệ thống CMS (Quản lý nội dung): Tích hợp viết bài, xuất bản và quản lý nội dung.  
![✅](https://static.xx.fbcdn.net/images/emoji.php/v9/t33/1/16/2705.png) Hệ thống ERP: Bao gồm các module như nhân sự, tài chính trong cùng một hệ thống.

**Thành phần chính:**

- Một codebase duy nhất.
    

**4. Microservices Architecture – Kiến Trúc Vi Dịch Vụ**

Chia hệ thống thành nhiều dịch vụ nhỏ, độc lập, mỗi dịch vụ đảm nhận một chức năng cụ thể.

 ![💡](https://static.xx.fbcdn.net/images/emoji.php/v9/t3c/1/16/1f4a1.png) **Ứng dụng thực tế:**  
![✅](https://static.xx.fbcdn.net/images/emoji.php/v9/t33/1/16/2705.png) Thương mại điện tử: Xử lý danh mục sản phẩm, đơn hàng, xác thực người dùng dưới dạng các dịch vụ riêng biệt.  
![✅](https://static.xx.fbcdn.net/images/emoji.php/v9/t33/1/16/2705.png) Đặt vé du lịch: Quản lý đặt chỗ chuyến bay, đặt phòng khách sạn và thanh toán riêng biệt.

**Thành phần chính:**

- Các dịch vụ độc lập, giao tiếp qua API.
    

- Mỗi dịch vụ có cơ sở dữ liệu riêng.
    

**5. Model-View-Controller (MVC) – Kiến Trúc MVC**

Chia ứng dụng thành ba phần riêng biệt giúp dễ quản lý và mở rộng.

 ![💡](https://static.xx.fbcdn.net/images/emoji.php/v9/t3c/1/16/1f4a1.png) **Ứng dụng thực tế:**  
![✅](https://static.xx.fbcdn.net/images/emoji.php/v9/t33/1/16/2705.png) Lập trình web: Cấu trúc website với phần dữ liệu, giao diện và điều khiển riêng biệt.

 ![🔧](https://static.xx.fbcdn.net/images/emoji.php/v9/t52/1/16/1f527.png) **Thành phần chính:**

- **Model:** Xử lý dữ liệu và logic nghiệp vụ.
    

- **View:** Hiển thị giao diện cho người dùng.
    

- **Controller:** Nhận yêu cầu từ người dùng và điều hướng luồng xử lý.
    

**6. Master-Slave Architecture – Kiến Trúc Chủ-Tớ**

Một node chính (master) điều khiển các node phụ (slave), giúp tối ưu hóa hiệu suất.

 ![💡](https://static.xx.fbcdn.net/images/emoji.php/v9/t3c/1/16/1f4a1.png) **Ứng dụng thực tế:**  
![✅](https://static.xx.fbcdn.net/images/emoji.php/v9/t33/1/16/2705.png) Sao chép cơ sở dữ liệu: Master ghi dữ liệu, các Slave chỉ đọc dữ liệu để giảm tải.

 ![🔧](https://static.xx.fbcdn.net/images/emoji.php/v9/t52/1/16/1f527.png) **Thành phần chính:**

- **Master:** Xử lý các thao tác ghi dữ liệu.
    

- **Slave:** Sao chép dữ liệu để phục vụ truy vấn đọc.
    

**Tóm lại:** Mỗi kiến trúc đều có ưu và nhược điểm riêng, tùy vào nhu cầu mà lựa chọn cho phù hợp.

 ![📢](https://static.xx.fbcdn.net/images/emoji.php/v9/t39/1/16/1f4e2.png) Bạn đang phát triển một doanh nghiệp công nghệ và muốn bứt phá với chiến lược marketing hiệu quả? Đừng để sản phẩm của bạn bị lu mờ.

----
![[attachments/Pasted image 20250225113316.png]]


### 🎯 **Xu hướng khác cũng được quan tâm:**

- **Event-Driven Architecture (EDA):** Cực kỳ phổ biến trong các hệ thống thời gian thực như IoT, thanh toán trực tuyến.
- **Layered Architecture:** Vẫn phổ biến trong các hệ thống doanh nghiệp truyền thống như ngân hàng, ERP.

---

👉 **Tóm lại:**

- **Ứng dụng lớn, cần mở rộng:** 👉 _Microservices Architecture_
- **Ứng dụng web, dễ bảo trì:** 👉 _MVC_
- **Hệ thống xử lý thời gian thực:** 👉 _EDA_
- **Dự án nhỏ, phát triển nhanh:** 👉 _Monolithic Architecture_