Toàn bộ các link quan trọng:

1. Link Task Manager: [Team Management](https://stepupenglish.sg.larksuite.com/docx/IMd1dyI6qojomlx7Ddol3S05gNb?table=tblc8CmGjl7QKPi6&view=vewuCREkVn&302from=wiki)
    
2. https://stepup-english.atlassian.net/wiki/spaces/RP/pages/edit-v2/1148026881
    
3. https://stepup-english.atlassian.net/wiki/spaces/TCT/pages/1132527620/Onion+Assistant+V2+-+th+n+o+l+1+output+y+c+production
    

# 2025

## July

### Week 3 - July

  

- Robot: - Info: ver 1 bản fast response cứng, ver 2 bản a Hoài. - Output: 1. Bản fast response mới demo cho chị Trang. - Input: conversation user thực + Pila bibble, ví dụ về fast response (tài liệu) - Outcome: tăng content, sau dùng để check data finetune. Doing: - Ra ver1 chị Trang sáng T3 - Check cách a Hoài đang làm thành của mình.
    
- Robot: Memory Robot: Output: 1. Use case Memory được các bên thống nhất (Dịu, a Minh, c Trang). - AI First: memory Use cases - Brainstorm với các bên 2. 1 report về check lại toàn bộ cách a Hoài đang làm (tách các phần) - Data finetune, model, ... Test model - Test luồng, update.
    
- TheCoach (Cá nhân hóa): - Dựng full luồng auto build kho cá nhân hóa. Info: Nhận Prompt + Format ouput. Output: 1. 1 file Figma luông confirm với a Trúc và gửi team. 2. 1 luồng tự động từ Input USER PROFILE(ngành nghề, job level, user info) => Kho bài học cá nhân hóa cho các nhóm USER PROFILE. (ver1) 3. Đóng gói lại tài liệu vào Jira. ---
    

  

|            |                                     |                                                                       |
| ---------- | ----------------------------------- | --------------------------------------------------------------------- |
| Day        | Hôm qua                             | Hôm nay                                                               |
| 16/07/2025 | Update V3 - Fast Response chị Trang | 1. Dựng full luồng build 1000 Nghề gồm AI Automation + Service a Hiến |
|            |                                     |                                                                       |
|            |                                     |                                                                       |
|            |                                     |                                                                       |
|            |                                     |                                                                       |

## Tháng 7/2025

1. **MINDSET**
    

|   |   |   |
|---|---|---|
|Problem||Solve|
|Output đưa ra cho các bên chưa chuẩn, chẳng hạn: - Có thể tự check kỹ hơn output trước khi gửi cho chị Trang||- CHỊU TRÁCH NHIỆM CHO TỪNG BÀI MÌNH LÀM.Define DOD kỹ: (Phản biện DOD của người ra đề / Tự define DOD cho mình).  <br>- QC: Đặt mình vào vai trò của người ra đề để QC trước.|
|Chưa code chính phần nào của Robot, mới chỉ đọc qua qua bên ngoài. / Học kiến thức ngoài chưa dùng được hoặc dùng hiệu quả chỉ khi vào dự án||LEARN NHANH = VIỆC VÀO DỰ ÁN THẬT + NHẬN FEEDBACK|

2. **PHÂN BỔ:**
    

|                           |                                                                                                                                                          |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1. AI ENGINEERING ROLE    | AI Engineering: 10 % Research Model + 70% Engineering (MLOps, System Design) + 10 % AI Application (Prompting, AI Workflow, Tools, ...) + 10% Product.   |
| Giai đoạn 1 (2-3 năm tới) | 10% Research Model (4 điểm) + 70% Engineering (MLOps, System Design) (4 điểm -> 10 điểm) + 10% AI Application (7 điểm) + 10% Product (3 điểm -> 5 điểm). |
| Giai đoạn 2               | Research Model (4 điểm) + Engineering (MLOps, System Design) (10 -> 100 điểm) + AI Application (7 điểm) + Product (5 điểm -> 10 điểm).                   |

  

**Các tasks chính trong 6 tháng tới:**

  

|   |   |   |
|---|---|---|
|1. Engneering|- Robot 80%: Incharge dần code tiếp, sau refactor phần anh Hùng,  <br>(giao tiếp BE, FE, Test, PO)  <br>  <br>- TheCoach 20%|Dài hạn|
|2. Prompting|- AI Worlflow 1000 Nghề (support a Trúc, a Vũ)  <br>- AI Prompting, Workflow: Build bài chị Trang.|- Workflow 1000 Nghề ko quá khó  <br>- Bài chị Trang cần Problem Solving 2 tuần tới.|

  
### 22/07/2025 - 27/07/2025 

#### Task 1000 Nghề: 
##### KR1: 
- Output 1: 1 output code. Từ execel hiện tại -> đẩy ra đúng format hiện giờ ở trong DB. Bằng AI Code 1 prompt. 
  -=> Chuyển hướng khác đi. 
  +, Step 1: Run lấy Scenario bằng Dify 
  +, Step 2: Run code excel để lấy ra user_id từ việc map các phần 
  Lấy topic và các phần liên quan để gen outcome_topic 
  và mapping với từng dòng của scenario ở từng stakeholder. 
  
  Có cách nào tối ưu hơn ko? 
  +, Tại sao ko run để lấy outcome_topic bằng Dify? 
  (Từ file excel chạy code trung gian để tạo ra 1 file trung gian là file có full các phần gom outcome_topic), sau đó mới chạy 
  


  
  Ra hết các tường cần thiết cho việc import và hiển thị, 
- Output 2: Test kiểm tra output đó kĩ trên web đã từng tự dựng 
- Output 3: ping a Hiến để check


Bàn về cách làm tối ưu: 

Mục tiêu chính là: ra được chuẩn JSON format. 


![[Pasted image 20250724105731.png]]


KR1: Thông luồng từ file excel chưa có outcome_topic, scenario, detail scenario -> ra file excel final
- Cần thêm 1 API từ cả cục topic ra topic_outcome và scenario luôn. 

+, 1. File từ excel ra 



---

KR2: Xây DB dựa trên file excel đã thống nhất. 
- Hướng 1: Tự xây DB theo tagging của mình, chỉ cần query 1 bảng và chơi trò define theo tags. 
- Hướng 2: Chơi trò define chuẩn từng bảng từng bảng. Có thể suy nghĩ triển khai sau? 

Liên quan đến việc Search và Query: 
- Search như nào, 
- Query như nào, 
  
  Khi user search các thứ thì bảng nên được làm như nào

---
KR3: Thông luồng từ chỗ chị Thủy sang chỗ a Vũ  

---


# Define 3O1T (Outcome - Output DOS - Tasks)

| Result (Hook: ở đây có ai muốn đạt được điều gì đó)                        |      |
| -------------------------------------------------------------------------- | ---- |
| Situation                                                                  |      |
| Think (nghĩ, cảm thấy Feel, <br>vì sao đặt câu hỏi phản biện Nếu ) - 80-20 | <br> |
| Action                                                                     | <br> |
| Results                                                                    |      |
| Call to action                                                             |      |

| **3O1T**                                                    | **OKRs**                                     |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | Kết luận                                                                                                                                                                                                                                            | Estimate Time |
| ----------------------------------------------------------- | -------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------- |
| ✅ **Objective**                                             | Objective cảm hứng và hướng mục tiêu dài hạn |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |                                                                                                                                                                                                                                                     |               |
| 🎯 **Outcome**                                              | Why?                                         | - Tại sao phải làm cái task này nhỉ? -> Để ra được 1000 Nghề. <br>- Làm phần 1000 Nghề để làm gì nhỉ, để ra tiền ? Có chắc là làm bài 1000 Nghề thì ra tiền ko?  => <br>- Để làm 1000 Nghề chúng ta hiện tại đang build 1 thư viện khổng ồ với 1000 Nghề.<br>+, Mục đích của việc test định tính và định lượng các jobs hiện tại là gì ? <br>Là để verify được là ông user A, user B đang thích cái nào hơn.<br>+, Thu thập những cái user A, user B thích đó thì sẽ dựa vào log để lọc các tình huống user ko thích đi. <br>+, Sau khi user điền khảo sát là thích và không thích, quá trình lọc được tiến hành để loại bỏ những thứ không cần thiết.<br><br>+, Outcome nên mô tả ngắn gọn như nào | +, Tăng trải nghiệm của user với việc tôi có sẵn 1000 Nghề, user ngành nghề nào thì cũng đều có lộ trình đã được cá nhân hóa.                                                                                                                       |               |
| 📦 **Output**<br>- 📊 **Metrics**<br>- ✔ **Define to Done** | Key Results 1, 2, 3 cụ thể, đo lường được    | Output cần trả ra là gì: <br>- 1 cái web khảo sát: User nhập và chọn ngành nghề (bên trong là thuật toán cơ chế cho việc Search DB như nào) và                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | Output 1: Data cá nhân hóa khớp cho các nhóm ngành nghề khác nhau                                                                                                                                                                                   |               |
| 🧩 **Tasks**                                                | 🧩Actions                                    | - Cách kiến trúc db như nào để trả ra được output đó? Có cần phối hợp gì với DB phía a Quân không?<br>- Hay chỉ đơn giản là lên được web khảo sát trước , theo bạn thì sao? <br>-                                                                                 Cách đang làm: <br>- Dựng 1 DB với các bảng sau <br><br>+, Bảng user_profile chứa <br>user_id và JSON data (JSOn chứa chung topic, scenario, detail scenario)<br>+, Bảng user_profile này <br><br>- Cắm API đoạn domain -> JTBD? <br>() ày                                                                                                                                                                                        | 1. Cắm API Pika để chạy từng ngành nghề<br>+, Input chia nhóm ngành nghề chỗ chị Thủy chuẩn <br>+, Input chỗ a Vũ Prompt chuẩn <br>+, Luồng chạy của Cường bé chuẩn <br>2. Prompt/Agent đánh giá output xem có vấn đề gì ko? <br>3. Search Database |               |
| 🧩 **Tasks**                                                |                                              |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |                                                                                                                                                                                                                                                     |               |

Đâu là cấu trúc Structure để làm việc hiệu quả

```
Mục tiêu của tôi là: làm việc mọi việc với việc rõ 3O1T (Object, Outcome, Output, Tasks)

Hãy giúp tôi giải quyết vấn đề trên

Nhưng đầu tiên hãy tách lớp thành cấu trúc 4-5 phần quan trọng nhất tác động đến B ....... (sắp xếp theo thứ tự)

Trong mỗi cấu trúc nhỏ chỉ rõ kết quả đầu ra rõ ràng
```


---

| **3O1T**                                                    | **OKRs**                                                                                                                                                           |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | Kết luận                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | Estimate Time |
| ----------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------- |
| ✅ **Objective**                                             |                                                                                                                                                                    |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |               |
| 🎯 **Outcome**                                              | Why?<br>Đánh giá ưu tiên <br>- Mentor đánh giá? <br>- Impact (Làm thì sao, ko làm thì sao)<br>- Time (có gấp ko)<br>- Risk (Tệ nhất là gì? giảm cái tệ đi được ko) | Fast Response nhanh và siêu cute                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |               |
| 📦 **Output**<br>- 📊 **Metrics**<br>- ✔ **Define to Done** | Key Results 1, 2, 3 cụ thể, đo lường được                                                                                                                          | Output cần trả ra là gì: <br>- 1 cái web khảo sát: User nhập và chọn ngành nghề (bên trong là thuật toán cơ chế cho việc Search DB như nào) và                                                                                                                                                                                                                                                                                                                                                               | Output 1: Data cá nhân hóa khớp cho các nhóm ngành nghề khác nhau                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |               |
| 🧩 **Tasks**                                                | 🧩Actions                                                                                                                                                          | - Cách kiến trúc db như nào để trả ra được output đó? Có cần phối hợp gì với DB phía a Quân không?<br>- Hay chỉ đơn giản là lên được web khảo sát trước , theo bạn thì sao? <br>-                                                                                 Cách đang làm: <br>- Dựng 1 DB với các bảng sau <br><br>+, Bảng user_profile chứa <br>user_id và JSON data (JSOn chứa chung topic, scenario, detail scenario)<br>+, Bảng user_profile này <br><br>- Cắm API đoạn domain -> JTBD? <br>() ày | 1. Cắm API Pika để chạy từng ngành nghề<br>+, Input chia nhóm ngành nghề chỗ chị Thủy chuẩn <br>+, Input chỗ a Vũ Prompt chuẩn <br>+, Luồng chạy của Cường bé chuẩn <br>2. Prompt/Agent đánh giá output xem có vấn đề gì ko? <br>- Outcome là: đánh giá được chất lượng output trả ra???<br>- Output là số trả ra với các metrics quan trọng: <br>+, Độ chính xác <br>+, ....<br>- How: Cách đánh giá như thế nào??? <br>Cách nào để thực hiện việc đánh giá từ 5-10 topic (tương đương với 250-300 dòng excel????)<br><br>3. Search Database |               |
| 🧩 **Tasks**                                                |                                                                                                                                                                    |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |               |



----

# 3. 3 version cho tasks 1000 nghề 

- Version 1: 
  <industry_job-role_job-level>
- Version 2: 
  <domain_group_job-role_job-level_industry> 
  +, Với việc có group chung cho toàn bộ job-role trong domain, group riêng cho từng job-role 
  +, Với việc có domain, group_job-role_job-level thì industry khác nhau nó có output khác nhau 
- Version 3: 
  <industry_job-role_job-level> và <domain> 
  +, Khi user điền indutry và job-role, nó mapping trực tiếp với lộ trình của industry và job-role đó. 
  +, Khi user điền thông tin sai khác đi, thì cố gắng recommend cho đúng job-role có trong DB và Group đúng của nó. 
  +, Khi user điền sai bét nhè, thì recommend <domain> đúng. 

---


