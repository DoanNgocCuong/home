**

Phân Tích Toàn Diện: Corner Case, Bug và Rủi Ro Hệ Thống

Tác giả: Manus AI Ngày: 05/12/2025

  

Lời Mở Đầu

Tài liệu này cung cấp một phân tích chi tiết và toàn diện về các trường hợp đặc biệt (corner case), lỗi (bug) và các rủi ro tiềm ẩn có thể ảnh hưởng đến trải nghiệm người dùng (UX) trong suốt hành trình tương tác với robot Pika. Phân tích được thực hiện dựa trên các tài liệu "Chi Tiết Luồng Tương Tác Người Dùng (User Journey)" và "Phân Tích Chi Tiết Luồng Kỹ Thuật (Technical Breakdown)".

  

Mục tiêu của tài liệu là:

  

1. Xác định và liệt kê một cách có hệ thống tất cả các corner case và bug có thể xảy ra ở từng hoạt động.
    
2. Phân tích nguyên nhân và đánh giá mức độ ảnh hưởng của từng vấn đề đến trải nghiệm người dùng.
    
3. Đề xuất các giải pháp kỹ thuật và chiến lược giảm thiểu rủi ro để xây dựng một sản phẩm ổn định và đáng tin cậy.
    
4. Cung cấp một cái nhìn tổng quan về các vấn đề kiến trúc và cross-functional, giúp đội ngũ phát triển có một kế hoạch hành động rõ ràng.
    

  

Nội dung được trình bày theo từng hoạt động trong User Journey, với sơ đồ luồng kỹ thuật (Mermaid) và bảng phân tích chi tiết, đảm bảo tính đầy đủ và dễ theo dõi (MECE - Mutually Exclusive, Collectively Exhaustive).

  

  

  

PHẦN 1: PHÂN TÍCH CHI TIẾT THEO TỪNG HOẠT ĐỘNG

Phần này đi sâu vào từng hoạt động trong hành trình của người dùng, từ lúc mở hộp cho đến các tương tác hàng ngày, để xác định các rủi ro cụ thể.

  

  

  

# GIAI ĐOẠN 0: ONBOARDING (NGÀY 0 - NGÀY 1)

## HOẠT ĐỘNG 1: MỞ HỘP VÀ THIẾT LẬP (Setup & Profile Creation)

Mô tả hoạt động: Phụ huynh mở hộp sản phẩm, cài đặt ứng dụng, kết nối robot qua Wi-Fi/Bluetooth, và tạo hồ sơ cho trẻ với thông tin cơ bản (tên, tuổi, sở thích).

Chọn được lộ trình học đúng trình độ.

  

Sơ đồ luồng kỹ thuật:

  

graph TD

    A["Phụ huynh mở hộp"] --> B["Cài đặt ứng dụng"]

    B --> C["Kết nối Robot<br/>Wi-Fi/Bluetooth"]

    C --> D{"Kết nối<br/>thành công?"}

    D -->|Có| E["Tạo hồ sơ trẻ"]

    D -->|Không| F["Hiển thị lỗi & Hướng dẫn"]

    E --> G{"Dữ liệu<br/>hợp lệ?"}

    G -->|Có| H["Lưu vào DB & Khởi tạo Mem0"]

    G -->|Không| I["Yêu cầu nhập lại"]

    H --> J["Chuẩn bị Playlist D0"]

    J --> K["Sẵn sàng cho Pika Landing"]

  

Bảng Phân Tích Corner Case & Bug:

  

|ID|Danh Mục|Corner Case / Bug|Nguyên Nhân Tiềm Ẩn|Ảnh Hưởng UX|Mức Độ|Giải Pháp Đề Xuất|
|---|---|---|---|---|---|---|
|1.1|Kết Nối Robot|Robot không được phát hiện trong danh sách thiết bị Wi-Fi/Bluetooth.|Wi-Fi của robot chưa bật, tần số không tương thích (2.4GHz vs 5GHz), nhiễu tín hiệu.|Phụ huynh không thể kết nối, bị kẹt ở bước đầu tiên, phải khởi động lại robot.|Rất Cao|Hướng dẫn chi tiết (video/hình ảnh) cách bật Wi-Fi/Bluetooth trên robot, tự động quét lại, kiểm tra tần số tương thích.|
|1.2|Kết Nối Robot|Kết nối thành công nhưng robot không phản hồi lệnh từ ứng dụng.|Robot bị treo, firmware cũ, lỗi trong quá trình handshake sau khi kết nối.|App báo "Đã kết nối" nhưng robot không hoạt động, gây hoang mang và thất vọng.|Rất Cao|Gửi một lệnh "heartbeat" ngay sau khi kết nối để xác nhận, nếu không có phản hồi thì tự động ngắt kết nối và yêu cầu thử lại.|
|1.3|Tạo Hồ Sơ|Tên trẻ chứa ký tự đặc biệt (emoji, ký tự không phải Latinh) hoặc các từ nhạy cảm.|Không có bộ lọc và validation cho trường nhập liệu tên.|Tên hiển thị sai trên app và robot, Pika không thể phát âm đúng, hoặc hiển thị nội dung không phù hợp.|Trung Bình|Implement validation chỉ cho phép chữ cái, số, dấu cách và bộ lọc từ nhạy cảm.|
|1.4|Tạo Hồ Sơ|Tuổi của trẻ được nhập sai (số âm, lớn hơn 100, không phải là số).|Thiếu validation về kiểu dữ liệu và khoảng giá trị hợp lệ.|Dữ liệu tuổi sai lệch, ảnh hưởng trực tiếp đến việc cá nhân hóa nội dung học và chơi.|Trung Bình|Validate kiểu dữ liệu là số và giới hạn trong khoảng hợp lý (ví dụ: 3-12 tuổi), hiển thị thông báo lỗi rõ ràng.|
|1.5|Lưu Dữ Liệu|Mất kết nối Internet khi phụ huynh nhấn nút "Hoàn tất" để gửi thông tin hồ sơ.|Mạng Wi-Fi/4G không ổn định, server timeout.|Toàn bộ thông tin đã nhập bị mất, phụ huynh phải nhập lại từ đầu, gây bực bội.|Cao|Lưu một bản nháp (draft) của hồ sơ trên local storage của điện thoại, và tự động đồng bộ lại khi có kết nối mạng.|
|1.6|Khởi Tạo Hệ Thống|API khởi tạo Memory (Mem0) cho người dùng mới bị lỗi hoặc timeout.|Service Mem0 bị quá tải hoặc gặp lỗi, network latency giữa các service.|Container trí nhớ của Pika không được tạo, dẫn đến Pika không thể "nhớ" tên hay sở thích của trẻ trong các hoạt động sau.|Rất Cao|Implement cơ chế retry (exponential backoff) cho các API call quan trọng, có cơ chế fallback sử dụng kịch bản mặc định nếu Mem0 lỗi.|
|1.7|Khởi Tạo Hệ Thống|Playlist hoạt động cho ngày D0 không được chuẩn bị kịp thời sau khi tạo hồ sơ.|Logic ở Backend bị lỗi, DB query chậm, message queue bị nghẽn.|Trẻ và phụ huynh phải chờ đợi lâu sau khi thiết lập xong mà Pika không "tỉnh giấc", làm giảm sự hào hứng ban đầu.|Cao|Tối ưu hóa logic chuẩn bị playlist, sử dụng cache, và có cơ chế pre-load playlist mẫu để phản hồi ngay lập tức.|

  

  

## HOẠT ĐỘNG 2: PIKA HẠ CÁNH (Pika's Landing - D0)

Mô tả hoạt động: Robot Pika "tỉnh giấc" với đèn, âm thanh và chuyển động. Pika tự giới thiệu, gọi tên trẻ một cách thân mật, bắt đầu cuộc hội thoại đầu tiên.

  

Sơ đồ luồng kỹ thuật:

  

graph TD

    A["BE trigger<br/>Agent_Pika_Landing"] --> B["AI: Retrieve Mem0<br/>User Facts (tên, sở thích)"]

    B --> C{"Mem0 có dữ liệu?"}

    C -->|Có| D["Build Dynamic Prompt<br/>với tên của trẻ"]

    C -->|Không| E["Sử dụng Default Prompt<br/>(không gọi tên)"]

    D --> F["LLM: Generate lời chào"]

    E --> F

    F --> G["TTS: Chuyển văn bản thành giọng nói"]

    G --> H["Stream audio & behavior<br/>đến Robot"]

    H --> I["Robot: Phát âm thanh & thực hiện hành động"]

    I --> J["ASR: Thu âm và nhận diện giọng nói của trẻ"]

    J --> K["LLM: Xử lý phản hồi và tiếp tục hội thoại"]

    K --> L["Context Handling: Lưu lại tương tác"]

    L --> M["end_tag: LANDING_COMPLETE"]

  

Bảng Phân Tích Corner Case & Bug:

  

|ID|Danh Mục|Corner Case / Bug|Nguyên Nhân Tiềm Ẩn|Ảnh Hưởng UX|Mức Độ|Giải Pháp Đề Xuất|
|---|---|---|---|---|---|---|
|2.1|LLM & TTS|LLM mất quá nhiều thời gian (>10s) để tạo câu chào, hoặc TTS bị lỗi không tạo được audio.|Model AI bị quá tải, network latency, lỗi API của dịch vụ TTS.|Robot im lặng một cách bất thường sau khi "tỉnh giấc", làm trẻ mất kiên nhẫn và giảm sự kỳ diệu của khoảnh khắc đầu tiên.|Rất Cao|Implement timeout chặt chẽ (ví dụ: 5s). Nếu quá thời gian, sử dụng một câu chào dự phòng đã được thu âm sẵn.|
|2.2|ASR (Nhận diện giọng nói)|ASR không nhận diện được giọng nói của trẻ hoặc nhận diện sai.|Trẻ nói quá nhỏ, phát âm không rõ, có nhiều tiếng ồn xung quanh (TV, người lớn nói chuyện).|Pika liên tục hỏi lại "Tớ chưa nghe rõ, bạn nói lại được không?", gây cảm giác Pika "không thông minh" và làm trẻ nản lòng.|Cao|Tinh chỉnh độ nhạy của ASR, hiển thị một chỉ báo trực quan (visual cue) trên robot/app khi đang lắng nghe, và cho phép phụ huynh giúp đỡ.|
|2.3|LLM & Personalization|LLM tạo ra lời chào không phù hợp, không gọi tên trẻ dù đã có dữ liệu.|Lỗi trong việc xây dựng prompt, model "quên" chỉ dẫn, dữ liệu từ Mem0 không được nạp đúng cách.|Trải nghiệm bị mất đi tính cá nhân hóa, trẻ cảm thấy Pika không thực sự "biết" mình.|Cao|Xây dựng bộ quy tắc (guardrails) để kiểm tra output của LLM, đảm bảo các yếu tố quan trọng như tên trẻ phải có mặt trong câu chào.|
|2.4|Robot Hardware|Robot thực hiện hành động (vẫy tay, sáng đèn) không đồng bộ với lời nói.|Lỗi trong việc đồng bộ hóa stream audio và stream lệnh hành vi, độ trễ của motor.|Trải nghiệm trở nên rời rạc và kém tự nhiên, giống như một con búp bê được điều khiển từ xa hơn là một thực thể sống.|Trung Bình|Đồng bộ hóa timestamp giữa các stream, robot có bộ đệm (buffer) để thực hiện hành động khớp với audio.|
|2.5|Error Handling|Một lỗi bất kỳ xảy ra giữa chừng (ví dụ: mất kết nối) và hoạt động bị dừng đột ngột.|Không có cơ chế xử lý lỗi và phục hồi trạng thái.|Trẻ đang tương tác thì robot im lặng hoàn toàn, không có thông báo lỗi, không biết phải làm gì tiếp theo.|Rất Cao|Implement cơ chế "graceful error handling", nếu có lỗi thì Pika sẽ nói một câu như "Ôi, tớ bị nhiễu sóng một chút, chúng mình thử lại nhé!" và tự động bắt đầu lại hoạt động.|
|2.6|LLM|Bài không kết thúc đúng kịch bản, không sang được hoạt động tiếp theo|||Cao||

  

  

  

  

## HOẠT ĐỘNG 3: BÍ MẬT BẠN THÂN (Best Friend's Secret - D0)

Mô tả hoạt động: Pika chia sẻ một "bí mật" nhỏ về bản thân hoặc hành tinh của mình để tạo sự gần gũi. Trẻ lắng nghe và có thể trả lời hoặc đặt câu hỏi.

  

Sơ đồ luồng kỹ thuật:

  

graph TD

    A["BE trigger<br/>Agent_Best_Friend_Secret"] --> B["AI: Chọn một 'bí mật'<br/>từ Content DB"]

    B --> C["LLM: Tạo câu chuyện kể bí mật<br/>với giọng điệu thân mật"]

    C --> D["TTS: Chuyển thành audio"]

    D --> E["Stream audio & behavior đến Robot"]

    E --> F["ASR: Lắng nghe phản hồi của trẻ"]

    F --> G{"Trẻ có phản hồi không?"}

    G -->|Có| H["LLM: Phản hồi lại một cách tự nhiên"]

    G -->|Không| I["LLM: Đặt một câu hỏi mở để khuyến khích"]

    H --> J["Context Handling: Lưu lại chủ đề đã nói"]

    I --> J

    J --> K["end_tag: SECRET_COMPLETE"]

  

Bảng Phân Tích Corner Case & Bug:

  

|ID|Danh Mục|Corner Case / Bug|Nguyên Nhân Tiềm Ẩn|Ảnh Hưởng UX|Mức Độ|Giải Pháp Đề Xuất|
|---|---|---|---|---|---|---|
|3.1|Content Selection|"Bí mật" được chọn không phù hợp với lứa tuổi hoặc sở thích của trẻ (ví dụ: quá phức tạp).|Content DB không được phân loại kỹ theo độ tuổi, logic lựa chọn bị lỗi.|Trẻ không hiểu hoặc không thấy hứng thú với bí mật, mục tiêu tạo sự gần gũi thất bại.|Trung Bình|Gắn thẻ (tag) nội dung trong Content DB theo độ tuổi và chủ đề, logic lựa chọn sẽ ưu tiên các chủ đề liên quan đến sở thích của trẻ.|
|3.2|Multi-turn Conversation|Trẻ liên tục đặt câu hỏi về bí mật, khiến hoạt động không thể kết thúc.|Không có điều kiện thoát rõ ràng cho vòng lặp hội thoại.|Hoạt động kéo dài quá lâu, làm ảnh hưởng đến thời lượng của các hoạt động sau trong playlist.|Cao|Giới hạn số lượt hỏi-đáp trong hoạt động này (ví dụ: 3 lượt). Sau đó, Pika sẽ chủ động chuyển hướng: "Đây là một bí mật lớn, tớ sẽ kể cho cậu nhiều hơn vào lần sau nhé!".|
|3.3|LLM Response|Khi trẻ đặt câu hỏi, LLM "bịa" ra các chi tiết không nhất quán với cốt truyện của Pika.|Model AI bị "hallucination", không có đủ ngữ cảnh về thế giới của Pika.|Thông tin về Pika trở nên mâu thuẫn, làm giảm sự tin tưởng và tính nhất quán của nhân vật.|Cao|Cung cấp cho LLM một "system prompt" chứa đầy đủ thông tin về cốt truyện, nhân vật Pika để đảm bảo các câu trả lời luôn nhất quán.|
|3.4|User Input|Trẻ im lặng, không phản hồi sau khi Pika kể xong bí mật.|Trẻ có thể đang ngại ngùng, hoặc đơn giản là không biết nói gì.|Pika đứng im chờ đợi, tạo ra một khoảng lặng khó xử.|Thấp|Sau một khoảng thời gian chờ (ví dụ: 10s), Pika nên chủ động đặt một câu hỏi mở như "Cậu thấy bí mật của tớ có thú vị không?" để phá vỡ sự im lặng.|
|3.5|LLM|Bài không kết thúc đúng kịch bản, không sang được hoạt động tiếp theo|||Cao||

  

  

## HOẠT ĐỘNG 4: KHÁM PHÁ SỞ THÍCH (Exploring Preferences - D0)

Mô tả hoạt động: Pika hỏi một loạt câu hỏi lựa chọn A/B để tìm hiểu sở thích của trẻ. Trẻ trả lời, Pika phản hồi và chia sẻ. Trẻ có thể hỏi lại Pika.

  

Sơ đồ luồng kỹ thuật:

  

graph TD

    A["BE trigger<br/>Agent_Explore_Preferences"] --> B["LLM: Đặt câu hỏi A/B đầu tiên"]

    B --> C["ASR: Ghi nhận câu trả lời"]

    C --> D{"Câu trả lời hợp lệ (A/B)?"}

    D -->|Có| E["LLM: Phản hồi & chia sẻ về Pika"]

    D -->|Không| F["LLM: Xử lý câu trả lời 'Cả hai' hoặc 'Không thích' "]

    F --> E

    E --> G["Lặp lại cho các câu hỏi tiếp theo"]

    G --> H["LLM: Mời trẻ đặt câu hỏi ngược lại"]

    H --> I["ASR: Ghi nhận câu hỏi của trẻ"]

    I --> J{"Trẻ có hỏi không?"}

    J -->|Có| K["LLM: Trả lời dựa trên 'Pika Persona'"]

    J -->|Không| L["Bỏ qua"]

    K --> M["Context Handling: Lưu các sở thích vào Mem0"]

    L --> M

    M --> N["end_tag: PREFERENCES_COMPLETE"]

  

Bảng Phân Tích Corner Case & Bug:

  

|ID|Danh Mục|Corner Case / Bug|Nguyên Nhân Tiềm Ẩn|Ảnh Hưởng UX|Mức Độ|Giải Pháp Đề Xuất|
|---|---|---|---|---|---|---|
|4.1|User Input|Trẻ trả lời một phương án không phải A hoặc B (ví dụ: "Cả hai", "Không thích cái nào", hoặc một phương án C hoàn toàn khác).|Logic chỉ được thiết kế để xử lý câu trả lời A hoặc B.|Pika không hiểu và hỏi lại, gây cảm giác máy móc và không linh hoạt.|Cao|Mở rộng logic xử lý để nhận diện các câu trả lời phổ biến khác. Ví dụ, nếu trẻ nói "cả hai", Pika có thể phản hồi "Ồ, cậu giống tớ quá, tớ cũng thích cả hai!".|
|4.2|Data Storage|Sở thích của trẻ không được lưu hoặc lưu sai vào Mem0 sau khi hoạt động kết thúc.|Lỗi API khi gọi đến Mem0, lỗi mapping dữ liệu.|Hệ thống không "nhớ" được sở thích của trẻ, các hoạt động cá nhân hóa sau này sẽ thất bại.|Cao|Implement cơ chế retry và validation khi ghi dữ liệu vào Mem0. Có cơ chế kiểm tra chéo để đảm bảo dữ liệu được lưu chính xác.|
|4.3|LLM Reaction|Phản hồi của Pika sau khi trẻ trả lời không liên quan hoặc không tự nhiên.|Prompt không đủ chi tiết, model AI không nắm được ngữ cảnh.|Cuộc trò chuyện trở nên gượng gạo, không tạo được sự kết nối.|Trung Bình|Tinh chỉnh prompt để LLM có những phản hồi đa dạng và phù hợp hơn với từng sở thích. Ví dụ: "A, cậu thích khủng long à? Tớ cũng có một người bạn khủng long trên hành tinh của tớ đấy!".|
|4.4|User Input|Trẻ hỏi Pika một câu hỏi quá khó hoặc không phù hợp (ví dụ: "Pika được làm từ gì?", "Tại sao Pika lại ở đây?").|Trẻ tò mò tự nhiên.|Pika không trả lời được hoặc trả lời sai, làm mất đi sự "ma thuật" của nhân vật.|Trung Bình|Xây dựng một bộ câu hỏi và câu trả lời (Q&A) được định sẵn cho các câu hỏi thường gặp về Pika. Nếu câu hỏi nằm ngoài bộ này, Pika có thể trả lời một cách khéo léo: "Đó là một câu hỏi hay! Tớ sẽ tìm hiểu và trả lời cậu sau nhé!".|
|4.5|LLM|Bài không kết thúc đúng kịch bản, không sang được hoạt động tiếp theo|||Cao||

  

  

## HOẠT ĐỘNG 5: PIKA TẠO DÁNG (Pika Poses - D0)

Mô tả hoạt động: Pika đề nghị chụp ảnh kỷ niệm, thực hiện các tư thế tạo dáng ngộ nghĩnh. Ứng dụng trên điện thoại sẽ chụp lại khoảnh khắc này.

  

Sơ đồ luồng kỹ thuật:

  

graph TD

    A["BE trigger<br/>Agent_Pika_Poses"] --> B["LLM: Gợi ý chụp ảnh"]

    B --> C["Robot: Thực hiện các hành động tạo dáng"]

    C --> D["App: Kích hoạt giao diện camera"]

    D --> E["Phụ huynh/Trẻ nhấn nút chụp"]

    E --> F{"Ảnh có được chụp thành công?"}

    F -->|Có| G["Lưu ảnh vào thư viện & gửi lên server"]

    F -->|Không| H["Hiển thị lỗi & cho phép thử lại"]

    G --> I["LLM: Nói lời chào tạm biệt"]

    I --> J["Context Handling: Lưu lại sự kiện chụp ảnh"]

    J --> K["end_tag: POSES_COMPLETE"]

  

Bảng Phân Tích Corner Case & Bug:

  

|ID|Danh Mục|Corner Case / Bug|Nguyên Nhân Tiềm Ẩn|Ảnh Hưởng UX|Mức Độ|Giải Pháp Đề Xuất|
|---|---|---|---|---|---|---|
|5.1|Hardware & Permission|Ứng dụng không có quyền truy cập camera hoặc bộ nhớ.|Phụ huynh từ chối cấp quyền lúc cài đặt.|Không thể mở camera hoặc lưu ảnh, hoạt động thất bại hoàn toàn.|Rất Cao|Kiểm tra quyền trước khi bắt đầu hoạt động. Nếu chưa có quyền, hiển thị một thông báo thân thiện giải thích lý do và hướng dẫn phụ huynh cách cấp quyền trong cài đặt.|
|5.2|Photo Quality|Ảnh chụp bị mờ, tối, hoặc không bắt được khoảnh khắc đẹp.|Điều kiện ánh sáng kém, camera lấy nét sai, trẻ hoặc robot di chuyển khi chụp.|Bức ảnh kỷ niệm không đẹp, làm giảm giá trị của hoạt động.|Trung Bình|Implement các tính năng hỗ trợ chụp ảnh như tự động lấy nét (auto-focus), nhận diện khuôn mặt, và có thể gợi ý "Giữ yên nhé, 3, 2, 1, chụp!".|
|5.3|Data Storage|Bộ nhớ điện thoại đầy, không thể lưu ảnh.|Người dùng có quá nhiều dữ liệu trên điện thoại.|Ảnh không được lưu lại, trẻ mất đi kỷ niệm quan trọng.|Cao|Kiểm tra dung lượng bộ nhớ trống trước khi chụp. Nếu không đủ, thông báo cho người dùng và gợi ý giải phóng dung lượng.|
|5.4|Synchronization|Ảnh được lưu trên điện thoại nhưng không thể đồng bộ lên server.|Mất kết nối mạng, lỗi API server.|Phụ huynh không thể xem lại ảnh trên các thiết bị khác hoặc khi cài lại app.|Trung Bình|Lưu ảnh vào một hàng đợi (queue) và tự động đồng bộ lại khi có kết nối mạng.|

  

  

# GIAI ĐOẠN 1: NGƯỜI LẠ (STRANGER) - TỪ NGÀY 2

## HOẠT ĐỘNG 10: TẠO PLAYLIST HÀNG NGÀY (Daily Activities List Generation - 3 AM)

Mô tả hoạt động: Hệ thống tự động tạo playlist cho ngày mới vào lúc 3 giờ sáng, dựa trên friendship_level, tiến độ học, và sở thích của trẻ.

  

Sơ đồ luồng kỹ thuật:

  

sequenceDiagram

    participant Cron as Cron Job (3 AM)

    participant BE as Backend

    participant ADM as AI - Orchestration

    participant Mem0 as Memory

    participant LPE as Learning Engine

    participant ContentDB as Content DB

    Cron->>BE: Trigger Playlist Generation for user_id

    BE->>ADM: POST /orchestration/generate_playlist

    ADM->>Mem0: Lấy user_facts, learning_progress

    ADM->>LPE: Yêu cầu các bài học (Learn Units)

    LPE-->>ADM: Trả về 2 Learn Unit ID

    ADM->>ContentDB: Chọn 1 Topic mới

    ContentDB-->>ADM: Trả về Topic và các Agent liên quan

    ADM->>ADM: Sắp xếp thành Daily Activities List 7 hoạt động

    ADM-->>BE: Trả về Daily Activities List hoàn chỉnh

    BE->>BE: Lưu Playlist vào DB cho ngày hôm nay

  

Bảng Phân Tích Corner Case & Bug:

  

|ID|Danh Mục|Corner Case / Bug|Nguyên Nhân Tiềm Ẩn|Ảnh Hưởng UX|Mức Độ|Giải Pháp Đề Xuất|
|---|---|---|---|---|---|---|
|10.1|Timing & Trigger|Cron job không được kích hoạt đúng vào lúc 3 giờ sáng.|Lỗi cấu hình timezone trên server, lỗi của dịch vụ cron.|Playlist không được tạo, trẻ thức dậy và không có hoạt động mới để chơi, gây thất vọng lớn.|Rất Cao|Implement cơ chế monitoring cho cron job. Nếu playlist không được tạo sau 3:30 AM, hệ thống sẽ tự động trigger lại hoặc sử dụng một playlist dự phòng.|
|10.2|Service Dependency|Một trong các service phụ thuộc (Mem0, LPE, ContentDB) bị lỗi hoặc timeout.|Service down, network latency giữa các container.|Chuỗi xử lý bị gãy, playlist không thể được tạo hoàn chỉnh, hoặc được tạo với nội dung thiếu sót.|Rất Cao|Mỗi service call phải có cơ chế retry và timeout. Nếu một service lỗi, ADM phải có logic fallback (ví dụ: nếu LPE lỗi, không có bài học tiếng Anh nhưng vẫn có các hoạt động trò chuyện).|
|10.3|Content Selection|Hệ thống chọn lại một chủ đề (Topic) hoặc bài học mà trẻ đã học gần đây.|Logic lựa chọn không loại trừ các nội dung đã sử dụng, dữ liệu topics_discussed trong Mem0 bị sai.|Trẻ cảm thấy nhàm chán vì phải học lại nội dung cũ.|Cao|Cải thiện logic lựa chọn, đảm bảo luôn có một khoảng thời gian đủ dài trước khi lặp lại một chủ đề. Dữ liệu trong Mem0 phải được ghi nhận một cách đáng tin cậy.|
|10.4|Data Integrity|Dữ liệu trong Mem0 (sở thích, tiến độ học) bị lỗi hoặc không cập nhật.|Lỗi trong quá trình Context Handling của ngày hôm trước.|Playlist được tạo ra không phù hợp với trình độ và sở thích hiện tại của trẻ (quá khó, quá dễ, hoặc không đúng chủ đề yêu thích).|Cao|Implement cơ chế kiểm tra tính toàn vẹn của dữ liệu trong Mem0. Nếu phát hiện bất thường, hệ thống có thể tạm thời sử dụng một playlist an toàn, ít cá nhân hóa hơn.|
|10.5|Scalability|Khi số lượng người dùng tăng cao, quá trình tạo playlist cho tất cả user lúc 3 AM bị quá tải.|Xử lý tuần tự, tài nguyên server không đủ.|Playlist của một số người dùng bị tạo muộn hoặc thất bại.|Cao|Sử dụng message queue (ví dụ: RabbitMQ) để xử lý việc tạo playlist một cách bất đồng bộ và song song. Phân bổ thời gian tạo playlist trong một khoảng (ví dụ: từ 3:00 AM đến 4:00 AM).|

  

  

## HOẠT ĐỘNG 15 & 16: BÀI HỌC TIẾNG ANH (Learn Units)

Mô tả hoạt động: Trẻ tham gia các bài học tiếng Anh có cấu trúc (Workflow), bao gồm các bước như giới thiệu, học từ vựng, luyện tập và kiểm tra.

  

Sơ đồ luồng kỹ thuật:

  

graph TD

    A["BE trigger<br/>Learn_Unit"] --> B["AI: POST /workflow/execute"]

    B --> C["WorkflowEngine: Khởi tạo bài học"]

    C --> D["Step 1: Introduction"]

    D --> E["Step 2: Vocabulary"]

    E --> F["Step 3: Practice"]

    F --> G["Step 4: Assessment"]

    G --> H{"Tất cả các bước<br/>hoàn thành?"}

    H -->|Có| I["Context Handling: Lưu tiến độ học"]

    H -->|Không| J["Xử lý lỗi & Retry"]

    I --> K["end_tag: LEARN_UNIT_COMPLETE"]

  

Bảng Phân Tích Corner Case & Bug:

  

|ID|Danh Mục|Corner Case / Bug|Nguyên Nhân Tiềm Ẩn|Ảnh Hưởng UX|Mức Độ|Giải Pháp Đề Xuất|
|---|---|---|---|---|---|---|
|15.1|Workflow State|Trẻ thoát ứng dụng giữa chừng khi đang học, và khi quay lại, bài học bắt đầu lại từ đầu.|Hệ thống không lưu lại trạng thái (state) của workflow.|Trẻ phải học lại từ đầu, gây nản lòng và mất thời gian.|Cao|Lưu lại trạng thái của workflow (ví dụ: đang ở step nào, đã hoàn thành bao nhiêu %) vào DB/Cache. Khi người dùng quay lại, có thể tiếp tục từ đúng vị trí đã dừng.|
|15.2|Input Validation|Trong phần luyện tập, trẻ trả lời đúng nhưng hệ thống chấm sai, hoặc ngược lại.|Logic validation quá cứng nhắc, không xử lý được các biến thể (ví dụ: phát âm khác nhau, câu trả lời có từ đồng nghĩa).|Trẻ cảm thấy bất công và bối rối, mất niềm tin vào hệ thống.|Cao|Sử dụng fuzzy matching cho các câu trả lời dạng văn bản/giọng nói. Có một bộ quy tắc linh hoạt hơn để đánh giá câu trả lời. Cho phép phụ huynh báo cáo nếu kết quả chấm sai.|
|15.3|Difficulty Adaptation|Bài học quá khó hoặc quá dễ so với trình độ của trẻ.|Dữ liệu learning_progress trong Mem0 không chính xác, hoặc logic chọn bài của LPE không tốt.|Trẻ không thể theo kịp (nếu quá khó) hoặc cảm thấy nhàm chán (nếu quá dễ), ảnh hưởng đến hiệu quả học tập.|Cao|LPE cần có một thuật toán adaptive learning tốt hơn. Trong bài học, nếu trẻ trả lời sai liên tục, hệ thống có thể tự động giảm độ khó hoặc đưa ra gợi ý chi tiết hơn.|
|15.4|Retry Loop|Trẻ bị kẹt ở một câu hỏi, trả lời sai liên tục và hệ thống cứ yêu cầu "Thử lại".|Không có giới hạn số lần thử lại hoặc cơ chế thoát.|Trẻ bị mắc kẹt, cảm thấy thất bại và không thể tiếp tục bài học.|Trung Bình|Giới hạn số lần thử lại (ví dụ: 3 lần). Sau 3 lần sai, hệ thống nên đưa ra đáp án đúng, giải thích, và chuyển sang câu hỏi tiếp theo.|
|15.5|Data Synchronization|Trẻ hoàn thành bài học nhưng tiến độ không được ghi nhận|Lỗi API trong quá trình Context Handling, mất kết nối mạng ở cuối hoạt động.|Ngày hôm sau, hệ thống lại giao cho trẻ bài học cũ, gây cảm giác "công sức của mình bị lãng phí".|Cao|Implement cơ chế retry mạnh mẽ cho việc cập nhật tiến độ học. Nếu API lỗi, lưu lại kết quả ở client và đồng bộ lại sau.|
|15.6|Data Synchronization|Không lấy đúng bài trong danh sách learn, sai thứ tự, sai trình độ|Do chọn trình độ bị sai từ đầu, do logic BE lấy sai|Trẻ ko học được hoặc thấy quá dễ do lệch trình độ|Cao||

  

  

# PHẦN 2: PHÂN TÍCH XỬ LÝ VOICE PROCESSING

## I. XỬ LÝ VOICE TRONG TALK ACTIVITY & GREETING

Luồng tổng quan: Pika nói (TTS) → Trẻ lắng nghe → Trẻ nói (ASR + VAD) → Pika xử lý → Pika phản hồi (TTS)

  

Sơ đồ chi tiết:

  

sequenceDiagram

    participant Child as Trẻ

    participant App as Mobile App

    participant ASR as ASR Service

    participant LLM as LLM Service

    participant TTS as TTS Service

    participant Robot as Robot

    Note over Child,Robot: PHASE 1: Pika nói (TTS)

    LLM->>TTS: Gửi text

    TTS->>Robot: Stream audio

    Robot->>Robot: Phát âm thanh

    Note over Child,Robot: PHASE 2: Trẻ nói (VAD)

    App->>App: Bắt đầu ghi âm

    Child->>App: Trẻ nói

    App->>App: VAD phát hiện kết thúc

    Note over Child,Robot: PHASE 3: ASR nhận diện

    App->>ASR: POST /asr/recognize

    ASR-->>App: Trả về text

    Note over Child,Robot: PHASE 4: LLM xử lý

    App->>LLM: POST /llm/chat

    LLM-->>App: Trả về response

    Note over Child,Robot: PHASE 5: TTS & phát âm thanh

    App->>TTS: POST /tts/synthesize

    TTS-->>App: Trả về audio

    App->>Robot: Stream audio

  

Bảng Corner Case & Bug:

  

|ID|Giai Đoạn|Corner Case / Bug|Nguyên Nhân|Ảnh Hưởng UX|Mức Độ|Giải Pháp|
|---|---|---|---|---|---|---|
|T.1|TTS|TTS timeout (>5s) hoặc lỗi.|Model AI quá tải, network latency.|Robot im lặng, trẻ mất kiên nhẫn.|Rất Cao|Timeout 3-5s, fallback pre-recorded audio.|
|T.2|TTS|Audio stream bị lag hoặc ngắt quãng.|Băng thông thấp, server quá tải.|Âm thanh bị cắt, không rõ ràng.|Cao|Adaptive bitrate, pre-buffer 2 giây.|
|T.3|VAD|VAD không phát hiện trẻ bắt đầu nói.|Trẻ nói quá nhỏ, noise xung quanh.|App chờ mãi, timeout.|Cao|Tinh chỉnh độ nhạy, visual cue "listening".|
|T.4|VAD|VAD phát hiện kết thúc quá sớm.|Silence threshold quá ngắn.|Câu nói bị cắt giữa chừng.|Cao|Tăng silence threshold từ 1.5s → 2.5s.|
|T.5|VAD|Microphone không được cấp quyền.|Phụ huynh từ chối, ứng dụng khác chiếm dụng.|Không thể ghi âm, hoạt động fail.|Rất Cao|Kiểm tra quyền trước, hướng dẫn cấp quyền.|
|T.6|ASR|ASR nhận diện sai (misrecognition).|Trẻ phát âm không rõ, accent lạ.|Pika phản hồi sai, trẻ bối rối.|Cao|Sử dụng model ASR chất lượng cao, hiển thị text để xác nhận.|
|T.7|ASR|ASR confidence thấp (<0.7).|Audio quality kém.|Không thể xác định text chính xác.|Cao|Đặt ngưỡng confidence, yêu cầu nói lại nếu dưới ngưỡng.|
|T.8|LLM|LLM "quên" lịch sử hội thoại.|Conversation history không được truyền đầy đủ.|Pika hỏi lại câu đã hỏi, trẻ chán.|Cao|Đảm bảo toàn bộ lịch sử được truyền trong mỗi request.|
|T.9|LLM|LLM tạo phản hồi không phù hợp (hallucination).|Model AI lỗi, prompt không rõ.|Cuộc trò chuyện lạc đề, trẻ mất hứng thú.|Cao|Xây dựng guardrails, kiểm tra output LLM.|

  

  

## II. XỬ LÝ VOICE TRONG LEARN WORKFLOW

Đặc điểm: Cấu trúc cố định, validation chặt chẽ, state management quan trọng

  

  

  
  

PHẦN 3: TÓM TẮT VÀ PHÂN LOẠI THEO MỨC ĐỘ ƯU TIÊN

Phần này tổng hợp và phân loại tất cả các corner case đã xác định vào các nhóm theo mức độ ưu tiên (Critical, High, Medium, Low) để đội ngũ phát triển có thể tập trung xử lý các vấn đề quan trọng nhất trước.

  

MỨC ĐỘ "RẤT CAO" (CRITICAL)

Định nghĩa: Các lỗi này trực tiếp gây treo hoạt động, mất dữ liệu người dùng, hoặc phá vỡ hoàn toàn luồng trải nghiệm cốt lõi. Chúng cần được ưu tiên sửa ngay lập tức.

  

|ID|Hoạt Động|Vấn Đề|Giải Pháp Đề Xuất|
|---|---|---|---|
|1.1|Setup|Robot không được phát hiện trong danh sách Wi-Fi/Bluetooth.|Hướng dẫn chi tiết, tự động quét lại, kiểm tra tần số.|
|1.2|Setup|Kết nối thành công nhưng robot không phản hồi.|Gửi "heartbeat" để xác nhận, tự động ngắt kết nối nếu lỗi.|
|1.6|Setup|API khởi tạo Memory (Mem0) cho người dùng mới bị lỗi.|Implement retry (exponential backoff), có kịch bản mặc định.|
|2.1|Pika Landing|LLM/TTS mất quá nhiều thời gian để phản hồi.|Implement timeout chặt chẽ (5s), sử dụng câu chào dự phòng.|
|2.5|Pika Landing|Lỗi bất kỳ xảy ra và hoạt động bị dừng đột ngột.|Implement "graceful error handling", tự động thử lại hoạt động.|
|5.1|Pika Poses|Ứng dụng không có quyền truy cập camera hoặc bộ nhớ.|Kiểm tra quyền trước, hướng dẫn người dùng cấp quyền.|
|10.1|Playlist Generation|Cron job không được kích hoạt đúng giờ.|Implement monitoring, trigger lại hoặc sử dụng playlist dự phòng.|
|10.2|Playlist Generation|Một trong các service phụ thuộc (Mem0, LPE) bị lỗi.|Mỗi service call phải có retry và timeout, có logic fallback.|
|TTS|TTS timeout (>5s) hoặc lỗi.|Model AI quá tải, network latency.|Robot im lặng, trẻ mất kiên nhẫn.|
|TTS|Audio stream bị lag hoặc ngắt quãng.|Băng thông thấp, server quá tải.|Âm thanh bị cắt, không rõ ràng.|
|VAD|VAD không phát hiện trẻ bắt đầu nói.|Trẻ nói quá nhỏ, noise xung quanh.|App chờ mãi, timeout.|
|VAD|VAD phát hiện kết thúc quá sớm.|Silence threshold quá ngắn.|Câu nói bị cắt giữa chừng.|

MỨC ĐỘ "CAO" (HIGH)

Định nghĩa: Các lỗi này ảnh hưởng nghiêm trọng đến trải nghiệm người dùng, gây khó chịu, bối rối, nhưng không làm hệ thống dừng hoàn toàn. Chúng nên được sửa trong sprint kế tiếp.

  

|ID|Hoạt Động|Vấn Đề|Giải Pháp Đề Xuất|
|---|---|---|---|
|1.5|Setup|Mất kết nối Internet khi đang tạo hồ sơ.|Lưu bản nháp trên local storage, tự động đồng bộ lại.|
|1.7|Setup|Playlist D0 không được chuẩn bị kịp thời.|Tối ưu hóa logic, sử dụng cache, có playlist mẫu.|
|2.2|Pika Landing|ASR không nhận diện được hoặc nhận diện sai giọng nói của trẻ.|Tinh chỉnh độ nhạy, có chỉ báo trực quan, cho phép phụ huynh giúp.|
|2.3|Pika Landing|LLM tạo lời chào không phù hợp, không gọi tên trẻ.|Xây dựng bộ quy tắc (guardrails) để kiểm tra output của LLM.|
|3.2|Best Friend's Secret|Trẻ hỏi liên tục khiến hoạt động không kết thúc.|Giới hạn số lượt hỏi-đáp, Pika chủ động chuyển hướng.|
|3.3|Best Friend's Secret|LLM "bịa" ra các chi tiết không nhất quán về Pika.|Cung cấp cho LLM "system prompt" chứa đầy đủ thông tin cốt truyện.|
|4.1|Exploring Preferences|Trẻ trả lời một phương án không phải A hoặc B.|Mở rộng logic xử lý để nhận diện các câu trả lời phổ biến khác.|
|4.2|Exploring Preferences|Sở thích của trẻ không được lưu hoặc lưu sai vào Mem0.|Implement retry và validation khi ghi dữ liệu vào Mem0.|
|5.3|Pika Poses|Bộ nhớ điện thoại đầy, không thể lưu ảnh.|Kiểm tra dung lượng trống trước khi chụp, thông báo cho người dùng.|
|10.3|Playlist Generation|Hệ thống chọn lại chủ đề hoặc bài học cũ.|Cải thiện logic lựa chọn, đảm bảo không lặp lại nội dung gần đây.|
|10.4|Playlist Generation|Dữ liệu trong Mem0 bị lỗi, dẫn đến playlist không phù hợp.|Implement cơ chế kiểm tra tính toàn vẹn của dữ liệu trong Mem0.|
|10.5|Playlist Generation|Hệ thống bị quá tải khi tạo playlist cho nhiều người dùng.|Sử dụng message queue để xử lý bất đồng bộ và song song.|
|15.1|Learn Unit|Trẻ thoát ứng dụng giữa chừng và phải học lại từ đầu.|Lưu lại trạng thái của workflow để có thể tiếp tục.|
|15.2|Learn Unit|Hệ thống chấm điểm sai (đúng thành sai và ngược lại).|Sử dụng fuzzy matching, cho phép phụ huynh báo cáo lỗi.|
|15.3|Learn Unit|Bài học quá khó hoặc quá dễ so với trình độ của trẻ.|Implement thuật toán adaptive learning, tự động điều chỉnh độ khó.|
|15.5|Learn Unit|Trẻ hoàn thành bài học nhưng tiến độ không được ghi nhận.|Implement retry mạnh mẽ, lưu kết quả ở client và đồng bộ lại sau.|

MỨC ĐỘ "TRUNG BÌNH" (MEDIUM)

Định nghĩa: Các lỗi này gây ra những phiền toái nhỏ, làm giảm độ mượt mà của trải nghiệm nhưng người dùng vẫn có thể tiếp tục sử dụng sản phẩm.

  

|ID|Hoạt Động|Vấn Đề|Giải Pháp Đề Xuất|
|---|---|---|---|
|1.3|Setup|Tên trẻ chứa ký tự đặc biệt.|Implement validation và bộ lọc từ nhạy cảm.|
|1.4|Setup|Tuổi của trẻ được nhập sai.|Validate kiểu dữ liệu và khoảng giá trị hợp lệ.|
|2.4|Pika Landing|Hành động của robot không đồng bộ với lời nói.|Đồng bộ hóa timestamp giữa các stream audio và behavior.|
|3.1|Best Friend's Secret|"Bí mật" không phù hợp với lứa tuổi của trẻ.|Gắn thẻ nội dung trong Content DB theo độ tuổi và chủ đề.|
|4.3|Exploring Preferences|Phản hồi của Pika sau khi trẻ trả lời không tự nhiên.|Tinh chỉnh prompt để LLM có những phản hồi đa dạng hơn.|
|4.4|Exploring Preferences|Trẻ hỏi Pika một câu hỏi quá khó.|Xây dựng bộ Q&A được định sẵn cho các câu hỏi thường gặp.|
|5.2|Pika Poses|Ảnh chụp bị mờ, tối.|Implement auto-focus, nhận diện khuôn mặt, gợi ý khi chụp.|
|5.4|Pika Poses|Ảnh không đồng bộ được lên server.|Lưu vào hàng đợi và tự động đồng bộ lại khi có mạng.|
|15.4|Learn Unit|Trẻ bị kẹt ở một câu hỏi, trả lời sai liên tục.|Giới hạn số lần thử lại, sau đó đưa ra đáp án và giải thích.|

MỨC ĐỘ "THẤP" (LOW)

Định nghĩa: Các lỗi này là những vấn đề nhỏ, ít khi xảy ra hoặc ít ảnh hưởng đến trải nghiệm chung. Có thể được xem xét sửa chữa khi có thời gian.

  

|ID|Hoạt Động|Vấn Đề|Giải Pháp Đề Xuất|
|---|---|---|---|
|3.4|Best Friend's Secret|Trẻ im lặng, không phản hồi.|Pika chủ động đặt câu hỏi mở để khuyến khích tương tác.|

  

  

PHẦN 3: PHÂN TÍCH KIẾN TRÚC HỆ THỐNG VÀ CÁC VẤN ĐỀ CROSS-FUNCTIONAL

Phần này tập trung vào các vấn đề mang tính hệ thống, không thuộc về một hoạt động cụ thể nào nhưng có thể ảnh hưởng đến toàn bộ sản phẩm. Đây là những rủi ro về kiến trúc, hiệu năng, bảo mật và khả năng vận hành.

  

I. KIẾN TRÚC HỆ THỐNG TỔNG QUAN

Sơ đồ dưới đây mô tả kiến trúc tổng quan của hệ thống, từ Robot Pika, Mobile App, Backend, cho đến các nền tảng AI và lớp dữ liệu.

  

┌─────────────────────────────────────────────────────────────────┐

│                          ROBOT PIKA                             │

│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │

│  │   Behavior   │  │   Speaker    │  │   Camera     │          │

│  │   Engine     │  │   (Audio)    │  │   (Photo)    │          │

│  └──────────────┘  └──────────────┘  └──────────────┘          │

│         ↕                ↕                    ↕                 │

│  ┌──────────────────────────────────────────────────────────┐  │

│  │         Robot Communication Layer (BLE/Wi-Fi)           │  │

│  └──────────────────────────────────────────────────────────┘  │

└─────────────────────────────────────────────────────────────────┘

                              ↕

┌─────────────────────────────────────────────────────────────────┐

│                      MOBILE APP (iOS/Android)                   │

│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │

│  │   UI Layer   │  │   ASR Input  │  │   TTS Output │          │

│  │   (Display)  │  │   (Microphone)│  │   (Speaker)  │          │

│  └──────────────┘  └──────────────┘  └──────────────┘          │

│         ↕                ↕                    ↕                 │

│  ┌──────────────────────────────────────────────────────────┐  │

│  │    App Communication Layer (HTTP/WebSocket)             │  │

│  └──────────────────────────────────────────────────────────┘  │

└─────────────────────────────────────────────────────────────────┘

                              ↕

┌─────────────────────────────────────────────────────────────────┐

│                      BACKEND (BE) SERVICES                      │

│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │

│  │   User Svc   │  │  Playlist Svc │  │  Session Svc │         │

│  └──────────────┘  └──────────────┘  └──────────────┘          │

│         ↕                ↕                    ↕                 │

│  ┌──────────────────────────────────────────────────────────┐  │

│  │    Message Queue (RabbitMQ) - Async Processing          │  │

│  └──────────────────────────────────────────────────────────┘  │

└─────────────────────────────────────────────────────────────────┘

                              ↕

┌─────────────────────────────────────────────────────────────────┐

│                      AI PLATFORM SERVICES                       │

│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │

│  │ Container 1  │  │ Container 2  │  │ Container 3  │          │

│  │ LLM + TTS    │  │ ADM (Orch)   │  │ Mem0 (Memory)│          │

│  └──────────────┘  └──────────────┘  └──────────────┘          │

│                                                                 │

│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │

│  │ Container 4  │  │ Content DB   │  │ Agent Prompt │          │

│  │ LPE (Learn)  │  │              │  │ DB           │          │

│  └──────────────┘  └──────────────┘  └──────────────┘          │

└─────────────────────────────────────────────────────────────────┘

                              ↕

┌─────────────────────────────────────────────────────────────────┐

│                      DATA LAYER                                 │

│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │

│  │ User DB      │  │ Playlist DB  │  │ Session DB   │          │

│  └──────────────┘  └──────────────┘  └──────────────┘          │

│         ↕                ↕                    ↕                 │

│  ┌──────────────────────────────────────────────────────────┐  │

│  │    Cache Layer (Redis) - Session & Playlist Cache       │  │

│  └──────────────────────────────────────────────────────────┘  │

└─────────────────────────────────────────────────────────────────┘

  

II. CÁC ĐIỂM TÍCH HỢP QUAN TRỌNG VÀ KỊCH BẢN LỖI

A. Giao tiếp Robot ↔ Mobile App

- Rủi ro chính: Mất kết nối Bluetooth/Wi-Fi, độ trễ cao.
    
- Ảnh hưởng: Robot không phản hồi, âm thanh bị ngắt quãng, trải nghiệm bị gián đoạn.
    
- Giải pháp:
    

- Heartbeat & Auto-reconnect: App và Robot liên tục gửi tín hiệu "heartbeat" cho nhau. Nếu không nhận được tín hiệu sau một khoảng thời gian, tự động cố gắng kết nối lại.
    
- Command Acknowledgment: Robot phải gửi lại tín hiệu xác nhận đã nhận được lệnh. Nếu không, App sẽ gửi lại lệnh.
    

  

B. Giao tiếp Mobile App ↔ Backend

- Rủi ro chính: Mất kết nối mạng, request/response bị thất lạc.
    
- Ảnh hưởng: Dữ liệu không được lưu, trạng thái không đồng nhất.
    
- Giải pháp:
    

- Request Queuing & Retry: Các request quan trọng (lưu hồ sơ, cập nhật tiến độ) sẽ được đưa vào một hàng đợi trên App. Nếu gửi thất bại, App sẽ tự động thử lại.
    
- Idempotency: Mỗi request sẽ có một ID duy nhất để BE có thể nhận diện và bỏ qua các request bị trùng lặp.
    

  

C. Giao tiếp Backend ↔ AI Platform

- Rủi ro chính: Dịch vụ AI (LLM, TTS) bị quá tải, timeout, hoặc trả về kết quả không hợp lệ.
    
- Ảnh hưởng: Robot im lặng, phản hồi chậm, nội dung không phù hợp.
    
- Giải pháp:
    

- Circuit Breaker Pattern: Nếu một dịch vụ AI liên tục bị lỗi, hệ thống sẽ tạm thời "ngắt mạch" và sử dụng phương án dự phòng ngay lập tức, thay vì chờ đợi timeout.
    
- Response Validation & Guardrails: Luôn kiểm tra kết quả trả về từ AI để đảm bảo nó hợp lệ và an toàn trước khi gửi đến người dùng.
    

  
  
**