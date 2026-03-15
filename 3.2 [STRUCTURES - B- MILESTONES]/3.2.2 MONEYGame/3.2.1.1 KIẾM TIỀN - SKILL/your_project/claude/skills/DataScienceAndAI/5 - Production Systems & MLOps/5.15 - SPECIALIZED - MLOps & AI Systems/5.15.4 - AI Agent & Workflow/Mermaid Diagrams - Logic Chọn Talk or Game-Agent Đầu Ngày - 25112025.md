# Mermaid Diagrams: Logic Chọn Talk/Game-Agent Đầu Ngày

## 1. Flowchart Tổng Quan - Quy Trình Lựa Chọn Hoàn Chỉnh

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
  
    style Start fill:#e1f5e1
    style End fill:#ffe1e1
    style Phase1 fill:#fff4e1
    style Phase2 fill:#e1f0ff
    style Phase3 fill:#f0e1ff
    style Output fill:#e1ffe1
```

---

## 2. Flowchart Chi Tiết - Xác Định Phase

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
  
    style Start fill:#e1f5e1
    style Output fill:#e1ffe1
    style P1 fill:#fff4e1
    style P2 fill:#e1f0ff
    style P3 fill:#f0e1ff
```

---

## 3. Flowchart Chi Tiết - Chọn Greeting (Priority-Based)

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
  
    style Start fill:#e1f5e1
    style Output fill:#e1ffe1
    style G1 fill:#ffe1e1
    style G2 fill:#ffe1e1
    style G3 fill:#ffe1e1
    style G4 fill:#ffe1e1
    style Default fill:#fff4e1
```

---

## 4. Flowchart Chi Tiết - Tạo Danh Sách Ứng Viên

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
  
    style Start fill:#e1f5e1
    style CandidateList fill:#e1ffe1
    style S1Process fill:#e1f0ff
    style S2Process fill:#fff4e1
    style S3Add fill:#ffe1f0
    style S4Process fill:#f0e1ff
```

---

## 5. Flowchart Chi Tiết - Lắp Ráp Danh Sách Cuối Cùng

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
  
    style Start fill:#e1f5e1
    style Output fill:#e1ffe1
    style R1 fill:#fff4e1
    style R2 fill:#e1f0ff
    style R3 fill:#f0e1ff
    style Weight fill:#ffe1e1
```

---

## 6. Sequence Diagram - Toàn Bộ Quy Trình

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

## 7. State Diagram - Trạng Thái Phase Progression

```mermaid
stateDiagram-v2
    [*] --> Stranger: User mới<br/>score = 0
  
    Stranger: Phase 1: STRANGER
    Stranger: score < 500
    Stranger: ━━━━━━━━━━
    Stranger: Greeting: V1
    Stranger: Talk: Bề mặt
    Stranger: Game: Đơn giản
  
    Acquaintance: Phase 2: ACQUAINTANCE
    Acquaintance: 500 ≤ score ≤ 3000
    Acquaintance: ━━━━━━━━━━
    Acquaintance: Greeting: V1+V2
    Acquaintance: Talk: +Trường học, Bạn bè
    Acquaintance: Game: +Cá nhân hóa
  
    Friend: Phase 3: FRIEND
    Friend: score > 3000
    Friend: ━━━━━━━━━━
    Friend: Greeting: V1+V2+V3
    Friend: Talk: +Gia đình, Lịch sử
    Friend: Game: +Dự án chung
  
    Stranger --> Acquaintance: Tương tác tích cực<br/>score ≥ 500
    Acquaintance --> Friend: Tương tác sâu sắc<br/>score > 3000
  
    Acquaintance --> Stranger: Không tương tác lâu<br/>score < 500
    Friend --> Acquaintance: Giảm tương tác<br/>score ≤ 3000
  
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

## 8. Class Diagram - Cấu Trúc Dữ Liệu

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

## Tổng Kết

Các diagram trên mô tả toàn bộ logic chọn Talk/Game-Agent đầu ngày từ nhiều góc độ:

1. **Flowchart tổng quan**: Cái nhìn toàn cảnh về 5 bước chính
2. **Flowchart xác định Phase**: Chi tiết cách phân loại người dùng
3. **Flowchart chọn Greeting**: Logic ưu tiên dựa trên điều kiện đặc biệt
4. **Flowchart tạo ứng viên**: Cách xây dựng danh sách từ nhiều nguồn
5. **Flowchart lắp ráp**: Quy trình lọc và chọn cuối cùng
6. **Sequence diagram**: Tương tác giữa các thành phần theo thời gian
7. **State diagram**: Sự chuyển đổi giữa các Phase
8. **Class diagram**: Cấu trúc dữ liệu và quan hệ giữa các class