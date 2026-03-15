# Tài liệu Triển khai Kỹ thuật: Module Context Handling - Friendlyship Management

**Version:** 1.0
**Date:** 25/11/2025
**Author:** Manus AI

## 1. Tổng quan và Bối cảnh (Overview and Context)

Tài liệu này đặc tả chi tiết về mặt kỹ thuật cho việc xây dựng và tích hợp module **Context Handling**, với trọng tâm là quản lý trạng thái tình bạn (Friendship) và lựa chọn Agent (Talk/Game/Greeting) trong hệ sinh thái sản phẩm Pika. Module này là một phần của **Container 3: Context Handling** trong kiến trúc tổng thể, chịu trách nhiệm thu thập, xử lý, và duy trì tất cả dữ liệu liên quan đến người dùng và mối quan hệ của họ với Pika.

### 1.1. Mục tiêu Product

- **Tăng Retention và Engagement:** Tạo ra một mối quan hệ cá nhân hóa, sâu sắc và lâu dài giữa người dùng và Pika, khiến người dùng cảm thấy được thấu hiểu và quay trở lại thường xuyên.
- **Cá nhân hóa Trải nghiệm:** Chuyển đổi từ trải nghiệm "một cho tất cả" sang "một cho mỗi người", nơi các hoạt động, lời chào và chủ đề trò chuyện được điều chỉnh dựa trên lịch sử tương tác và mức độ thân thiết.
- **Tạo ra các khoảnh khắc "Aha!":** Khiến người dùng bất ngờ và thích thú khi Pika "nhớ" lại các chi tiết, sở thích, hoặc các sự kiện trong quá khứ, tạo ra một kết nối cảm xúc thực sự.

### 1.2. Thay đổi so với Thiết kế ban đầu

Dựa trên yêu cầu mới, luồng cập nhật điểm tình bạn (`friendship_score`) sẽ được thay đổi từ mô hình xử lý hàng loạt cuối ngày (batch processing) sang **mô hình xử lý theo thời gian thực (real-time processing)**.

> **Yêu cầu cốt lõi:** *"Sau khi kết thúc 1 cuộc hội thoại phía BE gửi user_id kèm log cho phía AI. Phía AI xử lý log luôn và tính điểm daily_score và code API phía BE để update điểm friendlyship_score."*

Điều này có nghĩa là `friendship_score` sẽ được cập nhật liên tục sau mỗi phiên tương tác, mang lại phản hồi tức thì về mức độ thân thiết và cho phép hệ thống điều phối (Orchestration) có được dữ liệu mới nhất để ra quyết định.

## 2. Thiết kế Kiến trúc Module

Để đáp ứng yêu cầu xử lý real-time, kiến trúc của module sẽ bao gồm ba thành phần chính: **Backend (BE) Service**, **AI Scoring Service**, và **Friendship Database**.

```mermaid
sequenceDiagram
    participant User as User
    participant BE as Backend Service
    participant AI as AI Scoring Service
    participant DB as Friendship Database

    User->>BE: End Conversation
    BE->>AI: POST /v1/scoring/calculate-friendship (user_id, conversation_log)
    activate AI
    AI-->>AI: 1. Phân tích log (tính total_turns, emotion, etc.)
    AI-->>AI: 2. Tính toán friendship_score_change
    deactivate AI
    AI->>BE: POST /v1/users/{user_id}/update-friendship (friendship_score_change, topic_metrics_change, ...)
    activate BE
    BE->>DB: 1. Read current friendship_status
    BE-->>BE: 2. Calculate new scores (friendship_score, topic_scores)
    BE-->>BE: 3. Update friendship_level, streak_day, etc.
    BE->>DB: 3. Write updated friendship_status
    deactivate BE
    BE-->>AI: Response: {success: true}
    AI-->>BE: Response: {success: true}

```

*Sơ đồ 1: Luồng cập nhật Friendship Score theo thời gian thực*

### Luồng hoạt động:

1. **Kết thúc hội thoại:** Người dùng hoàn thành một phiên trò chuyện.
2. **BE gửi yêu cầu:** Backend Service gửi một yêu cầu (POST) đến AI Scoring Service, đính kèm `user_id` và toàn bộ `conversation_log` của phiên vừa kết thúc.
3. **AI tính toán:** AI Scoring Service nhận log, phân tích và tính toán ra một "điểm thay đổi" (`friendship_score_change`) cùng các chỉ số liên quan khác (ví dụ: sự thay đổi của `topic_score`).
4. **AI gọi BE để cập nhật:** AI Service gọi một API do BE cung cấp để gửi "điểm thay đổi" này.
5. **BE cập nhật vào DB:** BE nhận điểm thay đổi, đọc bản ghi `friendship_status` hiện tại từ Database, tính toán các giá trị mới, và ghi đè bản ghi đã cập nhật trở lại vào Database.

## 3. Định nghĩa Database Schema và Data Structure

Cấu trúc dữ liệu sẽ được lưu trong một cơ sở dữ liệu SQL (Postgress). Cấu trúc này dựa trên `Tài liệu 1` nhưng có điều chỉnh để phù hợp với logic cập nhật real-time.

**Collection/Table:** `friendship_status`

| Tên trường             | Kiểu dữ liệu    | Mô tả                                                          | Ghi chú                                               |  |
| :------------------------ | :----------------- | :--------------------------------------------------------------- | :----------------------------------------------------- | - |
| `user_id`               | String             | (Primary Key) Mã định danh duy nhất của người dùng.      | Bắt buộc.                                            |  |
| `friendship_score`      | Float              | Điểm số tổng thể đo lường mức độ thân thiết.        | Cập nhật sau mỗi phiên.                            |  |
| `friendship_level`      | String             | Cấp độ tình bạn:`STRANGER`, `ACQUAINTANCE`, `FRIEND`. | Tự động cập nhật dựa trên `friendship_score`. |  |
| `last_interaction_date` | ISO 8601 Timestamp | Dấu thời gian của lần tương tác cuối cùng.              | Cập nhật sau mỗi phiên.                            |  |
| `streak_day`            | Integer            | Số ngày tương tác liên tiếp.                              | Cập nhật sau mỗi phiên.                            |  |
| `topic_metrics`         | Object / Map       | Lưu trữ điểm và lịch sử tương tác cho từng chủ đề. | Cập nhật sau mỗi phiên.                            |  |
| `dynamic_memory`        | Array of Objects   | Danh sách các "ký ức chung" giữa Pika và người dùng.    | Thêm mới khi có sự kiện đáng nhớ.              |  |

**Lưu ý:** Trường `daily_metrics` trong thiết kế ban đầu sẽ không còn cần thiết, vì các chỉ số giờ đây được xử lý và tích luỹ trực tiếp vào các trường chính sau mỗi phiên, thay vì được thu thập tạm thời và xử lý cuối ngày.

### Ví dụ bản ghi:

```json
{
  "user_id": "user_123",
  "friendship_score": 785.5, // Đã được cập nhật sau phiên gần nhất
  "friendship_level": "ACQUAINTANCE",
  "last_interaction_date": "2025-11-25T18:30:00Z",
  "streak_day": 6, // Tăng lên vì hôm qua cũng tương tác
  "topic_metrics": {
    "agent_movie": {
      "topic_score": 52.0, // Đã tăng sau phiên nói về phim
      "total_turns": 65,
      "last_talked_date": "2025-11-25T18:25:00Z"
    }
  },
  "dynamic_memory": [
    {
      "memory_id": "mem_003",
      "content": "Thích xem phim của đạo diễn Hayao Miyazaki.",
      "related_topic": "agent_movie",
      "timestamp": "2025-11-25T18:28:00Z"
    }
  ]
}
```

## 4. Thiết kế API Endpoints

Sẽ có 2 API chính được định nghĩa để phục vụ cho module này.

### 4.1. API 1: Tính toán Friendship Score (BE -> AI)

> **a. Thu thập các chỉ số từ `daily_metrics`:**
> *   `total_turns`: Tổng số lượt trò chuyện trong ngày.
> *   `user_initiated_questions`: Số lần người dùng chủ động hỏi Pika.
> *   `followup_topics_count`: Tên chủ đề mới do người dùng gợi ý.
> *   `session_emotion`: Cảm xúc chủ đạo trong ngày ('interesting', 'boring', 'neutral', 'angry', 'happy','sad').
> *   `new_memories_count`: Số ký ức mới được tạo.
> *   `topic_details`: Chi tiết tương tác cho từng topic (số turn, số câu hỏi).

> Logic Mapping Friendship vs Kho

API này cho phép BE yêu cầu AI phân tích một cuộc hội thoại và trả về các điểm số cần cập nhật.

- **Endpoint:** `POST /v1/scoring/calculate-friendship`
- **Service:** AI Scoring Service
- **Mô tả:** Nhận log hội thoại, tính toán và trả về các thay đổi về điểm tình bạn và các chỉ số liên quan.
- **Request Body:**

  ```json
  {
    "user_id": "user_123",
    "conversation_log": [
      {"speaker": "user", "turn_id": 1, "text": "Hello Pika!"},
      {"speaker": "pika", "turn_id": 2, "text": "Hi there! How are you?"},
      // ... thêm các turn khác
    ],
    "session_metadata": {
        "emotion": "interesting", // Do AI tự phân tích hoặc BE gửi sang
        "new_memories_created": 2
    }
  }
  ```
- **Response Body (Success 200):**

  ```json
  {
    "friendship_score_change": 35.0,
    "topic_metrics_update": {
        "agent_movie": {
            "score_change": 7.0,
            "turns_increment": 15
        }
    },
    "new_memories": [
        {
          "content": "Thích xem phim của đạo diễn Hayao Miyazaki.",
          "related_topic": "agent_movie"
        }
    ]
  }
  ```

### 4.2. API 2: Cập nhật Friendship Status (AI -> BE)

API này cho phép AI gửi các điểm số đã tính toán để BE cập nhật vào cơ sở dữ liệu.

- **Endpoint:** `POST /v1/users/update-friendship`
- **Service:** Backend Service
- **Mô tả:** Nhận các thay đổi về điểm số và chỉ số từ AI, sau đó cập nhật vào bản ghi `friendship_status` của người dùng trong DB.
- **Path Parameter:** `user_id` (String, required)
- **Request Body:** (Giống hệt Response Body của API 1)
- **Response Body (Success 200):**

  ```json
  {
    "success": true,
    "message": "Friendship status updated successfully."
  }
  ```

### 4.3. API 3: Lấy danh sách Agent đề xuất (BE -> AI/Orchestration)

API này phục vụ cho việc lấy danh sách các hoạt động (Greeting, Talk, Game) được cá nhân hóa cho người dùng khi bắt đầu một phiên mới.

- **Endpoint:** `GET /v1/users/suggested-activities`
- **Service:** AI Orchestration Service (hoặc một service riêng cho việc lựa chọn)
- **Mô tả:** Dựa trên `friendship_status` của người dùng, chọn ra một danh sách các hoạt động phù hợp.
- **Query Parameters:**

  - truyền vào user_id
  - `type`: (String, optional) Loại agent cần lấy, ví dụ: `greeting`, `talk`, `game`. Nếu không có, trả về cả gói.
  - `count`: (Integer, optional) Số lượng cần lấy.
- **Response Body (Success 200):**

  ```json
  {
    "greeting_agent": {
        "agent_id": "greeting_streak_milestone_5_days",
        "type": "greeting"
    },
    "suggested_agents": [
        {"agent_id": "talk_agent_movie_preference", "type": "talk"},
        {"agent_id": "game_agent_drawing_challenge", "type": "game"},
        {"agent_id": "talk_agent_school_life", "type": "talk"},
        {"agent_id": "talk_agent_follow_up_pet_milu", "type": "talk"}
    ]
  }
  ```

## 5. Logic Xử lý Scoring và Selection

### 5.1. Logic tính điểm (Scoring Logic - Real-time)

Logic này được thực thi trong **AI Scoring Service** sau mỗi cuộc hội thoại, dựa trên `Tài liệu 2` nhưng được điều chỉnh cho phù hợp.

1. **Thu thập chỉ số từ `conversation_log`:**

   * `total_turns`: Tổng số lượt trò chuyện trong phiên.
   * `user_initiated_questions`: Số lần người dùng chủ động hỏi Pika.
   * `session_emotion`: Cảm xúc chủ đạo của phiên (ví dụ: 'interesting', 'boring').
   * `new_memories_count`: Số ký ức mới được tạo trong phiên.
   * `topic_details`: Chi tiết tương tác cho từng topic (số turn, số câu hỏi).
2. **Tính toán `friendship_score_change`:**

   * `base_score = total_turns * 0.5`
   * `engagement_bonus = (user_initiated_questions * 3)`
   * `emotion_bonus`: +15 cho 'interesting', -15 cho 'boring'.
   * `memory_bonus = new_memories_count * 5`
   * **`friendship_score_change`** = `base_score + engagement_bonus + emotion_bonus + memory_bonus`
3. **Tính toán `topic_metrics_update`:**

   * Với mỗi topic trong `topic_details`, tính `score_change` = (`turns` * 0.5 + `user_questions` * 3) và `turns_increment` = `turns`.

### 5.2. Logic lựa chọn Agent (Selection Logic)

Logic này được thực thi trong **AI Orchestration Service** (API 3) và tuân thủ chặt chẽ theo `Tài liệu 3`.

1. **Tải dữ liệu và Xác định Phase:** Lấy `friendship_status` mới nhất của user, xác định `Phase` (Stranger, Acquaintance, Friend) từ `friendship_score`.
2. **Lọc Kho Hoạt động:** Giới hạn các kho Greeting, Talk, Game dựa trên `Phase`.
3. **Chọn Greeting:** Dựa trên các quy tắc ưu tiên (sinh nhật, quay lại sau thời gian dài, cảm xúc phiên trước, v.v.).
4. **Chọn 4 Talk/Game:** Sử dụng phương pháp `Weighted Candidate Selection`:
   * Tạo danh sách ứng viên từ sở thích (`topic_score` cao), khám phá (ít tương tác), cảm xúc, và game.
   * Lắp ráp danh sách cuối cùng, cân bằng tỷ lệ Talk:Game, và chống lặp.
5. **Trả về kết quả:** Gửi danh sách `agent_id` đã được lựa chọn.

### 5.3 Visulize Logic Chọn lựa Agent

#### Mermaid Diagrams: Logic Chọn Talk/Game-Agent Đầu Ngày

######## 1. Flowchart Tổng Quan - Quy Trình Lựa Chọn Hoàn Chỉnh

```mermaid
flowchart TD
    Start([Người dùng mở app đầu ngày]) --> Input[Input: user_id]
    Input --> Step1[Bước 1: Tải dữ liệu<br/>& Xác định Phase]
  
    Step1 --> LoadData[Tải friendship_status]
    LoadData --> DeterminePhase{Xác định Phase<br/>dựa trên friendship_score}
  
    DeterminePhase -->|score < 500| Phase1[Phase 1: STRANGER]
    DeterminePhase -->|500 ≤ score ≤ 3000| Phase2[Phase 2: ACQUAINTANCE]
    DeterminePhase -->|score > 3000| Phase3[Phase 3: FRIEND]
  
    Phase1 --> Step2[Bước 2: Lọc Kho Hoạt Động]
    Phase2 --> Step2
    Phase3 --> Step2
  
    Step2 --> FilterPools[Giới hạn kho theo Phase:<br/>- Greeting Pool<br/>- Talk Agent Pool<br/>- Game/Activity Pool]
  
    FilterPools --> Step3[Bước 3: Chọn Greeting]
    Step3 --> GreetingLogic[Priority-Based Selection]
    GreetingLogic --> GreetingSelected[greeting_id được chọn]
  
    GreetingSelected --> Step4[Bước 4: Chọn 4 Talk/Game]
    Step4 --> BuildCandidates[4a. Tạo danh sách ứng viên]
  
    BuildCandidates --> Pref[Ứng viên sở thích<br/>2 Agent topic_score cao nhất]
    BuildCandidates --> Explore[Ứng viên khám phá<br/>1 Agent ít tương tác]
    BuildCandidates --> Emotion[Ứng viên cảm xúc<br/>Nếu lastday_emotion tiêu cực]
    BuildCandidates --> Game[Ứng viên Game<br/>Từ kho Game của Phase]
  
    Pref --> Assemble[4b. Lắp ráp danh sách cuối cùng]
    Explore --> Assemble
    Emotion --> Assemble
    Game --> Assemble
  
    Assemble --> ApplyRatio[Áp dụng tỷ lệ Talk:Activity<br/>theo Phase]
    ApplyRatio --> AntiDup[Áp dụng bộ lọc chống lặp]
    AntiDup --> WeightPriority[Ưu tiên theo trọng số]
  
    WeightPriority --> Select4[Chọn 4 activity_id]
  
    Select4 --> Step5[Bước 5: Trả về kết quả]
    Step5 --> Output[Output: 1 greeting_id<br/>+ 4 activity_id]
    Output --> End([Kết thúc])
  
    style Start fill:####e1f5e1
    style End fill:####ffe1e1
    style Phase1 fill:####fff4e1
    style Phase2 fill:####e1f0ff
    style Phase3 fill:####f0e1ff
    style Output fill:####e1ffe1
```

---

######## 2. Flowchart Chi Tiết - Xác Định Phase

```mermaid
flowchart LR
    Start([Input: user_id]) --> Load[Tải friendship_status<br/>từ Database]
    Load --> GetScore[Lấy friendship_score]
  
    GetScore --> Check{Kiểm tra<br/>friendship_score}
  
    Check -->|< 500| P1[Phase 1: STRANGER<br/>━━━━━━━━━━<br/>Kho Greeting: V1<br/>Talk: Bề mặt<br/>Game: Đơn giản]
    Check -->|500-3000| P2[Phase 2: ACQUAINTANCE<br/>━━━━━━━━━━<br/>Kho Greeting: V1+V2<br/>Talk: +Trường học, Bạn bè<br/>Game: +Cá nhân hóa]
    Check -->|> 3000| P3[Phase 3: FRIEND<br/>━━━━━━━━━━<br/>Kho Greeting: V1+V2+V3<br/>Talk: +Gia đình, Lịch sử<br/>Game: +Dự án chung]
  
    P1 --> Output([Phase đã xác định])
    P2 --> Output
    P3 --> Output
  
    style Start fill:####e1f5e1
    style Output fill:####e1ffe1
    style P1 fill:####fff4e1
    style P2 fill:####e1f0ff
    style P3 fill:####f0e1ff
```

---

######## 3. Flowchart Chi Tiết - Chọn Greeting (Priority-Based)

```mermaid
flowchart TD
    Start([Bắt đầu chọn Greeting]) --> Input[Input: Phase + friendship_status]
  
    Input --> Check1{Kiểm tra:<br/>user.birthday<br/>== hôm nay?}
  
    Check1 -->|Có| G1[✓ Chọn Greeting:<br/>S2 Birthday]
    Check1 -->|Không| Check2{Kiểm tra:<br/>last_interaction_date<br/>> 7 ngày?}
  
    Check2 -->|Có| G2[✓ Chọn Greeting:<br/>S4 Returning After<br/>Long Absence]
    Check2 -->|Không| Check3{Kiểm tra:<br/>lastday_emotion<br/>== sad?}
  
    Check3 -->|Có| G3[✓ Chọn Greeting:<br/>Agent hỏi cảm xúc]
    Check3 -->|Không| Check4{Kiểm tra:<br/>last_day_follow_up_topic<br/>tồn tại?}
  
    Check4 -->|Có| G4[✓ Chọn Greeting:<br/>Agent follow up topic]
    Check4 -->|Không| Default[Chọn ngẫu nhiên<br/>từ kho Greeting của Phase<br/>ưu tiên chưa dùng gần đây]
  
    G1 --> Output([greeting_id])
    G2 --> Output
    G3 --> Output
    G4 --> Output
    Default --> Output
  
    style Start fill:####e1f5e1
    style Output fill:####e1ffe1
    style G1 fill:####ffe1e1
    style G2 fill:####ffe1e1
    style G3 fill:####ffe1e1
    style G4 fill:####ffe1e1
    style Default fill:####fff4e1
```

---

######## 4. Flowchart Chi Tiết - Tạo Danh Sách Ứng Viên

```mermaid
flowchart TD
    Start([Bắt đầu tạo<br/>danh sách ứng viên]) --> Input[Input: Phase +<br/>friendship_status]
  
    Input --> Parallel{Tạo ứng viên<br/>từ nhiều nguồn}
  
    Parallel --> Source1[Nguồn 1: Sở thích]
    Parallel --> Source2[Nguồn 2: Khám phá]
    Parallel --> Source3[Nguồn 3: Cảm xúc]
    Parallel --> Source4[Nguồn 4: Game]
  
    Source1 --> S1Process[Lấy 2 Agent có<br/>topic_score cao nhất<br/>từ topic_metrics]
  
    Source2 --> S2Process[Lấy 1 Agent ngẫu nhiên<br/>từ kho Talk của Phase<br/>trong top 10 topic<br/>total_turns thấp nhất]
  
    Source3 --> S3Check{lastday_emotion<br/>tiêu cực?}
    S3Check -->|Có| S3Add[Thêm Game/Talk<br/>vui vẻ, hài hước]
    S3Check -->|Không| S3Skip[Bỏ qua]
  
    Source4 --> S4Process[Thêm các Game<br/>từ kho Game của Phase]
  
    S1Process --> Merge[Gộp tất cả ứng viên]
    S2Process --> Merge
    S3Add --> Merge
    S3Skip --> Merge
    S4Process --> Merge
  
    Merge --> CandidateList([Danh sách ứng viên<br/>hoàn chỉnh])
  
    style Start fill:####e1f5e1
    style CandidateList fill:####e1ffe1
    style S1Process fill:####e1f0ff
    style S2Process fill:####fff4e1
    style S3Add fill:####ffe1f0
    style S4Process fill:####f0e1ff
```

---

######## 5. Flowchart Chi Tiết - Lắp Ráp Danh Sách Cuối Cùng

```mermaid
flowchart TD
    Start([Danh sách ứng viên]) --> Input[Input: Candidate List +<br/>Phase]
  
    Input --> Step1[Bước 1: Áp dụng tỷ lệ Talk:Activity]
  
    Step1 --> Ratio{Xác định tỷ lệ<br/>theo Phase}
  
    Ratio -->|Phase 1| R1[Tỷ lệ 40:60<br/>VD: 2 Talk + 2 Game<br/>hoặc 1 Talk + 3 Game]
    Ratio -->|Phase 2| R2[Tỷ lệ theo Phase 2<br/>cân bằng Talk/Game]
    Ratio -->|Phase 3| R3[Tỷ lệ theo Phase 3<br/>linh hoạt hơn]
  
    R1 --> Step2[Bước 2: Áp dụng bộ lọc chống lặp]
    R2 --> Step2
    R3 --> Step2
  
    Step2 --> Filter1[Kiểm tra: Greeting + Talk<br/>không cùng hỏi về cảm xúc]
    Filter1 --> Filter2[Kiểm tra: Không cùng<br/>hỏi về 1 topic]
    Filter2 --> Filter3[Loại bỏ các ứng viên<br/>trùng lặp]
  
    Filter3 --> Step3[Bước 3: Ưu tiên theo trọng số]
  
    Step3 --> Weight[Sắp xếp ưu tiên:<br/>1. Sở thích cao<br/>2. Ký ức liên quan<br/>3. Cảm xúc phù hợp<br/>4. Khám phá mới]
  
    Weight --> Select[Chọn 4 activity_id<br/>từ danh sách đã sắp xếp]
  
    Select --> Output([Output:<br/>4 activity_id])
  
    style Start fill:####e1f5e1
    style Output fill:####e1ffe1
    style R1 fill:####fff4e1
    style R2 fill:####e1f0ff
    style R3 fill:####f0e1ff
    style Weight fill:####ffe1e1
```

---

######## 6. Sequence Diagram - Toàn Bộ Quy Trình

```mermaid
sequenceDiagram
    participant User as Người dùng
    participant App as Ứng dụng
    participant Service as Selection Service
    participant DB as Database
    participant GreetingPool as Greeting Pool
    participant ActivityPool as Talk/Game Pool
  
    User->>App: Mở app đầu ngày
    App->>Service: Gọi với user_id
  
    rect rgb(230, 245, 255)
        Note over Service,DB: BƯỚC 1: Tải dữ liệu & Xác định Phase
        Service->>DB: Query friendship_status(user_id)
        DB-->>Service: Trả về friendship_status
        Service->>Service: Tính Phase từ friendship_score
    end
  
    rect rgb(255, 245, 230)
        Note over Service,ActivityPool: BƯỚC 2: Lọc Kho Hoạt Động
        Service->>GreetingPool: Lọc theo Phase
        GreetingPool-->>Service: Kho Greeting khả dụng
        Service->>ActivityPool: Lọc theo Phase
        ActivityPool-->>Service: Kho Talk/Game khả dụng
    end
  
    rect rgb(230, 255, 230)
        Note over Service,GreetingPool: BƯỚC 3: Chọn Greeting
        Service->>Service: Kiểm tra điều kiện ưu tiên
        alt Birthday
            Service->>GreetingPool: Lấy S2 (Birthday)
        else Long Absence
            Service->>GreetingPool: Lấy S4 (Returning)
        else Sad Emotion
            Service->>GreetingPool: Lấy Agent hỏi cảm xúc
        else Follow-up Topic
            Service->>GreetingPool: Lấy Agent follow-up
        else Default
            Service->>GreetingPool: Lấy ngẫu nhiên
        end
        GreetingPool-->>Service: greeting_id
    end
  
    rect rgb(255, 230, 245)
        Note over Service,ActivityPool: BƯỚC 4: Chọn 4 Talk/Game
        Service->>DB: Query topic_metrics
        DB-->>Service: Trả về topic_metrics
        Service->>Service: Tạo danh sách ứng viên
        Service->>Service: Áp dụng tỷ lệ Talk:Activity
        Service->>Service: Áp dụng bộ lọc chống lặp
        Service->>Service: Sắp xếp theo trọng số
        Service->>ActivityPool: Lấy 4 activity_id
        ActivityPool-->>Service: 4 activity_id
    end
  
    rect rgb(245, 230, 255)
        Note over Service,App: BƯỚC 5: Trả về kết quả
        Service->>Service: Lắp ráp danh sách cuối cùng
        Service-->>App: [greeting_id, activity_id_1, ..., activity_id_4]
        App-->>User: Hiển thị trải nghiệm cá nhân hóa
    end
```

---

######## 7. State Diagram - Trạng Thái Phase Progression

```mermaid
stateDiagram-v2
    [*] --> Stranger: User mới / score = 0

    state "Phase 1: STRANGER" as Stranger {
        [*] --> StateS
        StateS: score < 500
        StateS: Greeting: V1\nTalk: Bề mặt\nGame: Đơn giản
    }

    state "Phase 2: ACQUAINTANCE" as Acquaintance {
        [*] --> StateA
        StateA: 500 ≤ score ≤ 3000
        StateA: Greeting: V1+V2\nTalk: +Trường học, Bạn bè\nGame: +Cá nhân hóa
    }

    state "Phase 3: FRIEND" as Friend {
        [*] --> StateF
        StateF: score > 3000
        StateF: Greeting: V1+V2+V3\nTalk: +Gia đình, Lịch sử\nGame: +Dự án chung
    }

    Stranger --> Acquaintance: Tương tác tích cực\nscore ≥ 500
    Acquaintance --> Friend: Tương tác sâu sắc\nscore > 3000

    Acquaintance --> Stranger: Không tương tác lâu\nscore < 500
    Friend --> Acquaintance: Giảm tương tác\nscore ≤ 3000

    note right of Stranger
        Nội dung an toàn,
        khám phá ban đầu
    end note

    note right of Acquaintance
        Cá nhân hóa tăng,
        chủ đề đa dạng hơn
    end note

    note right of Friend
        Mối quan hệ sâu sắc,
        nội dung đặc biệt
    end note

```

---

######## 8. Class Diagram - Cấu Trúc Dữ Liệu

```mermaid
classDiagram
    class SelectionService {
        +selectDailyActivities(user_id)
        -loadFriendshipStatus(user_id)
        -determinePhase(friendship_score)
        -filterPools(phase)
        -selectGreeting(phase, friendship_status)
        -selectActivities(phase, friendship_status)
    }
  
    class FriendshipStatus {
        +String user_id
        +Float friendship_score
        +String friendship_level
        +DateTime last_interaction_date
        +Integer streak_day
        +Object topic_metrics
        +String lastday_emotion
        +String last_day_follow_up_topic
        +Array dynamic_memory
    }
  
    class Phase {
        <<enumeration>>
        STRANGER
        ACQUAINTANCE
        FRIEND
        +getGreetingPool()
        +getTalkPool()
        +getGamePool()
        +getTalkActivityRatio()
    }
  
    class GreetingSelector {
        +selectGreeting(phase, status)
        -checkBirthday()
        -checkLongAbsence()
        -checkEmotion()
        -checkFollowUpTopic()
        -selectRandom()
    }
  
    class ActivitySelector {
        +selectActivities(phase, status)
        -buildCandidateList()
        -getPreferenceCandidates()
        -getExploreCandidates()
        -getEmotionCandidates()
        -getGameCandidates()
        -applyRatio()
        -applyAntiDuplication()
        -applyWeighting()
    }
  
    class CandidateList {
        +Array preference_candidates
        +Array explore_candidates
        +Array emotion_candidates
        +Array game_candidates
        +merge()
        +filter()
        +sort()
    }
  
    class DailyActivityList {
        +String greeting_id
        +Array activity_ids
        +validate()
    }
  
    SelectionService --> FriendshipStatus: uses
    SelectionService --> Phase: determines
    SelectionService --> GreetingSelector: delegates
    SelectionService --> ActivitySelector: delegates
    ActivitySelector --> CandidateList: creates
    SelectionService --> DailyActivityList: returns
    Phase --> GreetingSelector: configures
    Phase --> ActivitySelector: configures
```

---

######## Tổng Kết

Các diagram trên mô tả toàn bộ logic chọn Talk/Game-Agent đầu ngày từ nhiều góc độ:

1. **Flowchart tổng quan**: Cái nhìn toàn cảnh về 5 bước chính
2. **Flowchart xác định Phase**: Chi tiết cách phân loại người dùng
3. **Flowchart chọn Greeting**: Logic ưu tiên dựa trên điều kiện đặc biệt
4. **Flowchart tạo ứng viên**: Cách xây dựng danh sách từ nhiều nguồn
5. **Flowchart lắp ráp**: Quy trình lọc và chọn cuối cùng
6. **Sequence diagram**: Tương tác giữa các thành phần theo thời gian
7. **State diagram**: Sự chuyển đổi giữa các Phase
8. **Class diagram**: Cấu trúc dữ liệu và quan hệ giữa các class

## 6. Integration Flow và Workflow

Sự tích hợp của module này vào hệ thống lớn được thể hiện qua hai luồng chính.

### 6.1. Luồng Cập nhật Trạng thái (Status Update Flow)

Đây là luồng chạy ngầm sau mỗi tương tác của người dùng, đảm bảo dữ liệu `friendship_status` luôn được cập nhật.

1. **Trigger:** `Conversation_End` event.
2. **BE:** Gói `user_id` và `log`.
3. **BE -> AI:** Gọi `POST /v1/scoring/calculate-friendship`.
4. **AI:** Xử lý và tính toán điểm thay đổi.
5. **AI -> BE:** Gọi `POST /v1/users/{user_id}/update-friendship`.
6. **BE:** Cập nhật `friendship_status` trong **Friendship Database**.

### 6.2. Luồng Lựa chọn Hoạt động (Activity Selection Flow)

Đây là luồng được kích hoạt khi người dùng bắt đầu một phiên mới, quyết định "hôm nay Pika sẽ nói gì?"

1. **Trigger:** `Session_Start` event (người dùng mở app).
2. **BE:** Nhận diện `user_id`.
3. **BE -> AI Orchestration:** Gọi `GET /v1/users/{user_id}/suggested-activities`.
4. **AI Orchestration:**
   a. Đọc `friendship_status` từ **Friendship Database**.
   b. Thực thi **Selection Logic**.
   c. Trả về danh sách `agent_id`.
5. **BE:** Nhận danh sách, lấy nội dung chi tiết của các Agent từ kho và hiển thị cho người dùng, bắt đầu với Greeting Agent.

## 7. Thiết kế DB

Bảng friendship of user : user_id, friendship_score, friendship_level, last_interaction_date, streak_day, topic_metrics

Bảng friendship map with agent (3 loại: Gretting, Talk, Game/ACtivitity, )

Database Schema (2 Bảng)

### 7.1. Bảng `friendship_status`

Lưu trạng thái tình bạn của user.

```sql
CREATE TABLE friendship_status (
    user_id VARCHAR(255) PRIMARY KEY,
    friendship_score FLOAT DEFAULT 0.0 NOT NULL,
    friendship_level VARCHAR(50) DEFAULT 'STRANGER' NOT NULL,
    -- STRANGER (0-99), ACQUAINTANCE (100-499), FRIEND (500+)
    last_interaction_date TIMESTAMP WITH TIME ZONE,
    streak_day INTEGER DEFAULT 0 NOT NULL,
    topic_metrics JSONB DEFAULT '{}' NOT NULL,
    -- {
    --   "agent_movie": { "score": 52.0, "turns": 65, "last_date": "..." },
    --   "agent_animal": { "score": 28.5, "turns": 32, "last_date": "..." }
    -- }
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_friendship_score ON friendship_status(friendship_score);
CREATE INDEX idx_friendship_level ON friendship_status(friendship_level);
CREATE INDEX idx_updated_at ON friendship_status(updated_at DESC);
```

| Cột                      | Kiểu        | Mô tả                                          |
| :------------------------ | :----------- | :----------------------------------------------- |
| `user_id`               | VARCHAR(255) | Primary key, định danh duy nhất của user     |
| `friendship_score`      | FLOAT        | Điểm tình bạn (cập nhật sau mỗi phiên)   |
| `friendship_level`      | VARCHAR(50)  | STRANGER / ACQUAINTANCE / FRIEND                 |
| `last_interaction_date` | TIMESTAMP    | Lần tương tác cuối cùng                    |
| `streak_day`            | INTEGER      | Số ngày tương tác liên tiếp               |
| `topic_metrics`         | JSONB        | Điểm và lịch sử tương tác cho mỗi topic |
| `created_at`            | TIMESTAMP    | Thời điểm tạo record                         |
| `updated_at`            | TIMESTAMP    | Thời điểm cập nhật cuối cùng              |

**Ví dụ dữ liệu:**

```json
{
  "user_id": "user_123",
  "friendship_score": 785.5,
  "friendship_level": "ACQUAINTANCE",
  "last_interaction_date": "2025-11-25T18:30:00Z",
  "streak_day": 6,
  "topic_metrics": {
    "agent_movie": {
      "score": 52.0,
      "turns": 65,
      "last_date": "2025-11-25T18:25:00Z"
    },
    "agent_animal": {
      "score": 28.5,
      "turns": 32,
      "last_date": "2025-11-24T14:10:00Z"
    }
  }
}
```

### 7.2. Bảng `friendship_agent_mapping`

Mapping giữa `friendship_level` và các Agent theo loại.

```sql
CREATE TABLE friendship_agent_mapping (
    id SERIAL PRIMARY KEY,
    friendship_level VARCHAR(50) NOT NULL,
    -- STRANGER, ACQUAINTANCE, FRIEND
    agent_type VARCHAR(50) NOT NULL,
    -- GREETING, TALK, GAME_ACTIVITY
    agent_id VARCHAR(255) NOT NULL,
    agent_name VARCHAR(255) NOT NULL,
    agent_description TEXT,
    weight FLOAT DEFAULT 1.0,
    -- Trọng số ưu tiên (cao hơn = được chọn nhiều hơn)
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(friendship_level, agent_type, agent_id)
);

-- Indexes
CREATE INDEX idx_mapping_level_type ON friendship_agent_mapping(friendship_level, agent_type);
CREATE INDEX idx_mapping_active ON friendship_agent_mapping(is_active);
```

| Cột                  | Kiểu        | Mô tả                                                          |
| :-------------------- | :----------- | :--------------------------------------------------------------- |
| `id`                | SERIAL       | Primary key                                                      |
| `friendship_level`  | VARCHAR(50)  | STRANGER / ACQUAINTANCE / FRIEND                                 |
| `agent_type`        | VARCHAR(50)  | GREETING / TALK / GAME_ACTIVITY                                  |
| `agent_id`          | VARCHAR(255) | ID duy nhất của agent                                          |
| `agent_name`        | VARCHAR(255) | Tên agent (hiển thị cho user)                                 |
| `agent_description` | TEXT         | Mô tả chi tiết                                                |
| `weight`            | FLOAT        | Trọng số ưu tiên (1.0 = bình thường, 2.0 = ưu tiên cao) |
| `is_active`         | BOOLEAN      | Có hoạt động hay không                                      |
| `created_at`        | TIMESTAMP    | Thời điểm tạo                                                |
| `updated_at`        | TIMESTAMP    | Thời điểm cập nhật                                          |

**Ví dụ dữ liệu:**

```sql
-- Greeting agents cho STRANGER
INSERT INTO friendship_agent_mapping (friendship_level, agent_type, agent_id, agent_name, agent_description, weight, is_active)
VALUES 
('STRANGER', 'GREETING', 'greeting_welcome', 'Welcome Greeting', 'Chào mừng người dùng mới', 1.0, TRUE),
('STRANGER', 'GREETING', 'greeting_intro', 'Introduce Pika', 'Giới thiệu về Pika', 1.5, TRUE);

-- Talk agents cho STRANGER
INSERT INTO friendship_agent_mapping (friendship_level, agent_type, agent_id, agent_name, agent_description, weight, is_active)
VALUES 
('STRANGER', 'TALK', 'talk_hobbies', 'Hobbies Talk', 'Nói về sở thích', 1.0, TRUE),
('STRANGER', 'TALK', 'talk_school', 'School Life Talk', 'Nói về học tập', 1.0, TRUE),
('STRANGER', 'TALK', 'talk_pets', 'Pets Talk', 'Nói về thú cưng', 0.8, TRUE);

-- Game agents cho STRANGER
INSERT INTO friendship_agent_mapping (friendship_level, agent_type, agent_id, agent_name, agent_description, weight, is_active)
VALUES 
('STRANGER', 'GAME_ACTIVITY', 'game_drawing', 'Drawing Game', 'Trò chơi vẽ', 1.0, TRUE),
('STRANGER', 'GAME_ACTIVITY', 'game_riddle', 'Riddle Game', 'Trò chơi đố', 0.9, TRUE);

-- Greeting agents cho ACQUAINTANCE
INSERT INTO friendship_agent_mapping (friendship_level, agent_type, agent_id, agent_name, agent_description, weight, is_active)
VALUES 
('ACQUAINTANCE', 'GREETING', 'greeting_streak_5days', 'Streak 5 Days', 'Chúc mừng 5 ngày liên tiếp', 1.5, TRUE),
('ACQUAINTANCE', 'GREETING', 'greeting_memory_recall', 'Memory Recall', 'Nhắc lại ký ức chung', 2.0, TRUE);

-- Talk agents cho ACQUAINTANCE
INSERT INTO friendship_agent_mapping (friendship_level, agent_type, agent_id, agent_name, agent_description, weight, is_active)
VALUES 
('ACQUAINTANCE', 'TALK', 'talk_movie_preference', 'Movie Preference', 'Nói về phim yêu thích', 1.2, TRUE),
('ACQUAINTANCE', 'TALK', 'talk_dreams', 'Dreams Talk', 'Nói về ước mơ', 1.0, TRUE);

-- Game agents cho ACQUAINTANCE
INSERT INTO friendship_agent_mapping (friendship_level, agent_type, agent_id, agent_name, agent_description, weight, is_active)
VALUES 
('ACQUAINTANCE', 'GAME_ACTIVITY', 'game_20questions', '20 Questions', 'Trò chơi 20 câu hỏi', 1.0, TRUE),
('ACQUAINTANCE', 'GAME_ACTIVITY', 'game_story_building', 'Story Building', 'Xây dựng câu chuyện chung', 1.5, TRUE);

-- Greeting agents cho FRIEND
INSERT INTO friendship_agent_mapping (friendship_level, agent_type, agent_id, agent_name, agent_description, weight, is_active)
VALUES 
('FRIEND', 'GREETING', 'greeting_special_moment', 'Special Moment', 'Khoảnh khắc đặc biệt', 2.0, TRUE),
('FRIEND', 'GREETING', 'greeting_anniversary', 'Anniversary', 'Kỷ niệm ngày gặp nhau', 2.5, TRUE);

-- Talk agents cho FRIEND
INSERT INTO friendship_agent_mapping (friendship_level, agent_type, agent_id, agent_name, agent_description, weight, is_active)
VALUES 
('FRIEND', 'TALK', 'talk_deep_conversation', 'Deep Conversation', 'Cuộc trò chuyện sâu sắc', 1.5, TRUE),
('FRIEND', 'TALK', 'talk_future_plans', 'Future Plans', 'Nói về kế hoạch tương lai', 1.3, TRUE);

-- Game agents cho FRIEND
INSERT INTO friendship_agent_mapping (friendship_level, agent_type, agent_id, agent_name, agent_description, weight, is_active)
VALUES 
('FRIEND', 'GAME_ACTIVITY', 'game_adventure', 'Adventure Quest', 'Cuộc phiêu lưu chung', 1.5, TRUE),
('FRIEND', 'GAME_ACTIVITY', 'game_collaborative_art', 'Collaborative Art', 'Tạo tác phẩm nghệ thuật chung', 2.0, TRUE);
```

---

## 8. Define Folder Structure SOLID (Đơn giản nhưng Mạnh)

### 8.1. Cấu trúc Tổng thể

```
context-handling-service/
│
├── README.md
├── .env.example
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
│
├── app/
│   ├── __init__.py
│   │
│   ├── core/                          # Cấu hình, constants, exceptions
│   │   ├── __init__.py
│   │   ├── config.py                  # Settings, environment variables
│   │   ├── constants.py               # Constants, enums
│   │   └── exceptions.py              # Custom exceptions
│   │
│   ├── models/                        # Database models (SQLAlchemy)
│   │   ├── __init__.py
│   │   ├── base.py                    # Base model class
│   │   ├── friendship.py              # FriendshipStatus model
│   │   └── agent.py                   # FriendshipAgentMapping model
│   │
│   ├── schemas/                       # Pydantic schemas (request/response)
│   │   ├── __init__.py
│   │   ├── friendship.py              # Friendship schemas
│   │   ├── agent.py                   # Agent schemas
│   │   └── common.py                  # Common schemas
│   │
│   ├── db/                            # Database layer
│   │   ├── __init__.py
│   │   ├── database.py                # Database connection, session
│   │   └── base_repository.py         # Base repository class
│   │
│   ├── repositories/                  # Data access layer (Repository pattern)
│   │   ├── __init__.py
│   │   ├── friendship_repository.py   # Friendship data access
│   │   └── agent_repository.py        # Agent mapping data access
│   │
│   ├── services/                      # Business logic layer
│   │   ├── __init__.py
│   │   ├── friendship_service.py      # Friendship logic
│   │   └── selection_service.py       # Agent selection logic
│   │
│   ├── api/                           # API routes
│   │   ├── __init__.py
│   │   ├── deps.py                    # Dependency injection
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── endpoints/
│   │       │   ├── __init__.py
│   │       │   ├── friendship.py      # Friendship endpoints
│   │       │   ├── agents.py          # Agent endpoints
│   │       │   └── health.py          # Health check
│   │       └── router.py              # API router
│   │
│   ├── utils/                         # Utility functions
│   │   ├── __init__.py
│   │   ├── logger.py                  # Logging setup
│   │   ├── validators.py              # Input validators
│   │   └── helpers.py                 # Helper functions
│   │
│   └── main.py                        # FastAPI app entry point
│
├── migrations/                        # Alembic migrations
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       ├── 001_create_friendship_status_table.py
│       └── 002_create_friendship_agent_mapping_table.py
│
├── scripts/                           # Utility scripts
│   ├── __init__.py
│   ├── seed_agents.py                 # Seed agent data
│   └── init_db.py                     # Initialize database
│
├── tests/                             # Tests
│   ├── __init__.py
│   ├── conftest.py                    # Pytest configuration
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_friendship_service.py
│   │   └── test_selection_service.py
│   └── integration/
│       ├── __init__.py
│       ├── test_friendship_api.py
│       └── test_agent_api.py
│
└── logs/
    └── .gitkeep
```

### 8.2. Giải thích Chi tiết

#### **`app/core/`** - Cấu hình & Constants

Tập trung tất cả cấu hình, constants, exceptions.

```python
# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
  
    class Config:
        env_file = ".env"

settings = Settings()
```

```python
# app/core/constants.py
from enum import Enum

class FriendshipLevel(str, Enum):
    STRANGER = "STRANGER"
    ACQUAINTANCE = "ACQUAINTANCE"
    FRIEND = "FRIEND"

class AgentType(str, Enum):
    GREETING = "GREETING"
    TALK = "TALK"
    GAME_ACTIVITY = "GAME_ACTIVITY"

# Score thresholds
FRIENDSHIP_SCORE_THRESHOLDS = {
    FriendshipLevel.STRANGER: (0, 100),
    FriendshipLevel.ACQUAINTANCE: (100, 500),
    FriendshipLevel.FRIEND: (500, float('inf'))
}
```

```python
# app/core/exceptions.py
class AppException(Exception):
    """Base exception"""
    pass

class FriendshipNotFoundError(AppException):
    """Raised when friendship status not found"""
    pass

class InvalidScoreError(AppException):
    """Raised when score calculation fails"""
    pass

class AgentSelectionError(AppException):
    """Raised when agent selection fails"""
    pass
```

#### **`app/models/`** - ORM Models

Tách models thành các file nhỏ theo domain.

```python
# app/models/base.py
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime
from datetime import datetime

Base = declarative_base()

class BaseModel(Base):
    """Base model with common fields"""
    __abstract__ = True
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

```python
# app/models/friendship.py
from sqlalchemy import Column, String, Float, Integer, DateTime, JSONB
from app.models.base import BaseModel

class FriendshipStatus(BaseModel):
    __tablename__ = "friendship_status"
    user_id = Column(String, primary_key=True)
    friendship_score = Column(Float, default=0.0, nullable=False)
    friendship_level = Column(String, default="STRANGER", nullable=False)
    last_interaction_date = Column(DateTime, nullable=True)
    streak_day = Column(Integer, default=0, nullable=False)
    topic_metrics = Column(JSONB, default={}, nullable=False)
```

#### **`app/schemas/`** - Pydantic Schemas

Tách schemas theo domain.

```python
# app/schemas/friendship.py
from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime

class FriendshipStatusResponse(BaseModel):
    user_id: str
    friendship_score: float
    friendship_level: str
    last_interaction_date: Optional[datetime]
    streak_day: int
    topic_metrics: Dict

    class Config:
        from_attributes = True
```

#### **`app/repositories/`** - Data Access Layer

Repository pattern cho data access.

```python
# app/repositories/base_repository.py
from sqlalchemy.orm import Session
from typing import TypeVar, Generic, Type

T = TypeVar('T')

class BaseRepository(Generic[T]):
    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model
  
    def get_by_id(self, id: any):
        return self.db.query(self.model).filter(self.model.id == id).first()
  
    def create(self, obj_in):
        db_obj = self.model(**obj_in.dict())
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
```

```python
# app/repositories/friendship_repository.py
from sqlalchemy.orm import Session
from app.models import FriendshipStatus
from app.repositories.base_repository import BaseRepository

class FriendshipRepository(BaseRepository[FriendshipStatus]):
    def __init__(self, db: Session):
        super().__init__(db, FriendshipStatus)
  
    def get_by_user_id(self, user_id: str):
        return self.db.query(FriendshipStatus).filter(
            FriendshipStatus.user_id == user_id
        ).first()
  
    def update_score(self, user_id: str, score_change: float):
        status = self.get_by_user_id(user_id)
        if status:
            status.friendship_score += score_change
            self.db.commit()
            self.db.refresh(status)
        return status
```

#### **`app/services/`** - Business Logic

Service layer chứa business logic.

```python
# app/services/friendship_service.py
from sqlalchemy.orm import Session
from app.repositories import FriendshipRepository
from app.schemas import CalculateFriendshipResponse
from app.core.exceptions import FriendshipNotFoundError

class FriendshipService:
    def __init__(self, db: Session):
        self.repository = FriendshipRepository(db)
  
    def calculate_score(self, request) -> CalculateFriendshipResponse:
        """Tính toán điểm từ log"""
        total_turns = len(request.conversation_log)
        user_initiated = sum(1 for msg in request.conversation_log if msg.speaker == "user")
      
        base_score = total_turns * 0.5
        engagement_bonus = user_initiated * 3
      
        return CalculateFriendshipResponse(
            friendship_score_change=base_score + engagement_bonus
        )
  
    def update_status(self, user_id: str, score_change: float):
        """Cập nhật trạng thái"""
        status = self.repository.update_score(user_id, score_change)
        if not status:
            raise FriendshipNotFoundError(f"User {user_id} not found")
        return status
```

#### **`app/api/v1/endpoints/`** - API Routes

Tách routes theo domain.

```python
# app/api/v1/endpoints/friendship.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas import CalculateFriendshipRequest, CalculateFriendshipResponse
from app.services import FriendshipService

router = APIRouter(prefix="/scoring", tags=["friendship"])

@router.post("/calculate-friendship", response_model=CalculateFriendshipResponse)
def calculate_friendship(
    request: CalculateFriendshipRequest,
    db: Session = Depends(get_db)
):
    """Tính toán điểm tình bạn"""
    service = FriendshipService(db)
    return service.calculate_score(request)
```

#### **`app/api/deps.py`** - Dependency Injection

Centralized dependency injection.

```python
# app/api/deps.py
from sqlalchemy.orm import Session
from app.db.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

#### **`app/utils/logger.py`** - Logging

Structured logging setup.

```python
# app/utils/logger.py
import logging
import json
from app.core.config import settings

def get_logger(name: str):
    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
  
    if settings.ENVIRONMENT == "production":
        formatter = logging.Formatter(
            '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
        )
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
  
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(settings.LOG_LEVEL)
  
    return logger
```

---

### 8.3. SOLID Principles Áp dụng

| Principle                           | Cách Áp dụng                                                                   | Lợi ích                                      |
| :---------------------------------- | :-------------------------------------------------------------------------------- | :--------------------------------------------- |
| **S - Single Responsibility** | Mỗi file có 1 trách nhiệm duy nhất (models, schemas, services, repositories) | Dễ test, dễ bảo trì                        |
| **O - Open/Closed**           | Dùng BaseRepository, BaseModel → dễ extend                                     | Dễ thêm feature mới                         |
| **L - Liskov Substitution**   | Repository, Service có interface rõ ràng                                       | Dễ mock, dễ test                             |
| **I - Interface Segregation** | Tách schemas, models theo domain                                                 | Không phụ thuộc vào những gì không cần |
| **D - Dependency Inversion**  | Dùng dependency injection (get_db, services)                                     | Loose coupling, dễ test                       |

---

## 9. Chi tiết luồng đi của API

1. [Luồng Dữ liệu Tổng thể (v3)](#luồng-dữ-liệu-tổng-thể-v3)
2. [Health Check](#health-check)
3. [API 1: Notify Conversation End (BE → AI)](#api-1-notify-conversation-end-be--ai)
4. [API 2: Get Conversation Data (AI → BE)](#api-2-get-conversation-data-ai--be)
5. [API 3: Get Friendship Status (BE → Context Service)](#api-3-get-friendship-status-be--context-service)
6. [API 4: Get Suggested Activities (BE → Context Service)](#api-4-get-suggested-activities-be--context-service)
7. [API 5-8: Agent Mapping Management](#api-5-8-agent-mapping-management)
8. [Async Processing &amp; Scheduling](#async-processing--scheduling)
9. [Error Handling](#error-handling)

---

### Luồng Dữ liệu Tổng thể (v3)

#### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          EVENT-DRIVEN ARCHITECTURE                          │
└─────────────────────────────────────────────────────────────────────────────┘

PHASE 1: REAL-TIME NOTIFICATION
═════════════════════════════════════════════════════════════════════════════

1. Frontend/Main App
   └─> User kết thúc cuộc trò chuyện
   
2. Backend Service
   └─> API 1: POST /conversations/end
       (Body: user_id + conversation_id)
       (Response: 202 Accepted - không cần đợi)
   
3. Message Queue (RabbitMQ / Kafka)
   └─> Enqueue event: "conversation.ended"
   └─> Payload: {user_id, conversation_id}


PHASE 2: ASYNC PROCESSING (AI Service)
═════════════════════════════════════════════════════════════════════════════

4. AI Scoring Service (Background Worker)
   └─> Consume event từ queue
   └─> API 2: GET /conversations/{conversation_id}
       (Call BE để lấy conversation data)
   
5. AI Service
   └─> Mổ xẻ conversation log
   └─> Tính toán: friendship_score_change, topic_metrics_update
   └─> Tính toán: new_memories, emotion analysis
   
6. AI Service
   └─> API 3: POST /friendship/update
       (Update friendship_status vào DB)
       (Update: friendship_score, friendship_level, streak_day, topic_metrics)
   
7. AI Service
   └─> API 4: POST /candidates/compute
       (Tính toán & cache candidates cho user)
       (Greeting, Talk, Game agents phù hợp nhất)
       (Có thể batch mỗi 6h hoặc real-time)


PHASE 3: SERVING CACHED DATA (BE Service)
═════════════════════════════════════════════════════════════════════════════

8. Backend Service (Lần tiếp theo user mở app)
   └─> API 5: POST /friendship/status
       (Lấy friendship_status - từ cache/DB)
   
9. Backend Service
   └─> API 6: POST /activities/suggest
       (Lấy pre-computed candidates - từ cache)
       (Response: Greeting + Talk + Game agents)
       (Không cần đợi, dữ liệu đã sẵn!)
   
10. Frontend/Main App
    └─> Hiển thị greeting + 4 agents cho user


PHASE 4: BATCH RECOMPUTATION (Optional - mỗi 6h)
═════════════════════════════════════════════════════════════════════════════

11. Scheduler (AI Service)
    └─> Mỗi 6 giờ, trigger batch job
    └─> Duyệt tất cả active users
    └─> Recompute candidates dựa trên friendship_level hiện tại
    └─> Update cache
```

---

### Health Check

#### Endpoint

```
GET /health
```

#### Description

Kiểm tra trạng thái của service và database connection.

#### cURL Example

```bash
curl -X GET http://localhost:8000/v1/health
```

#### Response (200 OK)

```json
{
  "status": "ok",
  "timestamp": "2025-11-25T18:30:00Z",
  "database": "connected",
  "cache": "connected",
  "queue": "connected"
}
```

---

### API 1: Notify Conversation End (BE → AI)

#### Endpoint

```
POST /conversations/end
```

#### Description

**Gọi bởi:** Backend Service
**Gọi tới:** AI Scoring Service (via Message Queue)
**Mục đích:** Thông báo rằng một cuộc hội thoại đã kết thúc

Backend chỉ gửi `conversation_id` (và `user_id` để tracking). AI Service sẽ consume event từ queue và tự động xử lý.

**Đặc điểm:**

- **Non-blocking:** Response 202 Accepted ngay, không cần đợi AI xử lý
- **Asynchronous:** AI xử lý ở background
- **Reliable:** Message được queue, đảm bảo không mất dữ liệu

#### Request Headers

```
Content-Type: application/json
```

#### Request Body

```json
{
  "user_id": "user_123",
  "conversation_id": "conv_abc123xyz",
  "session_metadata": {
    "duration_seconds": 1200,
    "agent_type": "talk"
  }
}
```

#### Request Fields

| Field                | Type   | Required | Description                                      |
| :------------------- | :----- | :------- | :----------------------------------------------- |
| `user_id`          | String | Yes      | ID duy nhất của user                           |
| `conversation_id`  | String | Yes      | ID duy nhất của cuộc hội thoại              |
| `session_metadata` | Object | No       | Metadata về phiên (duration, agent_type, v.v.) |

#### cURL Example

```bash
curl -X POST http://localhost:8000/v1/conversations/end \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123",
    "conversation_id": "conv_abc123xyz",
    "session_metadata": {
      "duration_seconds": 1200,
      "agent_type": "talk"
    }
  }'
```

#### Response (202 Accepted)

```json
{
  "status": "accepted",
  "message": "Conversation end event received and queued for processing",
  "user_id": "user_123",
  "conversation_id": "conv_abc123xyz",
  "processing_id": "proc_xyz789abc"
}
```

#### Response Fields

| Field               | Type   | Description                           |
| :------------------ | :----- | :------------------------------------ |
| `status`          | String | "accepted" - event đã được queue |
| `message`         | String | Thông báo                           |
| `user_id`         | String | ID của user (echo lại)              |
| `conversation_id` | String | ID của conversation (echo lại)      |
| `processing_id`   | String | ID để tracking quá trình xử lý  |

---

### API 2: Get Conversation Data (AI → BE)

#### Endpoint

```
GET /conversations/{conversation_id}
```

#### Description

**Gọi bởi:** AI Scoring Service
**Gọi tới:** Backend Service
**Mục đích:** Lấy toàn bộ conversation data dựa trên conversation_id

AI Service gọi API này để lấy conversation log, metadata, v.v. để phân tích và tính điểm.

**Đặc điểm:**

- **Gọi bởi AI:** Chỉ AI Service gọi API này, không phải BE
- **Caching:** Kết quả có thể cache để tránh gọi lại
- **Timeout:** Nên có timeout hợp lý (ví dụ: 30s)

#### Path Parameters

| Parameter           | Type   | Required | Description                         |
| :------------------ | :----- | :------- | :---------------------------------- |
| `conversation_id` | String | Yes      | ID duy nhất của cuộc hội thoại |

#### cURL Example

```bash
curl -X GET http://localhost:8000/v1/conversations/conv_abc123xyz
```

#### Response (200 OK)

```json
{
  "conversation_id": "conv_abc123xyz",
  "user_id": "user_123",
  "agent_id": "talk_movie_preference",
  "agent_type": "talk",
  "start_time": "2025-11-25T18:00:00Z",
  "end_time": "2025-11-25T18:20:00Z",
  "duration_seconds": 1200,
  "conversation_log": [
    {
      "speaker": "pika",
      "turn_id": 1,
      "text": "Hi! What's your favorite movie genre?",
      "timestamp": "2025-11-25T18:00:00Z"
    },
    {
      "speaker": "user",
      "turn_id": 2,
      "text": "I love animated movies, especially Miyazaki films!",
      "timestamp": "2025-11-25T18:00:15Z"
    },
    {
      "speaker": "pika",
      "turn_id": 3,
      "text": "Miyazaki is amazing! Which is your favorite?",
      "timestamp": "2025-11-25T18:00:30Z"
    },
    {
      "speaker": "user",
      "turn_id": 4,
      "text": "Spirited Away! The animation is incredible.",
      "timestamp": "2025-11-25T18:00:45Z"
    },
    {
      "speaker": "pika",
      "turn_id": 5,
      "text": "Spirited Away is a masterpiece! Have you watched Howl's Moving Castle?",
      "timestamp": "2025-11-25T18:01:00Z"
    },
    {
      "speaker": "user",
      "turn_id": 6,
      "text": "Yes! That's my second favorite. The music is beautiful.",
      "timestamp": "2025-11-25T18:01:15Z"
    }
  ],
  "metadata": {
    "emotion": "interesting",
    "user_initiated_questions": 2,
    "pika_initiated_topics": 2,
    "new_memories_created": 1
  }
}
```

#### Response Fields

| Field                | Type     | Description                                |
| :------------------- | :------- | :----------------------------------------- |
| `conversation_id`  | String   | ID của conversation                       |
| `user_id`          | String   | ID của user                               |
| `agent_id`         | String   | ID của agent được sử dụng            |
| `agent_type`       | String   | Loại agent: GREETING, TALK, GAME_ACTIVITY |
| `start_time`       | DateTime | Thời điểm bắt đầu                    |
| `end_time`         | DateTime | Thời điểm kết thúc                    |
| `duration_seconds` | Integer  | Thời lượng (giây)                      |
| `conversation_log` | Array    | Danh sách các lượt nói                |
| `metadata`         | Object   | Metadata về phiên                        |

### API Update Score: ngoài việc cho con rjob chạy ngầm, thì thêm 1 API để update friendship level of user_id

---

### API 3: Get Friendship Status (BE → Context Service)

#### Endpoint

```
POST /friendship/status
```

#### Description

**Gọi bởi:** Backend Service
**Gọi tới:** Context Handling Service
**Mục đích:** Lấy trạng thái tình bạn hiện tại của user

Khi user mở app hoặc cần lấy thông tin tình bạn, Backend gọi API này. Dữ liệu được lưu trong cache/DB, response nhanh.

#### Request Headers

```
Content-Type: application/json
```

#### Request Body

```json
{
  "user_id": "user_123"
}
```

#### Request Fields

| Field       | Type   | Required | Description            |
| :---------- | :----- | :------- | :--------------------- |
| `user_id` | String | Yes      | ID duy nhất của user |

#### cURL Example

```bash
curl -X POST http://localhost:8000/v1/friendship/status \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123"
  }'
```

#### Response (200 OK)

```json
{
  "user_id": "user_123",
  "friendship_score": 835.5,
  "friendship_level": "ACQUAINTANCE",
  "last_interaction_date": "2025-11-25T18:30:00Z",
  "streak_day": 6,
  "total_turns": 67,
  "topic_metrics": {
    "agent_movie": {
      "score": 59.0,
      "total_turns": 12,
      "last_date": "2025-11-25T18:30:00Z"
    },
    "agent_animal": {
      "score": 28.5,
      "total_turns": 8,
      "last_date": "2025-11-24T14:10:00Z"
    },
    "agent_school": {
      "score": 15.0,
      "total_turns": 5,
      "last_date": "2025-11-23T09:15:00Z"
    }
  }
}
```

#### Response (404 Not Found)

```json
{
  "error": "User not found",
  "user_id": "user_123"
}
```

---

### API 4: Get Suggested Activities (BE → Context Service)

#### Endpoint

```
POST /activities/suggest
```

#### Description

**Gọi bởi:** Backend Service
**Gọi tới:** Context Handling Service
**Mục đích:** Lấy danh sách Agent được đề xuất (pre-computed)

**Đặc điểm quan trọng:**

- **Pre-computed:** Dữ liệu đã được tính toán sẵn bởi AI Service (real-time hoặc batch)
- **Cached:** Response từ cache, rất nhanh (< 100ms)
- **No Waiting:** BE không cần đợi AI xử lý, dữ liệu đã sẵn

#### Request Headers

```
Content-Type: application/json
```

#### Request Body

```json
{
  "user_id": "user_123"
}
```

#### Request Fields

| Field       | Type   | Required | Description            |
| :---------- | :----- | :------- | :--------------------- |
| `user_id` | String | Yes      | ID duy nhất của user |

#### cURL Example

```bash
curl -X POST http://localhost:8000/v1/activities/suggest \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123"
  }'
```

#### Response (200 OK) - User ở ACQUAINTANCE Level

```json
{
  "user_id": "user_123",
  "friendship_level": "ACQUAINTANCE",
  "computed_at": "2025-11-25T18:30:00Z",
  "greeting_agent": {
    "id": 8,
    "friendship_level": "ACQUAINTANCE",
    "agent_type": "GREETING",
    "agent_id": "greeting_memory_recall",
    "agent_name": "Memory Recall",
    "agent_description": "Nhắc lại ký ức chung với user",
    "weight": 2.0,
    "is_active": true,
    "reason": "High affinity with past memories"
  },
  "talk_agents": [
    {
      "id": 10,
      "friendship_level": "ACQUAINTANCE",
      "agent_type": "TALK",
      "agent_id": "talk_movie_preference",
      "agent_name": "Movie Preference",
      "agent_description": "Nói về phim yêu thích",
      "weight": 1.2,
      "is_active": true,
      "reason": "Highest topic_score (59.0)",
      "topic_score": 59.0,
      "total_turns": 12
    },
    {
      "id": 11,
      "friendship_level": "ACQUAINTANCE",
      "agent_type": "TALK",
      "agent_id": "talk_dreams",
      "agent_name": "Dreams Talk",
      "agent_description": "Nói về ước mơ",
      "weight": 1.0,
      "is_active": true,
      "reason": "Exploration candidate - low interaction",
      "topic_score": 8.5,
      "total_turns": 2
    }
  ],
  "game_agents": [
    {
      "id": 12,
      "friendship_level": "ACQUAINTANCE",
      "agent_type": "GAME_ACTIVITY",
      "agent_id": "game_20questions",
      "agent_name": "20 Questions",
      "agent_description": "Trò chơi 20 câu hỏi",
      "weight": 1.0,
      "is_active": true,
      "reason": "Engagement booster"
    },
    {
      "id": 13,
      "friendship_level": "ACQUAINTANCE",
      "agent_type": "GAME_ACTIVITY",
      "agent_id": "game_story_building",
      "agent_name": "Story Building",
      "agent_description": "Xây dựng câu chuyện chung",
      "weight": 1.5,
      "is_active": true,
      "reason": "Creative engagement"
    }
  ]
}
```

#### Response Fields

| Field                | Type     | Description                         |
| :------------------- | :------- | :---------------------------------- |
| `user_id`          | String   | ID của user                        |
| `friendship_level` | String   | STRANGER / ACQUAINTANCE / FRIEND    |
| `computed_at`      | DateTime | Thời điểm tính toán candidates |
| `greeting_agent`   | Object   | 1 greeting agent được chọn      |
| `talk_agents`      | Array    | Danh sách talk agents (2-3 cái)   |
| `game_agents`      | Array    | Danh sách game agents (1-2 cái)   |
| `reason`           | String   | Lý do chọn agent này             |
| `topic_score`      | Float    | Điểm topic (nếu có)             |
| `total_turns`      | Integer  | Số lượt tương tác (nếu có)  |

---

### API 5-8: Agent Mapping Management

#### API 5: List Agent Mappings

###### Endpoint

```
GET /agent-mappings
```

###### Query Parameters

| Parameter            | Type   | Required | Description                                     |
| :------------------- | :----- | :------- | :---------------------------------------------- |
| `friendship_level` | String | No       | Lọc theo level: STRANGER, ACQUAINTANCE, FRIEND |
| `agent_type`       | String | No       | Lọc theo loại: GREETING, TALK, GAME_ACTIVITY  |

###### cURL Examples

```bash
# Lấy tất cả mappings
curl -X GET http://localhost:8000/v1/agent-mappings

# Lấy mappings cho STRANGER level
curl -X GET "http://localhost:8000/v1/agent-mappings?friendship_level=STRANGER"

# Lấy Greeting agents cho ACQUAINTANCE level
curl -X GET "http://localhost:8000/v1/agent-mappings?friendship_level=ACQUAINTANCE&agent_type=GREETING"
```

###### Response (200 OK)

```json
[
  {
    "id": 1,
    "friendship_level": "STRANGER",
    "agent_type": "GREETING",
    "agent_id": "greeting_welcome",
    "agent_name": "Welcome Greeting",
    "agent_description": "Chào mừng người dùng mới",
    "weight": 1.0,
    "is_active": true
  },
  {
    "id": 2,
    "friendship_level": "STRANGER",
    "agent_type": "GREETING",
    "agent_id": "greeting_intro",
    "agent_name": "Introduce Pika",
    "agent_description": "Giới thiệu về Pika",
    "weight": 1.5,
    "is_active": true
  }
]
```

---

#### API 6: Create Agent Mapping

###### Endpoint

```
POST /agent-mappings
```

###### Request Body

```json
{
  "friendship_level": "FRIEND",
  "agent_type": "GREETING",
  "agent_id": "greeting_special_moment",
  "agent_name": "Special Moment",
  "agent_description": "Khoảnh khắc đặc biệt",
  "weight": 2.0
}
```

###### cURL Example

```bash
curl -X POST http://localhost:8000/v1/agent-mappings \
  -H "Content-Type: application/json" \
  -d '{
    "friendship_level": "FRIEND",
    "agent_type": "GREETING",
    "agent_id": "greeting_special_moment",
    "agent_name": "Special Moment",
    "agent_description": "Khoảnh khắc đặc biệt",
    "weight": 2.0
  }'
```

###### Response (201 Created)

```json
{
  "id": 20,
  "friendship_level": "FRIEND",
  "agent_type": "GREETING",
  "agent_id": "greeting_special_moment",
  "agent_name": "Special Moment",
  "agent_description": "Khoảnh khắc đặc biệt",
  "weight": 2.0,
  "is_active": true
}
```

---

#### API 7: Update Agent Mapping

###### Endpoint

```
PUT /agent-mappings/{mapping_id}
```

###### Path Parameters

| Parameter      | Type    | Required | Description           |
| :------------- | :------ | :------- | :-------------------- |
| `mapping_id` | Integer | Yes      | ID của agent mapping |

###### Request Body

```json
{
  "weight": 2.5,
  "is_active": true
}
```

###### cURL Example

```bash
curl -X PUT http://localhost:8000/v1/agent-mappings/20 \
  -H "Content-Type: application/json" \
  -d '{
    "weight": 2.5,
    "is_active": true
  }'
```

###### Response (200 OK)

```json
{
  "id": 20,
  "friendship_level": "FRIEND",
  "agent_type": "GREETING",
  "agent_id": "greeting_special_moment",
  "agent_name": "Special Moment",
  "agent_description": "Khoảnh khắc đặc biệt",
  "weight": 2.5,
  "is_active": true
}
```

---

#### API 8: Delete Agent Mapping

###### Endpoint

```
DELETE /agent-mappings/{mapping_id}
```

###### Path Parameters

| Parameter      | Type    | Required | Description           |
| :------------- | :------ | :------- | :-------------------- |
| `mapping_id` | Integer | Yes      | ID của agent mapping |

###### cURL Example

```bash
curl -X DELETE http://localhost:8000/v1/agent-mappings/20
```

###### Response (200 OK)

```json
{
  "success": true,
  "message": "Agent mapping deleted successfully"
}
```

---

### Async Processing & Scheduling

#### Background Job: Process Conversation End Event

**Trigger:** Khi event "conversation.ended" được enqueue
**Worker:** AI Scoring Service (Background Worker)
**Processing Time:** Sớm nhất có thể (thường < 5 giây)

###### Pseudocode

```python
@app.on_event("startup")
async def start_background_tasks():
    """Khởi động background worker"""
    asyncio.create_task(consume_conversation_events())

async def consume_conversation_events():
    """Consume events từ message queue"""
    while True:
        event = queue.get()  # Blocking call
      
        user_id = event.user_id
        conversation_id = event.conversation_id
      
        try:
            # Step 1: Lấy conversation data từ BE
            conv_data = await get_conversation_data(conversation_id)
          
            # Step 2: Tính toán điểm
            score_change, topic_updates, memories = calculate_friendship_score(conv_data)
          
            # Step 3: Update friendship status
            await update_friendship_status(user_id, score_change, topic_updates, memories)
          
            # Step 4: Compute & cache candidates
            candidates = compute_candidates(user_id)
            await cache_candidates(user_id, candidates)
          
            logger.info(f"Processed conversation {conversation_id} for user {user_id}")
          
        except Exception as e:
            logger.error(f"Error processing conversation {conversation_id}: {e}")
            queue.nack(event)  # Requeue for retry
```

---

#### Scheduled Job: Batch Recompute Candidates (Optional)

**Trigger:** Mỗi 6 giờ (hoặc theo cấu hình)
**Worker:** AI Scoring Service (Scheduler)
**Purpose:** Recompute candidates cho tất cả active users

###### Pseudocode

```python
@scheduler.scheduled_job('interval', hours=6)
async def batch_recompute_candidates():
    """Recompute candidates cho tất cả users mỗi 6 giờ"""
  
    logger.info("Starting batch recompute candidates job")
  
    # Lấy tất cả active users
    users = db.query(FriendshipStatus).filter(
        FriendshipStatus.last_interaction_date >= now() - timedelta(days=30)
    ).all()
  
    for user in users:
        try:
            # Compute candidates dựa trên friendship_level hiện tại
            candidates = compute_candidates(user.user_id)
          
            # Cache candidates
            await cache_candidates(user.user_id, candidates)
          
            logger.info(f"Recomputed candidates for user {user.user_id}")
          
        except Exception as e:
            logger.error(f"Error recomputing candidates for user {user.user_id}: {e}")
  
    logger.info("Batch recompute candidates job completed")
```

---

### Error Handling

#### Common Error Responses

###### 400 Bad Request

```json
{
  "detail": [
    {
      "loc": ["body", "user_id"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

###### 404 Not Found

```json
{
  "error": "Conversation not found",
  "conversation_id": "conv_invalid"
}
```

###### 500 Internal Server Error

```json
{
  "error": "Internal server error",
  "message": "Failed to process conversation",
  "request_id": "req_abc123xyz"
}
```

#### Error Status Codes

| Status Code | Meaning               | Example                                |
| :---------- | :-------------------- | :------------------------------------- |
| 200         | OK                    | Request thành công                   |
| 201         | Created               | Resource được tạo thành công     |
| 202         | Accepted              | Event được queue, sẽ xử lý async |
| 400         | Bad Request           | Request body không hợp lệ           |
| 404         | Not Found             | Resource không tìm thấy             |
| 422         | Unprocessable Entity  | Validation error                       |
| 500         | Internal Server Error | Server error                           |

---

### Complete Integration Example (v3)

#### Scenario: User Hoàn thành hội thoại và mở app lần tiếp theo

```bash
# ========== STEP 1: User kết thúc cuộc hội thoại ==========
# Backend gửi conversation_id (không gửi toàn bộ log)

curl -X POST http://localhost:8000/v1/conversations/end \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123",
    "conversation_id": "conv_abc123xyz",
    "session_metadata": {
      "duration_seconds": 1200,
      "agent_type": "talk"
    }
  }'

# Response: 202 Accepted (không cần đợi)


# ========== STEP 2: AI Service xử lý async (background) ==========
# 1. Consume event từ queue
# 2. Call API 2 để lấy conversation data
# 3. Tính toán score
# 4. Update friendship_status
# 5. Compute & cache candidates
# (Tất cả diễn ra ở background, BE không cần biết)


# ========== STEP 3: Lần tiếp theo, user mở app ==========
# Backend lấy trạng thái hiện tại

curl -X POST http://localhost:8000/v1/friendship/status \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123"
  }'

# Response: Trạng thái tình bạn hiện tại (từ cache/DB)


# ========== STEP 4: Backend lấy agents được đề xuất ==========
# Dữ liệu đã được pre-computed, response rất nhanh!

curl -X POST http://localhost:8000/v1/activities/suggest \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123"
  }'

# Response: 1 greeting agent + 4 talk/game agents (từ cache)
# Không cần đợi AI tính toán!
```

---

### Architecture Benefits (v3)

| Benefit                 | Giải thích                                                        |
| :---------------------- | :------------------------------------------------------------------ |
| **Non-blocking**  | BE không cần đợi AI xử lý, response ngay với 202 Accepted    |
| **Scalable**      | AI xử lý ở background, có thể scale workers độc lập         |
| **Reliable**      | Message queue đảm bảo không mất dữ liệu, có retry mechanism |
| **Fast Response** | Candidates đã pre-computed, BE lấy từ cache (< 100ms)           |
| **Flexible**      | Có thể xử lý real-time hoặc batch mỗi 6h                      |
| **Decoupled**     | BE và AI độc lập, có thể deploy riêng                        |

---

### Technology Stack (Recommended)

| Component                   | Technology           | Purpose                                |
| :-------------------------- | :------------------- | :------------------------------------- |
| **Message Queue**     | RabbitMQ / Kafka     | Enqueue conversation end events        |
| **Cache**             | Redis                | Cache pre-computed candidates          |
| **Database**          | PostgreSQL           | Lưu friendship_status, agent_mappings |
| **Background Worker** | Celery / APScheduler | Consume events, batch jobs             |
| **API Framework**     | FastAPI              | HTTP API endpoints                     |

---

### Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         PRODUCTION                              │
└─────────────────────────────────────────────────────────────────┘

Frontend/App
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ Backend Service (FastAPI)                                       │
│ - API 1: POST /conversations/end                                │
│ - API 3: POST /friendship/status                                │
│ - API 4: POST /activities/suggest                               │
│ - API 2: GET /conversations/{id} (for AI)                       │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ Message Queue (RabbitMQ / Kafka)                                │
│ - Queue: conversation.ended                                     │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ AI Scoring Service (FastAPI + Celery)                           │
│ - Background Worker (consume events)                            │
│ - Scheduler (batch jobs mỗi 6h)                                 │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ Context Handling Service (FastAPI)                              │
│ - Database: PostgreSQL                                          │
│ - Cache: Redis                                                  │
│ - Tables: friendship_status, agent_mappings, candidates_cache   │
└─────────────────────────────────────────────────────────────────┘
```

---

### Summary: API Endpoints (v3)

| # | Endpoint                 | Method | Gọi bởi | Mục đích                  | Response     |
| :- | :----------------------- | :----- | :-------- | :--------------------------- | :----------- |
| 1 | `/conversations/end`   | POST   | BE        | Notify conversation end      | 202 Accepted |
| 2 | `/conversations/{id}`  | GET    | AI        | Lấy conversation data       | 200 OK       |
| 3 | `/friendship/status`   | POST   | BE        | Lấy friendship status       | 200 OK       |
| 4 | `/activities/suggest`  | POST   | BE        | Lấy pre-computed candidates | 200 OK       |
| 5 | `/agent-mappings`      | GET    | Admin     | Lấy danh sách mappings     | 200 OK       |
| 6 | `/agent-mappings`      | POST   | Admin     | Tạo mapping mới            | 201 Created  |
| 7 | `/agent-mappings/{id}` | PUT    | Admin     | Cập nhật mapping           | 200 OK       |
| 8 | `/agent-mappings/{id}` | DELETE | Admin     | Xóa mapping                 | 200 OK       |

---

### Key Differences: v2 vs v3

| Aspect                 | v2 (Synchronous)           | v3 (Event-Driven Async)   |
| :--------------------- | :------------------------- | :------------------------ |
| **BE gửi**      | Toàn bộ conversation log | Chỉ conversation_id      |
| **AI lấy data** | Từ request body           | Gọi API riêng           |
| **Processing**   | Synchronous (BE đợi)     | Asynchronous (background) |
| **Response**     | 200 OK sau khi xong        | 202 Accepted ngay         |
| **Candidates**   | Tính khi BE request       | Pre-computed, cached      |
| **Latency**      | Cao (phụ thuộc AI)       | Thấp (từ cache)         |
| **Scalability**  | Khó scale                 | Dễ scale                 |
| **Reliability**  | Có thể mất dữ liệu    | Queue đảm bảo          |

---

---

**Kết luận:** Tài liệu này cung cấp một kế hoạch triển khai kỹ thuật toàn diện cho module **Context Handling - Friendlyship Management**, chuyển đổi hệ thống sang mô hình cập nhật thời gian thực để tạo ra một trải nghiệm người dùng linh hoạt và cá nhân hóa hơn. Các API và cấu trúc dữ liệu được định nghĩa rõ ràng để đảm bảo sự phối hợp nhịp nhàng giữa Backend, AI và Database.