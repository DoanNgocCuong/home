https://ecomstoryvn.substack.com/p/toi-muon-hoc-cach-su-dung-claude?utm_source=publication-search

---



<iframe src="https://substack.com/visited-surface-frame" width="0" height="0" class="visitedSurfacesIFrame-yy8AJL"></iframe>

<iframe src="https://substack.com/session-attribution-frame" width="0" height="0" class="visitedSurfacesIFrame-yy8AJL"></iframe>

[![Alex Quang](https://substackcdn.com/image/fetch/$s_!pZKs!,w_40,h_40,c_fill,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fec7f29c0-273a-4896-aaf4-905c680dcddc_160x160.png)](https://ecomstoryvn.substack.com/)

# [Alex Quang](https://ecomstoryvn.substack.com/)

# Tôi muốn học cách sử dụng Claude Skills (Khóa học toàn diện)

### Tôi đã tổng hợp mọi tài liệu mình tìm thấy để tạo ra một khóa học toàn diện về Claude Skills.

[](https://substack.com/@alexquang)

[Alexquang](https://substack.com/@alexquang)

Mar 12, 2026

[![](https://substackcdn.com/image/fetch/$s_!4Bx0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F49aa8bf5-2189-4941-8967-ad864daa2286_1376x768.jpeg)](https://substackcdn.com/image/fetch/$s_!4Bx0!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F49aa8bf5-2189-4941-8967-ad864daa2286_1376x768.jpeg)

Chỉ trong vòng chưa đầy 10 phút, bạn sẽ xây dựng và triển khai thành công Skill (Kỹ năng) tùy chỉnh đầu tiên của mình. Sau khi đọc xong bài viết này, bạn sẽ hiểu về Claude Skills rõ hơn 99% mọi người (thật đấy).

Bạn sắp được hướng dẫn toàn bộ quá trình tạo ra một Claude Skill, một tệp hướng dẫn cố định chỉ cho Claude chính xác cách thực thi một tác vụ cụ thể.

Cách tận dụng bài viết này:

* **Học phần 1:** Nền tảng
* **Học phần 2:** Kiến trúc
* **Học phần 3:** Thử nghiệm và Cải tiến (Iteration)
* **Học phần 4:** Triển khai Thực tế (Production Deployment)

### Học phần 1: Nền tảng

Trong mỗi học phần, tôi sẽ cung cấp cho bạn kiến thức nền tảng + cách nhờ AI hỗ trợ để bạn: 1. Hiểu được chuyện gì đang xảy ra, và 2. Xây dựng nó chuẩn xác mà không cần kỹ năng lập trình.

Cùng bắt đầu ngay nhé...

**SKILLS (Kỹ năng) vs PROJECTS (Dự án) vs MCP:**

Trước khi xây dựng bất cứ thứ gì, bạn cần hiểu vị trí của Skills bên trong hệ sinh thái Claude. Ba công cụ, ba vai trò khác nhau:

* **Projects (Dự án)** = cơ sở kiến thức của bạn. Tải lên một file PDF chứa quy chuẩn thương hiệu và bạn đang nói với Claude: “Đây là những gì bạn cần biết”. Tính chất: Tĩnh. Tài liệu tham khảo. Một thư viện.
* **Skills (Kỹ năng)** = cẩm nang hướng dẫn của bạn. Bạn đang nói với Claude: “Đây chính xác là cách bạn thực hiện tác vụ này, từng bước một”. Tính chất: Theo quy trình. Tự động. Một nhân viên đã qua đào tạo.
* **MCP (Model Context Protocol)** = lớp kết nối của bạn. Tính năng này cắm Claude vào các nguồn dữ liệu trực tiếp (lịch, cơ sở dữ liệu, hộp thư đến của bạn). Sau đó, Skills sẽ chỉ cho Claude biết phải làm gì với những dữ liệu đó.

Bạn có cần một Skill không? Nếu bạn đã phải gõ đi gõ lại cùng một đoạn hướng dẫn ở phần mở đầu của hơn ba cuộc trò chuyện, thì đó chính là một Skill đang “gào thét” đòi được tạo ra. Hoặc, nếu bạn muốn giúp Claude trở thành một chuyên viên điều hành chuyên nghiệp trong nhiều nhiệm vụ khác nhau, thì việc tạo ra các Skill sẽ giúp nó trở thành một “nhân viên” trong từng lĩnh vực.

[![](https://substackcdn.com/image/fetch/$s_!rqgO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd814509f-2654-417d-8b5a-99135ff7ff55_1376x768.jpeg)](https://substackcdn.com/image/fetch/$s_!rqgO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd814509f-2654-417d-8b5a-99135ff7ff55_1376x768.jpeg)

**CẤU TRÚC CỦA MỘT SKILL:**

Đây là phần mà hầu hết các bài hướng dẫn làm phức tạp hóa vấn đề (và dù sao thì Claude cũng sẽ giúp bạn tạo ra nó, nên đừng hoảng hốt):

Một Skill chỉ đơn giản là một thư mục (folder) trên máy tính của bạn. Bên trong thư mục đó là một tệp văn bản (text file). Chỉ vậy thôi.

Một thư mục chứa một tệp văn bản có tên là `SKILL.md`.

Thư mục này tuân theo ba quy tắc:

1. **Thư mục gốc (Root Folder)** phải được đặt tên theo định dạng `kebab-case`. Tức là chữ thường, các từ cách nhau bằng dấu gạch ngang. Ví dụ: `invoice-organiser`, `email-formatter`, `csv-cleaner`. Không có khoảng trắng. Không có dấu gạch dưới. Không viết hoa.
2. `SKILL.md` là bộ não. Tên tệp này phân biệt chữ hoa chữ thường. Không phải `skill.md`. Không phải `README.md`. Phải chính xác là `SKILL.md`. Tất cả các hướng dẫn của bạn đều nằm ở đây.
3. **Thư mục **`references/` là tùy chọn. Nếu các hướng dẫn của bạn cần tham chiếu đến một bộ quy chuẩn thương hiệu đồ sộ hay một biểu mẫu dài dòng, hãy thả nó vào thư mục con này thay vì dán toàn bộ vào `SKILL.md`.

Thả toàn bộ thư mục đó vào đường dẫn `~/.claude/skills/` trên máy tính của bạn. Claude sẽ tự động tìm thấy nó.

Tôi muốn bạn nắm được sự hiểu biết cơ bản này để bạn thực sự làm chủ nó.

**CHÚNG CHẠY Ở ĐÂU?**

Điều này quan trọng hơn những gì mà hầu hết các bài hướng dẫn nói với bạn.

* **Claude Code** là công cụ dòng lệnh (command-line) dành cho các lập trình viên. Các Skill ở đây nằm trong thư mục dự án của bạn dưới dạng `.claude/skills/` hoặc nằm ở cấp độ toàn cầu tại `~/.claude/skills/`. Chúng có quyền truy cập vào hệ thống tệp tin, các lệnh bash và có thể thực thi code. Đây là nơi bạn xây dựng các Skill để thao tác với các tệp, chạy các tập lệnh (scripts) và tương tác với kho lưu trữ mã nguồn (codebase) của bạn.
* **Claude Desktop (CoWork)** là tác tử (agent) trên máy tính để bàn dành cho những người không phải lập trình viên. Các Skill ở đây hoạt động thông qua giao diện máy tính để bàn và có thể tương tác với màn hình, các ứng dụng cũng như tệp tin của bạn thông qua các khả năng của tác tử. Vẫn giữ nguyên định dạng `SKILL.md`. Nhưng môi trường thực thi thì khác biệt.

Nếu bạn không chắc chắn, bạn luôn có thể sử dụng câu lệnh (prompt) này:

Markdown

```
Tôi muốn bạn giúp tôi xác định xem tôi có cần một Claude Skill hay không.

Cách thức hoạt động như sau:

1. Hãy yêu cầu tôi mô tả 3-5 tác vụ mà tôi lặp lại thường xuyên nhất khi
   sử dụng các trợ lý AI. Đối với mỗi tác vụ, hãy hỏi tôi:
   - Tôi thường đưa ra những hướng dẫn gì lúc bắt đầu?
   - Tôi lặp lại tác vụ này bao nhiêu lần mỗi tuần?
   - Kết quả đầu ra có cần tuân theo một định dạng, giọng văn,
     hoặc cấu trúc cụ thể nào mỗi lần không?

2. Sau khi tôi mô tả từng tác vụ, hãy chấm điểm tác vụ đó theo thang điểm
   "Mức độ Sẵn sàng làm Skill" từ 1-10 dựa trên:
   - Tần suất lặp lại (càng cao = càng sẵn sàng)
   - Độ phức tạp của hướng dẫn (hướng dẫn càng cụ thể =
     càng sẵn sàng)
   - Yêu cầu về tính nhất quán của đầu ra (yêu cầu định dạng càng nghiêm ngặt =
     càng sẵn sàng)

3. Xếp hạng các tác vụ của tôi từ điểm "Sẵn sàng" cao nhất đến thấp nhất.

4. Đối với tác vụ có điểm cao nhất, hãy cho tôi biết:
   - Tại sao đây là ứng cử viên tốt nhất cho Skill đầu tiên của tôi
   - Skill này sẽ cần chứa những gì
   - Ước tính thời gian tiết kiệm được mỗi tuần nếu tôi tự động hóa nó
   - Liệu tác vụ này phù hợp hơn với Claude Code hay
     Claude Desktop (CoWork)

Hãy bắt đầu bằng cách hỏi tôi về tác vụ lặp đi lặp lại đầu tiên của tôi.
```

**XÂY DỰNG SKILL ĐẦU TIÊN CỦA BẠN:**

**Bước 1: Xác định Công việc**

Trước khi viết bất kỳ chữ nào, hãy trả lời ba câu hỏi sau:

1. **Skill này dùng để làm gì?** Hãy cực kỳ cụ thể. “Giúp xử lý dữ liệu” là một câu vô dụng. “Chuyển đổi các file CSV lộn xộn thành các bảng tính gọn gàng với các tiêu đề cột chuẩn, ép buộc định dạng ngày tháng YYYY-MM-DD và xóa các hàng trống” mới là một Skill xài được.
2. **Khi nào nó nên được kích hoạt?** Hãy nghĩ về những gì bạn thực sự sẽ gõ. “Dọn dẹp file CSV này”. “Sửa các tiêu đề này”. “Định dạng dữ liệu này”. Đó chính là các trình kích hoạt (triggers) của bạn.
3. **Thế nào là “tốt”?** Bạn cần một ví dụ cụ thể về kết quả hoàn chỉnh. Không phải là một lời mô tả. Mà là một ví dụ thực tế về Trước-và-Sau.

Hãy nghe kỹ đây. Đây chính là bước mà 90% các Skill tồi tệ được sinh ra. Hướng dẫn mơ hồ sẽ tạo ra kết quả mơ hồ. Luôn là như vậy.

Bạn không tin tưởng vào khả năng đưa ra yêu cầu cụ thể của bản thân? Câu lệnh (prompt) này sẽ ép buộc sự chính xác ra khỏi bạn.

*PROMPT: CUỘC PHỎNG VẤN XÁC ĐỊNH SKILL:*

Markdown

```
Bạn là một Chuyên gia Xác định Skill. Công việc của bạn là phỏng vấn 
tôi cho đến khi chúng ta có được một định nghĩa sắc bén về Claude Skill 
mà tôi muốn xây dựng. Bạn sẽ không để tôi dễ dàng lướt qua bằng những câu trả lời mơ hồ.

Hãy chạy quy trình phỏng vấn này:

GIAI ĐOẠN 1 - TÁC VỤ
Hỏi tôi: "Bạn muốn tự động hóa tác vụ gì?" 
Sau khi tôi trả lời, hãy kiểm tra áp lực (pressure-test) câu trả lời của tôi:
- Nếu câu trả lời của tôi mơ hồ (ví dụ: "giúp viết email"), hãy phản bác 
  và yêu cầu tôi mô tả CHÍNH XÁC những gì Skill nên làm, 
  với một đầu vào cụ thể và đầu ra cụ thể.
- Tiếp tục hỏi "Bạn có thể cụ thể hơn được không?" cho đến khi mô tả 
  tác vụ trở nên cụ thể và có thể thực thi được.
- Xác nhận lại định nghĩa tác vụ cuối cùng cho tôi trong một câu.

GIAI ĐOẠN 2 - CÁC TRÌNH KÍCH HOẠT (TRIGGERS)
Hỏi tôi: "Bạn thực sự sẽ gõ gì vào Claude để kích hoạt 
Skill này? Hãy cho tôi 5 cách diễn đạt khác nhau mà bạn có thể dùng để yêu cầu."
Sau khi tôi trả lời:
- Gợi ý thêm 3-5 cụm từ kích hoạt mà tôi có thể đã bỏ lỡ.
- Hỏi tôi về các ranh giới phủ định: "Những yêu cầu nào nghe có vẻ tương tự 
  nhưng KHÔNG NÊN kích hoạt Skill này?"

GIAI ĐOẠN 3 - TIÊU CHUẨN CHẤT LƯỢNG
Hỏi tôi: "Hãy cho tôi xem hoặc mô tả chính xác một kết quả HOÀN HẢO 
sẽ trông như thế nào đối với tác vụ này."
Sau khi tôi trả lời:
- Yêu cầu tôi mô tả một kết quả THẤT BẠI trông như thế nào 
  (để chúng ta biết cần tránh điều gì).
- Hỏi tôi về các trường hợp ngoại lệ (edge cases): "Đầu vào kỳ lạ nhất hoặc 
  hỏng hóc nhất mà Skill này có thể nhận được là gì? Nó nên xử lý như thế nào?"

GIAI ĐOẠN 4 - TÓM TẮT
Tổng hợp mọi thứ thành một "Bản tóm tắt Định nghĩa Skill" có cấu trúc 
với các phần sau:
- Tên Skill (định dạng kebab-case)
- Mục đích (Tóm tắt trong một câu)
- Các cụm từ Kích hoạt (tích cực)
- Ranh giới Phủ định (khi nào KHÔNG kích hoạt)
- Mô tả Đầu vào
- Mô tả Đầu ra
- Tiêu chuẩn Chất lượng (thế nào là "tốt")
- Các trường hợp Ngoại lệ cần xử lý

Trình bày bản tóm tắt này và yêu cầu tôi xác nhận hoặc sửa đổi trước khi 
chúng ta tiếp tục.

Bắt đầu Giai đoạn 1 ngay bây giờ.
```

**Bước 2: Viết các Trình kích hoạt YAML (YAML Triggers)**

Ở trên cùng của tệp `SKILL.md`, bạn viết một khối dữ liệu siêu meta (metadata) giữa các dòng `---`. Phần này được gọi là YAML frontmatter. Nó báo cho Claude biết khi nào cần kích hoạt Skill của bạn.

Đây là một ví dụ:

Markdown

```
---
name: csv-cleaner
description: Chuyển đổi các file CSV lộn xộn thành các bảng tính gọn gàng. Sử dụng skill này bất cứ khi nào người dùng nói 'dọn dẹp file CSV này', 'sửa các tiêu đề', 'định dạng dữ liệu này', hoặc 'tổ chức lại bảng tính này'. KHÔNG sử dụng cho PDF, tài liệu Word, hoặc tệp hình ảnh.
---
```

Ba quy tắc quyết định sự thành bại cho các trình kích hoạt của bạn:

1. **Viết ở ngôi thứ ba.** “Xử lý các tệp tin...” thay vì “Tôi có thể giúp bạn...”
2. **Liệt kê chính xác các cụm từ kích hoạt.** Claude khá “rụt rè” trong việc kích hoạt. Bạn cần phải đánh vần rõ ràng những gì người dùng có thể nói. Hãy tỏ ra “hổ báo” (pushy) một chút.
3. **Thiết lập các ranh giới phủ định.** Cho Claude biết khi nào KHÔNG kích hoạt. Điều này ngăn Skill của bạn “cướp diễn đàn” trong các cuộc hội thoại không liên quan.

Đây là điều mà hầu hết mọi người thường bỏ lỡ. Trường `description` (mô tả) là dòng quan trọng nhất trong toàn bộ Skill của bạn. Nếu nó quá yếu, Skill của bạn sẽ không bao giờ được kích hoạt. Nếu nó quá chung chung, nó sẽ kích hoạt cả những lúc bạn không muốn.

Câu lệnh này sẽ tạo ra một khối YAML đã được kiểm chứng thực tế từ định nghĩa của bạn:

*PROMPT: TRÌNH TẠO TRÌNH KÍCH HOẠT YAML:*

Markdown

```
Bạn là một Chuyên gia viết YAML Frontmatter cho Claude Skills. 
Công việc của bạn là viết một khối trigger YAML hiệu quả nhất có thể 
cho phần trên cùng của tệp SKILL.md.

Đây là định nghĩa Skill của tôi:
[DÁN BẢN TÓM TẮT ĐỊNH NGHĨA SKILL CỦA BẠN VÀO ĐÂY, HOẶC MÔ TẢ 
SKILL CỦA BẠN TRONG 2-3 CÂU]

Tạo YAML frontmatter tuân theo các quy tắc nghiêm ngặt sau:

1. Trường "name" phải ở định dạng kebab-case (chữ thường, 
   chỉ dùng dấu gạch ngang, không có khoảng trắng hay dấu gạch dưới).

2. Trường "description" phải mang tính "thúc ép/hổ báo" - nghĩa là nó 
   nên liệt kê một cách quyết liệt các tình huống kích hoạt vì Claude 
   thường bảo thủ trong việc kích hoạt skill. Bao gồm:
   - Một câu tóm tắt rõ ràng về những gì skill làm 
     (viết ở ngôi thứ ba: "Xử lý..." thay vì "Tôi có thể...")
   - Ít nhất 5-7 cụm từ kích hoạt rõ ràng mà người dùng có thể nói, 
     được định dạng như sau: "Sử dụng skill này bất cứ khi nào người dùng nói 
     '[cụm từ 1]', '[cụm từ 2]', '[cụm từ 3]'..."
   - Ranh giới phủ định: "KHÔNG sử dụng skill này cho [X], 
     [Y], hoặc [Z]."
   - Manh mối ngữ cảnh: "Đồng thời kích hoạt khi người dùng tải lên 
     [loại tệp] và yêu cầu [hành động]."

3. Giữ toàn bộ phần mô tả dưới 300 từ nhưng phải làm cho 
   mỗi từ đều có giá trị.

CHỈ xuất ra khối YAML (nằm giữa các dấu ---), sẵn sàng để 
dán trực tiếp vào tệp SKILL.md. Không cần giải thích thêm.

Sau đó, bên dưới khối YAML, cung cấp một "Báo cáo Độ Tự Tin của Trigger" đánh giá:
- Khả năng kích hoạt trên các yêu cầu liên quan: X/10
- Nguy cơ nhận diện sai (kích hoạt khi không nên): X/10
- Mức độ bao phủ các cách diễn đạt phổ biến: X/10

Nếu bất kỳ điểm nào dưới 7/10, hãy đề xuất các cải tiến cụ thể.
```

[![](https://substackcdn.com/image/fetch/$s_!L8d2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9820cb1a-2182-4f35-abc8-817fc5736f31_2752x1536.jpeg)](https://substackcdn.com/image/fetch/$s_!L8d2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9820cb1a-2182-4f35-abc8-817fc5736f31_2752x1536.jpeg)

**Bước 3: Viết Hướng dẫn**

Bên dưới các dấu `---`, bạn viết quy trình làm việc của mình bằng tiếng Anh (hoặc tiếng Việt) thông thường. Có cấu trúc bằng các tiêu đề. Tuần tự. Dưới 500 dòng.

Hai thành phần làm cho phần này hoạt động hiệu quả:

**1. Các Bước (The Steps).** Chia nhỏ quy trình làm việc thành một trình tự logic:

* Đầu tiên, đọc tệp được cung cấp để hiểu cấu trúc của nó
* Xác định hàng chứa các tiêu đề cột thực sự
* Xóa bất kỳ hàng trống hoặc hàng nào chỉ chứa dấu phẩy
* Ép buộc các kiểu dữ liệu phù hợp (ngày tháng phải là YYYY-MM-DD)
* Xuất tệp đã dọn dẹp kèm theo bản tóm tắt các thay đổi đã thực hiện

**2. Các Ví dụ (The Examples).** Đây là nơi phép màu xuất hiện. Một ví dụ cụ thể, thực tế cho thấy đầu vào và đầu ra mong đợi có giá trị hơn 50 dòng mô tả trừu tượng.

*PROMPT: KIẾN TRÚC SƯ HƯỚNG DẪN SKILL:*

Markdown

```
Bạn là người viết hướng dẫn cho Claude Skill. Công việc của bạn là 
tạo ra toàn bộ phần nội dung hướng dẫn cho tệp SKILL.md sao cho 
rõ ràng, tuần tự và dưới 500 dòng.

Đây là định nghĩa Skill của tôi:
[DÁN BẢN TÓM TẮT ĐỊNH NGHĨA SKILL CỦA BẠN TỪ BƯỚC 1]

Đây là phần YAML frontmatter đã được viết:
[DÁN KHỐI YAML CỦA BẠN TỪ BƯỚC 2]

Bây giờ hãy tạo toàn bộ nội dung hướng dẫn sẽ nằm BÊN DƯỚI 
dấu --- đóng của khối YAML. Tuân thủ chính xác các quy tắc sau:

QUY TẮC CẤU TRÚC:
1. Bắt đầu bằng một đoạn "Overview" (Tổng quan) nêu rõ những gì 
   skill này làm và khi nào nó kích hoạt, được viết cho Claude hiểu 
   (không phải cho con người đọc).
2. Chia quy trình làm việc thành các bước được đánh số dưới 
   tiêu đề "## Workflow". Mỗi bước phải là:
   - Một hành động rõ ràng duy nhất
   - Được viết dưới dạng câu mệnh lệnh ("Đọc tệp..." 
     thay vì "Tệp tin nên được đọc...")
   - Đủ cụ thể để chỉ có MỘT cách hiểu duy nhất
3. Bao gồm phần "## Output Format" quy định 
   chính xác cách kết quả cuối cùng nên được cấu trúc 
   (loại tệp, định dạng, các phần, giọng văn, v.v.)
4. Bao gồm phần "## Edge Cases" báo cho Claude biết 
   cách xử lý:
   - Đầu vào bị thiếu hoặc không đầy đủ
   - Các yêu cầu mơ hồ
   - Các hướng dẫn mâu thuẫn nhau
   - Định dạng tệp hoặc kiểu dữ liệu không mong đợi

QUY TẮC VÍ DỤ:
5. Bao gồm ít nhất 2 ví dụ cụ thể dưới 
   tiêu đề "## Examples":
   - Ví dụ 1: Một kịch bản chuẩn "happy path" cho thấy 
     đầu vào bình thường → đầu ra mong đợi
   - Ví dụ 2: Một trường hợp ngoại lệ (edge case) cho thấy đầu vào bất thường → 
     cách Claude nên xử lý nó
   Mỗi ví dụ phải hiển thị THỰC TẾ đầu vào và THỰC TẾ đầu ra 
   mong đợi, không phải là những mô tả trừu tượng.

QUY TẮC CHẤT LƯỢNG:
6. Tổng độ dài: nhắm đến khoảng 100-300 dòng. Cắt bỏ bất cứ thứ gì 
   không trực tiếp hướng dẫn Claude cách 
   thực thi tác vụ.
7. Không bao giờ sử dụng ngôn ngữ mơ hồ như "xử lý phù hợp" 
   hoặc "định dạng đẹp mắt." Mỗi hướng dẫn phải cụ thể 
   và có thể kiểm chứng được.
8. Nếu skill yêu cầu tham chiếu đến các tệp bên ngoài 
   (quy chuẩn thương hiệu, biểu mẫu), hãy thêm phần "## References" 
   với hướng dẫn: "Đọc [tên tệp] từ thư mục 
   references/ trước khi bắt đầu tác vụ."

Xuất ra toàn bộ phần nội dung hướng dẫn dưới dạng markdown, sẵn sàng để 
dán trực tiếp bên dưới phần YAML frontmatter trong tệp SKILL.md.

Sau phần hướng dẫn, hãy cung cấp một "Checklist Chất lượng" để 
xác nhận:
- [ ] Mỗi bước là một hành động đơn lẻ, không mơ hồ
- [ ] Đã bao gồm ít nhất 2 ví dụ cụ thể
- [ ] Đã bao trùm các trường hợp ngoại lệ
- [ ] Định dạng đầu ra được xác định rõ ràng
- [ ] Tổng độ dài dưới 500 dòng
- [ ] Không còn ngôn ngữ mơ hồ hoặc dễ bị hiểu sai
```

**Bước 4: Quy tắc “Sâu Một Tầng” (Tham chiếu)**

Nếu các hướng dẫn của bạn cần tham chiếu đến một bộ quy chuẩn thương hiệu hay một biểu mẫu đồ sộ, đừng dán tất cả vào `SKILL.md`.

Hãy lưu nó thành một tệp riêng biệt bên trong thư mục `references/`. Sau đó liên kết trực tiếp đến nó từ các hướng dẫn của bạn.

Nhưng đây là ràng buộc mang tính sống còn:  **không bao giờ để các tệp tham chiếu liên kết đến các tệp tham chiếu khác** . Claude sẽ cắt bớt việc đọc của mình và bỏ sót thông tin. Sâu một tầng. Chỉ vậy thôi.

Nếu bạn có các tài liệu hiện có (bộ quy chuẩn thương hiệu, stylesheet, biểu mẫu, quy trình SOP) mà Skill của bạn cần tham chiếu, câu lệnh này sẽ chuyển đổi chúng thành các tệp tham chiếu được định dạng chuẩn:

*PROMPT: TRÌNH TỔ CHỨC TỆP THAM CHIẾU:*

Markdown

```
Bạn là một Người Tổ chức Tệp Tham chiếu cho Skill. Tôi có các tài liệu 
mà Claude Skill của tôi cần tham chiếu trong quá trình thực thi. 
Công việc của bạn là chuẩn bị chúng cho thư mục references/.

Đây là các tài liệu tham chiếu của tôi:
[DÁN HOẶC TẢI LÊN QUY CHUẨN THƯƠNG HIỆU / BIỂU MẪU / SOP / 
STYLE SHEET / BẤT KỲ TÀI LIỆU THAM CHIẾU NÀO CỦA BẠN]

Đối với mỗi tài liệu, hãy làm như sau:

1. ĐÁNH GIÁ: Tài liệu này có đủ ngắn để đưa vào 
   trực tiếp trong tệp SKILL.md không (dưới 50 dòng nội dung 
   liên quan)? Nếu có, hãy khuyên nên chèn trực tiếp (inline) 
   thay vì tạo một tệp tham chiếu riêng biệt.

2. NÉN: Nếu nó cần phải là một tệp tham chiếu riêng, 
   CHỈ trích xuất các phần liên quan trực tiếp 
   đến tác vụ của Skill. Loại bỏ tất cả phần mở đầu, ngữ cảnh 
   nền tảng và những thông tin mà Skill sẽ không bao giờ cần. 
   Nhắm đến việc giảm bớt 50%+ tài liệu trong khi vẫn giữ lại 
   tất cả các hướng dẫn có thể thực thi.

3. ĐỊNH DẠNG: Cấu trúc tệp tham chiếu đã nén với:
   - Các tiêu đề markdown rõ ràng
   - Các dấu đầu dòng (bullet points) cho các quy tắc và ràng buộc
   - Chữ in đậm cho các yêu cầu quan trọng
   - Một bản tóm tắt "Tham chiếu Nhanh" ở trên cùng (dưới 10 dòng) 
     nắm bắt các quy tắc quan trọng nhất

4. ĐẶT TÊN: Đề xuất một tên tệp theo định dạng kebab-case cho mỗi tệp 
   tham chiếu (ví dụ: brand-voice-guide.md, email-template.md).

5. LIÊN KẾT: Viết chính xác dòng lệnh mà tôi nên thêm vào tệp SKILL.md 
   của mình để tham chiếu đến tài liệu này, ví dụ:
   "Trước khi bắt đầu tác vụ, hãy đọc hướng dẫn giọng nói thương hiệu 
   tại references/brand-voice-guide.md"

6. XÁC THỰC: Kiểm tra quy tắc "Sâu Một Tầng" (One Level Deep). Đánh dấu 
   bất kỳ tệp tham chiếu nào liên kết đến hoặc phụ thuộc vào 
   MỘT tệp tham chiếu KHÁC. Nếu tìm thấy, hãy hợp nhất chúng thành một 
   tệp duy nhất.

Xuất ra từng tệp tham chiếu đã chuẩn bị đầy đủ, sẵn sàng để lưu 
trực tiếp vào thư mục references/.
```

**Bước 5: Lắp ráp và Triển khai**

Bây giờ bạn đã có mọi thành phần. Đã đến lúc ghép chúng lại với nhau.

Cấu trúc thư mục của bạn sẽ trông như thế này:

Markdown

```
ten-skill-cua-ban/
├── SKILL.md          (phần YAML header + hướng dẫn từ Bước 2-3)
└── references/       (tùy chọn, từ Bước 4)
    └── file-tham-chieu-cua-ban.md
```

Thả thư mục này vào `~/.claude/skills/` trên máy tính của bạn. Xong.

Nhưng chờ đã. Trước khi triển khai, bạn muốn đảm bảo toàn bộ hệ thống này kín kẽ không có kẽ hở. Câu lệnh này sẽ thực hiện một đợt kiểm tra đảm bảo chất lượng (QA) cuối cùng trên toàn bộ tệp `SKILL.md` của bạn:

*PROMPT: CHUYÊN VIÊN KIỂM TOÁN QA SKILL*

Markdown

```
Bạn là một Chuyên viên Kiểm toán Đảm bảo Chất lượng cho Claude Skill. Tôi đã 
xây dựng một tệp SKILL.md hoàn chỉnh và tôi cần bạn kiểm toán nó 
trước khi tôi triển khai.

Đây là toàn bộ tệp SKILL.md của tôi:
[DÁN TOÀN BỘ TỆP SKILL.MD CỦA BẠN VÀO ĐÂY]

Chạy các bước kiểm tra kiểm toán sau và báo cáo kết quả:

## 1. KIỂM TOÁN YAML FRONTMATTER
- [ ] Trường name tồn tại và là kebab-case hợp lệ
- [ ] Trường description tồn tại và dài hơn 50 từ
- [ ] Description được viết ở ngôi thứ ba
- [ ] Ít nhất 5 cụm từ kích hoạt được liệt kê
- [ ] Ranh giới phủ định được xác định (khi nào KHÔNG kích hoạt)
- [ ] Description đủ mức "thúc ép" (liệu Claude có thực sự 
      kích hoạt skill này cho một yêu cầu liên quan không?)
ĐIỂM: X/10

## 2. KIỂM TOÁN ĐỘ RÕ RÀNG CỦA HƯỚNG DẪN
- [ ] Mỗi bước là một hành động đơn lẻ, không mơ hồ
- [ ] Không có ngôn ngữ mơ hồ ("xử lý phù hợp", 
      "định dạng đẹp mắt", "khi cần thiết")
- [ ] Hướng dẫn ở dạng câu mệnh lệnh ("Đọc 
      tệp" thay vì "Tệp nên được đọc")
- [ ] Logic tuần tự chính xác (không có bước nào phụ thuộc vào 
      thông tin từ một bước sau đó)
- [ ] Tổng độ dài hướng dẫn dưới 500 dòng
ĐIỂM: X/10

## 3. KIỂM TOÁN CHẤT LƯỢNG VÍ DỤ
- [ ] Ít nhất 2 ví dụ được đưa vào
- [ ] Các ví dụ hiển thị THỰC TẾ đầu vào và THỰC TẾ đầu ra 
      (không phải mô tả trừu tượng)
- [ ] Có ít nhất một ví dụ về trường hợp ngoại lệ
- [ ] Các ví dụ mang tính thực tế (đại diện cho việc sử dụng trong thế giới thực)
ĐIỂM: X/10

## 4. KIỂM TOÁN MỨC ĐỘ BAO PHỦ TRƯỜNG HỢP NGOẠI LỆ
- [ ] Đầu vào bị thiếu/không đầy đủ được xử lý
- [ ] Các yêu cầu mơ hồ được xử lý
- [ ] Các loại tệp hoặc định dạng dữ liệu không mong đợi được xử lý
- [ ] Skill biết khi nào cần hỏi để làm rõ 
      so với việc đưa ra một giả định hợp lý
ĐIỂM: X/10

## 5. KIỂM TOÁN TỆP THAM CHIẾU (nếu có)
- [ ] Tất cả các tệp được tham chiếu đều chỉ sâu một tầng
- [ ] Không có tham chiếu vòng tròn
- [ ] Hướng dẫn tham chiếu trong SKILL.md rõ ràng 
      ("Đọc X trước khi bắt đầu")
ĐIỂM: X/10

## TỔNG ĐIỂM SẴN SÀNG TRIỂN KHAI: X/50

Nếu bất kỳ phần nào có điểm dưới 7/10, hãy cung cấp BẢN VIẾT LẠI CỤ THỂ 
cho các phần bị trượt. Xuất ra văn bản đã được sửa chữa 
sẵn sàng để dán trực tiếp vào tệp.

Nếu tổng điểm từ 40+/50, xác nhận: "SẴN SÀNG TRIỂN KHAI."
Nếu dưới 40, liệt kê các bản sửa lỗi quan trọng cần thiết trước khi 
triển khai, theo thứ tự ưu tiên.
```

**TỰ ĐỘNG HÓA VIỆC XÂY DỰNG SKILL ĐẦU TIÊN CỦA BẠN:**

Nếu mọi thứ ở trên cảm thấy quá tốn công sức, có một lối tắt.

Anthropic đã xây dựng một siêu-kỹ-năng (meta-skill) gọi là `skill-creator` giúp cấu trúc các Skill cho bạn thông qua trò chuyện.

Cách nó hoạt động:

1. Mở một cuộc trò chuyện mới. Gõ: “Use the skill-creator to help me build a skill for [tác vụ của bạn].” (Sử dụng skill-creator để giúp tôi xây dựng một kỹ năng cho [tác vụ của bạn]).
2. Tải lên các tài sản của bạn. Các biểu mẫu bạn sử dụng. Các ví dụ về công việc trước đây. Quy chuẩn thương hiệu. Bất cứ thứ gì cho Claude thấy “tốt” là như thế nào.
3. Trả lời phỏng vấn. `skill-creator` sẽ hỏi bạn các câu hỏi làm rõ về quy trình của bạn, các trường hợp ngoại lệ và các tiêu chuẩn chất lượng của bạn.
4. Nó sẽ tạo ra mọi thứ. Tệp `SKILL.md` đã được định dạng. Phần mô tả “hổ báo”. Cấu trúc thư mục. Đã được đóng gói và sẵn sàng.
5. Lưu thư mục vào `~/.claude/skills/`. Xong.

Lần tới khi bạn yêu cầu Claude thực hiện tác vụ đó, Skill của bạn sẽ tự động kích hoạt.

Học phần 1 đã hoàn tất. Bây giờ bạn đã có một Skill được triển khai. Trong Học phần 2, bạn sẽ học cách tận dụng cấu trúc.

---

### Học phần 2: Kiến trúc

Cuối cùng, bạn sẽ có khá nhiều skill, đây là lúc kiến trúc trở thành một phần quan trọng trong kho vũ khí của bạn.

Một lần nữa, tôi sẽ dạy bạn phiên bản thủ công của việc này và sau đó cung cấp cho bạn các câu lệnh để hệ thống tự làm việc này cho bạn, nhưng bạn nên biết lý do tại sao bạn đang xây dựng kiến trúc, đó là lý do tại sao tôi vẫn giữ nguyên phần hướng dẫn thủ công...

**KHI NÀO CÁC HƯỚNG DẪN LÀ KHÔNG ĐỦ:**

Mọi thứ bạn đã xây dựng cho đến nay đều sử dụng các hướng dẫn bằng tiếng Anh/Việt thông thường. Claude đọc chúng, làm theo chúng, và tạo ra kết quả.

Nhưng một số tác vụ cần sự tính toán. Chúng cần các đoạn mã (code) để chạy. Các phép tính cần thực thi. Các biến đổi dữ liệu quá chính xác nên không thể dùng ngôn ngữ tự nhiên để hướng dẫn.

Đó là mục đích của thư mục `scripts/`.

**KHI NÀO NÊN SỬ DỤNG SCRIPTS (TẬP LỆNH):**

* **Sử dụng Hướng dẫn (Instructions) khi:** Tác vụ liên quan đến sự phán đoán, ngôn ngữ, định dạng hoặc ra quyết định. “Viết lại đoạn này theo giọng văn thương hiệu của chúng tôi.” “Phân loại các ghi chú cuộc họp này.” “Soạn một email.” Khả năng ngôn ngữ của Claude xử lý những việc này một cách hoàn hảo.
* **Sử dụng Scripts (Tập lệnh) khi:** Tác vụ yêu cầu tính toán chính xác, thao tác trên tệp, biến đổi dữ liệu hoặc tích hợp với các công cụ bên ngoài. “Tính trung bình cộng của các số này.” “Phân tích cú pháp tệp XML này và trích xuất các trường cụ thể.” “Đổi kích thước tất cả hình ảnh trong thư mục này thành 800x600.”
* **Sử dụng Cả hai khi:** Tác vụ yêu cầu cả tính toán VÀ phán đoán. “Xử lý file CSV này (script), sau đó viết một bản tóm tắt dễ đọc cho con người về các điểm bất thường được tìm thấy (hướng dẫn).”

**Cách các Scripts Hoạt động Bên trong một Skill**

Các hướng dẫn trong Skill của bạn sẽ cho Claude biết khi nào và làm thế nào để thực thi các script. Bản thân các script nằm trong thư mục `scripts/` và thực hiện phần tính toán thực tế.

Dưới đây là một ví dụ hoàn chỉnh:

Markdown

```
data-analyser/
├── SKILL.md
├── references/
│   └── analysis-template.md
└── scripts/
    ├── parse-csv.py
    └── calculate-stats.py
```

Trong tệp `SKILL.md` của bạn, bạn tham chiếu đến các script như thế này:

Markdown

```
## Workflow

1. Đọc tệp CSV được tải lên để hiểu cấu trúc của nó.

2. Chạy scripts/parse-csv.py để làm sạch dữ liệu:
   - Câu lệnh: `python scripts/parse-csv.py [input_file] [output_file]`
   - Thao tác này xóa các hàng trống, chuẩn hóa tiêu đề, và
     ép buộc các kiểu dữ liệu.

3. Chạy scripts/calculate-stats.py trên dữ liệu đã làm sạch:
   - Câu lệnh: `python scripts/calculate-stats.py [cleaned_file]`
   - Thao tác này xuất ra: giá trị trung bình, trung vị, độ lệch chuẩn, và
     các ngoại lệ cho mỗi cột số.

4. Đọc đầu ra thống kê và viết một bản tóm tắt dễ đọc cho con người
   theo biểu mẫu trong references/analysis-template.md.
   Làm nổi bật bất kỳ điểm bất thường hoặc ngoại lệ nào có thể gây lo ngại
   cho một người đọc không có chuyên môn về kỹ thuật.
```

Điểm cốt lõi cần nhớ: Các script xử lý phần tính toán. Hướng dẫn xử lý phần phán đoán. Chúng phối hợp làm việc cùng nhau.

**Thực hành Tốt nhất cho Script**

* **Giữ cho các script luôn tập trung.** Một script, một công việc. `parse-csv.py` sẽ không đồng thời tính toán số liệu thống kê. Đó là việc của một script riêng biệt.
* **Làm cho script chấp nhận các đối số (arguments).** Script của bạn nên nhận đường dẫn tệp đầu vào/đầu ra làm các đối số dòng lệnh, không nên “hardcode” (gắn cứng) chúng vào trong code. Điều này làm cho Skill trở nên linh hoạt.
* **Bao gồm xử lý lỗi.** Script của bạn nên thoát ra với một thông báo lỗi rõ ràng nếu đầu vào bị sai định dạng, bị thiếu hoặc không đúng định dạng. Sau đó, Claude có thể đọc lỗi này và thông báo lại cho người dùng.
* **Tài liệu hóa phần giao diện (interface).** Ở đầu mỗi script, hãy bao gồm một khối bình luận giải thích: script này làm gì, nó mong đợi những đối số nào, nó xuất ra cái gì và những lỗi nào nó có thể đưa ra.

Đây là một câu lệnh giúp xây dựng các script cho Skill của bạn:

*PROMPT: TRÌNH XÂY DỰNG SCRIPT CHO SKILL:*

Markdown

```
Tôi có một Claude Skill cần các script có thể thực thi cho 
các tác vụ yêu cầu tính toán thay vì xử lý ngôn ngữ.

Đây là tệp SKILL.md hiện tại của tôi:
[DÁN SKILL.MD CỦA BẠN]

Dưới đây là các tác vụ tính toán không thể được xử lý 
chỉ bằng các hướng dẫn:
[MÔ TẢ MỖI TÁC VỤ CẦN MỘT SCRIPT, ví dụ:
- "Phân tích các tệp XML và trích xuất các trường cụ thể"
- "Tính toán các bản tóm tắt thống kê của dữ liệu số"
- "Đổi kích thước và nén hình ảnh trong một thư mục"]

Đối với mỗi tác vụ, hãy xây dựng một script tuân theo các quy tắc sau:

1. Ngôn ngữ: Sử dụng Python trừ khi tác vụ đặc biệt yêu cầu 
   một ngôn ngữ khác. Python có sẵn trong cả hai môi trường 
   Claude Code và CoWork.

2. Giao diện: Chấp nhận tất cả các đầu vào dưới dạng đối số dòng lệnh. 
   Không hardcode (gắn cứng) các đường dẫn tệp. In đầu ra ra stdout hoặc ghi 
   vào một tệp đầu ra được chỉ định.

3. Xử lý lỗi: Bắt tất cả các chế độ lỗi phổ biến (thiếu 
   tệp, dữ liệu sai định dạng, sai kiểu dữ liệu) và thoát ra với một 
   thông báo lỗi rõ ràng mà Claude có thể phân tích được.

4. Tài liệu: Bao gồm một khối bình luận ở trên cùng với:
   - Script này làm gì
   - Các đối số bắt buộc
   - Định dạng đầu ra mong đợi
   - Các điều kiện lỗi có thể xảy ra

5. Phụ thuộc (Dependencies): Chỉ sử dụng thư viện chuẩn của Python 
   khi có thể. Nếu yêu cầu các gói bên ngoài, hãy liệt kê chúng 
   vào một tệp requirements.txt.

Sau khi tạo các script:

6. Cập nhật quy trình làm việc trong SKILL.md để tham chiếu đến từng script 
   với cú pháp lệnh chính xác mà Claude nên sử dụng.

7. Thêm hướng dẫn xử lý lỗi vào SKILL.md: Claude nên 
   nói gì với người dùng nếu một script thất bại?

Đầu ra:
- Mỗi tệp script đã sẵn sàng để lưu vào thư mục scripts/
- Tệp SKILL.md đã cập nhật với các tham chiếu script
- Tệp requirements.txt (nếu cần các gói bên ngoài)
```

**ĐIỀU PHỐI ĐA SKILL (MULTI-SKILL ORCHESTRATION):**

Đây là điều sẽ xảy ra sau khi bạn xây dựng Skill thứ năm của mình. Bạn sẽ bắt đầu nhận thấy sự xung đột.

Ví dụ: Skill “Brand Voice Enforcer” (Bộ kiểm tra Giọng văn Thương hiệu) lại kích hoạt khi bạn chỉ muốn dùng Skill “Email Drafter” (Bộ soạn thảo Email). Trợ lý Đánh giá Mã nguồn (Code Review Assistant) lại kích hoạt trên một đoạn mã mà bạn chỉ muốn định dạng cho đẹp chứ không cần đánh giá. Hai Skill cùng nghĩ rằng chúng nên xử lý cùng một yêu cầu.

Đây là bài toán điều phối đa Skill. Và nó sẽ ngày càng trở nên tồi tệ hơn khi bạn xây dựng càng nhiều Skill.

**TẠI SAO & NHƯ THẾ NÀO?**

Khi bạn đưa ra một yêu cầu, Claude sẽ quét qua tất cả các Skill hiện có và đánh giá các phần mô tả YAML của chúng so với câu lệnh (prompt) của bạn. Quá trình lựa chọn hoạt động đại khái như sau:

* Claude đọc tất cả các mô tả Skill hiện có.
* Nó chấm điểm độ liên quan cho mỗi mô tả so với yêu cầu của bạn.
* Skill có điểm cao nhất sẽ được kích hoạt.
* Nếu không có Skill nào đạt điểm vượt qua ngưỡng kích hoạt, sẽ không có Skill nào được chạy.

**Vấn đề:** Nếu hai Skill có các cụm từ kích hoạt trùng lặp, Skill sai có thể sẽ “giành chiến thắng”. Nếu các mô tả quá mơ hồ, Skill sẽ kích hoạt cho các yêu cầu không liên quan. Nếu các mô tả quá hẹp, Skill sẽ không bao giờ được kích hoạt.

**QUY TẮC ĐỂ ĐẠT ĐƯỢC SỰ HÀI HÒA GIỮA NHIỀU SKILL:**

* **Quy tắc 1: Lãnh thổ không chồng chéo.** Mỗi Skill phải có một miền (domain) được xác định rõ ràng, không được lấn sân sang miền của một Skill khác. Bộ kiểm tra Giọng văn lo phần tuân thủ giọng văn. Bộ soạn thảo Email lo việc viết email. Bộ tái chế Nội dung lo việc chuyển đổi định dạng. Không có sự chồng chéo.
* **Quy tắc 2: Ranh giới phủ định quyết liệt.** Phần mô tả YAML của mỗi Skill phải liệt kê rõ ràng lãnh thổ của các Skill khác như là các trường hợp bị loại trừ. Bộ soạn thảo Email của bạn nên nói: “KHÔNG sử dụng để kiểm tra giọng văn thương hiệu hoặc tái chế nội dung”. Bộ kiểm tra Giọng văn của bạn nên nói: “KHÔNG sử dụng để soạn email từ con số không hoặc tái chế nội dung”.
* **Quy tắc 3: Ngôn ngữ kích hoạt đặc trưng.** Mỗi Skill nên có các cụm từ kích hoạt chỉ dành riêng cho chức năng của nó. “Kiểm tra giọng văn” chỉ nên khớp với Bộ kiểm tra Giọng văn. “Soạn một email” chỉ nên khớp với Bộ soạn thảo Email. Nếu bạn thấy mình đang sử dụng cùng một cụm từ kích hoạt cho hai Skill, thì một trong hai Skill đó đang gặp vấn đề về phạm vi.

**Chẩn đoán Xung đột Skill**

Khi một Skill sai kích hoạt, vấn đề hầu như luôn nằm ở phần mô tả YAML. Đây là một câu lệnh giúp kiểm toán toàn bộ thư viện Skill của bạn để tìm ra các xung đột:

*PROMPT: KIỂM TOÁN VIÊN XUNG ĐỘT SKILL*

Markdown

```
Tôi có nhiều Claude Skill đang được triển khai và tôi đang gặp phải 
xung đột (kích hoạt sai Skill, Skill không kích hoạt khi 
chúng nên kích hoạt, hoặc chức năng chồng chéo).

Dưới đây là các mô tả YAML cho TẤT CẢ các Skill đã triển khai của tôi:

SKILL 1:
[DÁN TOÀN BỘ MÔ TẢ YAML TỪ SKILL 1]

SKILL 2:
[DÁN TOÀN BỘ MÔ TẢ YAML TỪ SKILL 2]

SKILL 3:
[DÁN TOÀN BỘ MÔ TẢ YAML TỪ SKILL 3]

[THÊM NHIỀU HƠN NẾU CẦN]

Hãy chạy quy trình phân tích xung đột sau:

## 1. BẢN ĐỒ LÃNH THỔ
Đối với mỗi Skill, hãy xác định lãnh thổ của nó trong một câu.
Trực quan hóa các lãnh thổ dưới dạng một danh sách và xác định bất kỳ sự chồng chéo nào.

## 2. BÀI KIỂM TRA VA CHẠM CỤM TỪ KÍCH HOẠT
Liệt kê mọi cụm từ kích hoạt từ mọi Skill.
Đánh dấu bất kỳ cụm từ nào có thể khớp với nhiều hơn một Skill.
Đối với mỗi va chạm, hãy đề xuất Skill nào nên sở hữu 
cụm từ đó và đề xuất một phương án thay thế cho Skill kia.

## 3. KIỂM TOÁN RANH GIỚI PHỦ ĐỊNH
Đối với mỗi Skill, hãy kiểm tra xem các ranh giới phủ định của nó 
có loại trừ rõ ràng lãnh thổ của TẤT CẢ các Skill khác hay không.
Đánh dấu bất kỳ sự loại trừ nào bị thiếu.

## 4. BÀI KIỂM TRA YÊU CẦU MƠ HỒ
Tạo ra 10 yêu cầu thực tế của người dùng mang tính mơ hồ 
(có khả năng khớp với nhiều Skill).
Đối với mỗi yêu cầu, hãy dự đoán Skill nào sẽ kích hoạt và liệu 
đó có phải là lựa chọn chính xác hay không.

## 5. KIỂM TRA VÙNG CHẾT (DEAD ZONE)
Xác định bất kỳ yêu cầu phổ biến nào của người dùng KHÔNG kích hoạt 
bất kỳ Skill nào đã triển khai nhưng đáng lẽ ra là có.

## 6. CÁC ĐỀ XUẤT SỬA LỖI
Đối với mỗi vấn đề được tìm thấy, hãy cung cấp phần mô tả YAML đã được sửa 
sẵn sàng để dán trực tiếp vào tệp SKILL.md.

Trình bày các phát hiện dưới dạng một báo cáo có cấu trúc với các 
bản sửa lỗi được xếp hạng theo mức độ ưu tiên.
```

**CHIẾN LƯỢC THAM CHIẾU (REFERENCE STRATEGIES):**

Học phần 1 đã đề cập đến những điều cơ bản: một tệp tham chiếu, độ sâu một tầng, giữ cho nó được nén gọn.

Nhưng điều gì sẽ xảy ra khi Skill của bạn cần tham chiếu đến một bộ quy chuẩn thương hiệu dài 50 trang, một cẩm nang phong cách dài 30 trang, VÀ một thư viện các biểu mẫu?

Bạn cần giúp nó tránh làm lãng phí “cửa sổ ngữ cảnh” (context window) vào những tài liệu tham chiếu không cần thiết cho tác vụ hiện tại:

*PROMPT: KIẾN TRÚC SƯ THIẾT KẾ THAM CHIẾU:*

Markdown

```
Tôi có một Claude Skill cần tham chiếu đến nhiều tài liệu 
lớn. Tôi cần hỗ trợ thiết kế kiến trúc tệp tham chiếu 
sao cho Claude chỉ tải những gì nó cần cho mỗi yêu cầu.

Dưới đây là các tài liệu mà Skill của tôi cần truy cập:
[LIỆT KÊ MỖI TÀI LIỆU KÈM THEO ĐỘ DÀI VÀ MỤC ĐÍCH ƯỚC TÍNH,
ví dụ:
- Quy chuẩn giọng văn thương hiệu (50 trang, bao gồm giọng điệu, từ vựng,
  định dạng)
- Biểu mẫu email (10 biểu mẫu cho các tình huống khác nhau)
- Danh sách khách hàng kèm theo sở thích (200 mục nhập)
- Cẩm nang phong cách (30 trang, bao gồm phong cách hình ảnh và văn bản)]

Đây là tệp SKILL.md của tôi:
[DÁN TỆP SKILL.MD HIỆN TẠI CỦA BẠN]

Hãy thiết kế một kiến trúc tham chiếu đảm bảo:

1. Chia nhỏ các tài liệu lớn thành các tệp con tập trung để có thể 
   tải độc lập.

2. Tạo một phiên bản "tham chiếu nhanh" cho mỗi tài liệu 
   lớn (dưới 30 dòng) bao trùm 80% các trường hợp sử dụng.

3. Viết các hướng dẫn tải có điều kiện cho tệp SKILL.md 
   báo cho Claude biết cần đọc các tài liệu tham chiếu nào dựa trên 
   loại yêu cầu.

4. Đảm bảo quy tắc "sâu một tầng" được duy trì (không có 
   tệp tham chiếu nào liên kết đến một tệp tham chiếu khác).

5. Ước tính mức độ tiết kiệm token so với việc tải mọi thứ 
   trong mỗi lần thực thi.

Đầu ra:
- Sơ đồ cấu trúc thư mục hoàn chỉnh
- Từng tệp tham chiếu (đã được nén và định dạng)
- Tệp SKILL.md đã được cập nhật với các hướng dẫn tải có điều kiện
- Ước tính hiệu suất sử dụng token
```

Học phần 2 đã hoàn tất. Bạn đã hiểu về kiến trúc nâng cao: các script để tính toán, điều phối nhiều Skill để triển khai không bị xung đột và các chiến lược tham chiếu có thể mở rộng.

Trong Học phần 3, bạn sẽ học cách chứng minh rằng các Skill của mình thực sự hiệu quả. Không phải kiểu “cứ dùng thử xem sao”. Mà là chứng minh bằng dữ liệu.

---

### Học phần 3: Thử nghiệm + Cải tiến

Sự khác biệt giữa một Skill “hoạt động tạm ổn” và một Skill vận hành như một nhân viên được đào tạo bài bản nằm ở học phần này. Thử nghiệm, gỡ lỗi (debugging), cải tiến liên tục cho đến khi mọi khả năng thất bại bị loại bỏ.

**CÁC CHẾ ĐỘ THẤT BẠI (FAILURE MODES):**

Trước khi kiểm tra bất cứ thứ gì, bạn cần biết mình đang kiểm tra cái gì. Mọi thất bại của Skill đều rơi vào một trong năm danh mục sau. Nếu học được cách chẩn đoán danh mục đó, cách khắc phục sẽ trở nên hiển nhiên.

**Chế độ Thất bại 1: Skill Câm Lặng (Không bao giờ kích hoạt)**

* **Triệu chứng:** Bạn gõ một yêu cầu đáng lẽ phải kích hoạt Skill. Claude phản hồi bình thường mà không hề sử dụng Skill đó. Không có dấu hiệu nào cho thấy Skill thậm chí đã được xem xét.
* **Nguyên nhân gốc rễ:** Mô tả YAML của bạn quá yếu. Ngưỡng kích hoạt của Claude đòi hỏi sự tương khớp chặt chẽ giữa yêu cầu của người dùng và phần mô tả. Nếu mô tả của bạn mơ hồ, chung chung hoặc thiếu các cụm từ kích hoạt chính, nó sẽ không bao giờ vượt qua được ngưỡng này.
* **Chẩn đoán:** Hãy xem lại phần mô tả của bạn. Nó có liệt kê rõ ràng những từ và cụm từ mà bạn vừa gõ không? Nếu bạn yêu cầu “dọn dẹp bảng tính này” nhưng phần mô tả của bạn chỉ đề cập đến “các file CSV”, thì bạn đã tìm ra lỗ hổng.
* **Khắc phục:** Làm cho mô tả của bạn mang tính “thúc ép” mạnh mẽ hơn. Thêm nhiều cụm từ kích hoạt hơn. Thêm manh mối ngữ cảnh. Phần mô tả nên cực kỳ rõ ràng, rành mạch về thời điểm cần kích hoạt.

**Chế độ Thất bại 2: Kẻ Không Tặc (Kích hoạt sai yêu cầu)**

* **Triệu chứng:** Bạn hỏi Claude một vấn đề không liên quan nhưng Skill của bạn lại kích hoạt. Bạn muốn nháp một email nhưng Bộ Tái chế Nội dung lại nhảy vào.
* **Nguyên nhân gốc rễ:** Mô tả YAML của bạn quá rộng, hoặc các ranh giới phủ định bị thiếu. Phần mô tả khớp với quá nhiều loại yêu cầu.
* **Chẩn đoán:** Nhìn vào những gì bạn vừa gõ và tìm xem từ nào trong yêu cầu của bạn đã khớp với mô tả của Skill. Sau đó kiểm tra xem những từ đó lẽ ra có nên bị loại trừ hay không.
* **Khắc phục:** Thêm ranh giới phủ định. “KHÔNG sử dụng cho [liệt kê mọi tác vụ tương tự nhưng khác biệt].” Siết chặt các cụm từ kích hoạt của bạn để chúng cụ thể hơn với chức năng thực sự của Skill.

**Chế độ Thất bại 3: Kẻ Đi Lạc (Kích hoạt nhưng cho ra kết quả sai)**

* **Triệu chứng:** Skill kích hoạt đúng lúc nhưng kết quả đầu ra không khớp với những gì bạn mong đợi. Nó gần đúng nhưng không hẳn là đúng. Định dạng bị lệch, giọng văn sai, hoặc nó nhảy cóc qua một vài bước.
* **Nguyên nhân gốc rễ:** Hướng dẫn của bạn quá mơ hồ. Có nhiều hơn một cách để hiểu những gì bạn đã viết, và Claude đã chọn một cách hiểu khác với ý định của bạn.
* **Chẩn đoán:** Đọc các hướng dẫn của bạn như thể bạn chưa từng thấy chúng trước đây. Tìm những câu có thể có hai nghĩa khác nhau. Đó chính là nơi sự “đi lạc” xảy ra.
* **Khắc phục:** Thay thế ngôn ngữ mơ hồ bằng các hướng dẫn cụ thể, có thể kiểm chứng được. “Định dạng cho đẹp” sẽ trở thành “Sử dụng tiêu đề H2 cho mỗi phần, bôi đậm câu đầu tiên của mỗi đoạn, giữ mỗi đoạn tối đa 3 dòng.” Không để lại bất kỳ kẽ hở nào cho sự diễn giải theo ý muốn.

**Chế độ Thất bại 4: Skill Mỏng Manh (Đôi khi hoạt động, hỏng hóc ở các trường hợp ngoại lệ)**

* **Triệu chứng:** Skill hoạt động hoàn hảo trên các đầu vào sạch sẽ, định dạng chuẩn. Nhưng khi bạn đưa cho nó một thứ gì đó hơi kỳ lạ (dữ liệu không đầy đủ, định dạng bất thường, thiếu trường), nó sẽ sụp đổ.
* **Nguyên nhân gốc rễ:** Cách xử lý trường hợp ngoại lệ (edge case) của bạn chưa hoàn thiện. Bạn đã không lường trước được thực tế hỗn loạn của các đầu vào ngoài đời thực.
* **Chẩn đoán:** Cung cấp cho Skill của bạn phiên bản tồi tệ nhất của mọi loại đầu vào. Thiếu trường thông tin. Thừa trường. Sai kiểu dữ liệu. Các tệp bị hỏng một phần. Ngôn ngữ bị trộn lẫn. Xem nó gãy ở đâu.
* **Khắc phục:** Thêm các hướng dẫn rõ ràng cho các trường hợp ngoại lệ. Đối với mỗi kịch bản mà nó gặp lỗi, hãy thêm một hướng dẫn cụ thể: “Nếu [điều kiện], thì [hành động cụ thể].”

**Chế độ Thất bại 5: Kẻ Quá Thể Hiện (Thêm những thứ bạn không yêu cầu)**

* **Triệu chứng:** Skill tạo ra kết quả như yêu cầu nhưng lại thêm vào những lời bình luận ngoài lề, các phần thừa thãi, hoặc những tô vẽ sáng tạo mà bạn không hề muốn.
* **Nguyên nhân gốc rễ:** Hướng dẫn của bạn báo cho Claude biết cần làm gì, nhưng lại không nói cho nó biết KHÔNG ĐƯỢC làm gì. Không có những ràng buộc, Claude sẽ mặc định trở nên hữu ích nhất có thể, điều này đôi khi đồng nghĩa với việc nó sẽ làm nhiều hơn những gì bạn yêu cầu.
* **Chẩn đoán:** Xem xét phần đầu ra bị thừa. Sau đó kiểm tra lại các hướng dẫn của bạn xem đã có những ràng buộc rõ ràng về phạm vi và giới hạn đầu ra chưa.
* **Khắc phục:** Thêm các ràng buộc phạm vi rõ ràng. “KHÔNG thêm văn bản giải thích, bình luận hoặc đề xuất trừ khi người dùng yêu cầu. CHỈ xuất ra [định dạng được chỉ định] và không có gì khác.”

*PROMPT: TRÌNH CHẨN ĐOÁN CHẾ ĐỘ THẤT BẠI:*

Markdown

```
Claude Skill của tôi không hoạt động như mong đợi. Tôi cần giúp đỡ 
để chẩn đoán và khắc phục sự cố.

Đây là toàn bộ tệp SKILL.md của tôi:
[DÁN TỆP SKILL.MD CỦA BẠN]

Đây là những gì đã xảy ra:
- Những gì tôi đã gõ: [DÁN CHÍNH XÁC YÊU CẦU BẠN ĐÃ ĐƯA RA]
- Những gì tôi mong đợi: [MÔ TẢ HÀNH VI MONG ĐỢI]
- Những gì thực sự đã xảy ra: [MÔ TẢ HÀNH VI THỰC TẾ]

Hãy chẩn đoán tình trạng này dựa trên 5 Chế độ Thất bại:

1. Skill Câm lặng (không bao giờ kích hoạt) — Mô tả YAML 
   có đủ mạnh để khớp với yêu cầu của tôi không?
2. Kẻ Không Tặc (kích hoạt sai yêu cầu) — Mô tả có quá 
   rộng không? Có thiếu các ranh giới phủ định không?
3. Kẻ Đi Lạc (kết quả sai) — Hướng dẫn có mơ hồ không?
4. Skill Mỏng Manh (hỏng ở trường hợp ngoại lệ) — Có phải đầu vào của tôi 
   là một trường hợp ngoại lệ không được bao hàm?
5. Kẻ Quá Thể Hiện (thêm nội dung không yêu cầu) — Các ràng buộc 
   về phạm vi có bị thiếu không?

Đối với chế độ thất bại được xác định:
- Giải thích chính xác nguyên nhân gây ra sự thất bại
- Cung cấp cách sửa lỗi cụ thể (YAML đã sửa, hướng dẫn mới, 
  hoặc cách xử lý ngoại lệ)
- Hiển thị phần đã sửa của SKILL.md sẵn sàng để dán
- Đề xuất một câu lệnh kiểm tra (test prompt) để xác minh xem cách khắc phục có hiệu quả không
```

**KIỂM TRA SKILL CỦA BẠN:**

Đây là điều mà hầu hết mọi người đều làm sai.

Họ xây dựng một Skill, thử nghiệm nó hai lần, thấy “ổn ổn”, rồi chuyển sang việc khác. Sau đó nó sẽ thất bại thảm hại ở trường hợp ngoại lệ thứ ba mà họ không lường trước được.

Bản cập nhật Skills 2.0 đã chấm dứt trò phỏng đoán đó. Giờ đây bạn đã có bộ công cụ kiểm thử chuẩn chuyên nghiệp được tích hợp sẵn trong Claude, vậy nên hãy đi và sử dụng nó!

* **Evals (Đánh giá):** Viết các câu lệnh kiểm tra. Xác định chính xác hành vi mong đợi phải là gì. Hệ thống sẽ chạy Skill của bạn để đối chiếu với các câu lệnh đó và trả về điểm Đạt/Trượt. Không có chuyện “trông có vẻ ổn”. Đạt. Hoặc Trượt.
* **Benchmarks (Điểm chuẩn):** Theo dõi tỷ lệ đạt của Skill, mức tiêu thụ token (chi phí), và tốc độ thực thi theo thời gian. Bạn có thể thấy liệu bản viết lại phiên bản thứ 3 của bạn có thực sự làm mọi thứ tốt hơn không, hay chỉ là bạn CẢM THẤY như vậy.
* **A/B Comparator (Trình So sánh A/B):** Chạy thử nghiệm mù (blind test) giữa hai phiên bản hướng dẫn của Skill. Lấy dữ liệu cứng xem phiên bản nào chiến thắng.
* **Description Optimiser (Trình Tối ưu hóa Mô tả):** Báo cho bạn biết một cách chắc chắn liệu các trigger YAML của bạn có kích hoạt chính xác khi người dùng yêu cầu tác vụ hay không.

Hãy tiếp tục lặp lại quá trình này (iterate) cho đến khi hai lần chạy đánh giá liên tiếp không cho thấy sự cải thiện đáng kể nào nữa. Đó chính là tín hiệu của bạn. Skill của bạn đã sẵn sàng để đi vào sản xuất (production-ready).

Học phần 3 đã hoàn tất. Bạn hiện đã sở hữu một skill đạt chuẩn chuyên nghiệp.

Học phần 4 là mảnh ghép cuối cùng: triển khai các skill có khả năng hoạt động xuyên suốt qua nhiều phiên làm việc (sessions).

[![](https://substackcdn.com/image/fetch/$s_!4BAj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F01a36653-08e1-44cb-bb36-0c9064103cb2_1376x768.jpeg)](https://substackcdn.com/image/fetch/$s_!4BAj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F01a36653-08e1-44cb-bb36-0c9064103cb2_1376x768.jpeg)

### Học phần 4: Triển khai Thực tế (Production Deployment)

Các Skill của bạn đã hoạt động tốt. Chúng đã được kiểm tra. Chúng đã được triển khai.

Giờ đây, câu hỏi chuyển từ “nó có hoạt động không?” sang “nó có hoạt động ở quy mô lớn, qua thời gian, và xuyên suốt các phiên làm việc không?”

**QUẢN LÝ TRẠNG THÁI (STATE MANAGEMENT):**

Khi bạn đang chạy một Skill xuyên suốt nhiều phiên làm việc (ví dụ: viết một cuốn sách, xây dựng một ứng dụng phức tạp, quản lý một dự án kéo dài nhiều tuần), cửa sổ ngữ cảnh (context window) của Claude cuối cùng sẽ bị đầy.

Nó sẽ quên mất những gì đã xảy ra ngày hôm qua.

Các chuyên gia xây dựng Skill giải quyết vấn đề này bằng một hệ thống “bàn giao ca”. Bên trong tệp `SKILL.md` của mình, bạn hãy thêm một hướng dẫn duy nhất:

> “Vào đầu mỗi phiên làm việc, hãy đọc tệp `context-log.md` để xem chúng ta đã hoàn thành những gì trong lần trước. Vào cuối mỗi phiên làm việc, hãy viết một bản tóm tắt về những gì bạn đã hoàn thành và những gì vẫn còn đang dang dở.”

Chỉ vậy thôi. Claude sẽ tự đọc lại các ghi chú của chính mình từ phiên trước và tiếp tục công việc chính xác ở nơi nó đã dừng lại.

Hãy coi việc này giống như việc chuyển ca trong bệnh viện. Bác sĩ trực ca sau sẽ đọc hồ sơ bệnh án. Họ biết chính xác chuyện gì đã xảy ra, việc gì đang chờ xử lý và cần chú ý những gì. Trí tuệ nhân tạo của bạn cũng hoạt động theo cách tương tự.

**CUỐI CÙNG...**

Bạn có thể tiếp tục mở Claude ra vào mỗi buổi sáng và gõ lại y chang những hướng dẫn mà bạn đã gõ ngày hôm qua. Và ngày hôm kia. Và nhiều ngày trước đó nữa. Đốt cháy những phút giây rảnh rỗi, để chúng tích tụ thành hàng giờ, rồi tích tụ thành hàng tuần lễ đánh mất hiệu suất.

Hoặc, bạn có thể dành ra 10 phút ngay lúc này, xây dựng một Skill, và không bao giờ phải gõ lại những hướng dẫn đó nữa.

Những người xây dựng Skills đang điều hành Claude giống như một hệ thống được tùy chỉnh (custom-built) và tinh chỉnh chính xác theo nhu cầu cụ thể của họ.

Tất cả những người còn lại thì chỉ đang sử dụng nó như một hộp chat (chatbox) bình thường.

Hãy xây dựng Skill đầu tiên của bạn ngay hôm nay. Chọn một tác vụ mà bạn lặp lại thường xuyên nhất. Làm theo các bước trên. Triển khai nó. Bấm giờ xem phiên làm việc tiếp theo của bạn chạy nhanh hơn bao nhiêu.

Sau đó, hãy xây dựng một Skill khác.

Bạn định tự động hóa tác vụ nào đầu tiên? Hãy để lại bình luận nhé. Tôi sẽ đọc tất cả.

**P.S.** Siêu-kỹ-năng (meta-skill) `skill-creator` có thể xây dựng Skill đầu tiên cho bạn trong vòng chưa đầy 5 phút chỉ thông qua trò chuyện. Nếu bạn vẫn còn đang lưỡng lự, hãy bắt đầu từ đó.

[![Alex Quang](https://substackcdn.com/image/fetch/$s_!pZKs!,w_48,h_48,c_fill,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fec7f29c0-273a-4896-aaf4-905c680dcddc_160x160.png)](https://ecomstoryvn.substack.com/)#### Recommend Alex Quang to your readers

AI guy

#### Discussion about this post

[🚨TIN NÓNG: Claude vừa trở thành một trong những AI mạnh nhất trên Internet.](https://ecomstoryvn.substack.com/p/tin-nong-claude-vua-tro-thanh-mot)

[Nhưng 99% mọi người vẫn chỉ dùng nó để hỏi những câu hỏi cơ bản.](https://ecomstoryvn.substack.com/p/tin-nong-claude-vua-tro-thanh-mot)

Mar 11 **•** [Alexquang](https://substack.com/@alexquang)

4

1

![](https://substackcdn.com/image/fetch/$s_!aD01!,w_320,h_213,c_fill,f_auto,q_auto:good,fl_progressive:steep,g_center/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1c8a6ff8-fd4c-46cc-9bf5-ec1b5c768169_1200x673.jpeg)

[Hai cuốn sách tôi sẽ đọc lại mỗi năm cho đến ngày tôi qua đời.](https://ecomstoryvn.substack.com/p/hai-cuon-sach-toi-se-oc-lai-moi-nam)

[Tôi hứa rằng bạn sẽ học được điều gì đó mới mỗi lần đọc.](https://ecomstoryvn.substack.com/p/hai-cuon-sach-toi-se-oc-lai-moi-nam)

Feb 13 **•** [Alexquang](https://substack.com/@alexquang)

2

![](https://substackcdn.com/image/fetch/$s_!zjc1!,w_320,h_213,c_fill,f_auto,q_auto:good,fl_progressive:steep,g_center/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7696016d-4bf8-4afd-8e11-649978f58772_5712x4284.jpeg)

[Tôi đã lãng phí 80 giờ và 800$ để cài OpenClaw – để bạn không phải làm thế.](https://ecomstoryvn.substack.com/p/toi-a-lang-phi-80-gio-va-800-e-cai)

[Tôi đã thử mọi thứ. Server AWS, cài đặt từ xa, sai API key, sai model. Tôi đốt khoảng 800 đô chỉ riêng tiền token API của Anthropic. Thử Kimi. Thử Opus.](https://ecomstoryvn.substack.com/p/toi-a-lang-phi-80-gio-va-800-e-cai)

Feb 17 **•** [Alexquang](https://substack.com/@alexquang)

1

![](https://substackcdn.com/image/fetch/$s_!F4ug!,w_320,h_213,c_fill,f_auto,q_auto:good,fl_progressive:steep,g_center/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdce13bb3-bf0b-4c90-aedf-ba5ea79494d3_1250x500.jpeg)

© 2026 Ecomstory · [Privacy](https://substack.com/privacy) ∙ [Terms](https://substack.com/tos) ∙ [Collection notice](https://substack.com/ccpa#personal-data-collected)

[Start your Substack](https://your.substack.com/publish)[Get the app](https://substack.com/app/app-store-redirect?utm_campaign=app-marketing&utm_content=web-footer-button)

[Substack](https://substack.com/) is the home for great culture

<iframe height="1" width="1"></iframe>

![]()

Beta

1 / 10used queries

![](chrome-extension://amfojhdiedpdnlijjbhjnhokbnohfdfb/img/logo/icon@2x.png)

![]()

1
