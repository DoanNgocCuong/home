1. Bài viết hay : [9 Laws That Every Software Developer Should Know | by Jarek Orzel | Sep, 2024 | Level Up Coding](https://levelup.gitconnected.com/9-laws-that-every-software-developer-should-know-a5518bfef022)
2. [10 Best Resources to Learn Software Architecture in 2025 | by javinpaul | Javarevisited | Oct, 2024 | Medium](https://medium.com/javarevisited/10-best-resources-to-learn-software-architecture-in-2025-2524ac91dc76)


1. Software Detail Design – SDD
Mục lục
1 Introduction 4
1.1 Purpose . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 4
1.2 Scope . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 4
2 Deployment Diagram 5
3 Architecture design 6
3.1 Phân tích use case . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 6
3.1.1 Khách . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 6
Đăng nhập . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 6
3.1.2 General . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 7
Change pass word . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 7
Forgot pass word . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 7
Update personal information . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 8
3.1.3 Quản trị viên . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 8
Xoá người dùng . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 8
Thêm người dùng . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9
Xem người dùng . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9
Sửa người dùng . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9
Tìm kiếm người dùng . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 10
3.1.4 Nhóm trưởng . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 10
Quản lý ngân hàng câu hỏi . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 10
Tạo tiêu chí chấm điểm . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 11
3.1.5 Giáo viên . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 11
Quản lý đề thi . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 11
Xem lịch sử đề thi . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 12
Chấm điểm bài thi . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 12
3.1.6 Student . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 13
search and register exam code . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 13
Submit essay . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 14
View Results . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 14
View previous essays . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 15
3.2 System Architecture Design . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 15
3.3 Detailed Class Design . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 16
3.3.1 Class User . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 17
3.3.2 Class GroupLeader, Teacher, Student . . . . . . . . . . . . . . . . . . . . . . . . . 18
3.3.3 Other Classes . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 19
2
4 Data Model Design 20
4.1 Entity Relationship Diagram . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 20
4.1.1 Customer . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 20
Login . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 20
4.1.2 General . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 20
4.1.3 Admin . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 20
User Search . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 20
User Management (User Creation) . . . . . . . . . . . . . . . . . . . . . . . . . . 20
4.1.4 Group Leader . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 21
Question Bank Management . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 21
Create Grading Criteria . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 21
4.1.5 Teacher . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 22
Exam Management (Create Exam) . . . . . . . . . . . . . . . . . . . . . . . . . . 22
View Exam History . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 22
Grade Exams (Create ExamResult) . . . . . . . . . . . . . . . . . . . . . . . . . . 22
4.1.6 Student . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 22
Search and Register for Exam . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 22
Submit Essay . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 23
View Results . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 23
View History of Exam Participated . . . . . . . . . . . . . . . . . . . . . . . . . . 23
4.2 Detailed Table Design . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 24
Table User . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 24
Table QuestionBank . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 24
Table ExamResult . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 24
Table Essay . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 24
Table Question . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 25
Table ExamResultCriteria . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 25
Table Exam . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 25
Table ExamQuestion . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 25
Table Criteria . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 25
Table CriteriaDetail . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 26
5 Thiết kế giao diện 27
5.1 Giao diện với thiết bị phần cứng . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 27
5.2 Giao diện với phần mềm khác . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 27
5.3 Giao diện người dùng . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 27
5.3.1 Biểu đồ dịch chuyển màn hình . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 27
5.3.2 Thiết kế giao diện . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 29
i. Chung . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 29
ii. Quản trị viên . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 31
iii. Giáo viên . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 33
iv. Học sinh . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 36
v. Nhóm trưởng . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 38





### 1. Sequence Diagram
Tool 1: [Online FlowChart & Diagrams Editor - Mermaid Live Editor](https://mermaid.live/)


```mermaid
%%{init: {'theme': 'neutral', 'themeVariables': { 'primaryColor': '#F0F0F0', 'primaryTextColor': '#000000', 'lineColor': '#000000', 'actorBorderColor': '#333333', 'actorTextColor': '#000000' }}}%%
sequenceDiagram
    participant Guest as Guest
    participant WebClient as Web Client
    participant System as System

    Guest ->> WebClient: Select login function
    WebClient -->> Guest: Display login interface
    Guest ->> WebClient: Enter email and password
    WebClient ->> System: Send login request
    System ->> System: Verify login information
    System -->> WebClient: Return verification result
    WebClient -->> Guest: Display notification


```
	
Tool 2: [Untitled - WebSequenceDiagrams](https://www.websequencediagrams.com/app)
```[Học sinh nộp bài luận - WebSequenceDiagrams](https://www.websequencediagrams.com/app)
title Học sinh nộp bài luận

actor Học sinh
participant Giao diện
participant Hệ thống
participant Cơ sở dữ liệu

Học sinh -> Giao diện: Click vào textbox
Giao diện -> Giao diện: Hiển thị textbox để soạn thảo
Học sinh -> Giao diện: Soạn thảo câu trả lời rồi chọn nút "Nộp bài luận"
Giao diện -> Hệ thống: Hiển thị hộp thoại xác nhận nộp bài luận
alt [Chọn từ chối]
  Học sinh -> Giao diện: Chọn từ chối
else [Chọn đồng ý]
  Học sinh -> Giao diện: Chọn đồng ý
  Giao diện -> Hệ thống: Lưu thông tin và câu trả lời của học sinh
  Hệ thống -> Cơ sở dữ liệu: Lưu câu trả lời
  Cơ sở dữ liệu -> Hệ thống: Thông báo lưu thành công
  Hệ thống -> Giao diện: Thông báo: Nộp bài luận thành công
end

```

### 2. Thiết kế chi tiết gói


Dưới đây là phiên bản chi tiết biểu diễn các gói Module (M_...) với các mũi tên và quan hệ đã được sửa đúng:

```mermaid
classDiagram
    M_User <|-- M_Student
    M_User <|-- M_GroupLeader
    M_User <|-- M_Teacher

    M_GroupLeader --> M_QuestionBank : manageQuestionBank
    M_QuestionBank --> M_Question : contains
    M_Exam --> M_ExamQuestion : contains
    M_ExamQuestion --> M_Question : partOf
    M_Student --> M_Essay : submitEssay
    M_Teacher --> M_ExamResult : gradeEssay
    M_ExamResult --> M_ExamResultCriteria : associatedWith
    M_ExamResult --> M_Essay : gradeEssay
```

### Giải thích các thay đổi:

1. **Prefix `M_`**:
    
    - Đã thêm prefix `M_` để biểu diễn các module (ví dụ: `M_User`, `M_Student`,...).
2. **Quan hệ**:
    
    - Được điều chỉnh theo logic từ sơ đồ gốc:
        - `M_User` là lớp cha của các module `M_Student`, `M_GroupLeader`, và `M_Teacher`.
        - `M_GroupLeader` quản lý `M_QuestionBank`.
        - `M_QuestionBank` chứa `M_Question`.
        - `M_Exam` chứa `M_ExamQuestion`.
        - `M_ExamQuestion` là một phần của `M_Question`.
        - `M_Student` gửi bài luận (`M_Essay`).
        - `M_Teacher` chấm điểm và quản lý `M_ExamResult`.
        - `M_ExamResult` liên quan đến các tiêu chí (`M_ExamResultCriteria`) và bài luận (`M_Essay`).

- **M_User**: Stores user information in the system, including common attributes such as name, account, and roles. It serves as the parent class for specific user groups like students, group leaders, and teachers.
- **M_Student**: Defines information and functions specific to students, such as submitting essays (**submitEssay**) and viewing exam results.
- **M_GroupLeader**: Responsible for managing question banks (**manageQuestionBank**), including creating, updating, and deleting questions in the system.
- **M_Teacher**: Stores information and functions for teachers, including creating, updating, deleting exams, and grading essays (**gradeEssay**).
- **M_QuestionBank**: Stores information about question banks, which contain related questions (**contains**).
- **M_Question**: Stores detailed information about a specific question in the system. It is part of **M_QuestionBank** and linked to exams through **M_ExamQuestion**.
- **M_Exam**: Manages information about exams, including a list of questions (**contains**).
- **M_ExamQuestion**: Stores information linking exams (**M_Exam**) and questions (**M_Question**), representing a "part of" relationship (**partOf**).
- **M_Essay**: Represents student essays, submitted by **M_Student** via the **submitEssay** function and graded by teachers through **M_ExamResult**.
- **M_ExamResult**: Stores exam results, including scores and related information. These results are linked to evaluation criteria (**M_ExamResultCriteria**) and essays (**M_Essay**) to support grading.
- **M_ExamResultCriteria**: Stores grading criteria for exam results, linked to **M_ExamResult** to ensure transparency in the grading process.

Below is the Mermaid syntax to represent the **Controller package** diagram as shown in the uploaded image:

### Controller Diagram Syntax (Mermaid)

Here’s the updated **Controller** diagram corresponding to the provided Model structure:

```mermaid
classDiagram
    C_User <|-- C_Student
    C_User <|-- C_GroupLeader
    C_User <|-- C_Teacher

    C_GroupLeader --> C_QuestionBank : manageQuestionBank
    C_QuestionBank --> C_Question : contains
    C_Exam --> C_ExamQuestion : contains
    C_ExamQuestion --> C_Question : partOf
    C_Student --> C_Essay : submitEssay
    C_Teacher --> C_ExamResult : gradeEssay
    C_ExamResult --> C_ExamResultCriteria : associatedWith
    C_ExamResult --> C_Essay : gradeEssay
```

### Comments in English:

The **Controller package** diagram represents the logic-handling layer for the corresponding **Model** structure. Each controller class is dedicated to processing specific actions related to its associated model. Here’s a detailed explanation:

1. **Controller Classes**:
    
    - **C_User**: Acts as the base class for all user-related controllers, handling actions like user login, profile management, and authentication.
    - **C_Student**: Handles operations specific to students, such as submitting essays (**submitEssay**) and accessing exam results.
    - **C_GroupLeader**: Manages the question bank operations, including creating, updating, and deleting question banks (**manageQuestionBank**).
    - **C_Teacher**: Facilitates teacher-specific operations, such as creating exams, grading essays (**gradeEssay**), and reviewing student progress.
    - **C_QuestionBank**, **C_Question**: Manage question banks and their related questions, with clear relationships for "contains" and "part of."
    - **C_Exam**: Manages operations related to exams, linking with exam questions (**C_ExamQuestion**) and results.
    - **C_ExamResult**: Handles the grading and management of exam results, including linking with criteria (**C_ExamResultCriteria**) and essays.
2. **Responsibilities**:
    
    - Each controller receives requests from the **View** layer and uses the **Model** layer to process and fetch data.
    - Controllers implement the business logic needed for specific tasks, ensuring a clear separation of concerns.
3. **Highlights**:
    
    - **Modular Design**: Each controller class is focused on a single domain, enhancing maintainability and reducing coupling.
    - **MVC Integration**: The controllers bridge the View and Model layers, maintaining a smooth data flow and interaction.
    - **Scalability**: Adding new functionality or extending existing ones (e.g., new user types or features for teachers) is straightforward due to the structured controller hierarchy.

This design ensures a robust and scalable system that adheres to **MVC principles**, making it easy to maintain, test, and extend over time.
### Hướng dẫn sử dụng:

Bạn có thể sao chép đoạn mã này vào [Mermaid Live Editor](https://mermaid.live/) để kiểm tra hoặc hiển thị sơ đồ. Nếu cần thêm chỉnh sửa hoặc chi tiết khác, hãy cho mình biết!

Chi tiết hơn thì 

![[Pasted image 20241209001709.png]]