
1. Frequently 
2. ....
3. Matrix Factorition 
4. Session based


1. Why we need recommender system? 
- Google, Amazon
- Youtube
- News ???
- Facebook : user - user ~ LINK ANALYSIS ~ Link Prediction

2. Recommender vs Information retrieval
- Information Retrieval: for user that user want
- Recommender System: suggest for user thing that user don't know they want

3. Applications: 
- Amazon: increase 30% vanue
- Netflix: 1B $ each year
- ....
<chú tâm liên tục cảm giác nổi trội toàn thân>



## 1. Content-based Approach
- User info : gender, age  + History purchase
- Product info: categpory, prices, ...

item - 

**Content-based Approach (Cách tiếp cận dựa trên nội dung)**

Content-based approach là một cách mà hệ thống khuyến nghị (recommendation systems) sử dụng để đề xuất sản phẩm cho người dùng. Nó dựa vào thông tin mà người dùng đã cung cấp và các sản phẩm họ đã từng mua hoặc yêu thích.

- **Thông tin người dùng (User info):**
    
    - **Giới tính (Gender):** Hệ thống biết bạn là nam hay nữ để đề xuất sản phẩm phù hợp hơn.
    - **Độ tuổi (Age):** Độ tuổi giúp hệ thống hiểu được sở thích của bạn. Ví dụ: Một người trẻ tuổi có thể thích thời trang năng động, còn người lớn tuổi có thể thích phong cách trang nhã.
    - **Lịch sử mua hàng (History purchase):** Nếu bạn đã từng mua sách về âm nhạc, hệ thống có thể gợi ý những sách khác cùng thể loại.
- **Thông tin sản phẩm (Product info):**
    
    - **Danh mục sản phẩm (Category):** Ví dụ: quần áo, sách, đồ điện tử, hoặc mỹ phẩm.
    - **Giá cả (Prices):** Hệ thống sẽ xem bạn thường mua những món đắt tiền hay rẻ hơn để gợi ý sản phẩm phù hợp với ngân sách của bạn.

**Ví dụ thực tế:**  
Bạn là một học sinh nữ, 16 tuổi, và đã mua sách về tiếng Anh. Hệ thống có thể gợi ý thêm sách học ngữ pháp, sách luyện IELTS, hoặc những sản phẩm liên quan đến học tập.


## 2. 
**Giải thích Collaborative Filtering cho học sinh cấp 2:**

Hãy tưởng tượng em và các bạn cùng lớp đang thảo luận xem nên xem phim gì. Em thích phim hoạt hình, còn bạn An thích phim hành động. Một ngày, có một bạn mới vào lớp tên là Minh, và Minh cũng thích phim hành động như bạn An.

Dựa trên sở thích giống nhau, em có thể đoán rằng Minh sẽ thích những bộ phim mà bạn An từng giới thiệu, đúng không? Đây chính là cách mà **Collaborative Filtering** hoạt động.

Cụ thể hơn:

- Nếu hai người có sở thích giống nhau (như Minh và An), hệ thống sẽ gợi ý những gì một người thích cho người còn lại.
- Thay vì chỉ nhìn vào từng món đồ, hệ thống dựa vào dữ liệu từ nhiều người giống nhau để đưa ra gợi ý.

Ví dụ thực tế: Trên Netflix, nếu em và bạn của em đều xem nhiều phim hoạt hình, Netflix sẽ gợi ý thêm các phim hoạt hình mà bạn em đã xem nhưng em chưa xem. Nó giống như bạn bè chia sẻ sở thích vậy! 😊


## Challenges: 
- The number of transactions << actual 
- Not enough information 
- Real-time ? 
- Change of behavior buy 

## 3. Evaluation Method?


Give: user U , item I 

5 stage scale: 1, 2, 3, 4, 5 
Binary scale : 0, 1 

Dataset seperated into 


train/test




## 4. A/B Testing

![[Pasted image 20241126113005.png]]

![[Pasted image 20241126113106.png]]

==========

Exercise: 


```
Giả sử John dự đoán cho các phim: Aliens(5), Terminator(5), Nero(1), Gladiator (6)
Giá trị cao hơn thì tốt hơn 

giả sự dự đoán của hệ gợi ý là: Aliens(4, 3), Terminator(5, 4), Nero(1, 3) và Gldiator(5)

a, Cal : MSE
b, Calucatlate: MAE
c, RMSE
d, Calculate NMAE and NRMSE, given that rating is in the range of (1, 2, ...6)


```
**Giải thích từng bước một cách dễ hiểu:**

Chúng ta có 4 bộ phim và điểm số mà John thực sự đánh giá (điểm thật) và điểm mà hệ thống dự đoán (điểm dự đoán):

|**Phim**|**Điểm thật (T)**|**Điểm dự đoán (P)**|
|---|---|---|
|Aliens|5|4.3|
|Terminator|5|5.4|
|Nero|1|1.3|
|Gladiator|6|5|

**Bước 1: Tính lỗi cho mỗi phim**

Lỗi (E) cho mỗi phim là sự chênh lệch giữa điểm dự đoán và điểm thật:

E = P - T

Chúng ta cũng tính giá trị tuyệt đối của lỗi (|E|) và bình phương của lỗi (E²):
```
| **Phim** | **T** | **P** | **E = P - T** | **|E|** | **E²** | |----------------|-------|-------|---------------|--------|---------| | Aliens | 5 | 4.3 | -0.7 | 0.7 | 0.49 | | Terminator | 5 | 5.4 | 0.4 | 0.4 | 0.16 | | Nero | 1 | 1.3 | 0.3 | 0.3 | 0.09 | | Gladiator | 6 | 5 | -1.0 | 1.0 | 1.00 |
```


**a) Tính MSE (Mean Squared Error - Trung bình bình phương lỗi)**

MSE là trung bình của các bình phương lỗi:

1. Cộng tất cả các E² lại:
    
    - Tổng E² = 0.49 + 0.16 + 0.09 + 1.00 = **1.74**
2. Chia tổng này cho số lượng phim (n = 4):
    
    - MSE = Tổng E² / n = 1.74 / 4 = **0.435**

**b) Tính MAE (Mean Absolute Error - Trung bình giá trị tuyệt đối của lỗi)**

MAE là trung bình của các giá trị tuyệt đối của lỗi:

1. Cộng tất cả các |E| lại:
    
    - Tổng |E| = 0.7 + 0.4 + 0.3 + 1.0 = **2.4**
2. Chia tổng này cho số lượng phim:
    
    - MAE = Tổng |E| / n = 2.4 / 4 = **0.6**

**c) Tính RMSE (Root Mean Squared Error - Căn bậc hai của MSE)**

RMSE là căn bậc hai của MSE:

- RMSE = √MSE = √0.435 ≈ **0.6595**

**d) Tính NMAE và NRMSE (Chuẩn hóa MAE và RMSE)**

Vì điểm số nằm trong khoảng từ 1 đến 6, phạm vi điểm số là:

- Phạm vi = Điểm cao nhất - Điểm thấp nhất = 6 - 1 = **5**

**Tính NMAE (Normalized MAE):**

- NMAE = MAE / Phạm vi = 0.6 / 5 = **0.12**

**Tính NRMSE (Normalized RMSE):**

- NRMSE = RMSE / Phạm vi = 0.6595 / 5 ≈ **0.1319**

---

**Tóm lại:**

a) **MSE = 0.435**

b) **MAE = 0.6**

c) **RMSE ≈ 0.6595**

d) **NMAE = 0.12** và **NRMSE ≈ 0.1319**

**Giải thích đơn giản:**

- **MSE** đo lường độ chênh lệch bình phương trung bình giữa dự đoán và thực tế.
- **MAE** đo lường độ chênh lệch trung bình theo giá trị tuyệt đối.
- **RMSE** là căn bậc hai của MSE, giúp đưa đơn vị về cùng mức với dữ liệu gốc.
- **NMAE** và **NRMSE** chuẩn hóa các lỗi này dựa trên phạm vi điểm số, giúp so sánh dễ dàng hơn.

**Như vậy, chúng ta đã tính toán các chỉ số lỗi một cách dễ hiểu cho học sinh cấp 2!**




--------------
### **Tóm tắt công thức của các chỉ số: MAE, MSE, RMSE, NMAE, NMSE, NRMSE**

#### **Công thức:**

1. **MAE (Mean Absolute Error):**
    
    MAE=1n∑(u,i)∣pui−rui∣MAE = \frac{1}{n} \sum_{(u,i)} |p_{ui} - r_{ui}|
2. **MSE (Mean Square Error):**
    
    MSE=1n∑(u,i)(pui−rui)2MSE = \frac{1}{n} \sum_{(u,i)} (p_{ui} - r_{ui})^2
3. **RMSE (Root Mean Square Error):**
    
    RMSE=1n∑(u,i)(pui−rui)2RMSE = \sqrt{\frac{1}{n} \sum_{(u,i)} (p_{ui} - r_{ui})^2}
4. **NMAE (Normalized Mean Absolute Error):**
    
    NMAE=MAErmax−rminNMAE = \frac{MAE}{r_{max} - r_{min}}
5. **NMSE (Normalized Mean Square Error):**
    
    NMSE=MSE(rmax−rmin)2NMSE = \frac{MSE}{(r_{max} - r_{min})^2}
6. **NRMSE (Normalized Root Mean Square Error):**
    
    NRMSE=RMSErmax−rminNRMSE = \frac{RMSE}{r_{max} - r_{min}}

---

### **Bảng so sánh chi tiết: MAE, MSE, RMSE --- NMAE, NMSE, NRMSE**

|**Metric**|**Dạng Sai Số**|**Nhấn Mạnh Lỗi Lớn?**|**Chuẩn Hóa?**|**Ứng Dụng Phù Hợp**|
|---|---|---|---|---|
|**MAE**|Tuyệt đối|Không|Không|Dữ liệu ổn định, không cần nhấn mạnh lỗi lớn.|
|**MSE**|Bình phương|Có|Không|Phát hiện lỗi lớn, phù hợp khi dữ liệu ít outliers.|
|**RMSE**|Căn bình phương|Có|Không|Tập trung vào các lỗi lớn, phù hợp với dữ liệu nhạy cảm.|
|**NMAE**|Tuyệt đối (chuẩn hóa)|Không|Có|So sánh trên nhiều thang đo, không cần quan tâm lỗi lớn.|
|**NMSE**|Bình phương (chuẩn hóa)|Có|Có|Tổng quát, so sánh trên thang đo khác nhau, ít nhấn lỗi lớn.|
|**NRMSE**|Căn bình phương (chuẩn hóa)|Có|Có|So sánh trên nhiều thang đo, nhấn mạnh lỗi lớn.|

---

### **1. Format công thức và chú thích rõ ràng hơn:**

- **Cần đồng nhất về cách hiển thị công thức:** Ví dụ:

MAE=1n∑(u,i)∣pui−rui∣MAE = \frac{1}{n} \sum_{(u,i)} |p_{ui} - r_{ui}|

=> Thêm chú thích dưới công thức:

- puip_{ui}: Giá trị dự đoán.
- ruir_{ui}: Giá trị thực tế.
- nn: Số lượng ví dụ trong tập kiểm tra.

---

### **2. Phần Ranking (Precision, Recall, F-Score):**

- **Precision:**
    
    Precision=Soˆˊ lượng mục được gợi yˊ đuˊngTổng soˆˊ mục được gợi yˊPrecision = \frac{\text{Số lượng mục được gợi ý đúng}}{\text{Tổng số mục được gợi ý}}
- **Recall:**
    
    Recall=Soˆˊ lượng mục được gợi yˊ đuˊngTổng soˆˊ mục đuˊng trong thực teˆˊRecall = \frac{\text{Số lượng mục được gợi ý đúng}}{\text{Tổng số mục đúng trong thực tế}}
- **F-Score:**
    
    F=2⋅Precision⋅RecallPrecision+RecallF = 2 \cdot \frac{Precision \cdot Recall}{Precision + Recall}

**Lưu ý:**

- **Precision:** Hệ thống gợi ý bao nhiêu mục đúng so với tổng số mục đã gợi ý.
- **Recall:** Hệ thống gợi ý được bao nhiêu mục đúng trong tất cả các mục mà người dùng thực sự thích.
- **F-Score:** Cân bằng giữa Precision và Recall.

---

### **3. NMSE và NRMSE:**

- **Khác biệt:**
    
    - **NMSE** dựa trên MSE (không căn bậc hai), ít nhạy cảm với lỗi lớn.
    - **NRMSE** dựa trên RMSE (có căn bậc hai), nhạy cảm hơn với lỗi lớn.
- **Ứng dụng thực tế:**
    
    - **NMSE:** Thường được dùng trong bài toán đánh giá tổng thể khi không cần nhấn mạnh lỗi lớn.
    - **NRMSE:** Phù hợp với bài toán nhạy cảm với sai số lớn, như hệ thống gợi ý phim hoặc quảng cáo.

---

### **4. Khi nào sử dụng từng chỉ số?**

|**Chỉ số**|**Ứng dụng**|
|---|---|
|**MAE**|Dễ hiểu, phù hợp khi dữ liệu không có outliers và các lỗi lớn không quan trọng.|
|**MSE**|Nhấn mạnh lỗi lớn, phù hợp khi cần phát hiện các dự đoán sai nghiêm trọng.|
|**RMSE**|Tương tự MSE, nhưng nhạy cảm hơn với lỗi lớn, phù hợp với dữ liệu có outliers.|
|**NMAE**|Chuẩn hóa MAE để so sánh giữa các hệ thống hoặc mô hình với thang đo khác nhau.|
|**NMSE**|Chuẩn hóa MSE, phù hợp khi cần so sánh trên nhiều thang đo và không nhấn mạnh các lỗi lớn.|
|**NRMSE**|Chuẩn hóa RMSE, nhấn mạnh các lỗi lớn, phù hợp khi cần đánh giá độ chính xác trên các thang đo khác nhau.|

---

### **5. Kết luận:**

- **MAE và RMSE:** Thích hợp để đo sai số trực tiếp. RMSE nhấn mạnh lỗi lớn hơn MAE.
- **NMAE, NMSE, NRMSE:** Hữu ích khi cần chuẩn hóa sai số, giúp dễ dàng so sánh trên các thang điểm khác nhau.
- **Ranking metrics (Precision, Recall, F-Score):** Quan trọng trong các hệ thống gợi ý, tập trung vào việc đo lường hiệu quả gợi ý.



#### Câu hỏi : 

1. Giải thích dễ hiểu hơn đoạn "ứng dụng phù hợp của MSE và RMSE" - Phân biệt?? --- cho học sinh cấp 2
```
**Giải thích MSE và RMSE dễ hiểu hơn cho học sinh cấp 2:**

1. **MSE (Mean Square Error - Sai số bình phương trung bình):**

- **Hình dung đơn giản:**
    
    - Hãy tưởng tượng em đang cố gắng đoán số kẹo trong một lọ. Nếu em đoán sai, người ta sẽ tính xem em sai bao nhiêu kẹo và nhân đôi lỗi đó (bình phương) để "phạt nặng" lỗi lớn hơn.
    - Ví dụ: Em đoán sai 3 kẹo, thì mức sai số là 32=93^2 = 9. Nếu sai 1 kẹo, mức sai chỉ là 12=11^2 = 1.
- **Ứng dụng:**
    
    - MSE nhấn mạnh vào **những lỗi đoán sai lớn**, giúp phát hiện xem mô hình có dự đoán quá tệ ở đâu không.
    - Dùng khi em muốn kiểm tra xem mô hình dự đoán có vấn đề nghiêm trọng ở các lỗi lớn không, ví dụ như trong hệ thống gợi ý mà kết quả dự đoán bị lệch quá nhiều.

---

2. **RMSE (Root Mean Square Error - Sai số căn bình phương trung bình):**

- **Hình dung đơn giản:**
    
    - RMSE cũng giống như MSE nhưng sau khi tính mức phạt bằng bình phương, người ta lấy căn bậc hai để đưa sai số về **đơn vị giống với dự đoán ban đầu**.
    - Ví dụ: Thay vì mức phạt là 99 (như trong MSE), RMSE sẽ lấy căn bậc hai của 99, tức là 9=3 \sqrt{9} = 3.
- **Ứng dụng:**
    
    - RMSE dễ hiểu hơn MSE vì sai số cuối cùng (sau khi lấy căn bậc hai) có cùng đơn vị với dữ liệu ban đầu.
    - Thích hợp khi muốn **hiểu rõ mức sai trung bình thực tế** của hệ thống.

---

### **Phân biệt MSE và RMSE:**

|**MSE**|**RMSE**|
|---|---|
|Sai số được tính bằng cách **bình phương sai lệch**.|Sai số được tính bằng **bình phương** rồi lấy **căn bậc hai**.|
|Kết quả cuối cùng là một **giá trị lớn** hơn mức sai thực tế, vì sai số bị phóng đại.|Kết quả cuối cùng là một **giá trị dễ hiểu hơn**, gần với sai thực tế.|
|Nhấn mạnh mạnh hơn vào **những lỗi lớn**.|Nhấn mạnh lỗi lớn nhưng vẫn giữ được ý nghĩa với đơn vị dữ liệu.|
|Thích hợp để phát hiện lỗi cực lớn hoặc phân tích mức độ chệch lớn.|Thích hợp khi cần đánh giá tổng thể và hiểu mức sai số thực tế.|

---

### **Ví dụ cụ thể:**

- **Em đoán điểm bài kiểm tra của bạn mình (thang 1-10):**
    
    - Bạn được 9 điểm, nhưng em đoán là 6 (sai 3 điểm).
    - Nếu dùng **MSE**:
        - Sai số là 32=93^2 = 9.
        - Giá trị lớn hơn lỗi thực tế, nhấn mạnh rằng em đoán quá sai.
    - Nếu dùng **RMSE**:
        - Sai số là 9=3 \sqrt{9} = 3.
        - Kết quả gần với mức sai thực tế (sai 3 điểm), giúp dễ hiểu hơn.
- **Khi nào dùng MSE hoặc RMSE?**
    
    - Dùng **MSE** nếu em muốn phát hiện những dự đoán sai nghiêm trọng.
    - Dùng **RMSE** nếu em muốn biết sai số trung bình dễ hiểu và sát thực tế.
