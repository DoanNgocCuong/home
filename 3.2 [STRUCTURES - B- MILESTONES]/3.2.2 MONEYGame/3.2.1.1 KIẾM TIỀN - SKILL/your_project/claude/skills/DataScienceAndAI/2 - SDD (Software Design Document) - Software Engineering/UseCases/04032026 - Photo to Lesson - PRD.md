# PRODUCT REQUIREMENTS DOCUMENT

## Photo-to-Lesson

> Phụ huynh chụp ảnh nội dung học → Pika tạo bài học cá nhân hóa cho bé

|                    |                                                          |
| ------------------ | -------------------------------------------------------- |
| Feature Name       | Photo-to-Lesson (“Biến Ảnh Thành Bài Học”)               |
| **Version**        | 1.0 — PRD Draft                                          |
| **Date**           | 25/02/2026                                               |
| **Owner**          | Product Team                                             |
| **Teams Involved** | Product, AI, Tech (App + Backend)                        |
| **Priority**       | HIGH — Retention & Differentiation Play                  |
| **Est. Effort**    | M–L (4–6 sprints)                                        |
| **Target Users**   | Phụ huynh có con 4–8 tuổi, đặc biệt học song ngữ/quốc tế |

## MỤC LỤC

1. Bối cảnh & Vấn đề
    
2. Mục tiêu & Chỉ số Thành công
    
3. Scope & Giới hạn
    
4. User Stories & Use Cases
    
5. Functional Requirements
    
6. Lesson Templates theo Môn học
    
7. UX Flow chi tiết
    
8. Technical Architecture
    
9. AI Pipeline
    
10. Child Safety & Content Guardrails
    
11. Phân pha Rollout
    
12. Metrics & Đo lường
    
13. Open Questions & Risks
    

## 1. Bối cảnh & Vấn đề

### 1.1. User Pain Point

Hiện tại, Pika dạy tiếng Anh theo lộ trình riêng (Pre-Starters → Starters → Movers) được thiết kế bởi đội ngũ Product. Đây là điểm mạnh về chất lượng sư phạm, nhưng tạo ra một gap lớn:

> “Pika dạy một đằng, trường dạy một nẻo”

Phụ huynh muốn Pika giúp con ôn lại đúng nội dung đang học ở trường — khoa học bằng tiếng Anh, toán, từ vựng theo chương trình Cambridge/Oxford — nhưng hiện Pika không có cách nào biết con đang học gì ở trường.

### 1.2. Evidence từ User Research

Feedback từ chị Hương (phụ huynh, 2 bé 5 & 8 tuổi, học Song ngữ Cambridge):

- “Con chị học chương trình Song ngữ Cam, ở lớp nó hay học môn khoa học về mấy chủ đề như bộ phận cơ thể người, chuỗi thức ăn...”
    
- “Chị dốt tiếng Anh lắm, bạn ấy hỏi chị khoa học nhưng nếu chị trả lời tiếng Việt bạn ấy lại chuyển sang nói tiếng Việt với chị nên chị không muốn thế lắm.”
    
- “Pika trả lời, giải thích khoa học với ôn lại với bạn ấy thì tốt.”
    

### 1.3. Cơ hội Chiến lược

Feature này chuyển Pika từ “sản phẩm học thêm song song” thành “trợ lý học tập gắn với chính nội dung trường” — tăng stickiness đáng kể. Nó cũng mở rộng khỏi môn tiếng Anh, cho phép dạy bất kỳ môn nào có thể học qua voice conversation: toán, khoa học, từ vựng, địa lý...

## 2. Mục tiêu & Chỉ số Thành công

### 2.1. Mục tiêu Sản phẩm

|   |   |   |
|---|---|---|
|Mục tiêu|Mô tả|Đo bằng|
|Tăng giá trị sử dụng hàng ngày|Pika trở thành công cụ ôn bài mỗi tối, không chỉ “học thêm”|DAU, sessions/ngày|
|Tăng Retention|Phụ huynh thấy Pika giải quyết vấn đề thật → không bỏ|D7/D30 retention|
|Mở rộng use case|Không chỉ tiếng Anh: toán, khoa học, bất kỳ môn voice-friendly|Số môn học được tạo lesson|
|Tăng NPS/WoM|Phụ huynh giới thiệu cho nhau vì “Pika dạy đúng bài trường”|NPS score, referral rate|

### 2.2. Chỉ số Thành công (KPIs)

|   |   |   |   |
|---|---|---|---|
|KPI|Baseline|Target (sau 8 tuần)|Measurement|
|% PH tạo ≥1 lesson/tuần|0% (chưa có)|≥30% active PH|Analytics|
|Sessions từ custom lesson|0|≥2 sessions/user/tuần|Event tracking|
|Lesson completion rate|N/A|≥60%|Backend logs|
|D7 retention (có dùng feature)|Baseline chung|+15% vs không dùng|Cohort analysis|
|NPS từ PH dùng feature|Current NPS|+10 điểm|Survey|

## 3. Scope & Giới hạn

### 3.1. Trong Scope (V1)

- Phụ huynh chụp 1–5 trang ảnh nội dung học từ app
    
- AI extract nội dung → phân tích topic, từ vựng, concepts
    
- Phụ huynh chọn môn học + mục đích + ngôn ngữ
    
- Hệ thống tạo structured lesson (3–5 activities)
    
- Giao lesson lên robot Pika qua Orchestrator
    
- Report kết quả học trên Parent App
    

### 3.2. Hỗ trợ Môn học (V1)

|   |   |   |   |
|---|---|---|---|
|Môn|Ví dụ Nội dung|Interaction Mode|Lý do phù hợp voice|
|Tiếng Anh|Từ vựng, mẫu câu, ngữ pháp cơ bản|Q&A, phát âm, đặt câu|Luyện nghe–nói là cốt lõi|
|Khoa học (EN/VN)|Bộ phận cơ thể, chuỗi thức ăn, thực vật|Giải thích, hỏi đáp, kể chuyện|Giải thích concept qua đối thoại|
|Toán cơ bản|Cộng, trừ, nhân chia đơn giản|Bài tập đọc, đố vui toán học|Phép tính đơn giản nói được|
|Từ vựng chủ đề|Màu sắc, động vật, nghề nghiệp|Flashcard voice, quiz|Học từ qua lặp lại|
|Địa lý/Lịch sử cơ bản|Các châu lục, danh nhân|Hỏi đáp kiến thức|Factual Q&A phù hợp voice|

### 3.3. Ngoài Scope (V1)

- Môn cần visual nhiều: hình học phức tạp, vẽ, hóa học (cần diagram)
    
- Tự động nhận diện giáo trình: không map vào knowledge graph cụ thể (là roadmap)
    
- Spaced repetition tự động: chưa lên lịch ôn nhắc lại (là roadmap)
    
- Phụ huynh tự soạn bài thủ công: chỉ hỗ trợ từ ảnh, không từ text input (V1)
    

## 4. User Stories & Use Cases

### 4.1. User Stories

|   |   |   |   |
|---|---|---|---|
|ID|Vai trò|Muốn|Để|
|US-01|Phụ huynh|chụp ảnh bài học của con và tạo bài ôn tập|con ôn lại đúng nội dung trường với Pika mà không cần mình trực tiếp dạy|
|US-02|Phụ huynh|chọn ngôn ngữ dạy (TA/TV/song ngữ)|con được immerse trong ngôn ngữ mình muốn, không bị chuyển sang TV|
|US-03|Phụ huynh|xem kết quả sau khi con học xong|biết con hiểu bài đến đâu, cần ôn gì thêm|
|US-04|Bé|học bài với Pika như trò chuyện với bạn|ôn bài vui và không căng thẳng|
|US-05|Phụ huynh|chụp nhiều trang cùng lúc|bài học đầy đủ nội dung, không phải chụp từng trang một|

### 4.2. Use Case cụ thể: Chị Hương

**Scenario**: Con chị Hương (8 tuổi) học Song ngữ Cambridge. Hôm nay học về “Food Chains” trong môn Science. Chị muốn Pika ôn lại bằng tiếng Anh.

1. Chị mở app Pika → chạm “Tạo bài học mới”
    
2. Chụp 2 trang sách Science về Food Chains
    
3. Chọn: Môn = Khoa học | Mục đích = Ôn tập | Ngôn ngữ = Tiếng Anh
    
4. AI phân tích → hiển thị preview: “Topic: Food Chains — 5 từ vựng chính — 3 concepts — 4 activities”
    
5. Chị xem preview, chỉnh nhẹ nếu cần → “Giao cho Pika”
    
6. Buổi tối, Pika gọi: “Hey! Hôm nay mình cùng ôn về Food Chains nhé!”
    
7. Bé học xong → app hiển report: “4/5 từ vựng đúng, cần ôn lại: herbivore”
    

## 5. Functional Requirements

### 5.1. Parent App — Tạo Bài học

|   |   |   |   |
|---|---|---|---|
|ID|Tên|Mô tả|Priority|
|FR-01|Chụp/Upload ảnh|Phụ huynh có thể chụp hoặc chọn từ gallery 1–5 ảnh nội dung học|MUST|
|FR-02|Chọn Môn học|Dropdown: Tiếng Anh, Khoa học, Toán, Từ vựng, Khác|MUST|
|FR-03|Chọn Mục đích|Options: Ôn tập, Trò chuyện về chủ đề, Quiz kiểm tra, Tập phát âm|MUST|
|FR-04|Chọn Ngôn ngữ|Tiếng Anh / Tiếng Việt / Song ngữ|MUST|
|FR-05|Preview bài học|Hiển thị: topic, từ vựng chính, số activities, thời lượng ước tính|MUST|
|FR-06|Chỉnh sửa nhẹ|PH có thể xóa từ vựng không muốn, thêm ghi chú|SHOULD|
|FR-07|Giao cho Pika|1-tap assign lên robot. Chọn thời gian: ngay bây giờ / đặt lịch|MUST|

### 5.2. Robot Pika — Thực hiện Bài học

|   |   |   |   |
|---|---|---|---|
|ID|Tên|Mô tả|Priority|
|FR-08|Nhận lesson từ cloud|Orchestrator inject custom lesson vào queue với priority cao|MUST|
|FR-09|Mở bài học tự nhiên|Pika giới thiệu topic bằng giọng thân thiện, không “máy móc”|MUST|
|FR-10|Chạy structured activities|Tuân theo template: Warm Up → Present → Practice → Wrap Up|MUST|
|FR-11|Adaptive trong lesson|Nếu bé sai nhiều → đơn giản hóa. Nếu bé giỏi → tăng độ khó|SHOULD|
|FR-12|Trao thưởng|XP + Sao như các lesson thông thường|MUST|
|FR-13|Lưu kết quả|Gửi kết quả về backend: từ đúng/sai, thời gian, completion|MUST|

### 5.3. Parent App — Sau bài học

|   |   |   |   |
|---|---|---|---|
|ID|Tên|Mô tả|Priority|
|FR-14|Report kết quả|Hiển: từ đúng/sai, concepts đã hiểu, thời gian học|MUST|
|FR-15|Gợi ý ôn lại|“Bé cần ôn thêm: herbivore, carnivore” + nút tạo lại|SHOULD|
|FR-16|Lưu lịch sử|Lưu tất cả custom lessons đã tạo, có thể re-assign|MUST|

## 6. Lesson Templates theo Môn học

Mỗi môn học sử dụng một bộ activity template khác nhau, được thiết kế cho voice-first interaction. Dưới đây là các template cho V1.

### 6.1. Tiếng Anh (Vocabulary & Grammar)

|   |   |   |   |
|---|---|---|---|
|Phase|Activity|Mô tả|Thời lượng|
|Warm Up|Word Echo|Pika nói từ mới, bé nhắc lại. Đánh giá phát âm.|2 phút|
|Present|Story Context|Pika kể một câu chuyện ngắn sử dụng các từ mới, hỏi bé đoán nghĩa.|3 phút|
|Practice|Quick Quiz|Pika hỏi: “What does [word] mean?” hoặc “Use [word] in a sentence”|3 phút|
|Practice|Role Play|Bé và Pika đóng vai sử dụng từ vựng trong ngữ cảnh|3 phút|
|Wrap Up|Summary & Stars|Pika tóm tắt, trao sao, đọc lại từ cần ôn|1 phút|

### 6.2. Khoa học (Science)

|   |   |   |   |
|---|---|---|---|
|Phase|Activity|Mô tả|Thời lượng|
|Warm Up|Curiosity Spark|Pika hỏi một câu gợi mở: “Bạn nghĩ con thỏ ăn gì?”|2 phút|
|Present|Explain & Discuss|Pika giải thích concept chính, xen kẽ câu hỏi kiểm tra hiểu|4 phút|
|Practice|True or False|Pika đưa ra phát biểu, bé nói đúng/sai và giải thích|3 phút|
|Practice|Teach Pika|Bé giải thích lại concept cho Pika (“giả vờ” không biết)|2 phút|
|Wrap Up|Fun Fact + Stars|Pika chia sẻ 1 fun fact liên quan, trao thưởng|1 phút|

### 6.3. Toán cơ bản (Math)

|   |   |   |   |
|---|---|---|---|
|Phase|Activity|Mô tả|Thời lượng|
|Warm Up|Number Warm-up|Bài tập nhanh: Pika đọc số, bé tính nhẩm|2 phút|
|Present|Concept Intro|Pika giải thích phép tính bằng ví dụ thực tế (“Bạn có 3 quả táo...”)|2 phút|
|Practice|Mental Math Drill|Pika đọc phép tính, bé trả lời. Tăng dần độ khó.|4 phút|
|Practice|Word Problems|Pika đọc bài toán đố, bé giải và nói đáp án|3 phút|
|Wrap Up|Score + Challenge|Tóm tắt điểm, thách đố ngày mai|1 phút|

### 6.4. Từ vựng chủ đề (Topic Vocabulary)

|   |   |   |   |
|---|---|---|---|
|Phase|Activity|Mô tả|Thời lượng|
|Warm Up|Picture Describe|Pika mô tả 1 đối tượng, bé đoán tên|2 phút|
|Present|Vocab Intro|Pika giới thiệu 5–8 từ mới với nghĩa và ví dụ|3 phút|
|Practice|Category Sort|Pika nói từ, bé xếp vào nhóm đúng bằng lời|3 phút|
|Practice|Spelling Bee|Pika nói từ, bé đánh vần (voice)|2 phút|
|Wrap Up|Rapid Fire|Đọc nhanh tất cả từ đã học + trao thưởng|2 phút|

## 7. UX Flow chi tiết

### 7.1. Parent App Flow

**Entry Point**: Tab “Học tập” trên app → Nút nổi bật “+ Tạo bài học từ ảnh” (FAB hoặc card trên dashboard)

**Screen 1: Chụp / Upload ảnh**

- Camera viewfinder với khung chụp tài liệu (auto-crop, auto-enhance)
    
- Hỗ trợ chụp liên tục nhiều trang (swipe để xem các trang đã chụp)
    
- Hoặc chọn từ Gallery (multi-select, max 5 ảnh)
    
- Tip: “Hãy chụp rõ nét, đủ sáng để Pika hiểu tốt hơn nhé!”
    

**Screen 2: Cấu hình bài học**

- Chọn Môn học: Tiếng Anh | Khoa học | Toán | Từ vựng | Khác
    
- Chọn Mục đích: Ôn tập | Trò chuyện về chủ đề | Quiz kiểm tra | Tập phát âm
    
- Chọn Ngôn ngữ: Tiếng Anh | Tiếng Việt | Song ngữ
    
- Chọn Bé (nếu nhiều bé trong nhà)
    
- Nút: “Tạo bài học” → loading (5–15 giây)
    

**Screen 3: Preview & Edit**

- Hiển thị: Tên topic (AI-generated), số từ vựng, số concepts, số activities
    
- Danh sách từ vựng chính (swipe để xóa từ không muốn)
    
- Danh sách activities với thời lượng ước tính
    
- Tổng thời lượng ước tính: ~12 phút
    
- Nút: “Giao cho Pika ngay” hoặc “Đặt lịch” (chọn giờ)
    

**Screen 4: Xác nhận & Trạng thái**

- Confirmation: “Đã gửi bài học cho Pika! Pika sẽ gọi bé học lúc 20:00”
    
- Card trên dashboard: trạng thái “Đang chờ” → “Đang học” → “Hoàn thành”
    

**Screen 5: Report (sau khi học xong)**

- Từ vựng: 4/5 đúng (list chi tiết)
    
- Concepts: hiểu tốt 2/3, cần ôn 1/3
    
- Thời gian học: 11 phút
    
- Nút: “Tạo bài ôn lại” (1-tap → tạo lesson mới chỉ với từ/concept sai)
    

## 8. Technical Architecture

### 8.1. System Components bị ảnh hưởng

|   |   |   |
|---|---|---|
|Component|Hiện tại|Cần thay đổi|
|Parent App|Dashboard, Settings, Reports|Thêm: Photo capture, Lesson config, Lesson preview, Lesson history|
|Backend API|Auth, User profile, Learning data|Thêm: Image upload endpoint, Lesson CRUD, Lesson status tracking|
|AI Pipeline|ASR → LLM → TTS, Agent Routing|Thêm: Vision extract, Lesson Generator, Custom Teaching Agent|
|Orchestrator|Daily To-Do List generation|Thêm: Custom Lesson Queue với priority injection|
|Memory (Mem0)|Personal info, learning progress|Thêm: Custom lesson history, từ vựng đã học từ custom lessons|
|Learning Path Engine|Path Registry, Progress Tracker|Không thay đổi (custom lessons tách biệt khỏi main path)|
|Robot On-device|State machine, GIF, audio|Không thay đổi (nhận lesson như activity thông thường)|

### 8.2. Data Flow tổng quát

Dưới đây là data flow end-to-end của feature, từ lúc phụ huynh chụp ảnh đến lúc bé học xong:

|   |   |   |
|---|---|---|
|Bước|Hành động|Chi tiết|
|❶ Parent App|Chụp ảnh + chọn cấu hình|Upload images + config → Backend API|
|❷ Backend API|Nhận & validate|Store images, create lesson record (status: processing)|
|❸ AI: Vision Extract|OCR + Multimodal analysis|Extract: text, topic, vocabulary, concepts, difficulty level|
|❹ AI: Lesson Generator|Map vào template|Generate lesson plan: activities[], vocab[], concepts[], est_duration|
|❺ Backend → App|Gửi preview|App hiển preview cho PH review|
|❻ PH Confirm|Giao cho Pika|Backend update status: assigned, push to Orchestrator|
|❼ Orchestrator|Inject vào queue|Custom lesson được chèn vào Daily Queue với high priority|
|❽ Robot|Thực hiện lesson|Teaching Agent chạy activities, ASR → LLM → TTS như thường|
|❾ Backend|Lưu kết quả|Results → App report + Mem0 update|

## 9. AI Pipeline

### 9.1. Vision Extract Module (Mới)

|   |   |
|---|---|
|Thành phần|Chi tiết|
|Input|1–5 ảnh (JPEG/PNG, max 10MB mỗi ảnh)|
|Model|GPT-4o Vision hoặc Claude Vision (multimodal)|
|Processing|OCR text + nhận diện layout + phân tích nội dung học thuật|
|Output (JSON)|`{ topic, subject, vocabulary: [{word, meaning, example}], concepts: [{name, explanation}], difficulty_level, raw_text }`|
|Latency target|< 10 giây cho 3 ảnh|
|Fallback|Nếu OCR kém → yêu cầu chụp lại với hướng dẫn cụ thể|

### 9.2. Lesson Generator Module (Mới)

Nhận output từ Vision Extract + cấu hình của PH → tạo lesson plan có cấu trúc.

**Logic chọn template:**

- subject = “English” → Vocabulary & Grammar template
    
- subject = “Science” → Science template
    
- subject = “Math” → Math template
    
- subject = “Vocabulary” hoặc không rõ → Topic Vocabulary template
    

**Lesson plan output schema:**

```json
{   "lesson_id": "uuid",   "topic": "Food Chains",   "subject": "science",   "language": "en",   "purpose": "review",   "difficulty": "intermediate",   "est_duration_min": 12,   "vocabulary": [     { "word": "herbivore", "meaning": "...", "example": "..." }   ],   "concepts": [     { "name": "food chain", "explanation": "...", "check_question": "..." }   ],   "activities": [     {       "phase": "warm_up",       "type": "curiosity_spark",       "prompt_template": "...",       "duration_min": 2,       "adaptive_rules": { "if_wrong": "simplify", "if_right": "challenge" }     }   ] }
```

### 9.3. Custom Teaching Agent (Mới/Adapt)

Agent này là một biến thể của Teaching Agent hiện tại, nhưng được inject dynamic content từ lesson plan thay vì từ Path Registry cố định.

|   |   |   |
|---|---|---|
|Đặc điểm|Teaching Agent hiện tại|Custom Teaching Agent|
|Nội dung|Từ Path Registry (cố định)|Từ Lesson Generator (dynamic)|
|System Prompt|Hardcoded per activity type|Dynamic: inject topic + vocab + concepts vào prompt|
|Adaptive|Adaptive Triggers cố định|adaptive_rules trong mỗi activity (customizable)|
|Personality|Giữ nguyên Pika personality|Giữ nguyên (tái sử dụng Buddy System)|
|Rewards|XP + Stars|XP + Stars (tái sử dụng Retention System)|
|Memory|Update Mem0 sau lesson|Update Mem0 + custom_lesson_history|

## 10. Child Safety & Content Guardrails

**NGUYÊN TẮC: MỌI NỘI DUNG ĐẾN TAY TRẺ ĐỀU PHẢI QUA FILTER**

Đây là sản phẩm cho trẻ em 4–8 tuổi. Không có ngoại lệ cho content safety.

|   |   |   |
|---|---|---|
|Guardrail|Mô tả|Priority|
|Image Content Filter|Trước khi AI xử lý ảnh, filter kiểm tra: không chứa nội dung bạo lực, không phù hợp, hoặc nhạy cảm|MUST|
|Generated Content Review|LLM output được filter qua safety layer trước khi trả về preview|MUST|
|Age-appropriate Language|Giới hạn độ phức tạp ngôn ngữ theo độ tuổi của bé (từ profile)|MUST|
|Factual Accuracy Check|Với môn Khoa học/Toán: cross-check facts với knowledge base|SHOULD|
|Parent Preview Gate|Bài học LUÔN hiển preview cho PH trước khi gửi robot. Không có auto-assign.|MUST|
|Hallucination Guardrail|Nếu AI không chắc chắn về nội dung → đánh dấu và báo PH|MUST|
|Content Logging|Log tất cả generated lessons để audit|MUST|

## 11. Phân pha Rollout

### Phase 1: Foundation (Sprint 1–2)

|   |   |   |
|---|---|---|
|Team|Deliverable|Chi tiết|
|AI|Vision Extract Module|Deploy vision model, build extract pipeline, test với 50 mẫu ảnh|
|AI|Lesson Generator v0|Map 4 bộ template, generate lesson plan từ extracted content|
|Tech (Backend)|API: image upload + lesson CRUD|Endpoints, storage, lesson status management|
|Tech (App)|UI: Chụp ảnh + Cấu hình|Camera integration, config screen, loading state|
|Product|Template design|Thiết kế 4 bộ template chi tiết với prompt guidelines|

### Phase 2: Core Experience (Sprint 3–4)

|   |   |   |
|---|---|---|
|Team|Deliverable|Chi tiết|
|AI|Custom Teaching Agent|Adapt Teaching Agent cho dynamic content, test conversation quality|
|Tech (Backend)|Orchestrator integration|Custom lesson queue, priority injection, status sync|
|Tech (App)|UI: Preview + Report|Lesson preview, edit, assign, post-lesson report|
|Product|Content safety rules|Define guardrails, test với edge cases|
|QA|E2E testing|Full flow test: chụp → tạo → học → report|

### Phase 3: Polish & Launch (Sprint 5–6)

|   |   |   |
|---|---|---|
|Team|Deliverable|Chi tiết|
|AI|Quality tuning|Improve prompt quality, reduce hallucination, latency optimization|
|Tech|Analytics integration|Event tracking, funnel metrics, report data|
|Product|Onboarding flow|Tutorial, tooltip, first-time experience|
|All|Beta test|20–30 PH beta, collect feedback, iterate|
|All|GA Launch|Rollout to all users, monitor metrics|

## 12. Metrics & Đo lường

### 12.1. Funnel Metrics

|   |   |   |
|---|---|---|
|Step|Event|Target|
|Xem feature|photo_lesson_viewed|Baseline|
|Chụp ảnh|photo_lesson_photo_taken|≥70% của viewed|
|Cấu hình xong|photo_lesson_configured|≥80% của photo_taken|
|Preview xong|photo_lesson_previewed|≥90% của configured|
|Giao cho Pika|photo_lesson_assigned|≥75% của previewed|
|Bé bắt đầu học|photo_lesson_started|≥80% của assigned|
|Hoàn thành lesson|photo_lesson_completed|≥60% của started|
|PH xem report|photo_lesson_report_viewed|≥70% của completed|

### 12.2. Quality Metrics

|   |   |   |
|---|---|---|
|Metric|Mô tả|Target|
|OCR accuracy|% nội dung extract đúng từ ảnh|≥90%|
|Lesson relevance|PH đánh giá “bài học đúng nội dung”|≥4.0/5.0|
|AI generation latency|Thời gian từ chụp đến preview|< 15 giây|
|Hallucination rate|% bài học có thông tin sai|< 5%|
|Lesson completion rate|% bé hoàn thành hết activities|≥60%|
|Re-create rate|% PH tạo lại bài ôn từ report|≥20%|

## 13. Open Questions & Risks

### 13.1. Open Questions

|   |   |   |   |
|---|---|---|---|
|ID|Câu hỏi|Owner|Deadline|
|OQ-01|Bao nhiêu % user hiện tại có con học song ngữ/quốc tế?|Product — survey|Trước Phase 1|
|OQ-02|Nên limit số custom lessons/tuần để kiểm soát AI cost không?|AI + Business|Trước Phase 2|
|OQ-03|Custom lessons có tính XP vào Leaderboard không?|Product|Trước Phase 2|
|OQ-04|Có cần PH approve mỗi lần, hay cho phép “trust mode” (auto-assign)?|Product + Safety|Sau Beta|

### 13.2. Risks & Mitigations

|   |   |   |   |
|---|---|---|---|
|ID|Severity|Risk|Mitigation|
|R-01|HIGH|Ảnh chụp chất lượng kém → OCR sai|UX guidance khi chụp, auto-enhance, fallback message rõ ràng|
|R-02|HIGH|AI hallucination → dạy sai kiến thức|Parent preview gate bắt buộc, factual cross-check cho Science/Math|
|R-03|MEDIUM|AI cost cao nếu nhiều PH dùng|Rate limit, cache kết quả cho ảnh giống nhau, tối ưu prompt|
|R-04|MEDIUM|PH chụp nội dung không phù hợp|Image content filter, safety reject với message thân thiện|
|R-05|LOW|Ít PH dùng (không đủ demand)|Phase 1 làm nhẹ trước (Photo-to-Chat) để test demand|

---

_— End of Document —_

_PikaRobot Product Team · February 2026_