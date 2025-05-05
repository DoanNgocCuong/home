

1. Tool lớp check ngữ pháp; Check trong intent đúng, check tool 
-> ảnh hưởng response time. (sửa phát âm có cần extract hay làm gì nữa ko, ...)


## Danh sách flow bài học

|   |   |   |   |
|---|---|---|---|
|**STT**|**Bài học**|**Ví dụ**|**Vấn đề**|
|1|Có sẵn cụm từ và các câu có blank để hỏi|Pika "Cậu đang ở nhà bạn, và bạn ấy đang chơi trò chơi điện tử. Cậu cũng muốn chơi. Cậu sẽ nói, 'Can I ________ with you, please?' Từ nào điền vào chỗ trống?" Correct Answer "play video games!"||
|2|Có sẵn cụm từ và các đáp án để chọn|Pika "Đến giờ kiểm tra rồi! Tớ sẽ hỏi cậu một vài câu hỏi và cậu hãy chọn đáp án đúng nhé. Sẵn sàng chưa?" "Cậu làm gì ngay sau khi thức dậy? Là A) eat dinner, B) brush teeth, hay C) go to bed?"||
|3|Hỏi từ trong 1 topic|Pika "Được rồi, bây giờ chúng ta sẽ chơi một trò chơi! Hãy kể tên nhiều từ thuộc cùng 1 chủ đề nhé. Mỗi câu trả lời đúng sẽ được 1 điểm. Điểm cao nhất của tớ là 4, để xem cậu có đánh bại được tớ không nhé! Chủ đề lần này là hành động bắt đầu bằng từ "play". Tớ ví dụ nhé, "Play video games", đến lượt cậu nhé"||
|4|Sắp xếp lại từ thành câu đúng|Pika "Games playing I video love." Correct Answer "I love playing video games!"||
|5|Mở rộng cuộc hội thoại follow up theo câu trả lời của user|Start of the Day Pika "Good morning! Let’s start your day. First, do you want to A) Get out of bed B) Sleep more" Learner’s Response "Get out of bed." Pika "Great! Now you’re up. What do you do next? A) Eat breakfast B) Take a shower" Learner’s Response "Eat breakfast." Pika "Aah, you had a big breakfast! Next, what will you do? A) Brush your teeth B) Read a book"||
|6|Fill từ để đủ 1 đoạn|"I wake up at __________. Then, I __________. After that, I __________. In the afternoon, I usually __________. At night, I like to __________." Learner responds "I wake up at 700 am. Then, I brush my teeth and eat breakfast. After that, I go to school. In the afternoon, I usually play outside with my friends. At night, I like to read before bed."||
|7|Dạy các chunk có sẵn -> dạy câu có sẵn từ các chunk -> Dạy đoạn có sẵn từ các câu|Wake up -> I wake up at 7 am,... -> In the morning, I wake up at 7 a.m. After that,...||
|8|Dạy cách từ trong 1 topic user thích|Cậu thích học chủ đề gì -> Đồ ăn -> Cậu thích ăn gì -> Dạy các món user nói trong tiếng Anh||

  

  

## Một số case chưa ngon trên workflow

|   |   |   |
|---|---|---|
|**Tình huống**|**Conversation Sample**|**Hướng handle**|
|Hỏi tiếp để lấy chủ đề người học thích|Pika: "Hôm nay cậu thích học về chủ đề gì? Đồ ăn, thể thao hay động vật?" Người học: "Đồ ăn." Pika: "Tuyệt vời! Cùng tớ học các từ vựng về đồ ăn nhé. Tớ sẽ hỏi một vài câu để khởi động. Bắt đầu nào!"|?|
|Người học hỏi lại về một từ trong câu|Pika: "Chúng ta cùng thêm thông tin để tạo câu hoàn chỉnh nhé. I go to school with my family." Người học: "Family là gì? Cậu giải thích cho tớ được không?" Pika: "Family nghĩa là 'gia đình' – gồm bố, mẹ, anh chị em. Tớ lấy ví dụ nhé: I love my family."|?|
|Tính điểm sau một số câu hỏi|Pika: "Cậu trả lời rất tốt trong 5 câu vừa rồi. Tớ sẽ tính điểm nhé! Cậu được 4/5 điểm. Lần sau hãy cố gắng thêm nhé. Chúng ta thử một câu nữa nhé?"|?|
|Tiếp tục đoạn hội thoại từ câu trả lời của người học|Pika: "Good morning! Let’s start your day. First, do you want to: A) Get out of bed B) Sleep more? Người học: "Get out of bed." Pika: "Great! Now you’re up. What do you do next? A) Eat breakfast B) Take a shower" Người học: "Eat breakfast." Pika: "Nice choice! Breakfast is the most important meal of the day. What will you eat for breakfast today?"|Dài|
|Sửa câu sai nhiều lỗi|Pika: "Câu cậu nói là: 'I goes to the school every days.' Có một số lỗi nhé! Chúng ta sửa lại nào: - 'Goes' phải là 'go' vì chủ ngữ là 'I'. - 'The school' chỉ cần nói 'school' thôi nếu ý là trường học nói chung. - 'Every days' sửa thành 'every day'. Vậy câu đúng sẽ là: 'I go to school every day.' Cùng nói lại nào!"||
|Sửa lỗi phát âm|Pika: "Cậu vừa nói 'thíng' thay vì 'thing'. Âm /θ/ cần đặt đầu lưỡi giữa răng và thổi nhẹ. Nghe tớ nhé: 'thing'. Bây giờ cậu thử lại nào!"||
|Sửa lỗi ngữ pháp|Pika: "Câu của cậu là 'She don’t like apples.' Chúng ta sửa lại chút nhé! Với 'she', động từ phải dùng 'doesn't'. Câu đúng là: 'She doesn't like apples.' Nói thử nào!"|? - ảnh hưởng response time - tool|
|Người học đổi chủ đề giữa chừng|Người học: "Tớ không muốn nói về đồ ăn nữa. Chúng ta nói về bóng đá đi!" Pika: "Chắc chắn rồi! Bóng đá là môn thể thao thú vị. Cậu có đội bóng yêu thích không?"|? - out scope Handle đc|
|Người học chào giữa đoạn hội thoại|Người học: "Chào cậu, tớ đi đây"|? - out scope Handle đc|

### Gen content follow up

- Các đoạn cần **hỏi follow-up theo câu trả lời của user.** Thường có ở đầu bài hoặc các đoạn hỏi để lấy topic,...
    
- **Gen ra các từ để học** trong buổi hôm đó từ 1 topic user thích. Hôm nay cậu thích học về chủ đề gì? -> Đồ ăn
    
- **User hỏi ngược** về 1 kiến thức trong câu. Ví dụ: "Chúng ta cùng thêm thông tin để tạo câu hoàn chỉnh nhé. I go to school with my family" -> User hỏi lại family là gì? Cậu giải thích cho tớ được ko?
    
- Tính điểm cho các câu trả lời: Sau 5 câu, có tổng bao nhiêu điểm (cái này discuss thêm, backend sẽ xử lý đc)
    
- Gen tiếp đoạn hội thoại từ câu trả lời của user.
    
      Pika "Good morning! Let’s start your day. First, do you want to
    
      A) Get out of bed
    
      B) Sleep more"
    
      Learner’s Response "Get out of bed."
    
      
    
      Pika "Great! Now you’re up. What do you do next?
    
      A) Eat breakfast
    
      B) Take a shower"
    
      Learner’s Response "Eat breakfast."
    

  

### Các case sửa lỗi sai:

- Nói lại đoạn mẫu sai nhiều chỗ
    
- Sai phát âm
    
- Sai ngữ pháp
    
- ...
    

## Các case hiếm gặp khác:

- User muốn nói về 1 chủ đề khác
    
- User chào giữa luồng
    

  

*Case phát âm gần đúng: Vegetable - vettable => Xử lý cover ASR

*Độ chi tiết của bộ nhãn LLM


---

Response time cho bài ROBOT: 
