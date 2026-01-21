Đoàn Ngọc Cường - 03/10/2024 - update 09/10/2024

# **1. Thông tin cá nhân**

- Họ và tên: Đoàn Ngọc Cường
    
- Vị trí thực tập: AI Intern
    
- Thời gian thực tập: Từ ngày 27/06/2024 đến ngày 03/10/2024
    
- Người hướng dẫn: **anh Vũ Cao Cường, anh Lê Văn Trúc**
    

  

# **2. Mục tiêu cá nhân:**

(Những mục tiêu cho bản thân trong tháng thực tập thứ 3 này?)

- **2.1 CHUYÊN MÔN:** - Định hướng HIỆN TẠI: LLMs, Prompting, RAG, Chatbot (Research 30% - Product 70%) - Tập trung hơn vào những vùng, những tasks bản thân có lợi thế và có tiềm năng trong tương lai. (Task RAG, Task Chấm điểm tự động, Task Feedback to Backlog, Task Chấm điểm video mentor => điểm chung là các task liên quan đến LLMs, Prompting)
    
- **2.2 CON NGƯỜI: ...**
    

3. # Báo cáo thực tập tháng thứ 3
    

- **Bản cáo thực tập 2 tháng đầu**: https://www.notion.so/B-n-nh-gi-th-c-t-p-sinh-8cd4ece05b2b4f839d3502d94623eae4?pvs=4
    

1. ## **Đầu việc, Kết quả (Outcome) và Tác động (Impact)**
    

|   |   |   |   |   |   |
|---|---|---|---|---|---|
|Dự án/Đầu việc|Mô tả nhiệm vụ|Kết quả đạt được (Outcome)|Công nghệ/Kỹ thuật sử dụng|Tác động (Impact)|Nguyên nhân ?|
|1. Tối ưu JD|- Mindpal tối ưu JD  <br>- Tool crawl thông tin các công ty của `job position cụ thể`từ TopCV|- Các task tối ưu JD: Impact ko cao. Bản thân các leader muốn tuyển đã nắm khá sát mong muốn cần tuyển (chỉ khi có job mới mới cần đến Mindpal).  <br>- Viết tool crawl: Impact chưa quá cao, Complexity lại cao (Chị Mơ xài nhiều web để search 1 vị trí => Cần nhiều time để viết thêm nhiều tool)|- Mindpal app  <br>- Code python crawl data|0|- Bản thân khi nhận đề bài đã thấy task "Tối ưu JD" được chị Mơ đánh mức độ quan trọng 1/10 => hỏi lại trên nhóm chung và vẫn được a Trúc giao làm => làm.  <br>- Lúc làm chưa define kỹ: Impact của task.|
|2. Crawl Idea Gemini Competition|- Crawl idea|- Ideas crawled: [Ideas Gemini Competition](https://docs.google.com/spreadsheets/d/1DDWEzFSik89MMuFlHnYLLOTnt7Uh8ch-/edit?usp=sharing&ouid=106070054805248205712&rtpof=true&sd=true)|Code python crawl data|- Có thể sử dụng để tham khảo => Kết nối các ideas cho 1 số bài toán trong tháng 10, về sau.|Clear Task|
|3. Marketing Data Visualization|- Clean Data: Xử lý các thông tin thừa  <br>- Assign classification labels: xác định các thông tin cần khai thác (nghề, vị trí, mục đích học tiếng anh), và MECE của chúng.  <br>- Visualize đơn giản|- Link Outcome: [Marketing Visualization](https://docs.google.com/spreadsheets/d/17t7EUyqqA5tZTc2NIe-1iZRVGHvgQZiC48zFPChTDig/edit?gid=2141830678#gid=2141830678)  <br>- Link hướng dẫn để tiến hành đóng gói về sau: [DATA ANALYS - MARKETING: Bài "Phân nhóm khách hàng" Marketing - chị Phương](https://csg2ej4iz2hz.sg.larksuite.com/docx/SkAwdJqwnoGWDzxtAHTlWNtbgKh?from=from_copylink)|- LLM API GPT4o-mini  <br>- Excel|- Marketing có thể tối ưu data đầu vào  <br>- Marketing có thể dựa vào data để estimate 1 số insight khách hàng|Clear Task|
|4. Build các bộ test RAG|- Bộ test HitRate và test Responsibility của RAG  <br>(cho các tập: Mapping, Tính năng App, CSKH)|Link: [RAG: How to Đánh giá RAG pipeline](https://csg2ej4iz2hz.sg.larksuite.com/docx/XSsud3sJdoX66Xxx4f6ldEVNggd?from=from_copylink)  <br>1. Đóng gói cách build bộ test HitRate với 1 chunk và 2 chunks, 3 chunks  <br>2. Đóng gói cách build bộ test Responsibility: 16 loại câu hỏi  <br>-------------------|- chatGPT  <br>- Tool Python run Prompting hàng loạt.|- Testing for RAG outsource|Clear Task|
|5. Tinh chỉnh UI, UX, Cơ chế chấm, Câu hỏi câu trả lời|- Chỉnh lại UI, UX  <br>- Gen câu hỏi, câu trả lời  <br>- Chỉnh cơ chế chấm  <br>--------------------  <br>Theo order của PO Minh|||- Đảm bảo sản phẩm đúng nhu cầu khách hàng. Sản phẩm xài được (ngon dần trong tương lai).|- PO giúp làm việc với các bên => Đề bài clear hơn + có feedback từ User, khách hàng nhanh hơn.  <br>+ brainstorm tốt hơn.|
|6. Xử lý feedback -> Backlog|- Thu thập feedback  <br>- Gán nhãn phân loại|Hiện task chưa hoàn thiện:  <br>- Đã có demo 2 rounds và có feedback từ phía chị Hà (user) => Đang tinh chỉnh Prompt để cải thiện kết quả "GÁN NHÃN PHÂN LOẠI".||Runing|- PO giúp làm việc với các bên => Đề bài clear hơn + có feedback từ User, khách hàng nhanh hơn.  <br>+ brainstorm tốt hơn.|
|7. Video Mentor|- Prompting Testing để Detect các tiêu chí và Gợi ý chấm điểm|Hiện đã đóng thành luồng Prompting. Deploy trực tiếp trên Trang Tính hoặc code BackEnd.||TODO|- PO giúp làm việc với các bên => Đề bài clear hơn + có feedback từ User, khách hàng nhanh hơn.  <br>+ brainstorm tốt hơn.|
|1 số tasks khác:  <br>- Build Demo chatbot từ API RAG cho bên CSKH||||- Sau khi có kết quả test HitRate có thể gửi cho bên CSKH check => Đẩy nhanh tiến độ testing||

  

Tự nhận xét về các Tasks, Outcome, Impact:

- Outcome nhiều hơn do 3 lý do:
    

1. Các tasks hợp với những vùng ưu thế của bản thân hơn (Vùng prompt ảnh chưa có nhiều kinh nghiệm).

2. Quen với các task Prompting hơn nhờ 2 tháng trước.
    
3. PO giúp define bài toán rõ hơn, trao đổi thường xuyên hơn, Impact rõ hơn đúng ý User hơn**.**
    

---

2. ## **Đánh giá năng lực và tiềm năng phát triển**
    

3. **Kỹ năng chuyên môn**: (Đánh giá khả năng về Machine Learning, Data Science, Lập trình, v.v.)
    
    1. Đánh giá từ 1-5 (1: Yếu, 5: Xuất sắc): 3
        
    2. Vùng lợi thế, vùng có kinh nghiệm:
        
        1. **Coding with AI First**(with about 500 dòng code),
            
        2. **Prompting, Gen bài testing hàng loạt.**
            
    3. Điểm cần cải thiện **TRONG GIAI ĐOẠN NÀY:**
        
        1. **Cải thiện việc Quản lý các tasks run đồng thời = cách nào?** (xác định rõ vai trò của mình - scope, vấn đề của từng tasks, xếp ưu tiên vấn đề quan trọng, OKRs: tập trung giải quyết Object quan trọng)
            
        2. **Kiểm chứng Hypothesis, Implement Giải Pháp nhiều hơn, nhanh hơn, đồng thời hơn** (Ở 2 tháng trước khi chưa có PO, điểm cần cải thiện là việc: Define kỹ vấn đề -> Define kỹ nhiều giải pháp. Ở tháng này khi có PO => Bản thân tập trung vào Kiểm chứng Hypothesis, Implement Giải Pháp nhiều hơn, nhanh hơn).
            
        3. **PROBLEM SOLVING** thật chú ý: DEFINE KỸ VẤN ĐỀ, NGUYÊN NHÂN. **(rõ requirements, thứ Impact cao user cần)**
            
        4. Mở rộng vùng chưa biết, và không biết mình không biết = việc tiếp tục **bám sát MENTOR TRONG NGÀNH + UPDATE HÀNG NGÀY. (Ý tưởng đến từ việc kết nối các điểm đã biết)**
            
4. **Tiềm năng phát triển**:
    
    4. **35% Research và 65% Product**
        
    5. **Code và No-Code: LLMs, Prompting, NLP, RAG, Chatbot** -> Các Tasks nhỏ -> Các tasks lớn -> Products -> Đi đường dài: AI Engineering/Software Engineering, Product Manager
        
    6. **Idea for App,** minh chứng:
        
        1. Trước khi vào The Coach, cũng có 1 vài ý tưởng hay nhắn với chị Trang (khá trùng với idea các anh chị định build). (Cá nhân hoá lộ trình học, 1 năm rùi mà App vẫn chưa có :<)
            
        2. Idea gần nhất: **MENTOR AI COACHING 1-1 24/7**
            
        3. ⇒ **Tự động điều chỉnh nội dung học** (học nhanh học chậm, lộ trình, ... chỉ cần quăng cho bot 1 link github: RAG Roadmap), Giúp người học KO CẦN SUY NGHĨ NAY HỌC GÌ MAI HỌC GÌ, cá nhân hoá như các dịch vụ coaching 1-1.
            
        4. => **Tự động kết nối với Google Calendar**(Không cần suy nghĩ nay bận thế thì học lúc nào, học bao lâu, ...)
            
5. **Kế hoạch học hỏi và phát triển bản thân trong 6 tháng tới là gì?**
    
    7. **Đảm bảo kỹ năng chuyên môn: LLMs, Prompting, NLP, RAG, Chatbot** theo định hướng bản thân (có thể là có 1 định hướng mới, nhưng cần đảm bảo: Impact trong tương lai, và Complexity không quá khó - phù hợp với bản thân)
        
    8. **“Problem Solving”:** Từ Define bài toán (Impact, Complexity, Urgency, Mentor). Define nguyên nhân, giải pháp (Mở rộng các điểm ideas, Nghĩ ngược lại, ), Define nguồn lực (Human, Material Resources), Define Rủi ro và các giải pháp ứng phó, …
        
    9. **Thực tập tại doanh nghiệp** **=>** Mục tiêu: RA SẢN PHẨM.
        
    10. **Việc học ở trường** (14 tín cuối + **RAG trên NLP Lab** **+** **Đồ án dự kiến: RAG**) -> (Tuỳ lúc đó sẽ: học tiếp lên thạc sỹ vào kỳ 2 năm 4, hoặc chưa...)
        
6. **Kế hoạch dài hạn hơn:**
    
    11. Phối hợp các công nghệ NO-CODE/LOW-CODE ⇒ ra sản phẩm: chatbot/video content/app AI/… (kinh doanh riêng thêm vào các thị trường xanh) + Update **CHUYÊN MÔN - CON NGƯỜI - KINH DOANH** ⇒ Tạo giá trị, đổi lấy lương, thăng tiến, ...
        

---

4. # **Kết luận: Tự đánh giá Impact - Tiềm năng - Nguyện vọng**
    

- **Impact:** Với những task hợp với kinh nghiệm bản thân => Impact nhiều hơn [Đi cùng với PO define bài toán kỹ hơn, tập trung vào high impact]. Cần cải thiện: Quản lý các tasks run đồng thời, ưu tiên tập trung task quan trọng để ra impact.
    
- **Tiềm năng:** 35% Research - 65% Product. Triển khai các phần MLOPs cùng team trong tương lai: LLMs, NLP, RAG, Chatbot, ... + Research Update công nghệ mới + Implement.
    
- **Nguyện vọng của em:**
    
    - Mong muốn thực tập tiếp tại công ty:
        
        - **Hybrid 4/5 buổi chiều, thời gian 3-6 tháng (hợp đồng 3 tháng 1), rate lương: 6 triệu/tháng**. Lý do:
            
        - Hybrid (offline >= 3 buổi chiều): Đảm bảo hiệu suất công việc ở mức cao nhất(tiến độ công việc được update, giảm thời gian đi lại dành thời gian làm Tasks).
            
        - Rate lương: Rate lương hiện tại đủ để tập trung làm tasks tại công ty, vừa với `Impact, Outcome hiện tại`.
            
        - Kỳ 1 năm 4 (12 tín), Kỳ 2 năm 4 (2 tín + đồ án) => Phần thời gian làm các tasks của công ty + học NLP, RAG, MLOPs, ...)
            
        - Thời gian 3-6 tháng: khoảng thời gian vừa đủ để "các sếp và em" đánh giá, nhìn lại, ...
            

---