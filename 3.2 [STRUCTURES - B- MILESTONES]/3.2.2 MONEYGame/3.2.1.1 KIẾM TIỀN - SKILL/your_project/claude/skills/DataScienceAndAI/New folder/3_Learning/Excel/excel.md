

Ctrl Shift xuống, Ctrl D


=TRIM(CLEAN(A1))



```
=IF(ISNUMBER(SEARCH("true", M5)), 1, 0)
=IF(ISNUMBER(SEARCH("""F1"": 1", J2)), 1, 0)
=OR(ISNUMBER(SEARCH(A166, F166)), ISNUMBER(SEARCH(A166, G166)), ISNUMBER(SEARCH(A166, H166)))
=IF(ISTEXT(Q2), 1, 0)
=PERCENTILE(P1:P1001, 0.95)
```



```
"{ ""ground_truth"": [] }" => 0 "{ ""ground_truth"": [""AI Research & Model Development""] }" => 1 "{ ""ground_truth"": [""AI Research & Model Development"", ""Machine leanring""] }" => 2 Đếm số phần tử trong list, bằng excel
=IFERROR((LEN(F2) - LEN(SUBSTITUTE(F2, """", "")))/2 - 1, 0)
```

```
=REGEXEXTRACT(D1, "\{[^\}]*ground_truth[^\}]*\]")
```

```
=IF(ISBLANK(A1), 0, 1)
```


Bạn chỉ cần dùng công thức **IF + SEARCH** trong Excel là được. Với ô `P2`, công thức như sau:

`=IF(ISNUMBER(SEARCH("NULL",P2)),0,1)`

- Nếu trong P2 có chứa chữ `"NULL"` → kết quả **0**
    
- Nếu không có `"NULL"` → kết quả **1**
    

---

⚠️ Lưu ý: `SEARCH` không phân biệt hoa thường (NULL, null, Null đều được tính).  
Nếu bạn muốn phân biệt chính xác hoa/thường, dùng `FIND` thay cho `SEARCH`:

`=IF(ISNUMBER(FIND("NULL",P2)),0,1)`

---
Cách lấy UNIQUE từ 1 cột. 

```
=UNIQUE(A:A)
```

|            |                  |          |                                                                                                                           |                                   |                        |                        |                                                                                                                                                                                                                                                                                                                                          |
| ---------- | ---------------- | -------- | ------------------------------------------------------------------------------------------------------------------------- | --------------------------------- | ---------------------- | ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 20/08/2025 | GroundTruth loại | Tổng mẫu | Phân tích chi tiết                                                                                                        | Kết quả chính                     | % Accuracy so với Loại | % Accuracy so với Tổng | Lý do                                                                                                                                                                                                                                                                                                                                    |
| Cường bé   | {} (rỗng)        | 361      | - Predict {}: 148  <br>- Predict GT rỗng: 213  <br>• Học sinh = 45 (12.4%)  <br>• Còn lại 168: 111 False (30.7%), 57 True | Accuracy = (148+57)/361 = 205/361 | 56.70%                 | 6.91%                  | 1. Bổ sung lộ trình cho Role: Học sinh, Sinh viên. 2. Trường hợp False chủ yếu do:  <br>- Noise / chữ vô nghĩa (Gbb, Kkk, Beeeeee…)  <br>- Role không rõ hoặc quá chung chung (Nhân viên, Senior, Applicant…)  <br>- Sai domain / mapping lệch (Đầu bếp → BĐS)  <br>- Level học tập thay vì nghề (Sinh viên, Thực tập sinh, hs, Cấp 2…). |
|            | Có 1 phần tử     | 891      | - Predict True (TP): 849  <br>- Predict False (FN): 42                                                                    | Accuracy ≈ 849/891                | 95.30%                 | 28.61%                 | Cần check kỹ để bổ sung thêm vào description.                                                                                                                                                                                                                                                                                            |
|            | Có ≥ 2 phần tử   | 1706     | - TP ≥ 1 (đúng ≥ 1 phần tử): 1436  <br>- TP = 0 (sai hoàn toàn): 270                                                      | TP ≥ 1 đúng = 1436/1706           | 84.20%                 | 48.38%                 | Các case này cũng cần check kỹ để bổ sung vào description.                                                                                                                                                                                                                                                                               |
|            | Tổng hợp chung   | 2968     | Đúng = 205 + 849 + 1436 = 2489                                                                                            | Accuracy chung = 2489/2968        | 83.80%                 | 83.89%                 | —                                                                                                                                                                                                                                                                                                                                        |


---
Rồi 👍 mình tóm gọn như sau:

---

### 1. Công thức ban đầu

```excel
=VLOOKUP(Interview_aVu_CuongBe!C2, Database!A2:B289, 2, FALSE)
```

- Tìm giá trị `C2` trong **cột A** (phạm vi A2:A289).
    
- Nếu khớp → trả về giá trị tương ứng ở **cột B**.
    
- Hạn chế: chỉ quét đến dòng 289, và **không thể tìm trong cột B để trả về A**.
    

---

### 2. Công thức với mảng giới hạn dòng

```excel
=VLOOKUP(Interview_aVu_CuongBe!C2, {Database!B2:B289, Database!A2:A289}, 2, FALSE)
```

- Đảo thứ tự cột bằng cách tạo mảng tạm `{B, A}`.
    
- Tìm giá trị `C2` trong **cột B** (B2:B289).
    
- Nếu khớp → trả về giá trị ở **cột A** cùng dòng.
    
- Chỉ xét từ dòng 2 → 289.
    

---

### 3. Công thức với mảng toàn cột

```excel
=VLOOKUP(Interview_aVu_CuongBe!C2, {Database!B:B, Database!A:A}, 2, FALSE)
```

- Tương tự công thức (2) nhưng mở rộng toàn bộ **cột B** để tìm.
    
- Nếu khớp → trả về cột A tương ứng.
    
- Ưu điểm: không sợ bỏ sót dữ liệu vì không giới hạn số dòng.
    
- Nhược điểm: có thể chạy chậm hơn khi dữ liệu rất lớn.
    

---

👉 Ngắn gọn:

- **Công thức 1**: tìm trong A → trả về B.
    
- **Công thức 2**: tìm trong B (giới hạn dòng) → trả về A.
    
- **Công thức 3**: tìm trong B (toàn cột) → trả về A.
    

---

Bạn có muốn mình làm thêm bản dùng `IFERROR` để tránh lỗi `#N/A` khi không tìm thấy không?



---
file 15GB, xoá 2 cột rất nhiều dòng thì thành 16gb

file 2, 5, 5 gb => tổng lại merge vào 15GB?


---

Bạn có thể kiểm tra ô **A2** có trong cột **D** hay chưa bằng cách dùng công thức trong Excel hoặc Google Sheets:

### Cách 1: Dùng `COUNTIF`

`=COUNTIF(D:D, A2) > 0`

- Nếu kết quả **TRUE** → giá trị ở A2 đã tồn tại trong cột D.
    
- Nếu kết quả **FALSE** → chưa có trong cột D.
    

### Cách 2: Dùng `MATCH`

`=ISNUMBER(MATCH(A2, D:D, 0))`

- Trả về **TRUE** nếu tìm thấy.
    
- Trả về **FALSE** nếu không có.
    

👉 Cách nhanh nhất là dùng `COUNTIF`, vì nó dễ hiểu và gọn.




---



{"type": "LEARNING_FLEXIBLE", "data": {"description": "Hãy dịch cụm sau", "intro_audio": "https://smedia.stepup.edu.vn/web_mvp/thecoach/audio/hay_dich_cum_sau.mp3", "sentence_hide": "Yes, we have a problem with the supplier.", "sentence_en": "Yes, we have a problem with the supplier.", "sentence_vi": "Vâng, chúng ta có vấn đề với nhà cung cấp.", "word_mapping": {}, "sentence_audio_speaker": "https://smedia.stepup.edu.vn/web_mvp/thecoach/audio_TC2025/flexible_phrase/yes_we_have_a_problem_with_the_supplier_20250828_194741_eubjk9.mp3", "sentence_audio_auto_play": ""}, "check_audio": "HAVE"} 

1 ô có cái này Cách extract sentence_vi

=REGEXEXTRACT(TO_TEXT(O10), """sentence_vi"":\s*""([^""]+)""")



```
curl --location 'http://103.253.20.30:3000/api/generate-all-exercises-lyly-the-coach' \
 --header 'Content-Type: application/json' \
 --data '{
  "context": {
    "user_profile": "Work general",
    "topic": "CẬP NHẬT TÌNH HÌNH CÙNG SẾP",
    "scenario": "Bạn nhận thấy một rủi ro có thể ảnh hưởng đến dự án. Sếp hỏi bạn có trở ngại nào không trong cuộc họp."
  },
  "lesson": {
    "question": "Are there any blockers?",
    "structure": "Yes, we have a problem with ___.",
    "lesson_detail": [
      {
        "phrase_eng": "the supplier",
        "phrase_vi": "nhà cung cấp"
      },
      {
        "phrase_eng": "the budget",
        "phrase_vi": "ngân sách"
      },
      {
        "phrase_eng": "the timeline",
        "phrase_vi": "thời gian biểu"
      }
    ],
    "question_vi": "Có trở ngại nào không?",
    "structure_vi": "Vâng, chúng tôi có một vấn đề với ___."
  }
}'


=REGEXEXTRACT(TO_TEXT(M2), """question_vi"":\s*""([^""]+)""")

```


---
# 4. Cách tính PERCENTILE 

Chú ý: để ý bug: số trong cột ko được định dạng ở formt number / 

```
=COUNT(FILTER(F2:F109, TRIM(B2:B109)="RoleB"))
```