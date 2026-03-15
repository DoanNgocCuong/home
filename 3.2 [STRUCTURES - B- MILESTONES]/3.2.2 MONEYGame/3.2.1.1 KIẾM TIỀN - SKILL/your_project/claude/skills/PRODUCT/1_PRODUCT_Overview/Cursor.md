
Dưới đây là nội dung tài liệu "Cursor mechanism overview" được chuyển đổi sang định dạng Markdown, giữ nguyên nội dung gốc:

[cite_start]Báo cáo này đi sâu vào cơ chế hoạt động nội bộ của Cursor, một trình soạn thảo mã nguồn ưu tiên AI, để làm rõ cách nó xử lý các lệnh từ các chỉ thị cụ thể đến các thiết kế cấp cao (HLD)[cite: 1]. [cite_start]Bằng cách phân tích kiến trúc, hệ thống lệnh và các mô hình xử lý đầu vào, chúng tôi đặt mục tiêu cung cấp một sự hiểu biết toàn diện về khả năng và giới hạn của Cursor[cite: 2].

## Kiến trúc Cốt lõi và Cơ chế Hoạt động

[cite_start]Hoạt động của Cursor xoay quanh một nguyên tắc cơ bản: các Mô hình Ngôn ngữ Lớn (LLM) hoạt động bằng cách dự đoán từ tiếp theo một cách lặp đi lặp lại[cite: 4]. [cite_start]Khái niệm này, khi được kết hợp với các công cụ phức tạp và quản lý ngữ cảnh, tạo ra một trợ lý lập trình mạnh mẽ[cite: 5]. [cite_start]Kiến trúc của nó có thể được chia thành nhiều thành phần chính hoạt động phối hợp để diễn giải ý định của người dùng và thực hiện các tác vụ lập trình phức tạp[cite: 6].

### Lập chỉ mục Codebase và Nhúng Ngữ nghĩa

[cite_start]Nền tảng cho khả năng nhận thức toàn bộ dự án của Cursor là hệ thống lập chỉ mục codebase của nó[cite: 8]. [cite_start]Quá trình này bao gồm việc chia nhỏ các tệp mã nguồn thành các đoạn (chunks) nhỏ, có ý nghĩa về mặt ngữ nghĩa, thường có kích thước từ 100 đến 500 token[cite: 9].

Thay vì cắt một cách mù quáng, Cursor sử dụng các công cụ như tree-sitter để phân tích mã nguồn thành các cây cú pháp trừu tượng (AST), cho phép nó chia nhỏ mã tại các ranh giới logic như hàm và lớp. [cite_start]Mỗi đoạn sau đó được chuyển đổi thành một vector nhúng (embedding vector), là một biểu diễn số nắm bắt được nghĩa ngữ nghĩa của mã[cite: 10].

Các vector này được lưu trữ trong một cơ sở dữ liệu vector chuyên dụng như Turbopuffer, cùng với siêu dữ liệu ánh xạ chúng trở lại tệp và số dòng ban đầu. [cite_start]Để tối ưu hóa hiệu suất, Cursor sử dụng cây Merkle để phát hiện các thay đổi trong codebase, chỉ lập chỉ mục lại các đoạn đã bị ảnh hưởng thay vì xử lý lại toàn bộ dự án[cite: 11].

### Truy xuất-Tăng cường Tạo sinh (RAG)

[cite_start]Với codebase đã được lập chỉ mục, Cursor sử dụng một mô hình Truy xuất-Tăng cường Tạo sinh (Retrieval-Augmented Generation - RAG) để cung cấp ngữ cảnh có liên quan cho LLM[cite: 13].

Khi người dùng đặt một câu hỏi, chẳng hạn như "Tìm tất cả những nơi chúng ta gọi hàm authenticateUser", truy vấn đó được chuyển đổi thành một vector nhúng và được sử dụng để tìm kiếm các đoạn mã tương tự nhất trong cơ sở dữ liệu vector. [cite_start]Các đoạn mã có liên quan nhất sau đó được truy xuất và đưa vào cửa sổ ngữ cảnh của LLM[cite: 14]. [cite_start]Cách tiếp cận này cho phép AI vượt ra ngoài tệp hiện đang được chỉnh sửa và rút ra thông tin từ bất kỳ đâu trong dự án, mang lại cho nó khả năng nhận thức toàn bộ dự án một cách hiệu quả[cite: 15].

### Xây dựng Prompt và Quản lý Ngữ cảnh

[cite_start]Đằng sau mỗi tương tác của người dùng, Cursor thực hiện một quy trình phức tạp để xây dựng một prompt hiệu quả cho LLM[cite: 17]. [cite_start]Nó tổng hợp ngữ cảnh từ nhiều nguồn khác nhau, bao gồm truy vấn của người dùng, mã từ tệp đang mở, kết quả từ tìm kiếm ngữ nghĩa, lịch sử hội thoại và siêu dữ liệu môi trường như lỗi linter[cite: 18]. [cite_start]Để quản lý các giới hạn token của LLM, Cursor sử dụng các chiến lược như phân cửa sổ (windowing), chia các tác vụ lớn thành các phần nhỏ hơn và xử lý chúng một cách tuần tự[cite: 18].

[cite_start]Hơn nữa, nó làm phong phú thêm ngữ cảnh bằng cách sử dụng phân tích AST từ các máy chủ ngôn ngữ để cung cấp các định nghĩa ký hiệu và thông tin kiểu, mang lại cho mô hình một sự hiểu biết sâu sắc hơn về mã[cite: 19].

[cite_start]Một tính năng đáng chú ý là **Không gian làm việc bóng tối (Shadow Workspace)**, một phiên bản VSCode ẩn được sử dụng để xác thực các thay đổi[cite: 20]. [cite_start]Trước khi trình bày một bản vá cho người dùng, AI sẽ áp dụng các thay đổi trong không gian làm việc này, biên dịch hoặc lint mã, và sử dụng phản hồi (ví dụ: lỗi trình biên dịch) để tự sửa lỗi[cite: 21]. [cite_start]Vòng lặp tự tinh chỉnh này, vô hình đối với người dùng, đảm bảo rằng các thay đổi được đề xuất có nhiều khả năng đúng và áp dụng một cách sạch sẽ[cite: 22].

## Phân tích Lệnh và Đầu vào

[cite_start]Cursor hỗ trợ một loạt các loại đầu vào, từ các chỉ thị rất cụ thể đến các chỉ thị kiến trúc cấp cao[cite: 24]. [cite_start]Hiệu quả và độ tin cậy của nó thay đổi đáng kể trên phổ này[cite: 25].

| Cấp độ Đầu vào | Ví dụ | Tỷ lệ Thành công | Cơ chế Chính |
| :--- | :--- | :--- | :--- |
| **1. Chỉ thị Cụ thể** <br> **2. Chỉ thị Cấp tệp** | "Sửa lỗi null pointer ở dòng 42 của auth.ts" <br> "Tái cấu trúc thành phần UserService" | **Rất cao (95%+)** <br> **Cao (85-90%)** | Đọc tệp trực tiếp, áp dụng bản vá nhỏ <br> Đọc toàn bộ tệp, phân tích AST, áp dụng bản vá ngữ nghĩa |
| **3. Chỉ thị Cấp tính năng** | "Triển khai xác thực người dùng với JWT" | **Trung bình-Cao (70-85%)** | Tìm kiếm ngữ nghĩa, chỉnh sửa nhiều tệp, tự sửa lỗi |
| **4. Thiết kế Cấp cao (HLD)** | "Thiết kế kiến trúc microservices" | **Trung bình (50-70%)** | Phân rã HLD, lập kế hoạch, thực thi lặp đi lặp lại |

[cite_start][cite: 26]

### Cấp độ 1-2: Chỉ thị Cụ thể và Cấp tệp

[cite_start]Cursor hoạt động tốt nhất khi nhận được các chỉ thị có giới hạn, có thể thực hiện và có thể xác minh[cite: 28]. [cite_start]Các lệnh này chỉ định chính xác những gì cần phải làm, thường bao gồm các vị trí tệp, số dòng hoặc các yêu cầu chức năng rõ ràng[cite: 29].

[cite_start]Đối với các tác vụ này, phạm vi được xác định rõ ràng, cho phép AI đọc (các) tệp có liên quan, áp dụng một thay đổi tập trung và xác thực nó ngay lập tức bằng cách sử dụng phản hồi từ linter hoặc trình biên dịch[cite: 30]. [cite_start]Quá trình này hiệu quả và có độ tin cậy cao vì nó giảm thiểu sự mơ hồ và giảm số lượng quyết định thiết kế mà AI phải đưa ra[cite: 31].

### Cấp độ 3: Chỉ thị Cấp tính năng

[cite_start]Khi được giao nhiệm vụ triển khai các tính năng hoàn chỉnh trải dài trên nhiều tệp, Cursor dựa nhiều vào khả năng tìm kiếm ngữ nghĩa của mình để xác định tất cả các thành phần liên quan[cite: 33]. [cite_start]Sau đó, nó điều phối các chỉnh sửa trên nhiều tệp, cố gắng duy trì tính nhất quán[cite: 34].

[cite_start]Vòng lặp tự sửa lỗi trở nên quan trọng ở cấp độ này, vì các thay đổi trong một tệp có thể gây ra lỗi ở một tệp khác[cite: 35]. [cite_start]Mặc dù có khả năng, sự phức tạp tăng lên có thể dẫn đến các vấn đề như nhắm mục tiêu sai tệp do tên gọi không rõ ràng hoặc quản lý không chính xác các phụ thuộc giữa các tệp[cite: 36].

### Cấp độ 4: Thiết kế Cấp cao (HLD)

[cite_start]Khi xử lý đầu vào HLD, Cursor không "thiết kế" theo nghĩa con người; thay vào đó, nó phân rã các khái niệm trừu tượng thành một chuỗi các chỉ thị cụ thể, có thể thực hiện được[cite: 38, 39].

[cite_start]Ví dụ, khi được yêu cầu "Thiết kế kiến trúc microservices", AI sẽ trước tiên phân tích codebase hiện có, sau đó đề xuất một kế hoạch (thường sử dụng tính năng Todos của nó) để tạo các dịch vụ, thiết lập giao tiếp API và tái cấu trúc mã hiện có[cite: 40]. [cite_start]Sau đó, nó thực hiện từng bước trong kế hoạch một cách lặp đi lặp lại[cite: 41].

**Những gì hoạt động tốt với HLD:**

  * [cite_start]**Tạo tài liệu thiết kế:** Nó có thể tạo ra các tài liệu kiến trúc, sơ đồ (ở định dạng văn bản như Mermaid) và các kế hoạch triển khai chi tiết[cite: 43].
  * [cite_start]**Triển khai dựa trên mẫu:** Nếu HLD chỉ định các mẫu thiết kế nổi tiếng (ví dụ: MVC, Repository), Cursor có thể triển khai chúng một cách hiệu quả vì chúng có cấu trúc mã rõ ràng[cite: 44].
  * [cite_start]**Thiết kế nhận thức Codebase:** Nó có thể đề xuất các thiết kế phù hợp với các mẫu và quy ước hiện có của codebase[cite: 45].

**Những gì không hoạt động tốt với HLD:**

  * [cite_start]**Thiết kế khái niệm thuần túy:** Các chỉ thị quá trừu tượng không có cơ sở trong codebase (ví dụ: "Thiết kế một hệ thống có thể mở rộng cho hàng triệu người dùng") là quá mơ hồ để có thể thực hiện được[cite: 47, 48].
  * [cite_start]**Các quyết định kiến trúc phức tạp:** AI có thể không hiểu được các đánh đổi phức tạp, chẳng hạn như tính nhất quán so với tính khả dụng hoặc độ trễ so với thông lượng[cite: 49].
  * [cite_start]**Tích hợp hệ thống bên ngoài:** Mặc dù nó có thể tạo mã để tương tác với các API hoặc cơ sở dữ liệu bên ngoài, nó không thể kiểm tra hoặc xác thực các tích hợp này một cách tự động[cite: 50].

## Điểm mạnh và Hạn chế chính

### Điểm mạnh

1.  [cite_start]**Nhận thức Toàn bộ Dự án:** Lập chỉ mục RAG cho phép AI hiểu các mối quan hệ trên toàn bộ codebase, không chỉ tệp hiện tại[cite: 53].
2.  [cite_start]**Điều phối Đa tệp:** Nó có thể thực hiện các thay đổi được điều phối trên nhiều tệp để triển khai các tính năng phức tạp[cite: 54].
3.  [cite_start]**Tự sửa lỗi:** Bằng cách sử dụng phản hồi từ linter, trình biên dịch và các bài kiểm tra, AI có thể tự động tinh chỉnh mã của mình để sửa lỗi[cite: 55].
4.  [cite_start]**Thực thi Song song:** Các lệnh gọi công cụ độc lập, chẳng hạn như đọc nhiều tệp, được thực hiện song song để tăng tốc độ[cite: 56].

### Hạn chế

1.  **Giới hạn Token:** Giống như tất cả các hệ thống dựa trên LLM, cửa sổ ngữ cảnh hạn chế giới hạn phạm vi của các hoạt động phức tạp. [cite_start]Các HLD toàn diện có thể dễ dàng vượt quá giới hạn này[cite: 58, 59].
2.  [cite_start]**Hiện vật Phân đoạn:** Hiệu suất có thể giảm sút trên các tệp cực lớn (\>500 dòng mã), vì mô hình áp dụng bản vá có thể gặp khó khăn[cite: 60].
3.  **Phụ thuộc vào Tài liệu:** Chất lượng của tìm kiếm ngữ nghĩa phụ thuộc rất nhiều vào các bình luận và chuỗi tài liệu trong mã. [cite_start]Các codebase được ghi chép kém sẽ làm giảm hiệu quả của nó[cite: 61, 62].
4.  [cite_start]**Lỗi Mô hình Áp dụng:** Hệ thống "bản vá ngữ nghĩa", mặc dù hiệu quả, đôi khi có thể gây ra các lỗi tinh vi, chẳng hạn như xóa mã không liên quan hoặc các bình luận[cite: 63].

## Kết luận và Khuyến nghị

[cite_start]Kiến trúc của Cursor được tối ưu hóa một cách cơ bản cho các chỉ thị cụ thể, có thể thực hiện được, nơi phạm vi rõ ràng và việc xác thực là ngay lập tức[cite: 65]. [cite_start]Mặc dù nó có thể xử lý đầu vào HLD, nhưng nó thực hiện điều này bằng cách dịch các thiết kế trừu tượng thành một kế hoạch gồm các bước cụ thể và thực hiện chúng một cách tuần tự[cite: 66].

[cite_start]Do đó, câu hỏi không phải là "Cursor có hoạt động với HLD không?" mà là "Làm thế nào để tôi có thể phân rã HLD của mình thành các chỉ thị mà Cursor có thể triển khai một cách đáng tin cậy?"[cite: 68].

Để tối đa hóa hiệu quả của Cursor, người dùng nên áp dụng một quy trình làm việc kết hợp:

1.  [cite_start]**Sử dụng HLD để Lập kế hoạch:** Bắt đầu với một chỉ thị cấp cao để tạo ra một tài liệu kiến trúc và một kế hoạch triển khai có cấu trúc[cite: 69].
2.  [cite_start]**Sử dụng Chỉ thị Cụ thể để Thực thi:** Thực hiện từng bước của kế hoạch bằng cách sử dụng các lệnh cụ thể, có giới hạn[cite: 70].
3.  [cite_start]**Cung cấp Ngữ cảnh Rõ ràng:** Sử dụng cú pháp `@file` và `@folder` một cách tích cực để cung cấp cho AI ngữ cảnh có liên quan nhất[cite: 71].
4.  [cite_start]**Duy trì Chất lượng Codebase:** Giữ cho các tệp có kích thước vừa phải, sử dụng tên tệp duy nhất và viết các bình luận cũng như chuỗi tài liệu rõ ràng để cải thiện khả năng lập chỉ mục ngữ nghĩa[cite: 72].

[cite_start]Bằng cách hiểu rằng sức mạnh của Cursor không nằm ở việc thiết kế trừu tượng mà ở việc thực thi các tác vụ được xác định rõ ràng một cách không mệt mỏi, các nhà phát triển có thể tận dụng nó như một công cụ nhân lên lực lượng cực kỳ mạnh mẽ, tự động hóa các khía cạnh tẻ nhạt của việc viết mã trong khi vẫn giữ quyền kiểm soát chiến lược đối với kiến trúc và thiết kế[cite: 73].

## Tài liệu tham khảo

  * [1] Aditya Rohilla. (2025). [cite_start]How Cursor Works Internally? [cite: 75]
  * [2] Shrivu Shankar. (2025). [cite_start]How Cursor (AI IDE) Works. [cite: 76]
  * [3] Cursor. (n.d.). Commands | [cite_start]Cursor Docs. [cite: 77]
  * [4] Lakkanna Walikar. (2025). [cite_start]Cursor AI Architecture: System Prompts and Tools Deep Dive. [cite: 78]
  * [5] BitPeak. (2025). [cite_start]How Cursor works - Deep dive into vibe coding. [cite: 79]
  * [6] ByteByteGo. (2025). [cite_start]How Cursor Serves Billions of AI Code Completions Every Day. [cite: 80]
  * [7] Cursor. (n.d.). Overview | [cite_start]Cursor Docs. [cite: 81]


---

## (3) Thiết kế Sub-Agent trong Cursor (đội 5 vai)

### Sub-agent trong Cursor: làm “thật” như thế nào?

Tuỳ phiên bản Cursor, bạn có thể có/không có UI “Sub Agents”. Có report là đôi lúc mục này biến mất theo bản cập nhật. [Cursor - Community Forum+1](https://forum.cursor.com/t/sub-agents-section-missing-in-cursor-2-2-7-on-macos/145721?utm_source=chatgpt.com)  
Cách ổn định nhất: bạn tạo **Slash Commands** bằng file Markdown trong `.cursor/commands/`, rồi gọi nhanh bằng gõ `/` trong Agent chat. [Cursor+2ezablocki.com+2](https://cursor.com/docs/agent/chat/commands?utm_source=chatgpt.com)

**Cấu trúc gợi ý**

`.cursor/   commands/     planner.md     implementer.md     debugger.md     reviewer.md     test-writer.md`

---

### 1) Planner

**System intent (1–2 câu)**: Biến yêu cầu thành kế hoạch nhỏ, rõ file nào cần đọc/sửa, có tiêu chí hoàn thành.

**Prompt gọi (đặt trong `planner.md`)**

`Bạn là Planner. Nhiệm vụ: tạo kế hoạch nhỏ, không code vội. Input: <GOAL>, <CONSTRAINTS>, <FILES>. Output đúng format: - Summary (<=5 dòng) - Plan checklist (5–10 bước, mỗi bước có file + verify) - Assumptions (nếu thiếu info) - Risks Chỉ hỏi tối đa 3 câu nếu thiếu dữ kiện.`

**Output format chuẩn**

- Summary
    
- Plan checklist (Step 1…)
    
- Assumptions / Risks / Verify commands
    

---

### 2) Implementer

**System intent**: Viết code theo plan, **minimal diff**, không tự ý mở rộng phạm vi.

**Prompt mẫu**

`Bạn là Implementer. Làm theo Plan đã duyệt. Luật: minimal diff, chỉ sửa các file được liệt kê; không refactor ngoài scope. Trước khi viết code: nhắc lại files sẽ sửa + lý do. Output: - Patch đề xuất (mô tả thay đổi theo file) - Lệnh chạy verify - “What I did NOT change”`

---

### 3) Debugger

**System intent**: Đọc error/log, khoanh vùng nguyên nhân, đề xuất cách kiểm tra nhanh và fix nhỏ.

**Prompt mẫu**

`Bạn là Debugger. Dựa trên <ERROR_LOG> và <FILES>. Output: 1) Chẩn đoán: lỗi thuộc loại gì (config/runtime/type/logic) 2) Vị trí nghi ngờ (file + dòng/khối code) 3) 3 bước kiểm tra để xác nhận 4) Fix minimal diff + cách verify Không đoán mò nếu thiếu log.`

---

### 4) Reviewer

**System intent**: Review chất lượng, edge cases, clean code, security cơ bản (input validation, auth, secrets).

**Prompt mẫu**

`Bạn là Reviewer. Review theo checklist: - Đúng yêu cầu? Có phá backward compatibility? - Edge cases quan trọng? - Security cơ bản: validate input, tránh leak secrets, tránh unsafe eval - DX: tên hàm rõ, comment đúng chỗ Output: - Review comments theo mức: Blocker / Should / Nice - Đề xuất patch nhỏ (nếu cần)`

---

### 5) Test Writer

**System intent**: Viết test đúng trọng tâm, dễ chạy, lock bug/feature.

**Prompt mẫu**

`Bạn là Test Writer. Input: <GOAL> + <FILES> + (nếu có) patch. Output: - Danh sách test cases (3–6 cases) - Test code đề xuất (theo framework hiện có) - Lệnh chạy test Ưu tiên 1 happy path + 1 edge case quan trọng.`

---

## (4) Tip & Trick nâng cao cho nontech

### 1) Prompt patterns để AI không vòng vo

Công thức 1 câu: **Goal + Constraints + Context + Output format + Stop condition**

**Mẫu**

`<GOAL> <CONSTRAINTS> minimal diff, không bịa API, không đổi style <CONTEXT> @file... @folder... <OUTPUT> checklist + patch + test plan <STOP> nếu thiếu dữ kiện thì hỏi trước khi code`

### 2) Bắt AI “chỉ sửa đúng phần cần sửa” (minimal diff)

Dùng câu thần chú:

- “Chỉ sửa trong các file: …”
    
- “Không đổi format/lint nếu không bắt buộc”
    
- “Nếu cần đổi nhiều file: giải thích vì sao từng file”
    

**Prompt mini**

`Chỉ sửa: <FILES> Không được sửa: mọi file khác Minimal diff: không rename/format hàng loạt Trả về: danh sách thay đổi theo file + lý do`

### 3) Bắt AI tự kiểm tra (assumptions, constraints, test plan)

**Prompt mini**

`Trước khi code: - Liệt kê assumptions (tối đa 5) - Liệt kê constraints (tối đa 5) - Viết test plan (lệnh chạy + expected result) Nếu assumptions sai, hãy dừng và hỏi tôi.`

### 4) Dùng AI để đọc code nhanh

Các lệnh “đọc hiểu” siêu hợp nontech:

- “Explain like I’m 12” (giải thích như cho học sinh lớp 6–7)
    
- “Map luồng chạy” (từ entrypoint tới output)
    
- “Tóm tắt file” (mục đích + hàm chính + dữ liệu vào/ra)
    

**Prompt mini**

`Giải thích như mình 12 tuổi: - File này làm gì (<=5 dòng) - Luồng chạy: A -> B -> C - 3 điểm dễ bug nhất - Nếu muốn sửa X thì sửa chỗ nào?`

### 5) Khi AI sai: rollback + checkpoints (cứu bạn khỏi “toang”)

Tư duy: **checkpoint thường xuyên**.

**Checklist**

-  Tạo branch mới trước khi làm lớn
    
-  Commit nhỏ sau mỗi bước chạy được
    
-  Nếu AI làm bậy: quay lại commit trước
    

**Lệnh git cơ bản (copy)**

`git checkout -b fix/your-task git status git add -A git commit -m "checkpoint: step 1" git restore --staged . git restore . git log --oneline --max-count=10`

---

## Sai lầm phổ biến của nontech khi dùng AI trong Cursor (và cách tránh)

1. **Đưa yêu cầu mơ hồ** → AI đoán bừa  
    → Cách tránh: luôn viết `<GOAL>` + ví dụ input/output + “không được làm gì”.
    
2. **Cho AI sửa quá rộng ngay từ đầu**  
    → Cách tránh: ép **minimal diff**, giới hạn file, bắt plan trước.
    
3. **Không đính kèm context (file/log)**  
    → Cách tránh: dùng `@Files & Folders` để attach đúng file. [Cursor](https://cursor.com/docs/context/mentions?utm_source=chatgpt.com)
    
4. **Không có cách verify** (xong rồi… không biết đúng chưa)  
    → Cách tránh: bắt AI đưa **test plan + lệnh chạy** trước khi code.
    
5. **Không lưu plan/checkpoint**  
    → Cách tránh: plan lưu vào workspace (nếu dùng plan mode) và commit checkpoint. [Cursor - Community Forum+1](https://forum.cursor.com/t/what-happens-when-plan-file-is-saved/135261?utm_source=chatgpt.com)