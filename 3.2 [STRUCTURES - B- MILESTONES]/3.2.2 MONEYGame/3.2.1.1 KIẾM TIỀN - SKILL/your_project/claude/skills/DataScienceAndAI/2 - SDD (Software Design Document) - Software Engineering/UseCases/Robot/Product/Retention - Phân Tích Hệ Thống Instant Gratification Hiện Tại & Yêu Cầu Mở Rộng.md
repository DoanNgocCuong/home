**

# Phân Tích Hệ Thống Instant Gratification Hiện Tại & Yêu Cầu Mở Rộng

## I. HỆ THỐNG INSTANT GRATIFICATION V1 - PHÂN TÍCH HIỆN TẠI

### 1. Scope Hiện Tại

•Phạm vi: Thông luồng data công đón trên robot và luồng robot <> app liên quan đến điểm thưởng instant reward/gratification

•Dữ liệu chính:

•Tính thể Popa (XP) - Popa Points

•Sao (theo chất lượng của bài học)

•Ứng dụng: Luồng học, chưa áp dụng với các luồng freetalk

### 2. User Flow Hiện Tại (Workflow-based)

•Workflow điều khiển toàn bộ luồng

•Cấu trúc: User → Robot → Backend → App (PH)

•Các bước:

1.Người dùng bắt đầu học

2.Robot trình bày nội dung

3.Đánh giá hiệu suất

4.Trả điểm thưởng theo user intent

5.Công dồn XP trong hoạt động

6.Update tổng XP user

7.Đồng bộ với app phụ huynh

### 3. Acceptance Criteria V1

#### AC1: Robot trả điểm thưởng theo user intent

•Mục độ: +10, +20, +30 XP

•Trường hợp áp dụng:

•+10: Trả lời đúng các dạng bài đơn giản, practice dịch nghĩa

•+20: Trả lời đúng ngay lần đầu các dạng MCQ 2 đáp án, 3 đáp án

•+30: Trả lời đúng các dạng bài Phát âm, lập lại, trả lời câu hỏi bằng tiếng Anh ngay

#### AC2: Robot trả tổng điểm thưởng sau mỗi bài học

•Hiển thị tổng lượng XP kiếm được

•Ý nghĩa: "Câu vừa hoàn thành hoạt động và kiếm được lượng XP này, lượng này sẽ được thêm vào tổng XP của câu"

•Chữ [Tên bé] đã kiếm được

•Show lượng XP kiếm được [+120]

•Lượng XP biến mất, hoá thành tia sáng bay xuống dưới → thể hiện việc Pika đang hấp thu XP

#### AC3: Tổng XP theo user trong app PH

•Trả ra tổng lượng XP một user kiếm được

#### AC4: Trả số lượng sao cho từng bài nói

•<35%: 1 sao

•36-65%: 2 sao

•

65%: 3 sao

•Kèm với các động UX text nhận khi ngồi, động viên

•GIF animation theo condition

### 4. Các Thành Phần Kỹ Thuật

•Robot (Phần ứng/UX): Hiển thị điểm, GIF animation

•GIF: Background, hiệu ứng, text

•Hệ thống (BE): Tính toán XP, công dồn, update user

## II. YÊU CẦU MỞ RỘNG - SCOPE V2

### 1. Ba Hoạt Động Mới Cần Áp Dụng Instant Gratification

#### A. Learn dạng Agent (không phải Workflow)

•Hiện tại: Learn là Workflow → Điều khiển bởi workflow engine

•Mới: Learn sẽ là Agent → Có khả năng tự quyết định, tương tác động

•Đặc điểm:

•Agent Learn có thể tự điều chỉnh độ khó

•Có thể tự gợi ý bài tập dựa trên performance

•Tương tác linh hoạt hơn

•Vẫn cần instant gratification: XP, sao

#### B. Agentic Talk trong Buddy System

•Hiện tại: Buddy Talk là cuộc hội thoại tự nhiên, không có điểm thưởng

•Mới: Buddy Talk sẽ có instant gratification

•Đặc điểm:

•Trẻ tương tác tự nhiên với Pika

•Agent Buddy Talk đánh giá chất lượng tương tác

•Trả điểm thưởng dựa trên:

•Độ tự nhiên của câu trả lời

•Độ phức tạp của ngôn ngữ sử dụng

•Sự tham gia tích cực

•Có thể routing sang Learn Agent hoặc Game Agent

#### C. Game trong Buddy System

•Hiện tại: Game có thể là một hoạt động riêng

•Mới: Game sẽ được tích hợp trong Buddy System

•Đặc điểm:

•Trẻ chơi game được gợi ý từ Buddy Talk

•Game có instant gratification: XP, sao

•Điểm thưởng dựa trên:

•Độ khó của game

•Tốc độ hoàn thành

•Số lần thử

•Sau game, quay lại Buddy Talk

### 2. Các Thách Thức Chính

•Complexity: Agent có khả năng tự quyết định → khó kiểm soát instant gratification

•Fairness: Đảm bảo công bằng trong cách tính điểm giữa các hoạt động

•Consistency: Giữ consistency trong UX giữa Workflow-based (Learn v1) và Agent-based (Learn v2)

•Routing: Quản lý routing giữa các agent (Buddy Talk → Learn Agent → Game Agent)

•Memory: Lưu trữ context và performance data cho các agent

  

## III. ĐỊNH NGHĨA DONE (DOD) CHO PHASE 2 - REASONING

### DOD cho Reasoning Framework:

1.Xác định rõ các loại Instant Gratification cần mở rộng

•Danh sách đầy đủ các loại reward cho Learn Agent

•Danh sách đầy đủ các loại reward cho Buddy Talk

•Danh sách đầy đủ các loại reward cho Game

2.Xác định logic tính toán điểm cho mỗi hoạt động

•Công thức tính XP cho Learn Agent

•Công thức tính XP cho Buddy Talk

•Công thức tính XP cho Game

•Quy tắc kích hoạt sao

3.Xác định UX/UI requirements

•Cách hiển thị điểm thưởng trên robot

•Cách hiển thị animation/GIF

•Cách hiển thị trên app PH

4.Xác định data flow

•Data cần truyền từ Agent sang Backend

•Data cần lưu trữ

•Data cần đồng bộ với app PH

5.Xác định edge cases & special scenarios

•Khi agent routing sang activity khác

•Khi user bỏ dở activity

•Khi network error

•Khi user chơi game multiple times

6.Xác định acceptance criteria cụ thể

•Tương tự AC1-AC4 của v1 nhưng cho các hoạt động mới

  

# REASONING FRAMEWORK: INSTANT GRATIFICATION SYSTEM V2

## Mở Rộng Scope cho Learn Agent, Agentic Talk & Game trong Buddy System

## PHẦN I: FOUNDATION & CONTEXT

### 1. Mục Tiêu Chiến Lược

Hệ thống instant gratification v2 nhằm mở rộng cơ chế tích lũy tinh thể Popa (XP) từ các hoạt động học tập có cấu trúc (Workflow-based Learn v1) sang các hoạt động linh hoạt, tự nhiên, và tương tác động (Agent-based Learn, Agentic Talk, Game). Điều này tạo ra một hệ thống phần thưởng toàn diện khuyến khích trẻ tham gia tích cực trong tất cả các chế độ tương tác với Pika.

### 2. Các Ràng Buộc & Nguyên Tắc Thiết Kế

#### A. Nguyên Tắc Công Bằng (Fairness)

Trẻ phải nhận được phần thưởng tương xứng với nỗ lực và chất lượng tương tác, bất kể hoạt động là gì. Ví dụ, trả lời đúng một câu hỏi khó trong Learn Agent sẽ nhận cùng mức XP với việc trả lời tự nhiên một câu phức tạp trong Buddy Talk.

#### B. Nguyên Tắc Consistency (Nhất Quán)

Cách tính điểm, hiển thị, và công dồn phải nhất quán giữa các hoạt động. Công thức tính XP cơ bản giống nhau (base score + modifier), UX hiển thị điểm giống nhau (animation, text), và data structure cho XP giống nhau.

#### C. Nguyên Tắc Transparency (Minh Bạch)

Trẻ phải hiểu rõ tại sao nhận được bao nhiêu XP. Pika sẽ giải thích: "Cậu trả lời rất tự nhiên, kiếm được +25 XP". Hệ thống cần có khả năng giải thích quyết định của mình.

#### D. Nguyên Tắc Engagement (Gắn Bó)

Instant gratification phải kích thích tham gia lâu dài, không chỉ ngắn hạn. Điều này được thực hiện thông qua bonus XP cho streaks (học liên tục), unlock content khi đạt milestone, và varied rewards.

  

## PHẦN II: PHÂN TÍCH CHI TIẾT CÁC HOẠT ĐỘNG

### A. LEARN AGENT

#### 1. Cơ Chế Tặng Thưởng

Yêu cầu: Cơ chế tặng thưởng cho Learn Agent phải tương tự như Learn dạng Workflow hiện tại để đảm bảo trải nghiệm người dùng nhất quán.

Logic Áp Dụng:

•XP (Tinh thể Popa): Sử dụng 3 mức điểm chính dựa trên độ khó của hoạt động (xác định bởi loại bài và round):

•10 XP: Hoạt động dễ (lặp từ đơn, MCQ 2 đáp án).

•20 XP: Hoạt động trung bình (lặp câu đơn, QnA).

•30 XP: Hoạt động khó (lặp câu phức tạp, trả lời tự do).

•Sao (Stars): Logic tặng sao cũng được giữ nguyên như Learn Workflow. Sao được tính dựa trên độ khó của hoạt động và chất lượng thực hiện (số lần thử).

•Công thức: Stars = Difficulty_Level + Performance_Factor

•Ví dụ: Hoạt động khó (30 XP, base 2 sao) + trả lời đúng lần đầu (+1 sao) = 3 sao.

Kết luận: Không cần thiết kế cơ chế mới. Learn Agent sẽ kế thừa hoàn toàn hệ thống reward của Learn Workflow v1.

### B. AGENTIC TALK

#### 1. Yêu Cầu Mới

Cơ chế tặng thưởng cho Agentic Talk cần tập trung vào chất lượng câu trả lời của trẻ, với mức thưởng nhỏ hơn (3-5 XP) để khuyến khích tương tác tự nhiên mà không gây áp lực. Agentic Talk bao gồm ba trường hợp riêng biệt, mỗi trường hợp có đặc điểm và cơ chế tặng thưởng khác nhau.

#### 2. Ba Trường Hợp Agentic Talk

##### 2.1. Agent Talk trong Phần Trò Chuyện (Conversation Talk)

Mô tả: Trẻ và Pika có một cuộc hội thoại tự do, có thể là song ngữ (tiếng Việt + tiếng Anh) hoặc full tiếng Anh tùy theo cấu hình của phụ huynh.

Đặc điểm:

•Không có khái niệm "đúng/sai" - trẻ được khuyến khích nói bất kỳ điều gì miễn là tương tác tự nhiên.

•Mục tiêu chính là tăng engagement và duy trì retention qua các cuộc hội thoại có ý nghĩa.

•Có thể bao gồm các yếu tố như: hỏi về ngày hôm nay, kể chuyện, trò chuyện về sở thích, v.v.

Logic Tặng XP:

|   |   |   |
|---|---|---|
|Mức XP|Tiêu Chí Đánh Giá Chất Lượng Câu Trả Lời|Ví Dụ|
|5 XP|Câu trả lời cơ bản: Trả lời đúng, đủ ý, nhưng ngắn gọn, không có sự sáng tạo.|Pika: "What did you do today?" Trẻ: "I went to school."|
|10 XP|Câu trả lời khá: Trả lời đúng, có thêm chi tiết hoặc sử dụng từ vựng/cấu trúc tốt hơn.|Pika: "What did you do today?" Trẻ: "I went to school and I played with my friends."|
|15 XP|Câu trả lời xuất sắc: Trả lời đúng, chi tiết, có yếu tố sáng tạo, hài hước, hoặc đặt câu hỏi ngược lại cho Pika.|Pika: "What did you do today?" Trẻ: "I went to school and learned about dinosaurs. Do you like dinosaurs, Pika?"|

UX Flow:

1.Trẻ và Pika có cuộc hội thoại (ví dụ: 5 lượt nói).

2.Phiên kết thúc hoặc user yêu cầu dừng.

3.Pika tóm tắt: "That was a great conversation! You earned +18 XP for your amazing answers!"

4.(Optional) Pika gợi ý Post-Talk Practice nếu phát hiện các từ phát âm sai hoặc user có hứng thú.

##### 2.2. Agent Talk trong Phần Chơi Game (Game Talk)

Mô tả: Trẻ chơi một trò chơi (ví dụ: Story Building, Word Matching, v.v.) trong đó Pika đặt câu hỏi và trẻ phải trả lời. Khác với Conversation Talk, Game Talk có khái niệm "đúng/sai" - có một câu trả lời mục tiêu hoặc một tập hợp các câu trả lời chấp nhận được.

Đặc điểm:

•Có cấu trúc rõ ràng với các câu hỏi cụ thể và mục tiêu trả lời.

•Trẻ có thể trả lời "đúng" (theo mục tiêu) hoặc "không đúng" (lệch khỏi mục tiêu).

•Mục tiêu chính là kết hợp vui chơi với học tập, khuyến khích trẻ suy nghĩ sáng tạo trong khuôn khổ của trò chơi.

•Ví dụ: Story Building (trẻ xây dựng câu chuyện từ các từ được cho), Pronunciation Challenge (trẻ phát âm từ, so sánh với AI), v.v.

Logic Tặng XP:

|   |   |   |
|---|---|---|
|Mức XP|Tiêu Chí Đánh Giá|Ví Dụ|
|5 XP|Câu trả lời chấp nhận được nhưng cơ bản: Trả lời đúng theo mục tiêu, nhưng ngắn gọn, không sáng tạo.|Pika: "What happens next?" Trẻ: "The cat runs."|
|10 XP|Câu trả lời tốt: Trả lời đúng, có chi tiết, hoặc sử dụng từ vựng tốt hơn.|Pika: "What happens next?" Trẻ: "The black cat runs away from the dog."|
|15 XP|Câu trả lời xuất sắc: Trả lời đúng, chi tiết, sáng tạo, hoặc có yếu tố hài hước.|Pika: "What happens next?" Trẻ: "The big black cat quickly runs away because it is scared of the tiny puppy!"|
|0 XP|Câu trả lời sai hoặc không liên quan: Trẻ trả lời không đúng theo mục tiêu của trò chơi.|Pika: "What happens next?" Trẻ: "I like ice cream." (không liên quan)|

UX Flow:

1.Trẻ chơi game với Pika (ví dụ: 3-5 vòng).

2.Mỗi vòng, trẻ trả lời câu hỏi của Pika.

3.Game kết thúc.

4.Pika tóm tắt: "Great job! You completed the story game! You earned +14 XP!"

5.(Optional) Pika gợi ý Post-Talk Practice nếu cần.

##### 2.3. Post-Talk Practice (Luyện Tập Sau Hội Thoại)

Mô tả: Sau khi kết thúc Conversation Talk hoặc Game Talk, Pika có thể tự động gợi ý hoặc user chủ động yêu cầu một phiên luyện tập ngắn để ôn lại các từ hoặc cấu trúc được sử dụng trong hội thoại/game vừa rồi.

Trigger (Kích Hoạt):

1.Tự động: Khi Pika phát hiện trẻ nói nhiều từ phát âm sai hoặc sử dụng cấu trúc ngữ pháp không chính xác.

2.Tự động: Khi trẻ có hứng thú học (intent positive) - ví dụ: hỏi Pika về một từ hoặc cấu trúc.

3.Chủ động: Trẻ yêu cầu luyện tập thêm.

Data Passed từ Conversation/Game Talk:

JSON

{ "pronunciation_weak_words": ["chicken", "bedroom"], "grammar_issues": ["subject-verb agreement"], "preferred_topic": "animals", "engagement_level": "high", "session_type": "conversation_talk | game_talk" }

Logic Tặng XP: Post-Talk Practice sử dụng cơ chế tương tự Learn Agent (10/20/30 XP + Stars) vì nó là một phiên luyện tập có cấu trúc. Các từ được chọn từ phần Conversation/Game Talk vừa rồi.

|   |   |   |
|---|---|---|
|Mức XP|Hoạt Động|Ví Dụ|
|10 XP|Lặp từ đơn hoặc MCQ 2 đáp án|Pika: "Repeat: chicken" Trẻ: "Chicken."|
|20 XP|Lặp câu hoặc QnA|Pika: "Say: I like chicken." Trẻ: "I like chicken."|
|30 XP|Trả lời tự do hoặc lặp câu phức tạp|Pika: "Do you like chicken?" Trẻ: "Yes, I like chicken very much."|

UX Flow:

1.Conversation/Game Talk kết thúc.

2.Pika phát hiện các từ phát âm sai hoặc user có hứng thú.

3.Pika gợi ý: "Nãy cậu hơi khó ở các từ chicken và bedroom. Chuyển sang luyện phát âm nhé?"

4.Nếu user đồng ý, chuyển sang Post-Talk Practice.

5.Trẻ luyện tập các từ được chọn (ví dụ: 3-5 hoạt động).

6.Post-Talk Practice kết thúc.

7.Pika nói: "Giỏi quá trời! Rồi, quay lại talk tiếp nha." hoặc "Cậu đã luyện tập tốt! Cậu kiếm được +50 XP."

8.Quay trở lại Conversation Talk hoặc kết thúc phiên.

Đặc Điểm Riêng:

•Liên kết với Conversation/Game Talk: Các từ luyện tập được chọn từ phần hội thoại/game vừa rồi, giúp trẻ ôn lại và củng cố kiến thức.

•Cơ chế Reward: Sử dụng cơ chế Learn Agent (10/20/30 XP + Stars) để đảm bảo tính nhất quán với các phiên luyện tập khác.

•Tùy Chọn: User có thể chọn tham gia hay không. Nếu không, quay lại Conversation Talk hoặc kết thúc phiên.

  

#### 4. Khuyến Nghị

Phương Án B (Đánh Giá Cuối Luồng) được khuyến nghị cho Agentic Talk và Game. Lý do:

•Ưu tiên sự tự nhiên: Mục tiêu chính của Agentic Talk và Game là tạo ra một môi trường tương tác thoải mái, không áp lực. Việc đánh giá cuối luồng giúp bảo toàn trải nghiệm này.

•Phù hợp với lứa tuổi: Trẻ 6-10 tuổi có thể cảm thấy bối rối hoặc mất kiên nhẫn nếu cuộc trò chuyện liên tục bị ngắt quãng.

•Hiệu quả kỹ thuật: Giảm thiểu đáng kể số lượng API calls, giúp hệ thống hoạt động ổn định và tiết kiệm chi phí hơn.

Để khắc phục nhược điểm của việc trì hoãn, Pika có thể đưa ra một lời khen chung chung và một câu thông báo về phần thưởng tổng kết, ví dụ: "Chúng mình đã có một cuộc trò chuyện rất vui!

  
**