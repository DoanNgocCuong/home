


```mermaid

classDiagram
    %% VIEWER LAYER (Presentation Layer)
    package "Viewer Layer" {
        class AttendExam {
            + displayAttendExam(): void
        }
        class AutoGrade {
            + displayAutoGrading(): void
        }
        class ChangePassword {
            + displayChangePasswordForm(): void
        }
        class CreateQuestion {
            + displayCreateQuestionForm(): void
        }
        class CreateTest {
            + displayCreateTestInterface(): void
        }
        class Login {
            + displayLoginForm(): void
        }
        class LoginInvalid {
            + displayErrorMessage(): void
        }
        class ManualMark {
            + displayManualGrading(): void
        }
        class LayoutsPartials {
            + renderSharedTemplates(): void
        }
    }

    %% CONTROLLER LAYER (Business Layer)
    package "Controller Layer" {
        class UserController {
            + handleLogin(): void
            + handleChangePassword(): void
            + handleProfileManagement(): void
        }
        class StudentController {
            + handleEssaySubmission(): void
            + handleViewResults(): void
        }
        class GroupLeaderController {
            + manageQuestionBank(): void
            + createQuestion(): void
        }
        class TeacherController {
            + handleExamCreation(): void
            + handleGradeEssay(): void
        }
        class ExamController {
            + manageExam(): void
            + linkExamQuestions(): void
        }
        class ExamResultController {
            + handleGrading(): void
            + calculateScore(): void
        }
    }

    %% MODEL LAYER (Data Layer)
    package "Model Layer" {
        class User {
            - username: String
            - password: String
            - role: String
            - fullName: String
            - birthday: Date
            - gender: String
        }
        class GroupLeader {
            + manageQuestionBank(): void
        }
        class Teacher {
            + createExam(): void
            + gradeEssay(): void
        }
        class Student {
            + submitEssay(): void
            + viewResults(): void
        }
        class QuestionBank {
            - id: int
            - name: String
            + addQuestion(): void
        }
        class Question {
            - id: int
            - content: String
            + evaluateAnswer(): void
        }
        class Exam {
            - id: int
            - title: String
            + addQuestion(): void
        }
        class ExamResult {
            - score: float
            + calculateFinalScore(): void
        }
        class Essay {
            - id: int
            - content: String
            + submit(): void
        }
    }

    %% DEPENDENCIES
    AttendExam --> StudentController : interacts
    AutoGrade --> TeacherController : interacts
    ChangePassword --> UserController : interacts
    CreateQuestion --> GroupLeaderController : interacts
    CreateTest --> TeacherController : interacts
    Login --> UserController : interacts
    LoginInvalid --> UserController : handlesError
    ManualMark --> TeacherController : interacts

    UserController --> User : manages
    StudentController --> Student : manages
    StudentController --> Essay : submits
    TeacherController --> Exam : manages
    TeacherController --> ExamResult : grades
    GroupLeaderController --> QuestionBank : manages
    ExamController --> Exam : linksQuestions
    ExamResultController --> ExamResult : calculates

```



```mermaid
classDiagram
    %% Controller Classes
    class userController {
        +handleLogin(username: String, password: String): void
        +handleChangePassword(oldPassword: String, newPassword: String): void
        +handleForgotPassword(email: String): void
        +handleUpdatePersonalInfo(user: User): void
        +handleDeleteUser(id: int): void
        +handleAddUser(user: User): void
        +handleViewUser(): void
        +handleEditUser(user: User): void
        +handleSearchUser(criteria: String): void
    }

    class groupLeaderController {
        +handleAddQuestion(question: Question): void
        +handleDeleteQuestion(id: int): void
    }

    class questionBankController {
        +handleAddQuestion(question: Question): void
        +handleDeleteQuestion(id: int): void
    }

    class criteriaController {
        +handleCreateCriteria(criteria: Criteria, details: List<CriteriaDetail>): void
    }

    class teacherController {
        +handleCreateExam(exam: Exam): void
        +handleGradeEssay(essay: Essay, score: float, feedback: String): void
    }

    class examController {
        +handleCreateExam(exam: Exam): void
        +handleRetrieveExamByCode(code: String): Exam
    }

    class essayController {
        +handleSubmitEssay(essay: Essay): void
        +handleRetrieveEssaysForGrading(): List<Essay>
    }

    class examResultController {
        +handleRetrieveExamResults(student: Student): List<ExamResult>
        +handleSaveExamResult(result: ExamResult): void
    }

    class studentController {
        +handleRegisterExam(exam: Exam, student: Student): void
    }

    %% Relationships
    groupLeaderController --> questionBankController : interactsWith
    teacherController --> examController : manages
    essayController --> examResultController : interactsWith
    studentController --> examController : interactsWith

```

```mermaid
classDiagram
    userController <|-- studentController
    userController <|-- groupLeaderController
    userController <|-- teacherController

    groupLeaderController : manageQuestionBank
    questionBank : contains
    exam : contains
    examQuestion : partOf
    studentController : submitEssay
    teacherController : gradeEssay
    examResult : associatedWith
    examResult : gradeEssay

```


```mermaid
classDiagram

    class attendexam {

        Provides UI for attending exams

    }

    class autograde {

        Interface for automatic essay grading

    }

    class changepassword {

        Password change functionality

    }

    class createquestion {

        View for creating questions

    }

    class createtest {

        Test creation interface

    }

    class login {

        Login interface for users

    }

    class login_invalid {

        Displays error for invalid login

    }

    class manualmark {

        Interface for manual grading

    }
```


----------------
### **Class: attendexam**

#### **Attributes**

|**Attribute**|**Type**|**Access Modifier**|**Description**|
|---|---|---|---|
|`examId`|`String`|`private`|Stores the ID of the exam being attended.|
|`studentId`|`String`|`private`|Stores the ID of the student attending the exam.|

#### **Methods**

|**Method**|**Return Type**|**Arguments**|**Access Modifiers**|**Description**|
|---|---|---|---|---|
|`displayExamInterface`|`void`|`-`|`public`|Displays the exam participation interface.|
|`displaySuccessMessage`|`void`|`message: String`|`public`|Displays a success message.|
|`displayErrorMessage`|`void`|`message: String`|`public`|Displays an error message.|

---

### **Class: autograde**

#### **Attributes**

|**Attribute**|**Type**|**Access Modifier**|**Description**|
|---|---|---|---|
|`grades`|`List<Grade>`|`private`|Stores the grades generated by the autograding process.|

#### **Methods**

|**Method**|**Return Type**|**Arguments**|**Access Modifiers**|**Description**|
|---|---|---|---|---|
|`displayGradeSummary`|`void`|`grades: List<Grade>`|`public`|Displays automatically graded results.|
|`displaySuccessMessage`|`void`|`message: String`|`public`|Displays a success message.|

---

### **Class: changepassword**

#### **Attributes**

|**Attribute**|**Type**|**Access Modifier**|**Description**|
|---|---|---|---|
|`userId`|`String`|`private`|Stores the ID of the user changing their password.|
|`newPassword`|`String`|`private`|Stores the new password entered by the user.|

#### **Methods**

|**Method**|**Return Type**|**Arguments**|**Access Modifiers**|**Description**|
|---|---|---|---|---|
|`displayChangePasswordForm`|`void`|`-`|`public`|Displays the change password form.|
|`displaySuccessMessage`|`void`|`message: String`|`public`|Displays a success message.|
|`displayErrorMessage`|`void`|`message: String`|`public`|Displays an error message.|

---

### **Class: createquestion**

#### **Attributes**

|**Attribute**|**Type**|**Access Modifier**|**Description**|
|---|---|---|---|
|`questionId`|`String`|`private`|Stores the ID of the question being created.|
|`questionDetails`|`String`|`private`|Stores the details of the new question.|

#### **Methods**

|**Method**|**Return Type**|**Arguments**|**Access Modifiers**|**Description**|
|---|---|---|---|---|
|`displayQuestionForm`|`void`|`-`|`public`|Displays the form to add a new question.|
|`displaySuccessMessage`|`void`|`message: String`|`public`|Displays a success message.|

---

### **Class: createtest**

#### **Attributes**

|**Attribute**|**Type**|**Access Modifier**|**Description**|
|---|---|---|---|
|`testId`|`String`|`private`|Stores the ID of the test being created.|
|`testDetails`|`String`|`private`|Stores the details of the new test.|

#### **Methods**

|**Method**|**Return Type**|**Arguments**|**Access Modifiers**|**Description**|
|---|---|---|---|---|
|`displayTestCreationForm`|`void`|`-`|`public`|Displays the test creation interface.|
|`displaySuccessMessage`|`void`|`message: String`|`public`|Displays a success message.|

---

### **Class: login**

#### **Attributes**

|**Attribute**|**Type**|**Access Modifier**|**Description**|
|---|---|---|---|
|`username`|`String`|`private`|Stores the username entered by the user.|
|`password`|`String`|`private`|Stores the password entered by the user.|

#### **Methods**

|**Method**|**Return Type**|**Arguments**|**Access Modifiers**|**Description**|
|---|---|---|---|---|
|`displayLoginForm`|`void`|`-`|`public`|Displays the login interface.|
|`displaySuccessMessage`|`void`|`message: String`|`public`|Displays a success message.|


---

### **Class: login_invalid**

#### **Attributes**

|**Attribute**|**Type**|**Access Modifier**|**Description**|
|---|---|---|---|
|`errorMessage`|`String`|`private`|Stores the error message for invalid login.|
|`errorTimestamp`|`DateTime`|`private`|Stores the timestamp when the error occurred.|

#### **Methods**

|**Method**|**Return Type**|**Arguments**|**Access Modifiers**|**Description**|
|---|---|---|---|---|
|`displayInvalidLoginError`|`void`|`message: String`|`public`|Displays an error message for invalid login.|
|`logErrorDetails`|`void`|`message: String, timestamp: DateTime`|`private`|Logs the error details internally for tracking.|

---

### **Class: manualmark**

#### **Attributes**

|**Attribute**|**Type**|**Access Modifier**|**Description**|
|---|---|---|---|
|`essayList`|`List<Essay>`|`private`|Stores the list of essays for grading.|
|`currentEssay`|`Essay`|`private`|Stores the essay currently being graded.|
|`gradingCriteria`|`String`|`private`|Stores the criteria for manual grading.|

#### **Methods**

|**Method**|**Return Type**|**Arguments**|**Access Modifiers**|**Description**|
|---|---|---|---|---|
|`displayEssaysForGrading`|`void`|`essays: List<Essay>`|`public`|Displays the list of essays to be graded.|
|`displayGradingForm`|`void`|`essay: Essay`|`public`|Displays the grading form for a specific essay.|
|`submitGrade`|`void`|`essayId: String, grade: String`|`public`|Submits the grade for a specific essay.|
|`displaySuccessMessage`|`void`|`message: String`|`public`|Displays a success message after grading.|
|`displayErrorMessage`|`void`|`message: String`|`public`|Displays an error message if grading fails.|

---
