
Link Notebook LLMs: https://notebooklm.google.com/notebook/3af87cca-652b-4ff2-80d8-26e967c32a37

# 1. Summary 

```
NotebookLM: Tóm tắt bằng tiếng Việt 1 cách chi tiết, chuyên sâu, cụ thể, giữ nguyên số liệu, đúng thứ tự, đảm bảo cover đầy đủ nội dung. Các Heading Style sẽ được đặt mặc định với Chủ đề lớn( hoặc là tên sách nếu trong trường hợp tóm tắt sách ) là định Dạng H2 , Còn lại các Chương / Đề mục nhỏ hơn sẽ là định Dạng H3 và cứ thế phân cấp xuống các cấp độ Heading Style nhỏ hơn tùy theo cấp độ phân cấp của văn bản gốc. Có nhiều biểu tượng minh họa lớn nhỏ khác nhau trải dài khắp nội dung . giữ nguyên các câu chuyện kể ( nếu có ) và ko tóm tắt quá mức khiến câu chuyện bị tóm tắt quá trở nên khó hiểu. kẻ bảng tổng hợp ở cuối bài để cô đọng thông tin.
```

Đây là bản tóm tắt chi tiết, chuyên sâu và cụ thể theo yêu cầu của bạn, dựa trên các đoạn trích từ cuốn **Cẩm nang 100 triệu đô: Nuôi dưỡng Khách hàng Tiềm năng** của Alex Hormozi.

## Cẩm nang 100 triệu đô: Nuôi dưỡng Khách hàng Tiềm năng

_Cách khiến nhiều khách hàng tiềm năng hơn phản hồi, đặt lịch và có mặt_

**Tuyên bố miễn trừ trách nhiệm và thông tin chung**

Thông tin trong cuốn sách này chỉ nhằm mục đích giáo dục và cung cấp thông tin. Tác giả, nhà xuất bản và nhà phân phối được cấp phép không đưa ra bất kỳ tuyên bố hay bảo đảm nào về khả năng bán được, sự phù hợp, tính chính xác hoặc độ tin cậy. Các chiến lược được cung cấp nguyên trạng ("as-is").

Các tuyên bố về thu nhập chỉ là mong muốn về thu nhập tiềm năng; kết quả thành công được tham chiếu là những kết quả **đặc biệt, không điển hình**. Kết quả của mỗi cá nhân sẽ luôn khác nhau và phụ thuộc vào năng lực, đạo đức làm việc, kỹ năng, kinh nghiệm, nền kinh tế và các yếu tố khác. Điều hành doanh nghiệp liên quan đến nguy cơ thua lỗ. Công ty không chịu trách nhiệm pháp lý cho bất kỳ tổn thất kinh doanh tiềm ẩn nào liên quan đến các chiến lược này.

Cuốn sách này được Bản quyền © 2025 bởi Bumble IP, LLC.

### Nuôi dưỡng Khách hàng Tiềm năng

_“Nếu họ không có mặt, họ không thể mua.”_

**Câu chuyện về ALAN và sự khám phá các điểm dữ liệu then chốt**

Vào tháng 6 năm 2020, do COVID-19 và các quy định của chính phủ, các phòng gym truyền thống (nguồn khách hàng _duy nhất_ của tác giả) bị cấm hoạt động, khiến việc kinh doanh trở nên khó khăn. Tác giả đã phát triển phần mềm **ALAN** (**Artificial Lead Automation & Nurture**) để tự động hóa việc thiết lập cuộc hẹn và nhắc nhở mọi người đến các cuộc hẹn _trực tiếp_. Tuy nhiên, phần mềm này hoạt động theo mô hình "trả tiền cho mỗi lần có mặt" (pay per show), nên khi không ai đến các doanh nghiệp truyền thống, phần mềm không kiếm được tiền.

Tác giả chuyển sang phục vụ các công ty tiếp thị cho “các doanh nghiệp thiết yếu,” nhanh chóng có được **mười công ty (agency)** đầu tiên, mang lại **vài trăm khách hàng chỉ sau một đêm** (vì mỗi công ty có từ **10 đến 50 khách hàng**). Tuy nhiên, các tính năng phần mềm dành cho phòng gym không chuyển đổi tốt sang các cuộc hẹn qua điện thoại hoặc video. Công cụ này bắt đầu "quản lý" **hơn 4.000 cuộc hẹn mỗi ngày**, nhưng lại quản lý để làm hỏng chúng.

Tác giả đã thuê Vlad, một chuyên gia dữ liệu xuất sắc (từng chiến thắng cuộc thi Olympic máy học của Nga). Vlad đã sàng lọc dữ liệu cuộc hẹn và tìm ra **bốn điểm dữ liệu tương quan với các cuộc hẹn tích cực**:

1. Càng có **nhiều khung giờ trống**, tỷ lệ có mặt càng cao.
2. Khách hàng tiềm năng đặt lịch càng **ít ngày sau** (càng gần), tỷ lệ có mặt càng cao.
3. Càng có **nhiều lần theo dõi**, tỷ lệ có mặt càng cao.
4. Khách hàng tiềm năng **phản hồi các lần theo dõi càng thường xuyên**, tỷ lệ có mặt càng cao.

**Định nghĩa và Giá trị của Tỷ lệ Có mặt**

Để thống nhất ngôn ngữ:

- **Tỷ lệ đặt lịch (Schedule rate):** Phần trăm khách hàng tiềm năng đã tương tác có đặt lịch hẹn.
- **Tỷ lệ có mặt (Show rate):** Tỷ lệ phần trăm khách hàng tiềm năng đã đặt lịch có mặt tại cuộc hẹn.
- **Thông lượng (Throughput):** Tổng tỷ lệ phần trăm khách hàng tiềm năng đã tương tác có mặt.
- _Ví dụ:_ **100** khách hàng tiềm năng * 50% Tỷ lệ đặt lịch = **50** Cuộc hẹn đã đặt * 50% Tỷ lệ có mặt = **25** Cuộc hẹn có mặt. Thông lượng là **25%** (25 lần có mặt trên 100 khách hàng tiềm năng).

Mức tăng doanh thu **20-40%** có thể bằng **2 đến 3 lần lợi nhuận** của doanh nghiệp (với biên lợi nhuận **20%**) chỉ trong năm đầu tiên. Cẩm nang này tập trung vào nuôi dưỡng khách hàng tiềm năng trung hạn, nhằm tối đa hóa tỷ lệ có mặt trong **30 ngày**.

### Bốn Trụ cột của Nuôi dưỡng Khách hàng Tiềm năng

_Bạn phải nhất quán trước khi có thể trở nên xuất sắc._

Dựa trên dữ liệu thu thập từ ALAN và các công ty danh mục đầu tư (tạo ra **hơn 20.000 khách hàng tiềm năng mỗi ngày**), tỷ lệ có mặt được thúc đẩy bởi bốn yếu tố chính:

1. **Sự Sẵn có (Availability) ⏱️:** Số lượng khung giờ hẹn trống bạn có.
    - _Ví dụ:_ Mở cửa **bảy ngày một tuần, 24 giờ một ngày** so với đối thủ chỉ mở 3 ngày/tuần.
2. **Tốc độ liên hệ (Speed to contact) 🚀:** Tốc độ phản hồi khách hàng tiềm năng và thời gian đặt lịch hẹn trước.
    - _Ví dụ:_ Gọi trong vòng **42 giây** sau khi đăng ký so với đối thủ mất trung bình **42 giờ**.
3. **Cá nhân hóa (Personalization) 👤:** Làm cho giao tiếp hữu ích và phù hợp _với họ_. Việc theo dõi càng cá nhân hóa, khả năng phản hồi và có mặt càng cao.
4. **Số lượng (Volume) 📈:** Số lần bạn liên hệ với khách hàng tiềm năng trước khi từ bỏ.
    - _Ví dụ:_ Liên hệ **hơn 5 lần** thay vì trung bình **1,3 lần cố gắng** (với **44%** nhân viên bán hàng dừng lại sau lần cố gắng đầu tiên).

### Trụ cột I: Sự Sẵn có ⏱️

_Nếu khách hàng tiềm năng không thể đặt lịch, họ sẽ không có mặt._

**Câu chuyện tiệm làm móng của Leila**

Trong một chuyến công tác đến Los Angeles vào tháng 6 năm 2021, vợ tác giả là Leila muốn làm móng và tìm kiếm trên Yelp. Cô ấy gọi 4 tiệm:

- Tiệm 1: Không ai trả lời.
- Tiệm 2: Nhấc máy, không còn chỗ trống trong vòng một giờ, chỉ có thể hẹn ngày mai.
- Tiệm 3: Nhấc máy, nói có thể có chỗ nhưng sẽ gọi lại sau (và cúp máy).
- Tiệm 4: Nhấc máy, xác nhận nhận khách vãng lai (walk-in), hỏi tên và số điện thoại, gửi tin nhắn xác nhận ngay lập tức, và sắp xếp cho thợ làm móng tên Nancy.

Dữ liệu cho thấy, **sự sẵn có** là đòn bẩy lớn nhất để có thêm nhiều khách hàng tiềm năng có mặt. Sự sẵn có (tổng số ngày, số giờ mỗi ngày, và số khung giờ mỗi giờ) là yếu tố dự đoán lớn nhất cho thông lượng.

**Mô tả và Chiến thuật**

Sự sẵn có là sự _kết hợp của số lượng khung giờ hẹn và khách hàng tiềm năng có thể đặt lịch trước bao xa_. Việc tăng sự sẵn có có thể dễ dàng thấy sự gia tăng **20-40%**, đôi khi **hơn 200%** số lượng cuộc hẹn _có mặt_.

**Chiến thuật:**

1. **Nhận Lịch Hẹn Nhiều Ngày Hơn Trong Tuần:** Bán hàng **bảy ngày mỗi tuần**. Việc nhận lịch hẹn bảy ngày mỗi tuần giúp doanh nghiệp sẵn có hơn **40% để chấp nhận tiền**.
2. **Nhận Lịch Hẹn Nhiều Giờ Hơn Mỗi Ngày:** Hãy sẵn sàng bán hàng khi khách hàng của bạn sẵn sàng mua hàng. Đối với bán hàng trên toàn quốc, khung giờ **6 giờ sáng đến 6 giờ tối theo giờ PST** bao gồm tỷ lệ phần trăm doanh số bán hàng cao nhất ở Mỹ so với số giờ.
3. **Cho Khách Hàng Tiềm Năng Thời Gian Hẹn Linh Hoạt Hơn:** Cung cấp **bốn tùy chọn đặt lịch mỗi giờ** (ví dụ: 12:00, 12:15, 12:30, 12:45, v.v.) thay vì mỗi 30 hoặc 60 phút.
    - _Lưu ý:_ Việc sàng lọc khách hàng tiềm năng (qualify) và chốt đơn (close) trên các cuộc gọi riêng biệt (cuộc gọi sàng lọc **15 phút**) sẽ giải quyết vấn đề này.
4. **Có Các Tùy Chọn Đặt Lịch Gọi Vào (Inbound), Gọi Ra (Outbound) và Tự Đặt Lịch (Self-Scheduling):** Cần làm **cả ba**.

**Mẹo để Trình Đặt Lịch Trực Tuyến hoạt động tốt hơn:**

- Đảm bảo tiêu đề đầu trang xác nhận họ đang ở đúng nơi (Tiêu đề đầu trang = **Chú ý [Chân dung khách hàng]**).
- Làm cho các ngày và giờ có sẵn trở nên **siêu rõ ràng** ngay khi trang tải.
- Loại bỏ càng nhiều bước càng tốt. **Đừng bắt khách hàng tiềm năng làm lại** thông tin đã cung cấp, điều này tạo ra những cải tiến _khổng lồ_ trong tỷ lệ đặt lịch.

Để giải quyết tình trạng **quá nhiều cuộc hẹn kém chất lượng**, có thể thêm rào cản (friction) như thêm video xem trước, thư bán hàng, giá cả hoặc trì hoãn thời điểm trình đặt lịch xuất hiện.

### Trụ cột II: Tốc độ 🚀

_Tiền yêu tốc độ. Của cải yêu thời gian. Nghèo đói yêu sự thiếu quyết đoán._

**Thống kê về Tốc độ:**

- Tỷ lệ chuyển đổi bán hàng **tăng 391%** khi khách hàng tiềm năng được liên hệ trong vòng **60 giây** đầu tiên (Velocify).
- Các công ty liên hệ trong vòng **một giờ** có khả năng sàng lọc khách hàng tiềm năng **cao gấp 7 lần** so với gọi sau một giờ, và **cao gấp 60 lần** so với đợi 24 giờ (Harvard Business Review).
- **78%** khách hàng mua hàng từ công ty phản hồi yêu cầu của họ **đầu tiên** (Lead Connect).

Chi phí để tiếp cận khách hàng tiềm năng ngay lập tức là cần có _năng lực dư thừa_ (excess capacity) trong nhóm bán hàng.

**Cách Tăng Tốc Độ Liên Hệ:**

1. **Tốc Độ Liên Lạc Lần Đầu (Speed To First Contact):** Mục tiêu là liên hệ với tất cả khách hàng tiềm năng trong **năm phút hoặc ít hơn**. Liên hệ càng chậm, bạn càng phải liên hệ với họ nhiều lần hơn trước khi họ mua.
    - _Mẹo chuyên nghiệp:_ Nếu không nhận được câu “trời, nhanh thật đấy!” ít nhất **một lần mỗi ngày**, thì bạn chưa gọi đủ nhanh.
2. **Tốc Độ Đến Cuộc Hẹn Đầu Tiên (Speed To First Appointment):** Khoảng thời gian trì hoãn càng ngắn (giữa việc đặt lịch và có cuộc hẹn), tỷ lệ có mặt càng cao.
    - _Quy tắc:_ Hạn chế mọi người đặt lịch **tối đa ba ngày sau** (luôn là **72 giờ** trước).
    - **Kéo các cuộc hẹn lên sớm hơn—tốt nhất là ngay trong ngày:** Tỷ lệ có mặt cho các cuộc hẹn _ngay bây giờ_ là **100%**.
    - _Kịch bản kéo cuộc hẹn lên sớm hơn:_ Sàng lọc khách hàng tiềm năng qua điện thoại (Họ là ai? Họ muốn gì? Họ đang gặp khó khăn gì?) và sau đó đề nghị một chỗ trống bị hủy **vào cuối ngày hôm nay**.
    - _Chuyển giao nóng (hot handoff):_ Nếu người đặt lịch và người chốt đơn khác nhau, hãy thực hiện chuyển giao nóng (tin nhắn ba chiều) ngay lập tức, kèm theo tâng bốc (edify) người chốt đơn.
3. **Tốc độ Phản hồi (Speed of Response):** Phản hồi nhanh sau khi khách hàng tiềm năng đặt lịch hẹn và trước khi nó diễn ra. Phản hồi nhanh cho thấy bạn nghiêm túc và ngăn chặn việc họ bị mất kết nối.

### Trụ cột III: Cá nhân hóa 👤

_Cá nhân hóa, đừng gây áp lực._

**Câu chuyện về chiếc áo sơ mi màu hồng/đen**

Vào năm 2020, một trong những người thử nghiệm beta ALAN có tỷ lệ có mặt vượt xa bất kỳ ai khác. Bí quyết là họ đã tặng khách hàng tiềm năng một món quà khi họ đến. Cụ thể, họ nhắn tin _trên một chiếc iPhone riêng bên ngoài hệ thống_ và hỏi: "Tôi có một cái áo sơ mi đang đợi bạn ở đây. Bạn thích màu **đen** hay màu **hồng**?". Khách hàng tiềm năng phản hồi màu sắc, gần như mọi lúc họ đều có mặt.

Cá nhân hóa là làm cho bản thân trở nên **hữu ích, phù hợp và dễ chịu** _với từng khách hàng tiềm năng_. Nó làm giảm rủi ro lãng phí thời gian và tăng chi phí cơ hội nếu họ bỏ qua cuộc hẹn.

**Chiến thuật Cá nhân hóa (6 cách):**

1. **Sử Dụng Phương Thức Liên Lạc Ưa Thích Của Khách Hàng Tiềm Năng:** Bắt đầu giao tiếp bằng **nhiều cách** (tin nhắn, email, DM, gọi điện) nhưng _tiếp tục_ giao tiếp ở nơi họ phản hồi.
2. **Sàng Lọc Khách Hàng Tiềm Năng:** Tích cực _hủy_ các cuộc hẹn với những người không có khả năng mua bằng cách sử dụng **đơn đăng ký** để thu thập dữ liệu.
3. **Chuyển Khách Hàng Tiềm Năng Tốt Nhất cho Người Chốt Đơn Giỏi Nhất:**
    - Một nhân viên bán hàng sở hữu kỳ nghỉ số một ở Mỹ đã tăng sản lượng của văn phòng lên **5 lần** khi anh ta được giao những khách hàng tiềm năng tốt nhất.
    - _Quy trình:_ **Chấm điểm** khách hàng tiềm năng trên hệ thống **1-5 hoặc đỏ-vàng-xanh lá cây** dựa trên tiêu chí từ các khách hàng tốt nhất của bạn, sau đó phân tuyến người tốt nhất cho người chốt đơn tốt nhất.
4. **Phân khúc Thông Điệp Của Bạn:** Hubspot đã cải thiện ROI tiếp thị qua email lên **7 lần** sau khi phân khúc danh sách.
    - _Dễ:_ **Dành năm phút chuẩn bị** trước khi nói chuyện (nghiên cứu hồ sơ, trang web).
    - _Khó:_ Thiết lập **chuỗi email và tin nhắn văn bản riêng** cho mọi danh mục khách hàng tiềm năng (ví dụ: theo mức doanh thu hoặc mục tiêu giảm cân).
5. **Khuyến khích Việc Có Mặt:**
    - **"Đẩy":** Tặng quà _trước khi họ đến_ (ví dụ: thẻ quà tặng **$5** qua email) để tạo ra sự đáp trả (reciprocity). Ngay cả khi mọi người biết bạn đang làm gì—_nó vẫn hiệu quả_.
    - **"Kéo" A/B (Hối lộ):** Khách hàng tiềm năng chọn những gì họ nhận được _khi_ họ có mặt, giả định họ sẽ có mặt và chứng minh bạn đã chịu chi phí thay mặt họ.
6. **Đưa Ra Bằng Chứng:** Lồng ghép bằng chứng, nghiên cứu tình huống (case study), và lời chứng thực được **cá nhân hóa** (khớp bằng chứng với nhân khẩu học của khách hàng tiềm năng).
    - Lồng ghép: Sau khi đặt lịch, giữa cuộc gọi, và cứ sau **90 ngày** nếu họ "biến mất".

### Trụ cột IV: Số lượng 📈

_Số lượng phủ định may mắn._

Việc liên hệ lại có ý nghĩa về mặt đạo đức vì nếu họ đã đăng ký, _họ đã yêu cầu được liên hệ_. Vấn đề lớn là: **gần một nửa số nhân viên bán hàng bỏ cuộc sau nỗ lực đầu tiên**.

Mục tiêu là tăng số lượng liên hệ để có thêm phản hồi, lịch hẹn và có mặt.

**1) Đặt lịch hẹn (Tập trung cao độ vào thời gian đầu):**

- Gọi cho khách hàng tiềm năng trong vòng **5 phút** sau khi đăng ký.
- **Gọi kép (Double-dial)**: Gọi một lần và ngay lập tức gọi lại.
- Để lại thư thoại và gửi tin nhắn văn bản ngay sau đó.
- Gọi kép và nhắn tin **thêm hai lần nữa** trong ngày hôm đó (đảm bảo để lại vài giờ giữa mỗi lần cố gắng).
- Gọi **hai lần** trong **hai ngày tiếp theo** (sáng và tối).
- Gọi và nhắn tin **một lần mỗi ngày** trong **bốn ngày tiếp theo**.
- _Mẹo chuyên nghiệp:_ Trang bị một **trình quay số tự động (automatic dialer)** để cải thiện hiệu suất của nhóm lên **2-3 lần**.

**2) Nhắc nhở họ có mặt:**

- **Lời nhắc Tự động:** Phải làm rõ rằng chúng được tự động hóa.
    - Gửi ngay lập tức (xác nhận), **24 giờ trước**, **12 giờ trước**, và **3 giờ trước** cuộc hẹn.
    - _Mẹo:_ Sử dụng múi giờ _địa phương_ của khách hàng tiềm năng và thêm mã vùng bạn sẽ gọi từ đó (tăng gấp **2 lần** tỷ lệ nhấc máy).
- **Lời nhắc Thủ công (Cá nhân):** Gửi từ một điện thoại di động thực sự.
    - Gửi **Đêm hôm trước**, **Sáng hôm đó**, và **Một giờ trước**.
    - Khi họ phản hồi, sử dụng kịch bản **ACA** (**Ghi nhận - Khen ngợi - Hỏi** câu hỏi tiếp theo) để sàng lọc và kéo cuộc hẹn lên sớm hơn.

**3) Đặt Cuộc Hẹn Tiếp Theo Ngay Tại Cuộc Hẹn Hiện Tại (BAMFAM) 🗓️**

Sử dụng chiến lược **BAMFAM** (**Book-A-Meeting-From-A-Meeting**). KHÔNG BAO GIỜ kết thúc cuộc gọi với “Chúng ta sẽ liên lạc lại sau” hoặc “Tôi sẽ theo dõi và đề xuất một số thời gian”. Phải mở lịch và chọn thời gian _ngay tại đó_. Chiến lược BAMFAM đã làm tăng vọt tỷ lệ có mặt ở cuộc gọi thứ hai và doanh số bán hàng của một công ty bảo hiểm.

### Thực thi 🏆

_Hãy làm công việc nhàm chán._

Một khi bạn biết _phải làm gì_, chìa khóa để thực hiện nó là **văn hóa**.

**Câu chuyện về Jacob "Người nhặt rác"**

Jacob, một thiếu niên 15 tuổi, muốn kiếm tiền và được tác giả giới thiệu vào nhóm gọi điện lạnh. Chỉ tiêu của đội là **150 cuộc gọi mỗi ngày**. Tác giả yêu cầu Jacob làm việc chăm chỉ hơn mọi người khác: làm gấp đôi người giỏi nhất (ví dụ: **400 cuộc gọi một ngày**), làm việc **sáu ngày** thay vì năm, và không nghỉ trưa.

Khi Jacob than phiền về khách hàng tiềm năng không đủ tiêu chuẩn, tác giả khuyên cậu ấy nên coi đó là "món quà tuyệt vời nhất—thực hành miễn phí" (như 'những cú vung búa để đẽo gọt bộ kỹ năng').

Jacob nhận biệt danh là “người nhặt rác” vì cậu ấy nhận tất cả các khách hàng tiềm năng "rác" (khách hàng tiềm năng **Màu vàng**—ít đủ tiêu chuẩn hơn) từ cả nhóm. Hệ thống chấm điểm của công ty là Đỏ (không đủ tiêu chuẩn), Vàng (ít đủ tiêu chuẩn), và Xanh lá cây (hàng đầu).

Jacob đã phát triển câu cửa miệng: **“Màu vàng là vàng mới.”**.

Jacob thăng tiến và kết thúc nhiệm kỳ của mình tại Gym Launch với tư cách là nhân viên bán hàng **hàng đầu** trong quý cuối cùng, trong số **26 anh chàng**.

**Chiến thuật Văn hóa Thực thi**

Văn hóa là các quy tắc chi phối hành vi tốt và xấu trong một tổ chức. Cần chấp nhận các hành vi khiến chúng ta sẵn có, nhanh chóng, cá nhân, và kiên trì.

- **Phần thưởng Tiền tệ:** Bao gồm một khoản hoa hồng nhỏ tăng thêm cho tỷ lệ có mặt (thường ở khoảng **5-30%** những gì nhân viên bán hàng kiếm được từ một thương vụ).
- **Phần thưởng Phi tiền tệ:** Sự chú ý, tình cảm, và sự chấp thuận (khen ngợi những người có tỷ lệ có mặt cao nhất, củng cố các câu cửa miệng như “số lượng phủ định may mắn,” “tốc độ là vua”).
- **Theo dõi và Xếp hạng:** Xếp hạng đội ngũ theo **tỷ lệ có mặt**, **tỷ lệ chốt đơn**, và **tổng tỷ lệ từ cuộc gọi đến chốt đơn** để có bức tranh toàn diện.

**Kết luận về Thực thi:** Để có được tỷ lệ có mặt cao nhất, bạn cần 5 yếu tố: Tiện lợi, Tốc độ, Cá nhân hóa, Số lượng, và **Thực thi** (xây dựng các chuẩn mực văn hóa xung quanh việc yêu thích quy trình).

---

### Danh sách kiểm tra Nuôi dưỡng Khách hàng Tiềm năng

|Trụ cột|Mô tả|Các hành động cụ thể và số liệu|
|:--|:--|:--|
|**I. Sự Sẵn có**|Tăng số lượng khung giờ trống và giảm thời gian đặt lịch trước.|📅 Đặt lịch hẹn **cả bảy ngày mỗi tuần**.|
|||Mở cửa **9 giờ sáng đến 9 giờ tối theo giờ EST** là mục tiêu tốt.|
|||Cung cấp **bốn tùy chọn đặt lịch mỗi giờ** (mỗi **15 phút**) là mục tiêu tốt.|
|||Thêm quy trình **tự đặt lịch tự động**. Loại bỏ càng nhiều bước càng tốt.|
|**II. Tốc độ**|Phản hồi nhanh chóng giúp khách hàng tiềm năng đặt lịch và có mặt, giảm công việc về sau.|📞 **Tốc độ liên hệ lần đầu:** Phản hồi khách hàng tiềm năng trong vòng **dưới 5 phút** (Mục tiêu nâng cao: **dưới 60 giây**).|
|||**Tốc độ đến cuộc hẹn đầu tiên:** Đặt lịch hẹn **trong ngày, ngày hôm sau, hoặc ngày sau nữa**.|
|||**Kéo các cuộc hẹn lên sớm hơn** bất cứ khi nào có thể.|
|||**Tốc độ phản hồi:** Phản hồi tin nhắn nhanh chóng.|
|**III. Cá nhân hóa**|Làm cho giao tiếp dành riêng cho khách hàng tiềm năng.|📧 Sử dụng **phương thức liên lạc ưa thích** của họ (Bắt đầu ở mọi nơi, tập trung vào nơi họ phản hồi).|
|||**Sàng lọc khách hàng tiềm năng** bằng đơn đăng ký và thông tin nhân khẩu học.|
|||**Phân khúc thông điệp** dựa trên những gì bạn biết về họ.|
|||**Gửi khách hàng tiềm năng tốt nhất đến những người chốt đơn giỏi nhất.**|
|||**Khuyến khích việc có mặt:** Sử dụng khuyến khích A/B hoặc thẻ quà tặng (ví dụ: **$5**).|
|||**Bằng chứng:** Hiển thị bằng chứng phù hợp với tình huống của họ.|
|**IV. Số lượng**|Liên hệ nhiều lần để tăng tỷ lệ phản hồi và có mặt.|🎯 **Đợt tiếp cận ban đầu (Tuần 1):** Gọi kép + nhắn tin **3 lần** trong ngày đầu tiên; **2 lần** vào ngày thứ hai và ngày sau đó; **1 lần** trong **1–4 ngày** sau đó.|
|||**Lời nhắc Tự động:** Gửi **24 giờ, 12 giờ, 3 giờ trước** (bao gồm tên, ngày, giờ, và mã vùng sẽ gọi).|
|||**Lời nhắc Thủ công:** Đêm hôm trước, sáng hôm đó, **60 phút trước** từ điện thoại thực.|
|||**BAMFAM:** **Đặt một cuộc họp từ một cuộc họp**. Không bao giờ kết thúc cuộc gọi mà không đặt lịch cho cuộc hẹn tiếp theo.|
|**Thực thi**|Xây dựng văn hóa yêu thích quy trình để đảm bảo các chiến thuật được thực hiện.|📈 **Theo dõi và xếp hạng:** tỷ lệ có mặt, tỷ lệ chốt đơn, và tỷ lệ từ khách hàng tiềm năng đến chốt đơn theo nhân viên bán hàng.|
|||**Bình thường hóa các câu cửa miệng:** “Làm công việc nhàm chán,” “Màu vàng là vàng mới,” **“Số lượng phủ định may mắn.”**.|
|||“Quy trình > Tất cả.”.|

# 2. Vẽ Sơ đồ: 
```
Phong Cách Sơ Đồ DAS 4 - Claude
https://bimathocvienso1.sg.larksuite.com/docx/FZjEdlCQGoQYgFxtEfilRixlgkb

SỬ DỤNG CHÍNH XÁC PHONG CÁCH DAS 4 để vẽ sơ đồ với nội dung sau :
```



https://claude.ai/public/artifacts/4e34a882-1f0b-45fc-b8f7-4bc67d68ca00
https://www.genspark.ai/aidrive/preview/?f_id=a36a42de-e7e0-4191-8918-f9c8d990398b