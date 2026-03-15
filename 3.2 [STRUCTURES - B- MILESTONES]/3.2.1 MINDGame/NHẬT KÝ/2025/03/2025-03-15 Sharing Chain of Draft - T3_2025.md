1. # https://huggingface.co/papers
    

2. # Prompt Mang Về: Từ kỹ thuật cũ Chain of Thought (CoT)
    

- **Dài dòng và tốn tài nguyên**: CoT yêu cầu mô hình viết chi tiết mọi bước lý luận, dẫn đến lượng token lớn, chi phí cao và thời gian phản hồi chậm.
    

---

## **Giải pháp: Chain of Draft (CoD) lấy ý tưởng từ quá trình “nháp”**

- **Tư duy tự nhiên của con người**: Trong thực tế, khi giải một bài toán hay lập luận logic, con người thường phác thảo nhanh những ý chính (nháp) thay vì viết toàn bộ quá trình.
    

**Ý tưởng chính**:

- Dựa theo cách con người ghi chép tóm lược ý chính (“draft”), chỉ giữ lại tối thiểu các bước trung gian thật cần thiết.
    
- Mỗi bước nên giới hạn trong khoảng 5 từ (hoặc một giới hạn từ cụ thể), tránh mô tả dài dòng.
    

**Cách đặt prompt (ví dụ)**:

> _“Think step by step, but only keep a minimum draft for each thinking step, with 5 words at most. Return the answer at the end of the response after a separator ####.”_

- **Tối ưu token**: CoD chỉ ghi lại các “bản nháp” tối thiểu (giới hạn ~5 từ/bước) nhưng vẫn đảm bảo đủ ý để mô hình vận dụng.
    
- **Duy trì độ chính xác**: Mặc dù lược bớt diễn giải, CoD vẫn cho kết quả chính xác tương đương (hoặc cao hơn) so với CoT trong nhiều trường hợp.
    

  

---

  

  

# Ví dụ thực tế:

Dưới đây là ví dụ minh họa về cách sử dụng **Chain of Draft (CoD)** so sánh với cách trả lời thường gặp và Chain-of-Thought (CoT).

---

## Bài toán

> _"Lan có 15 quả táo. Cô ấy cho Phong một ít. Bây giờ Lan còn lại 10 quả táo. Hỏi Lan đã cho Phong bao nhiêu quả táo?"_

### 1. **Trả lời trực tiếp (Standard Prompting)**

Không có lý luận trung gian, chỉ trả lời:

```Plain
A: 5
```

- **Ưu điểm**: Nhanh, ít token, nhưng mô hình dễ đoán sai nếu bài toán phức tạp.
    
- **Nhược điểm**: Không giải thích, độ tin cậy chưa cao.
    

---

### 2. **Chuỗi suy luận chi tiết (Chain-of-Thought)**

```json
Prompt: step by step ...
```

Mô hình diễn giải từng bước một cách đầy đủ:

### A: Hãy suy nghĩ từng bước: Lan bắt đầu với 15 quả táo. Cô ấy cho Phong một số lượng quả táo. Sau khi cho, Lan còn lại 10 quả. Do đó, số táo Lan đã cho = 15 - 10 = 5. 5

- **Ưu điểm**: Chi tiết, minh bạch cách tính.
    
- **Nhược điểm**: Tốn nhiều token, đặc biệt với bài toán phức tạp hơn.
    

---

### 3. **Nháp ngắn gọn (Chain-of-Draft)**

```json
“Think step by step, but only keep a minimum draft for each thinking step, with 5 words at most. Return the answer at the end of the response after a separator ####.”
```

Chỉ ghi lại những bước tính toán thật cốt lõi, giới hạn từ. Ví dụ, giới hạn 5 từ/bước:

#### A: 15 - x = 10 x = 5 5

- **Ưu điểm**:
    
    - Giảm rất nhiều token so với CoT.
        
    - Vẫn có “bước trung gian” để mô hình không bị “nhảy cóc” suy luận.
        
    - Giữ độ chính xác cao.
        
- **Nhược điểm**: Có thể cần ví dụ few-shot để mô hình quen với “phong cách” viết ngắn gọn này.
    

---

## Lợi ích và gợi ý thực hành

1. **Giảm token**: Chuỗi nháp ngắn (CoD) giúp tiết kiệm chi phí tính toán, tăng tốc độ phản hồi.
    
2. **Cần ví dụ minh họa**: Thông thường, hãy cung cấp 2–3 ví dụ (few-shot) để mô hình “hiểu” rõ yêu cầu giới hạn lời giải.
    
3. **Giữ thông tin cốt lõi**: Ghi lại duy nhất các phép tính, giá trị, biến số, tránh miêu tả thừa.
    

Với bài toán đơn giản, bạn có thể hạn chế 3–5 từ cho mỗi bước. Nhưng nếu bài toán phức tạp hơn, nên tăng nhẹ giới hạn từ để mô hình không bỏ sót thông tin quan trọng.

---

## **Bài học rút ra**

1. **Hiệu quả hơn**: Việc rút gọn nháp giúp giảm thiểu token, tiết kiệm thời gian phản hồi và chi phí vận hành.
    
2. **Linh hoạt áp dụng**: Tùy độ phức tạp của bài toán, có thể điều chỉnh độ dài “bản nháp” hoặc thêm ví dụ few-shot để duy trì/cải thiện độ chính xác.
    
3. **Tối ưu cho môi trường sản xuất**: CoD đặc biệt hữu ích cho các mô hình lớn, nơi chi phí token là vấn đề, và tốc độ phản hồi phải được ưu tiên.
    

  

![](https://csg2ej4iz2hz.sg.larksuite.com/space/api/box/stream/download/asynccode/?code=ZDNjYTYyMmQ4MDk1NTdiNjNlMWU0NDYzZDRmYTBkNThfYlVuZ0NjNm9xcGVTa1ZFRjR3UFl2TGU0TnZZUWx1cHVfVG9rZW46VzlaNGJsdE0zbzdjRzF4THFCT2xEODFyZ01lXzE3NDQ5MDAwNTc6MTc0NDkwMzY1N19WNA)

  

  

  

# Bài toán thực tế:

Cần gen lộ trình cá nhân hóa cho team.

Từ 1 user profile => ra được 10 chủ đề chính lớn sát với công việc của user

```bash
Industry: [IT] 
Job: [CTO] 
Gender: Male Native language: Vietnamese 
English Level: [A2] 
Learning goals: [workplace communication] [job interviews] [salary review]
```

```c++
You are ESP learning path expert.  
Think step by step. Keep each step ≤ 5 words.  
Return output in strict JSON only.

Given user profile:  
- Industry  
- Job  
- English Level  
- Learning Goals  

Your task:  
1. Describe user briefly in a few key phrases
2. List groups of people this user communicates with.
3. With each group, suggest 7 most common and important types of meeting/discussion that requires good English speech to complete.
4. Create 6-week learning path:  
  * Topics = 1 type of meeting, conversation, presentation or discussion in that user's daily workflow based on above output. (e.g. daily standup). 
     - Ordered from basic to advance
- topic format: Output in English first then Vietnamese translation. 2-3 words max.
 - Week 1–3:   
     - For each topic, break it down into 5 scenarios for speaking practice. Scenarios should be ordered from basic to advance. 
   - Scenario title format : Vietnamese, 5–10 word phrase. Must not be a question or use adverbs. Scenarios must requires active speech, must be open-ended, and must be logically ordered steps from beginning to end.
- Week 4–5:  
   • No scenario list  
   • Include topic + description  
   • Week 5: Add `"status": "LOCKED"`  
   • Add `"text_status": "Mở khóa bài học"`  
- Week 6:  
   • No topic  
   • Show encouragement message only  

Rules:  
- No topic or scenario overlap  
- Output = strict JSON format only  

============
RESPONSE JSON TEMPLATE (no extra characters):  
{
  "user_profile_description": "...",
  "communication_partners": [
  "scenarios: [
    }
    }
  ],
  "learning_path": [
    {
      "week": 1,
      "topic": "Tên chủ đề",
      "scenarios": [
        { "scenario": "Tên tình huống", "status": "completed/pending" },
        ...
      ],
      "progress": "20%"
    },
    ...
    {
      "week": 4,
      "topic": "Tên chủ đề",
      "description": "Mô tả ngắn"
    },
    {
      "week": 5,
      "topic": "Tên chủ đề",
      "description": "Mô tả ngắn",
      "status": "LOCKED",
      "text_status": "Mở khóa bài học"
    },
    {
      "week": 6,
      "group": "Học bài trước để mở thêm",
      "description": "The Coach luôn cập nhật thêm tình huống giúp bạn"
    }
  ]
}
============

Use CoD:  
- Define who they talk to and for what 
- List realistic daily speaking needs  
- Build weekly learning path  
- Format JSON  
- Output only JSON  

####
```

```json
{
  "user_profile_description": "Vietnamese CTO in IT, A2 English",
  "communication_partners": [
    "team members",
    "senior management",
    "clients",
    "vendors",
    "recruiters"
  ],
  "scenarios": [
    {
      "group": "team members",
      "meetings": [
        "daily standup",
        "project updates",
        "technical discussions",
        "performance reviews",
        "team building",
        "problem-solving sessions",
        "feedback meetings"
      ]
    },
    {
      "group": "senior management",
      "meetings": [
        "strategic planning",
        "budget discussions",
        "progress reports",
        "risk management",
        "innovation proposals",
        "resource allocation",
        "policy updates"
      ]
    },
    {
      "group": "clients",
      "meetings": [
        "project kickoff",
        "requirements gathering",
        "progress updates",
        "issue resolution",
        "contract negotiations",
        "product demonstrations",
        "feedback sessions"
      ]
    },
    {
      "group": "vendors",
      "meetings": [
        "contract discussions",
        "service level agreements",
        "product evaluations",
        "pricing negotiations",
        "delivery schedules",
        "issue resolution",
        "partnership opportunities"
      ]
    },
    {
      "group": "recruiters",
      "meetings": [
        "job interviews",
        "candidate evaluations",
        "salary negotiations",
        "role expectations",
        "onboarding processes",
        "talent acquisition strategies",
        "market trends"
      ]
    }
  ],
  "learning_path": [
    {
      "week": 1,
      "topic": "Daily Standup - Họp hàng ngày",
      "scenarios": [
        {
          "scenario": "Chia sẻ tiến độ công việc",
          "status": "completed"
        },
        {
          "scenario": "Thảo luận vấn đề gặp phải",
          "status": "pending"
        },
        {
          "scenario": "Đề xuất giải pháp cải tiến",
          "status": "pending"
        },
        {
          "scenario": "Phân công nhiệm vụ mới",
          "status": "pending"
        },
        {
          "scenario": "Tổng kết và kết thúc họp",
          "status": "pending"
        }
      ],
      "progress": "20%"
    },
    {
      "week": 2,
      "topic": "Project Updates - Cập nhật dự án",
      "scenarios": [
        {
          "scenario": "Trình bày tiến độ dự án",
          "status": "pending"
        },
        {
          "scenario": "Thảo luận rủi ro tiềm ẩn",
          "status": "pending"
        },
        {
          "scenario": "Đề xuất thay đổi kế hoạch",
          "status": "pending"
        },
        {
          "scenario": "Phân tích phản hồi khách hàng",
          "status": "pending"
        },
        {
          "scenario": "Kết luận và định hướng tiếp theo",
          "status": "pending"
        }
      ],
      "progress": "0%"
    },
    {
      "week": 3,
      "topic": "Technical Discussions - Thảo luận kỹ thuật",
      "scenarios": [
        {
          "scenario": "Giới thiệu vấn đề kỹ thuật",
          "status": "pending"
        },
        {
          "scenario": "Phân tích nguyên nhân gốc rễ",
          "status": "pending"
        },
        {
          "scenario": "Thảo luận giải pháp khả thi",
          "status": "pending"
        },
        {
          "scenario": "Đánh giá tác động giải pháp",
          "status": "pending"
        },
        {
          "scenario": "Quyết định giải pháp thực hiện",
          "status": "pending"
        }
      ],
      "progress": "0%"
    },
    {
      "week": 4,
      "topic": "Performance Reviews - Đánh giá hiệu suất",
      "description": "Thảo luận về hiệu suất làm việc và mục tiêu phát triển"
    },
    {
      "week": 5,
      "topic": "Job Interviews - Phỏng vấn xin việc",
      "description": "Chuẩn bị và thực hành phỏng vấn",
      "status": "LOCKED",
      "text_status": "Mở khóa bài học"
    },
    {
      "week": 6,
      "group": "Học bài trước để mở thêm",
      "description": "The Coach luôn cập nhật thêm tình huống giúp bạn"
    }
  ]
}
```

  

  

```markdown
 1 -  mô tả công việc  
 2 -  trách nhiệm của bạn  
 3 - những người bạn cần giao tiếp hàng ngày. với mỗi  nhóm người cần giao tiếp trên, gợi ý cho tôi 10 tình huống  cần giao tiếp phổ biến nhất, quan trọng nhất mà bạn cần  sử dụng tiếng anh giao tiếp hàng ngày để làm tốt công việc  đó.  
 4 - mỗi tình huống bao gồm: tình huống cần giao tiếp là gì,  tại sao nó quan trọng, nhiệm vụ giao tiếp cần hoàn thành là  gì, các tip/trick và insight để giao tiếp được tốt tình huống  đó là gì
```

  

  

3. # Workflow:
    

![](https://csg2ej4iz2hz.sg.larksuite.com/space/api/box/stream/download/asynccode/?code=Y2MwZjIwNTY2OGI3NDI2M2IwMTljZmFjMmFkNDVmYzhfcDFuSVZKSFhEWG51WXdIbFlIaXNpWDZPT2Y0UURwajNfVG9rZW46TkNQZWJTNEZ0b1BSYXZ4VEVSR2xqS21jZ0dlXzE3NDQ5MDAwNTc6MTc0NDkwMzY1N19WNA)

  

https://www.facebook.com/share/p/18kfR1SdWM/

https://8738733.fs1.hubspotusercontent-na1.net/hubfs/8738733/eBooks/Weaviate%20Agentic%20Architectures-ebook.pdf?fbclid=IwY2xjawJQTWxleHRuA2FlbQIxMAABHf7VPGuEFJNKQU9Xay3AWCtsZB2u_7THytAV87ZNH_-mcfbPs5FZi0Kf9g_aem_giR2OklRq4FE3Sb7s7Zqwg

  

# 1 phút quảng cáo: https://www.facebook.com/groups/59553626976397

  

# Cursor:

- https://www.facebook.com/share/p/162CF9wn8n/
    

  

  

  

# Workflow và AI agents

  

![](https://csg2ej4iz2hz.sg.larksuite.com/space/api/box/stream/download/asynccode/?code=Y2NiZDIxY2M5MzdiMjFmNzMyZTAzNzMwMjZjMGNmZjlfdjg2OGtQZjR4ZWJxSmYwWEFqZk5Yc0ZLaFpEZkRZbGdfVG9rZW46WnMyd2JRa05LbzdHZ3V4dWQyMmxUR2pIZ2RiXzE3NDQ5MDAwNTc6MTc0NDkwMzY1N19WNA)

  

1. OpenAI Agents SDKs - chị Blue - @bluedataa
    

- 1 con Manager => Điều hướng đến các con Agents bên trong (mỗi Agents bên trong được gắn nhiều Action khác nhau).
    

Cơ chế điều hướng Function Calling.

- Code nhanh, vibe dễ và Xử lý mượt với các cases chị Blue test nó đều pass, ...
    
- ...
    

Sorry chị Blue - đoạn này em bị miss hơi nhiều :<

  

2. Dify Agents - chị Linh - @linhjasmine
    

+, Ra tính năng mới Agents (Cắm bên trong nó là nhiều tools) và Agent này được gói lại thành 1 node duy nhất trong 1 Workflow.

(Các version trước đó có các tools cũng được gắn vào Workflow, tuy nhiên mỗi tools là 1 node).

  

Còn với tính năng mới này: Agents tự động điều hướng đến các tools được gắn bên trong, nếu input vào không đủ để kích hoạt 1 tools thì Node Agent này tự động điều hướng đến các tools khác cùng được gắn trong Agents.

  

3. LangGraph (sâu ở tầng Code cho các Dev) - anh Trung Code On Sunday - @codeonsunday
    

Hệ sinh thái: Code LangChain, LangGraph -> Monitor, Visulize: LangSmith.

+, Có khái niệm Thread, nhiều Workflow đều chung trong 1 Thread thì đều chung 1 bộ nhớ. Memory trong 1 thread và có cả Memory chéo Thread.

+, Có cho Prompting ngay trên Hub => Code dễ dàng Pull - kéo xuống để dùng.

+, ...

  

  

  

  

# Research: Grok search trend

Perflexity:

  

supercraft.ai [https://supercraft.ai/](https://supercraft.ai/)

[SuperCraft - The AI Design Suite](http://supercraft.ai/)

Enter

###### Bạn đã gửi

Hôm nay lúc 09:59

[https://www.getdot.ai/](https://www.getdot.ai/)

  

---

# Vấn đề là: Kỹ thuật tốt, khả năng trình bày năng lượng. tuy nhiên, chưa mạch lạc nhiều chỗ conflict.

1. Tool: Paper AI => CHƯA RÕ MỤC ĐÍCH CUỐI CÙNG NGAY TỪ ĐẦU KHIẾN NGƯỜI NGHE PHẢI CHẠY THEO.
    
2. BỊ VỘI QUÁ, BỊ NÓI NHANH Ở NHIỀU CHỖ.
    
3. QUAN TRỌNG: Quên offer: Share group Facebook 1 phút thôi -)) Cơ mà quên mất.