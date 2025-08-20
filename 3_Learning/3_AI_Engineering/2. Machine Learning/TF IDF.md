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




--- 
# Embedding: 
- [intfloat/multilingual-e5-large · Hugging Face](https://huggingface.co/intfloat/multilingual-e5-large)
- [sentence-transformers/paraphrase-multilingual-mpnet-base-v2 · Hugging Face](https://huggingface.co/sentence-transformers/paraphrase-multilingual-mpnet-base-v2)