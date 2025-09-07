## **mỗi cách giải quyết một hạn chế của cách trước**

- **One-hot**: quá đơn giản, không biết từ nào quan trọng, không hiểu ngữ nghĩa.
    
- **BoW**: thêm tần suất → phân biệt văn bản khác nhau, nhưng vẫn coi “the, is, and” quan trọng ngang “dog, rocket”.
    
- **TF-IDF**: sửa được chuyện đó bằng cách giảm trọng số từ phổ biến, làm nổi bật từ “đặc trưng”. Nhưng vẫn **không hiểu nghĩa**, chỉ là thống kê số học.
    
- Sau đó mới đến **Word Embeddings (Word2Vec, GloVe)** → cho máy “cảm nhận nghĩa” bằng vector gần nhau (dog ~ puppy, king – man + woman ≈ queen).
    
- Rồi mới lên **Transformer, BERT, GPT** → hiểu ngữ cảnh, trật tự, sắc thái.

Hãy tưởng tượng bạn mô tả một người:

- **One-hot**: chỉ biết “người này có/không có mắt kính”.
    
- **BoW**: ghi lại bao nhiêu lần người này nói từ “pizza”.
    
- **TF-IDF**: biết rằng từ “pizza” đặc trưng cho người này hơn “hello”.
    
- **Embedding**: hiểu rằng “pizza” gần nghĩa với “pasta”, xa “computer”.

---

![[Pasted image 20250820212852.png]]

---
- TF: → Số lần từ ttt xuất hiện trong document d.
  

# Giải thích 

### 1.1 
Có 4 văn bản (documents):

- D1 = [dog, bites, man]
    
- D2 = [man, bites, dog]
    
- D3 = [dog, eats, meat]
    
- D4 = [man, eats, food]
    

Vocabulary = {bites, dog, eats, food, man, meat}


![[Pasted image 20250820213502.png]]

Stop-word: df lớn gần đến N. 

- Xuất hiện trong tất cả các tài liệu => IDF = 1. 
- 


--- 
# Embedding: 
- [intfloat/multilingual-e5-large · Hugging Face](https://huggingface.co/intfloat/multilingual-e5-large)
- [sentence-transformers/paraphrase-multilingual-mpnet-base-v2 · Hugging Face](https://huggingface.co/sentence-transformers/paraphrase-multilingual-mpnet-base-v2)




---

[Deep-ML | Chi-square Probability Distribution](https://beta.deep-ml.com/problems/176)



Ok 👍 mình sẽ **tóm tắt toàn bộ project** bạn vừa code thành một bản “project summary” đầy đủ.

---

# 📘 Project Summary: Text Classification with Different Representations and Models

## 🎯 Mục tiêu

- Thực hiện **phân loại văn bản (arXiv abstracts)** thành 5 lĩnh vực chính: `astro-ph, cond-mat, cs, math, physics`.
    
- So sánh hiệu quả giữa các **cách biểu diễn văn bản** (BoW, TF-IDF, Word Embeddings) khi áp dụng các **thuật toán Machine Learning khác nhau** (KMeans, KNN, Decision Tree, Naive Bayes).
    
- Đánh giá bằng **Accuracy** và **Confusion Matrix**.
    

---

## 🗂️ Dataset

- Nguồn: **HuggingFace – UniverseTBD/arxiv-abstracts-large**.
    
- Lọc 1000 samples, chỉ lấy những abstract có **một nhãn duy nhất** thuộc 5 categories.
    
- Tiền xử lý:
    
    - Loại bỏ ký tự đặc biệt, số, xuống dòng.
        
    - Chuẩn hoá chữ thường.
        
    - Chỉ giữ **primary label** (vd: `cs.AI → cs`).
        

---

## 🔠 Biểu diễn văn bản (Feature Engineering)

1. **Bag of Words (BoW)**
    
    - Dùng `CountVectorizer`, mỗi document → vector đếm số lần từ xuất hiện.
        
    - Đặc trưng: sparse, nhiều chiều, không giữ ngữ nghĩa.
        
2. **TF-IDF**
    
    - Dùng `TfidfVectorizer`, mỗi từ có trọng số dựa trên tần suất trong document và nghịch đảo tần suất trong toàn bộ corpus.
        
    - Đặc trưng: giảm trọng số từ phổ biến, làm nổi bật từ đặc trưng.
        
3. **Word Embeddings**
    
    - Dùng model **SentenceTransformer (intfloat/multilingual-e5-base)**.
        
    - Vector dense, continuous, có ngữ nghĩa (semantic meaning).
        

---

## 🤖 Machine Learning Models

1. **KMeans (Clustering)**
    
    - Unsupervised, chia thành số cluster bằng số labels.
        
    - Mapping cluster → label bằng majority vote.
        
    - Accuracy trung bình, TF-IDF > BoW, embedding không vượt trội vì dữ liệu ít.
        
2. **KNN (K-Nearest Neighbors)**
    
    - Supervised, gán label theo majority của k neighbors.
        
    - Hoạt động khá tốt với TF-IDF và embeddings.
        
    - Accuracy cao hơn KMeans.
        
3. **Decision Tree**
    
    - Supervised, rule-based splitting.
        
    - Kết quả **thấp nhất** trong các mô hình.
        
    - Nguyên nhân: dữ liệu sparse, ít mẫu (1000), dễ overfit, không tận dụng tốt embedding vector.
        
4. **Naive Bayes (GaussianNB)**
    
    - Supervised, giả định độc lập giữa các từ.
        
    - Phù hợp với text data (BoW, TF-IDF).
        
    - Accuracy cao, đặc biệt trên TF-IDF.
        

---

## 📊 Kết quả chính (tóm gọn)

- **BoW**: baseline, dễ bị noise.
    
- **TF-IDF**: tốt nhất cho Naive Bayes, KNN.
    
- **Embeddings**: mạnh nhưng chưa phát huy hết do tập nhỏ, DT không phù hợp.
    
- **Decision Tree**: accuracy thấp nhất → không khuyến nghị dùng cho text classification cơ bản.
    

---

## 📌 Kết luận

1. **TF-IDF + Naive Bayes/KNN** là lựa chọn tốt nhất cho dataset này.
    
2. **Embeddings** cần dataset lớn hơn và mô hình phù hợp (Logistic Regression, SVM, Neural Net).
    
3. **Decision Tree** không phù hợp với dữ liệu văn bản sparse/dense vector → performance thấp.
    
4. Dự án cho thấy **sự tiến hóa từ BoW → TF-IDF → Embeddings** trong NLP.
    

---

👉 Đây là một **mini research pipeline** giúp hiểu rõ ảnh hưởng của **feature representation** và **ML model selection** trong NLP.

---

Bạn có muốn mình viết thêm **phần “Future Work”** (gợi ý nên thử Logistic Regression, SVM, Neural Network, tăng dữ liệu, dùng stopword removal, n-gram…) để biến summary này thành một **báo cáo hoàn chỉnh dạng research report** không?



```
Ad ơi cho em hỏi thêm, hiện mình đang apply tất cả các classifer (model) và feature Extraction kết hợp với nhau. trong các tình huống thực tế mình cũng đi test kết hợp từng phương pháp với nhau như v hay có cách nào lựa chọn được trước mô hình rồi mới run code ko ạ
```

![[Pasted image 20250820224008.png]]


IDF = 

