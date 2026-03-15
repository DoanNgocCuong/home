Dưới đây là nội dung tài liệu được chuyển đổi sang định dạng Markdown, giữ nguyên nội dung gốc để bạn dễ dàng sử dụng và lưu trữ.

---

Hướng Dẫn Chi Tiết Triển Khai Bước 2 & 3 1

Chào bạn, tôi đã phân tích kỹ lưỡng tài liệu `PikaRobot_Experience_Spec_Edgecase_Catalog_VI.pdf` và hiểu rõ mức độ chi tiết, cấu trúc chặt chẽ mà bạn đang hướng tới2.

Dựa trên bối cảnh đó, tôi xin trả lời các băn khoăn của bạn về **Bước 2** và **Bước 3**, đảm bảo rằng các sản phẩm tạo ra sẽ khớp nối liền mạch với nhau và phục vụ hiệu quả cho việc phân tích bằng AI/agents3.

---

Bước 2: Cách Mô Tả Codebase Để Phân Tích Bằng LLM/Agents 4

### Băn khoăn của bạn

> "Cái tôi cần bạn làm là độ chi tiết và cách mô tả codebase đó nên như nào, để còn phù hợp cho việc đánh giá bugs và phân tích nút thắt... để có thể dùng các công cụ ngoài như LLM hay agents để đánh giá khả năng của nó khi phân tích integration testing/stresstesting/long running test." 5

### Giải pháp

Để LLM/Agent có thể phân tích được các bài test phức tạp (integration, stress, long-running), chúng ta cần cung cấp cho nó một bản "technical spec" của từng khối mã nguồn (component)6.

Bản spec này không chỉ mô tả chức năng, mà phải lượng hóa được các yếu tố quan trọng trong hệ thống nhúng: tài nguyên, thời gian, và sự tương tranh7. Nó chính là cầu nối giữa Experience Spec (cái nên có) và mã nguồn (cái đang có)8.

Chúng tôi đề xuất một cấu trúc mô tả chuẩn cho mỗi "Component" trong codebase, gọi là **Component Technical Profile (CTP)**9. Một component có thể là một FreeRTOS task, một module/driver, hoặc một nhóm hàm chức năng quan trọng10.

Cấu Trúc của một Component Technical Profile (CTP) 11

Đây là một template bạn có thể áp dụng, được thiết kế để máy (LLM) có thể đọc và người có thể hiểu12. Nó nên được viết dưới dạng Markdown và đặt gần mã nguồn, hoặc được sinh ra tự động trong pipeline CI/CD13.

Markdown

```
### CTP-ID: [Tên Component Độc Nhất]
**Maps to Spec Step**: [ID của Step trong Experience Spec, ví dụ: 1.2, 2.2.1]
**Description**: [Mô tả ngắn gọn chức năng của component]

#### 1. Resource Profile (Hồ sơ Tài nguyên)
**Static Memory (ROM)**: [số] KB (ước tính kích thước mã nguồn và dữ liệu hằng).
**Stack Memory (RAM)**: [số] bytes (dựa trên uxTaskGetStackHighWaterMark() sau khi chạy stress test).
**Dynamic Memory (Heap)**:
  - **Allocates**: [Yes/No]
  - **Pattern**: [Mô tả hành vi cấp phát, ví dụ: "Cấp phát 1 block 512KB khi bắt đầu, giải phóng khi kết thúc"]
  - **Max Allocation**: [số] bytes (tổng dung lượng cấp phát tối đa cùng lúc).

#### 2. Timing Profile (Hồ sơ Thời gian)
**CPU Time Slice**: [số] ms (thời gian CPU trung bình/tối đa trong một chu kỳ hoạt động).
**Execution Path Latency**:
  - **Path**: [Mô tả luồng, ví dụ: "Từ lúc nhận event A đến lúc phát ra event B"]
  - **Latency**: [số] ms (độ trễ trung bình/tối đa cho luồng đó).

#### 3. Concurrency Profile (Hồ sơ Tương tranh)
**Task Priority**: [số] (Mức ưu tiên của FreeRTOS task).
**Shared Resources**: [Liệt kê các tài nguyên dùng chung, ví dụ: SPI_BUS, g_wifi_status, i2s_driver].
**Synchronization**: [Liệt kê các cơ chế bảo vệ, ví dụ: Mutex(spi_mutex), Semaphore (wifi_semaphore)].

#### 4. I/O & Dependencies Profile (Hồ sơ Giao tiếp & Phụ thuộc)
**Inputs**: [Liệt kê các đầu vào: event, message queue, hàm được gọi].
**Outputs**: [Liệt kê các đầu ra: event, message queue, giá trị trả về].
**Dependencies**: [Liệt kê các component khác mà nó gọi hoặc phụ thuộc vào].

#### 5. State Machine & Error Handling
**States**: [Liệt kê các trạng thái chính, ví dụ: IDLE, CONNECTING, CONNECTED, ERROR].
**Error Handling**: [Mô tả cách xử lý lỗi, ví dụ: "Khi timeout, chuyển sang trạng thái ERROR và gửi event WIFI_CONNECT_FAIL"].
```

14

Cách Tạo và Sử Dụng 15

1. Tự động hóa là chìa khóa: Áp dụng phương án kết hợp Static Analysis + AI16.

- **Static Analysis Tools:** (như đã đề cập ở kế hoạch trước) sẽ tự động điền các thông số khách quan: Stack Memory, Shared Resources, Dependencies17.
    
- **AI-Generated Documentation:** Sẽ đọc mã nguồn để sinh ra bản nháp cho các phần mô tả: Description, State Machine, Error Handling18.
    

2. Vai trò của Lập trình viên:

Lập trình viên sẽ review, chỉnh sửa các thông tin do AI tạo ra và quan trọng nhất là điền vào trường Maps to Spec Step19. Đây là liên kết vàng giúp AI có thể đối chiếu yêu cầu sản phẩm với thực tế kỹ thuật20.

3. Cung cấp cho LLM/Agent:

Khi cần phân tích, bạn sẽ cung cấp cho Agent một bộ ngữ cảnh hoàn chỉnh21:

- **Yêu cầu:** "Phân tích kịch bản stress test cho tính năng WiFi Setup (Step 1.2)"22.
    
- **Ngữ cảnh:** 23
    
    1. File `Experience_Spec.pdf` (đặc biệt là section 1.2)24.
        
    2. File `CTP_wifi_manager.md` (Component Technical Profile của task quản lý WiFi)25.
        
    3. File `CTP_led_driver.md` (CTP của driver điều khiển LED)26.
        
    4. (Tùy chọn) Log của một lần bug xảy ra trước đây27.
        

Với bộ thông tin này, Agent có thể đưa ra những phân tích sâu sắc như:

> "Dựa trên CTP, task `wifi_manager` có độ ưu tiên là 5, trong khi task `led_driver` có độ ưu tiên là 6. Khi wifi_manager đang chờ kết nối (block), led_driver vẫn có thể chạy để cập nhật trạng thái đèn LED. Tuy nhiên, nếu wifi_manager cần truy cập một tài nguyên mà led_driver đang giữ, có nguy cơ xảy ra priority inversion. Spec yêu cầu thời gian kết nối <= 5 giây, nhưng CTP cho thấy latency của luồng kết nối có thể lên tới 7 giây trong trường hợp xấu nhất. Đây là một mâu thuẫn tiềm tàng (Bug Cấp 2)." 28

---

Bước 3: Mức Độ Chi Tiết Của Sơ Đồ Kiến Trúc C4 29

### Băn khoăn của bạn

> "Tôi sẽ chọn 4C, nhưng vẫn cần biết nên mô tả ở mức độ chi tiết như nào để khớp được với các nhiệm vụ khác." 30

### Giải pháp

Để khớp với các tài liệu khác và phục vụ phân tích, các sơ đồ C4 của bạn cần tuân thủ nguyên tắc **"Traceability by Naming"** – tức là tên của các thành phần trong sơ đồ phải ánh xạ trực tiếp đến tên trong Experience Spec và Component Technical Profile31.

Mức Độ Chi Tiết Cho Từng Cấp Độ C4 32

Cấp 1: System Context 33

- **Mục đích:** Trả lời câu hỏi "Hệ thống của chúng ta là gì và nó tương tác với ai/cái gì?" 34
    
- **Độ chi tiết:** Rất cao (high-level). Chỉ bao gồm35:
    
    - **Person:** Parent/Child (người dùng)36.
        
    - **System (hệ thống của bạn):** Pika Robot System (một hộp đen duy nhất)37.
        
    - **External Systems:** Cloud Backend, Companion App (ứng dụng di động), WiFi Router38.
        
- **Cách khớp nối:** Tên của các hệ thống phải nhất quán với các thuật ngữ trong Experience Spec39.
    

Cấp 2: Containers 40

- **Mục đích:** Phóng to vào Pika Robot System, cho thấy các khối lớn, có thể triển khai độc lập (deployable units)41.
    
- **Độ chi tiết:** Các "container" chính bên trong robot và các hệ thống bên ngoài42.
    
    - **Bên trong Robot:**
        
        - `Firmware Application (ESP32)`: Toàn bộ chương trình chạy trên chip ESP3243.
            
        - `SD Card Storage`: Hệ thống file trên thẻ nhớ44.
            
    - **Bên ngoài Robot:** 45
        
        - `Companion App`: Ứng dụng di động46.
            
        - `API Gateway`: Điểm vào của backend47.
            
        - `AI Service`: Dịch vụ xử lý ngôn ngữ tự nhiên48.
            
        - `Database`: Cơ sở dữ liệu người dùng49.
            
- **Cách khớp nối:** Tên của các container này sẽ là ngữ cảnh cấp cao cho các Component ở Cấp 350.
    

Cấp 3: Components 51

- **Mục đích:** Phóng to vào container `Firmware Application (ESP32)`, cho thấy các thành phần logic chính. **Đây là cấp độ quan trọng nhất để khớp với Component Technical Profile (CTP)**52.
    
- **Độ chi tiết:** Mỗi hộp trong sơ đồ này nên tương ứng với một CTP53.
    
    - **Tên Component:** Tên phải giống hệt với **CTP-ID**. Ví dụ: `wifi_manager`, `audio_player`, `led_driver`, `event_dispatcher`54.
        
    - **Mô tả Component:** Một dòng mô tả ngắn gọn, có thể lấy từ trường Description trong CTP55.
        
    - **Mũi tên (Relations):** Các mũi tên phải thể hiện rõ Dependencies trong CTP. Ví dụ, một mũi tên từ `audio_player` đến `SD Card Storage` với nhãn "Reads audio files via SPIFFS"56.
        
- **Cách khớp nối:** Đây là sự ánh xạ 1-157. Khi LLM/Agent đọc sơ đồ Cấp 3, nó thấy một hộp tên là `wifi_manager`58. Nó sẽ biết rằng cần phải tìm và đọc file `CTP_wifi_manager.md` để có thông tin chi tiết về tài nguyên, thời gian, và tương tranh của component này59.
    

Cấp 4: Code 60

- **Mục đích:** (Tùy chọn) Đi sâu vào một component để xem cấu trúc bên trong61.
    
- **Độ chi tiết:** Sơ đồ lớp (class diagram) hoặc sơ đồ các hàm chính62.
    
- Cấp độ này thường không cần thiết cho việc phân tích tổng thể, trừ khi cần đào sâu vào một bug rất phức tạp63. Các công cụ như IDE hoặc static analyzer có thể tự sinh ra sơ đồ này khi cần64.
    

---

**Tổng kết:**

Bằng cách áp dụng quy tắc đặt tên và ánh xạ chặt chẽ này, bạn tạo ra một bộ tài liệu có khả năng truy vết từ cao xuống thấp: từ một bước trong **Experience Spec** -> một Component trong **sơ đồ C4 Cấp 3** -> một **Component Technical Profile** chi tiết -> **mã nguồn** thực tế65.

Đây chính là nền tảng vững chắc để các công cụ AI có thể thực hiện những phân tích phức tạp và đáng tin cậy66.

Tôi đã sẵn sàng để tiếp tục hỗ trợ bạn triển khai các bước này hoặc trả lời bất kỳ câu hỏi nào khác67.