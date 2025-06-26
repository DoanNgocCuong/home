

1. Frequently 
2. ....
3. Matrix Factorition 
4. Session based


5. Why we need recommender system? 
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
ư





- Nhóm 2: ... 
- Nhóm 3: Book Recommneder system : 
		- Dataset: User Data: 
		- Aim to provide user 2 types of ouput : 
			- Top-K Movie Recommendtions 
			- Rating 
	- RMSE: ...
	- Methods: BPR, LighGCN, 
	- mETRICS: RMSE, Precision @10, Recall @10 
		- LightGCN, 
	- Cold Start Problem: 
		- with LightGCN, EmerG - Item Specific Feature Inteactions for Cold-Start CTR Prediction KDD 2024. 
		- GNN process and predict the likelihood ? 
		- EmerG designed to predict Click-through Rate CTR. 
		- Which estimate the probability that a user .... 
- Result : 
				-  Cold, Warm-A, Warm-B, Warm-C 
Model: LightGCN,   P@10, R@10, P@10, R@10, ... 
	EmerG 
Results: inclusing : MF (baseline), BPR, NCF, DeepFM, FM, BiVAE, LightGCN, EmerG. 

- Increase about result: Model: MF -> NCF -> 

---
LEARN FROM BEST PRACTICES AND MANY SUMMARY&PRACTICES OF PEOPLE 

- movie: LightGCN, BPR, DeepFM, BiVAE, NCF, MF baseline 
- RMSE, Pricision@10, Recall@10, NDCG@10

3. Book: 
- Basé on Singular Value Decomposition SVD, 
- Books - User 10.3M - Item 4.4M - Rating 29.5M (Amazon Reviews Dataset). 
- 2 methods: Conllaoborative (SA SREC, SVD, Sli_Rec) + Content-base (NAML, NPA)
NPA (Neural Recommendation with Personalized Attiion), 
NAML (NeÂMl News Recommendation , ... )

Transfomer based method: SASREC, SSEPT (Collaborative filtering), ... 
Single Value SV: 


4. RAG: 
- model and identify the topic distribution for each research paper. 
- Inputt Abstracts list of artivel 
- b, Co-Author Network: Nodes each node represents an author , edge weight = average topic distributions of co-authored pper 

Apporch1: Topic Model-Based Search 
	- Topic Filtering: 500 most relevant pape based on
	- Embedding and Reranking: 
		- embedding represent absstract 
		- rerank 500
Approach2 : Author Network-Based Search 
1. Topic Filerting: Similar approach 1 => 50 most 
2. Expand Dataset : top 100 author related to above papper 
3. Embedding Reranks 
4. Final: Choose top 10 for the relationship 

Dataset: Kaggle: metadataa: id, submitter, authors, ... 



-------------------------------------

Methods Semantic Analysis 
- mẹthod: Hỉeachical Graph Convolutions network HIER - GCN (bert encode the review sentence and gen re)
- Domain:Hotel, Resuatl, 
- 4 sentiment: none, pos, neg, neutral
- VNCorenlp, ... 
- Method 3; 

-----------------

Group 7: Film: 
Dataset: Netlfix 2006, 5600 ratings/users, 200 rating/1 films . 
User ID, Fil,, Date, Rading 

Trying to predict the ratings in the test set when given User ID, filmID, and dataset. 
(In other words: Given)

Method ; 

SVD : soimplest solutoion 

- A is the rating matrics, all missing values 
- A = U * Xích ma V_T 
- Either learn a function R'_ij directly 
Method: Time-aware rating predction from assumption that theré tesceits a shift in ủe preferrence s
Grading Boosting decision tree: 


--------------------------------
Group 8: Extract opinions about specific aspects, obtaining deeper and more details. 
3 Main subtassk: 
- MATE Multimodel Aspect Sentiment Classification MASC : MABSSC, MCBSC. 
	- mcbsc : USE , ....
- MASC Multimode 
- ASPE PEpect S Pairs

Method: Text : RNN< LSTM, Bert 
Image : Cnn, Resnet 
Cross model attention mechainis ,; Focus on inô, extract content form text or image, 

Fusion Techiniques : 
	-  Earrly fusion (Feature layer fusion) - Late fusion - Immedate ... 
Dataset;ViMACSA, ... 

Textual Data: Tokenize, Stemming Normalize remove stipss , Image : Normalize, Augmentation, .. 


3.3 Models: FCMF (main model, show in the papper, ) 
MIMN: Feature Extraction, Multimodel Memory Network, Multi, ... 
tomBERT?? 

-------------------

GROUP 8-
Machine learning: TF-IDF, Word Frequency, N-gram models, word couting 

- SVM for multi class finication : One-Rest  (1 class vs others classes)---- One vs One (classifier for every pair of classes : 20*19/2
)- Decision Tree, LSTM, Bi-LSTM
- Finetunging báes methofs: Finetuning the pretrained RoBERTa model (a new traing strategfy for the BERT MODEL). 

dATASET: 510.000 twết, each contain 1 emoji that servers as the classifi cation 

Metrics : Macro-averate F1 Score ??



-----------------

IGROUP 10

userID, ProductID of a related product 
ouput: top N products 

Dataset: Amazon Reviews 18

Methods: content-basé recommend TD-IDF, 
Collaborative Filtering: 
	- Item baed recommend with KNN
	- Single Value Decomposition
	- Nẻual 

User_item Interaction Graph, High-order Connectity 

Hybrid Approach: Combine, lessen the impact of item Cold Start Project


Evaluation 

HR Hir Ratio: HR = U_hit/U_all



======
group 11 : 
- GNN to capture  food recommendation 
Data: Inputs: User data, restaurant data, graph structure (user - item releations híp : review,s , purchased)
-> output: recommend list: ranks food 

- Matrix factoriaxz e 
- Neighborhood based collaborative filtering

GNNs: implemment deep learning, GNNS capture complex

CKAN: 
KGNN-LS : 

Dataset : Dianping-Food, - 10 milliojjn interractins *click, purchasesm add ing* (user, item, interactions, inter-avg, entities, relationship, ..)

Metrics : RMSE< F1 score 




# 6. OPINION WEBMING: 
Opinion mining is about understanding what people think about products, services, or anything else. Here’s a simple explanation for each problem:

1. **Sentiment Analysis**: This is figuring out if a comment or review is saying something good, bad, or just neutral (neither good nor bad). For example, “BPhone 3, chất đến từng chi tiết” is a positive comment.

2. **Opinion Summarization**: This is about summarizing reviews by identifying what people are talking about (the “aspect”) and whether they feel positive, negative, or neutral about each part of the product.

3. **Comparative Opinions**: Sometimes people compare two or more things, like saying “Object A is better than Object B” or “I like object A more than others.”

4. **Opinions Searching**: This is about finding what people are saying about a certain object or product when we search online (group or forum, ...).

5. **Opinions Filtering**: This is sorting out fake or misleading comments, like some people writing fake good reviews (hype spam) or fake bad reviews (defaming spam).

## 6.1 Methods of Sentiment Analysis 
![[Pasted image 20241022112012.png]]

### IMPORTANCE UNSUPERVISED:  Phân tích Cảm xúc Không Giám sát - Giải thích cho Học sinh Lớp 3

Bài toán này giống như việc chúng ta muốn biết một bài viết nói về một món đồ chơi là tốt hay xấu mà không cần ai nói trước cho chúng ta biết.

- Bước 1: Tìm Cụm Từ Biểu Lộ Ý Kiến
	- Use : Identify language patterns with potential for opinion expression) 
	- Ví dụ: "xe đẹp", "đồ chơi bền", "rất vui".
- Bước 2: Xác Định Hướng Cảm Xúc
	-  Compare whether that phrase often appears with the word "good" or "bad" in many other articles. (For example: "nice car" is more likely to go with "good" than "bad"). 
	- Sso sánh xem cụm từ đó thường xuất hiện cùng với từ "tốt" hay "xấu" hơn trong rất nhiều bài viết khác. (Ví dụ: "xe đẹp" thường đi với "tốt" hơn là "xấu", nên "xe đẹp" là ý kiến ​​tốt).
	- Step by Step: 
		1. **Đếm:** Đếm xem câu nói đó xuất hiện bao nhiêu lần trên mạng Internet.
		2. **Đếm cặp:** Đếm xem câu nói đó và từ "tốt" (hoặc "kém") xuất hiện **cùng nhau** bao nhiêu lần.
		3. **So sánh:** Nếu câu nói đó xuất hiện cùng "tốt" nhiều hơn "kém", thì câu nói đó là lời khen. Ngược lại, nếu câu nói đó xuất hiện cùng "kém" nhiều hơn "tốt", thì câu nói đó là lời chê.
- Bước 3: Từ đó đưa ra kết luận. 
	- **Ví dụ:** Câu nói: "Phim này hay quá!"
	- PMI("Phim này hay quá!"; "tốt") cao.
	- PMI("Phim này hay quá!"; "kém") thấp.

VỀ TOÁN: 
- Step by Step 'HOW TO CALCULATE PMI':

	1. Determine the similarity of two phrases based on the likelihood of co-occurrence on a large corpus: 
		- Large Text Set: Web Text
		- Possibility co-occurrence: Pointwise Mutual Information (PMI)
		- SO(t) = PMI(t; ‘tốt’) - PMI(t; ‘kém’)
	
	2. Then, VẬY THÌ CÔNG THỨC PMI() tính như nào? 
		Cách tính **PMI (Pointwise Mutual Information)** cho một từ t và một từ khác (ví dụ: từ "tốt" hoặc "kém") dựa trên xác suất của chúng trong tập văn bản lớn (corpus).

		Công thức PMI được tính như sau:
		$PMI(t, \text{"?"}) = \log \frac{P(t, \text{"?"})}{P(t) \cdot P(\text{"?"})}$

			Trong đó:
			- **P(t, "?"**) là xác suất của từ t và từ "?" cùng xuất hiện trong văn bản (xác suất đồng xuất hiện).
			- **P(t)** là xác suất xuất hiện của từ t.
			- **P("?")** là xác suất xuất hiện của từ "?" (ví dụ: từ "tốt" hoặc "kém").
		
		### Chi tiết tính toán:
		
		1. **Xác suất P(t)**:
		   $P(t) = \frac{\text{count}(t) + 1}{\sum_{t’} \text{count}(t’) + V}$
		   - **count(t)**: Số lần xuất hiện của từ t trong tập văn bản.
		   - **V**: Kích thước từ vựng (số từ khác nhau trong tập văn bản).
		
		2. **Xác suất đồng xuất hiện P(t, "?")**:
		  P(t, \text{"?"}) = $\frac{\text{count}(t, \text{"?"}) + 1}{\text{Tổng số lần xuất hiện của tất cả các cặp từ trong văn bản} + V}$
		   - **count(t, "?"**): Số lần t và "?" xuất hiện cùng nhau trong một câu hoặc đoạn văn.
	


- **Tại sao tính PMI lại là công thức kia, tại sao lại là P(t) * P(?) và tại sao lúc tính P lại phải count + 1/ tổng số lần xuất hiện + V, V là gì ? **   => GPT for detail. 
	- **P(t)⋅P(?)P(t) \cdot P(?)P(t)⋅P(?)** chính là cách đo **mức độ ngẫu nhiên**: Nếu từ ttt và từ ??? xuất hiện ngẫu nhiên, không liên quan đến nhau, thì xác suất chúng xuất hiện cùng nhau chỉ đơn giản là tích của xác suất từng từ xuất hiện riêng lẻ.
	- P(t,?), tức là xác suất đồng xuất hiện thực tế,

## 6.2 SOT - Sentinment Ontology Tree

1. explain for child: 
- Hãy nghĩ về SOT như một **cây gia đình** cho ý kiến về sản phẩm.
- **Gốc cây** là sản phẩm bạn quan tâm, ví dụ như điện thoại.
- **Các nhánh cây** là các đặc điểm của sản phẩm, ví dụ như màn hình, pin, camera.
- **Lá cây** là ý kiến ​​của mọi người về những đặc điểm đó.
    - **Lá xanh:** Ý kiến ​​tích cực, ví dụ như "màn hình đẹp", "pin lâu".
    - **Lá đỏ:** Ý kiến ​​tiêu cực, ví dụ như "camera mờ", "giá cao".
2. While SOT offers a robust solution for fine-grained sentiment analysis and is well-regarded for certain research purposes, its broader adoption is limited by its complexity and lack of widespread tool support.



```
IE architecture

IE problems

NER: CRF, LSTM

Relation extraction - Snowball --- Distant supervision

Coreperence resolution
```

Snowball: 

### Giải Thích Phương Pháp Snowball Đơn Giản cho Học Sinh Cấp 2

**Phương pháp Snowball** là một cách mà máy tính sử dụng để tìm hiểu và nhận diện các mối quan hệ giữa các từ hoặc cụm từ trong văn bản. Hãy tưởng tượng bạn đang xây dựng một **cái vòng tuyết** (snowball) từ những hạt tuyết nhỏ. Mỗi hạt tuyết thêm vào sẽ làm cho vòng tuyết trở nên lớn hơn và mạnh mẽ hơn. Tương tự, phương pháp Snowball bắt đầu từ một vài ví dụ nhỏ và dần dần mở rộng để nhận diện nhiều mối quan hệ hơn.

#### **Ví dụ Minh Họa:**

Giả sử bạn muốn dạy máy tính nhận biết mối quan hệ "tác giả viết sách".

1. **Bước 1: Bắt Đầu với Ví Dụ Ban Đầu (Seed Words)**
    
    - Bạn cung cấp cho máy tính một vài câu mẫu chứa mối quan hệ này, chẳng hạn:
        - "J.K. Rowling viết Harry Potter."
        - "George Orwell viết 1984."
2. **Bước 2: Tìm Các Mẫu Câu (Pattern)**
    
    - Máy tính sẽ nhận ra rằng trong các câu trên, từ "viết" thường xuất hiện giữa tên tác giả và tên sách.
    - Như vậy, mẫu câu có thể là: "**[Tên Tác Giả] viết [Tên Sách]**".
3. **Bước 3: Mở Rộng Tìm Kiếm**
    
    - Dựa vào mẫu câu này, máy tính sẽ quét toàn bộ văn bản để tìm thêm các câu có cấu trúc tương tự.
    - Ví dụ:
        - "Agatha Christie viết Mật Mã Da Vinci."
        - "Haruki Murakami viết Kafka bên bờ biển."
4. **Bước 4: Xác Nhận và Mở Rộng Mối Quan Hệ**
    
    - Khi máy tính tìm thấy nhiều ví dụ hơn, nó sẽ hiểu rõ hơn về mối quan hệ "tác giả viết sách" và có thể nhận diện được nhiều câu hơn mà không chỉ giới hạn trong những ví dụ ban đầu.

#### **Ưu Điểm của Phương Pháp Snowball:**

- **Đơn Giản:** Dễ hiểu và dễ triển khai.
- **Tự Động Mở Rộng:** Có khả năng tìm kiếm và nhận diện nhiều mối quan hệ mới dựa trên những gì đã học.

#### **Hạn Chế:**

- **Phụ Thuộc Vào Ví Dụ Ban Đầu:** Nếu các ví dụ ban đầu không đủ đa dạng, máy tính có thể bỏ sót nhiều mối quan hệ quan trọng.
- **Dễ Bị Lạc Đường:** Có thể tìm thấy các mối quan hệ không chính xác nếu không kiểm soát chặt chẽ.

#### **Tóm Lại:**

Phương pháp Snowball giống như việc bạn bắt đầu từ một hạt tuyết nhỏ và dần dần xây dựng thành một vòng tuyết lớn hơn. Bằng cách bắt đầu với một vài ví dụ, máy tính có thể tự động tìm kiếm và nhận diện nhiều mối quan hệ hơn trong văn bản. Đây là một công cụ hữu ích giúp máy tính hiểu ngôn ngữ tự nhiên và trích xuất thông tin quan trọng từ các đoạn văn bản lớn.


### Understanding the Snowball Method in Information Extraction

The **Snowball method** is a technique used in **Relation Extraction**, a subfield of **Information Extraction (IE)** in Natural Language Processing (NLP). Its primary goal is to identify and classify relationships between entities (like people, organizations, locations) within large volumes of text. Here's a breakdown of what the Snowball method does and how it operates:

#### **1. Purpose of the Snowball Method**

- **Identify Relationships:** The Snowball method is designed to discover and extract specific types of relationships between entities in text. For example, identifying that "Albert Einstein **developed** the theory of relativity" establishes a "developer-of" relationship between "Albert Einstein" and "the theory of relativity."
    
- **Expand Knowledge Bases:** By extracting relationships from vast amounts of text, the Snowball method helps in building and enriching structured databases or knowledge graphs, which can be used for various applications like search engines, recommendation systems, and question-answering systems.
    

#### **2. How the Snowball Method Works**

The Snowball method is primarily **rule-based** and operates through iterative pattern matching and expansion. Here's a step-by-step overview:

##### **a. Start with Seed Patterns and Examples**

- **Seed Patterns:** Begin with a few predefined patterns that represent the relationship you're interested in extracting. For instance, to extract "author-of" relationships, seed patterns might include:
    - "[Author] **wrote** [Book]"
    - "[Author] **authored** [Novel]"
- **Seed Examples:** Provide initial examples that fit these patterns:
    - "J.K. Rowling **wrote** Harry Potter."
    - "George Orwell **authored** 1984."

##### **b. Pattern Matching and Extraction**

- **Scan Text:** Use the seed patterns to scan large corpora (collections of text) and identify sentences that match these patterns.
    
- **Extract Relationships:** When a sentence matches a pattern, extract the entities and their relationship. From "J.K. Rowling wrote Harry Potter," extract ("J.K. Rowling", "wrote", "Harry Potter").
    

##### **c. Expand Patterns and Examples**

- **Iterative Expansion:** Use the newly extracted examples to discover new patterns or refine existing ones. For example, if the method frequently encounters variations like "J.K. Rowling **authored** Harry Potter," it can add "**authored**" as another pattern synonym for "wrote."
    
- **Generalization:** Broaden the patterns to capture more diverse expressions of the same relationship. This helps in identifying relationships expressed in different linguistic forms.
    

##### **d. Repeat the Process**

- **Snowball Effect:** As more patterns and examples are discovered, the method can uncover increasingly diverse and numerous instances of the target relationship, much like a snowball growing larger as it rolls.

##### **e. Filter and Validate**

- **Remove Noise:** Not all extracted relationships will be correct. Implement filtering mechanisms to eliminate false positives, ensuring the accuracy of the extracted data.
    
- **Refinement:** Continuously refine patterns based on feedback and validation to improve precision and recall.
    

#### **3. Advantages of the Snowball Method**

- **Scalability:** Capable of processing large volumes of text to extract a wide range of relationships without requiring extensive manual annotation.
    
- **Flexibility:** Can be adapted to extract different types of relationships by modifying seed patterns and examples.
    
- **Efficiency:** Automates the discovery of relationships, reducing the need for manual intervention.
    

#### **4. Limitations of the Snowball Method**

- **Dependency on Seed Patterns:** The quality and diversity of seed patterns significantly influence the method's effectiveness. Poorly chosen seeds can lead to limited or biased extraction.
    
- **Pattern Maintenance:** As language evolves or varies across different domains, maintaining and updating patterns can become challenging.
    
- **Noise and Precision:** Rule-based methods can generate false positives, especially in complex or ambiguous linguistic contexts. Ensuring high precision often requires additional filtering steps.
    

#### **5. Practical Example**

Imagine you're using the Snowball method to extract "parent-of" relationships from a collection of biographies:

1. **Seed Patterns:**
    
    - "[Parent] **is the parent of** [Child]"
    - "[Parent] **has a child named** [Child]"
2. **Initial Extraction:**
    
    - "Maria **is the parent of** Sophia."
    - "John **has a child named** Michael."
3. **Pattern Expansion:**
    
    - Discover sentences like "Maria **raised** Sophia," leading to adding "**raised**" as a new pattern.
4. **Further Extraction:**
    
    - "Carlos **brought up** Elena," extracting ("Carlos", "brought up", "Elena").
5. **Final Output:**
    
    - A comprehensive list of parent-child relationships extracted from the text.

#### **6. Comparison with Other Methods**

- **Rule-Based vs. Machine Learning:**
    
    - **Snowball (Rule-Based):** Relies on predefined linguistic patterns and iterative expansion. It's transparent and easier to control but may lack flexibility and require significant manual effort for pattern creation.
    - **Machine Learning-Based Methods:** Utilize statistical models or deep learning to learn patterns from data automatically. They can capture more nuanced relationships but often require large annotated datasets and can be less interpretable.
- **Snowball vs. Distant Supervision:**
    
    - **Snowball:** Begins with seed patterns and expands through pattern matching, focusing on rule-based extraction.
    - **Distant Supervision:** Uses existing databases to automatically label training data, assuming that sentences mentioning entity pairs express their relationship, which can introduce noise but leverages large datasets for training machine learning models.

#### **7. Modern Enhancements**

While the traditional Snowball method is purely rule-based, modern approaches often integrate it with machine learning to improve accuracy and scalability:

- **Hybrid Models:** Combine rule-based pattern matching with statistical models to validate and refine extracted relationships.
    
- **Natural Language Processing Tools:** Utilize advanced NLP techniques like dependency parsing to enhance pattern matching accuracy.
    
- **Feedback Loops:** Implement mechanisms where extracted data is reviewed and used to update and improve patterns continuously.
    

### **Conclusion**

The Snowball method is a foundational technique in Relation Extraction, leveraging iterative pattern matching to discover and extract meaningful relationships between entities in text. Its simplicity and scalability make it a valuable tool, especially when combined with other methods to enhance precision and adaptability. Understanding the Snowball method provides a stepping stone towards more advanced information extraction techniques used in modern NLP applications.



### Giải Thích Đoạn Công Thức Snowball Đơn Giản Cho Học Sinh Cấp 2

Hãy tưởng tượng bạn đang chơi trò tìm kiếm kho báu với những manh mối xung quanh. Đoạn công thức dưới đây giống như hướng dẫn cách bạn tìm kho báu đó một cách thông minh và hiệu quả. Dưới đây là cách giải thích từng bước một cách dễ hiểu:

#### **Đoạn Công Thức:**

```plaintext
1) {< o, ` >,< ls, t1, ms, t2, rs >} = = CreateOccurrence(text segment);
   TC = < o, ` >; SimBest = 0;
   foreach p in Patterns
2)    sim = Match(< ls, t1, ms, t2, rs >, p);
       if ( sim ≥ τsim )
3)          UpdatePatternSelectivity( p, TC );
           if( sim ≥ SimBest )
               SimBest = sim;
               PBest = p;
   if( SimBest ≥ τsim )
       CandidateTuples [TC].Patterns [PBest] = SimBest;
   return CandidateTuples;
```

#### **Giải Thích Bước Qua Bước:**

##### **Bước 1: Tạo Xuất Hiện (CreateOccurrence)**

- **Điều Gì Xảy Ra:**
    
    - Máy tính đọc một đoạn văn bản và tìm thấy hai thực thể (ví dụ: một công ty và một địa điểm).
    - Nó tạo ra một **5-tuple** gồm các phần thông tin xung quanh hai thực thể này: bên trái, giữa và bên phải.
- **Ví Dụ:**
    
    - Giả sử trong câu "Microsoft, Redmond, đã ra mắt sản phẩm mới," "Microsoft" là ORGANIZATION (công ty) và "Redmond" là LOCATION (địa điểm).
    - Máy tính sẽ lưu lại thông tin xung quanh hai từ này để so sánh với các mẫu đã biết.

##### **Bước 2: So Sánh Với Các Mẫu (Match)**

- **Điều Gì Xảy Ra:**
    
    - Máy tính sẽ kiểm tra xem đoạn văn bản vừa tìm thấy có phù hợp với bất kỳ mẫu nào trong danh sách các **Patterns** (mẫu trích xuất) hay không.
    - **sim** là mức độ tương đồng giữa đoạn văn bản và mẫu.
- **Điều Kiện Kiểm Tra:**
    
    - Nếu mức độ tương đồng **sim** lớn hơn hoặc bằng một ngưỡng đã định **τsim**, máy tính sẽ xem xét mẫu đó là phù hợp.

##### **Bước 3: Cập Nhật Độ Chọn Lọc và Chọn Mẫu Tốt Nhất**

- **Cập Nhật Độ Chọn Lọc (UpdatePatternSelectivity):**
    
    - Máy tính cập nhật thông tin về mức độ tin cậy của mẫu **p** dựa trên việc nó vừa trùng khớp với đoạn văn bản này hay không.
- **Chọn Mẫu Tốt Nhất:**
    
    - Nếu **sim** hiện tại lớn hơn hoặc bằng **SimBest** (mức độ tương đồng tốt nhất hiện tại), máy tính sẽ cập nhật **SimBest** và lưu lại mẫu **PBest** là mẫu có độ tương đồng cao nhất.
- **Lưu Kết Quả:**
    
    - Nếu **SimBest** vẫn lớn hơn hoặc bằng **τsim**, máy tính sẽ lưu lại rằng cặp thực thể **TC** (ví dụ: Microsoft và Redmond) được hỗ trợ bởi mẫu **PBest** với mức độ tương đồng **SimBest**.

##### **Trả Về Kết Quả (Return CandidateTuples):**

- **Điều Gì Xảy Ra:**
    - Máy tính trả về danh sách các cặp thực thể cùng với các mẫu đã hỗ trợ chúng. Đây chính là những mối quan hệ mà máy tính đã xác định được từ đoạn văn bản.

#### **Tóm Tắt Bằng Ví Dụ:**

1. **Tìm Xuất Hiện:**
    
    - Máy tính đọc câu "Microsoft, Redmond, đã ra mắt sản phẩm mới" và xác định "Microsoft" là công ty và "Redmond" là địa điểm. Nó cũng ghi nhớ các từ xung quanh hai từ này như "Microsoft, Redmond, đã ra mắt".
2. **So Sánh Với Mẫu:**
    
    - Máy tính so sánh đoạn "Microsoft, Redmond, đã ra mắt" với các mẫu đã biết như "<từ bên trái>, LOCATION, <từ giữa>, ORGANIZATION, <từ bên phải>".
    - Nếu mức độ tương đồng cao (ví dụ: **sim = 0.8** và **τsim = 0.7**), nó sẽ tiếp tục xử lý.
3. **Cập Nhật và Lưu Kết Quả:**
    
    - Máy tính cập nhật độ tin cậy của mẫu và lưu lại rằng cặp "Microsoft - Redmond" phù hợp với mẫu này với mức độ tin cậy là 0.8.
4. **Hoàn Thành:**
    
    - Cuối cùng, máy tính trả về danh sách các cặp thực thể và mẫu đã hỗ trợ chúng, ví dụ: ("Microsoft", "Redmond") được hỗ trợ bởi mẫu với **sim = 0.8**.

#### **Kết Luận:**

Đoạn công thức này giúp máy tính tự động tìm kiếm và xác định các mối quan hệ giữa các thực thể trong văn bản bằng cách so sánh các đoạn văn bản với các mẫu đã biết. Quá trình này giống như việc bạn sử dụng các manh mối để tìm kho báu, nơi máy tính sử dụng các mẫu và mức độ tương đồng để xác định các mối quan hệ một cách chính xác và hiệu quả.