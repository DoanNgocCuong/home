Chain-of-Thought x Chain of Prompt x Multi-Step Reasoning x Reflection Tuning

Chain of Thought Prompting Tabular Format Prompting Zero, One, and Few Shot Prompting Ask Before Answer Prompting Fill-In-The-Blank Prompting Perspective Prompting Constructive Critic Prompting Comparative Prompting Reverse Prompting RGC Prompting


```
Bash 1. CÁCH TẠO BỘ TEST (câu hỏi và câu trả lời 10 điểm): +, Các tiêu chí của 1 câu hỏi và câu đáp án soạn sẵn 10 điểm (chi tiết bên dưới): Độ chính xác 3 điểm, tính mạch lạc 2 điểm, phù hợp ngữ cảnh 2 điểm, tính đầy đủ của câu hỏi 2 điểm, tốc độ phản hồi 1 điểm. +, Mỗi đoạn (4-5 câu) => tạo 12 câu hỏi +, Thể loại: trắc nghiệm, tự luận, tình huống. Mỗi loại câu hỏi gồm 4 câu ở 4 mức độ sau: +, Mức độ: - Actual Questions: Câu hỏi yêu cầu thông tin cụ thể, chi tiết. Ví dụ: "Nhiệt độ cao nhất ở Hà Nội vào ngày mai là bao nhiêu?" - Conversational Queries: Câu hỏi theo phong cách hội thoại, yêu cầu mô hình hiểu và trả lời tự nhiên. Ví dụ: "Ngày mai ở Hà Nội có nên ra ngoài không?" - Ambiguous Questions: Câu hỏi mơ hồ, không rõ ràng, yêu cầu mô hình phải phán đoán hoặc làm rõ. Ví dụ: "Ngày mai thời tiết thế nào?" - Requests for Clarification: Câu hỏi yêu cầu làm rõ một thông tin trước đó. Ví dụ: "Bạn có thể giải thích rõ hơn về dự báo thời tiết cho ngày mai không?" -------------------------------------------------------------------------- -------------------------------------------------------------------------- 2. Metrics ĐÁNH GIÁ: +, Human: Độ chính xác 3 điểm, tính mạch lạc 2 điểm, phù hợp ngữ cảnh 2 điểm, tính đầy đủ của câu hỏi 2 điểm, tốc độ phản hồi 1 điểm. +, Metrics Logic: BLEU Score, ROUGE Scor BLEU Score: Đo lường mức độ trùng khớp giữa văn bản mô hình tạo ra và văn bản tham chiếu. Lý do: Đánh giá khả năng tạo ra câu trả lời tương đồng với dữ liệu mẫu. ROUGE Score: Tập trung vào khả năng hồi tưởng, so sánh số lượng n-gram, từ hoặc câu từ văn bản tham chiếu có trong phản hồi của mô hình. Lý do: Đo lường khả năng mô hình nắm bắt thông tin chính xác từ câu hỏi. Context Retention: Đánh giá khả năng duy trì ngữ cảnh qua các câu hỏi liên tiếp. Lý do: Kiểm tra tính mạch lạc và hiểu ngữ cảnh trong hội thoại dài. F1-score: Kết hợp giữa Precision (độ chính xác) và Recall (khả năng hồi tưởng) để đo lường hiệu quả mô hình. Lý do: Đánh giá khả năng trả lời đúng cho các câu hỏi có đáp án cụ thể.
```
```
Bash
### Tiêu chí đánh giá câu hỏi và câu đáp án soạn sẵn (10 điểm)

#### 1. Độ chính xác (Accuracy) - 3 điểm:
   - Tiêu chí: Đáp án có đúng và đầy đủ các thông tin quan trọng liên quan đến câu hỏi không.
   - Ví dụ: Nếu câu hỏi yêu cầu nhiệt độ cao nhất ở Hà Nội ngày mai, đáp án phải đưa ra đúng thông tin dự báo.
   
   - Cách cho điểm:
     - 3 điểm: Đáp án hoàn toàn chính xác và đầy đủ.
     - 2 điểm: Đáp án đúng nhưng thiếu một vài chi tiết nhỏ.
     - 1 điểm: Đáp án có lỗi sai nhưng vẫn có thông tin chính.
     - 0 điểm: Đáp án sai hoàn toàn hoặc không liên quan.

#### 2. Tính mạch lạc (Coherence) - 2 điểm:
   - Tiêu chí: Câu trả lời có rõ ràng, mạch lạc và logic không.
   - Ví dụ: Đáp án không được chứa các câu rời rạc, không liên kết với nhau.
   
   - Cách cho điểm:
     - 2 điểm: Đáp án rõ ràng, liên kết tốt, các ý bổ trợ lẫn nhau.
     - 1 điểm: Đáp án mạch lạc nhưng có một số ý chưa liên kết chặt chẽ.
     - 0 điểm: Đáp án không mạch lạc hoặc lủng củng.

#### 3. Phù hợp ngữ cảnh (Context Appropriateness) - 2 điểm:
   - Tiêu chí: Đáp án có phù hợp với ngữ cảnh câu hỏi và các chi tiết đưa ra không.
   - Ví dụ: Nếu câu hỏi yêu cầu mô tả thời tiết, đáp án không thể nói về giao thông.
   
   - Cách cho điểm:
     - 2 điểm: Đáp án hoàn toàn phù hợp với ngữ cảnh và chi tiết câu hỏi.
     - 1 điểm: Đáp án có một vài phần chưa phù hợp nhưng vẫn liên quan đến chủ đề chính.
     - 0 điểm: Đáp án không phù hợp với ngữ cảnh hoặc hoàn toàn lạc đề.

#### 4. Tính đầy đủ (Completeness) - 2 điểm:
   - Tiêu chí: Đáp án có trả lời đầy đủ tất cả các phần của câu hỏi không.
   - Ví dụ: Nếu câu hỏi yêu cầu giải thích thời tiết và đưa ra lời khuyên, đáp án cần cả hai phần.
   
   - Cách cho điểm:
     - 2 điểm: Đáp án đầy đủ, không bỏ sót bất kỳ phần nào của câu hỏi.
     - 1 điểm: Đáp án có thông tin chính nhưng thiếu một số phần nhỏ.
     - 0 điểm: Đáp án không hoàn thành các yêu cầu chính của câu hỏi.

#### 5. Tốc độ phản hồi (Response Time) - 1 điểm:
   - Tiêu chí: Đáp án có được đưa ra trong thời gian hợp lý không.
   - Ví dụ: Mô hình phải phản hồi nhanh chóng, không bị chậm trễ quá nhiều.
   
   - Cách cho điểm:
     - 1 điểm: Đáp án phản hồi nhanh chóng, không có độ trễ đáng kể.
     - 0 điểm: Đáp án bị trễ hoặc không phản hồi trong thời gian hợp lý.

### Tổng kết:
- Độ chính xác: 3 điểm
- Tính mạch lạc: 2 điểm
- Phù hợp ngữ cảnh: 2 điểm
- Tính đầy đủ: 2 điểm
- Tốc độ phản hồi: 1 điểm

Tổng cộng: 10 điểm

Cách chia điểm này giúp đánh giá toàn diện một câu trả lời dựa trên nhiều tiêu chí quan trọng từ chất lượng thông tin đến tốc độ xử lý.



```
```
Em đang research thêm. Có method: "LLM Self Evaluation": 1 pipeline tự động đánh giá chất lượng của hệ thống RAG (mà ko nhất thiết phải build sẵn câu hỏi và câu trả lời). Cơ chế hoạt động:

1. Câu hỏi (tự build/hệ thống tự động sinh câu hỏi).
2. Với mỗi câu hỏi -> LLM sẽ trả lời
3. Sau khi LLM tạo ra câu trả lời, pipeline sẽ đánh giá cặp câu hỏi - câu trả lời này bằng cách sử dụng chính LLM để kiểm tra tính chính xác của câu trả lời (hoặc sử dụng 1 LLM nâng cao như GPT4). Quá trình này lặp lại 3-5 lần => đo ra độ chính xác của model.

---

LLM Self Evaluation: Implement a LLM self-evaluation pipeline to provide a quantitative evaluation of the different splitting strategies and their performance
```

```
Retrieval-Augmented Generation (RAG) is a technique that enhances the capability of large language models (LLMs) by leveraging external knowledge. Here is a step-by-step evaluation of the RAG pipeline based on the 2023 insights:

### 1. Overview

RAG enhances language model generation by combining it with external knowledge. This method involves retrieving relevant information from a knowledge base and using it to generate responses with LLMs.

### 2. The Rise of RAG

Hallucination, a common issue with LLMs like GPT-4 and others, inspires the development of RAG. These models often generate plausible but incorrect information. RAG addresses this by retrieving specific, relevant information from large, specialized documents, thus providing a more controlled and accurate output.

### 3. Neural Retrieval Models

Understanding neural retrieval models is crucial:

- They use neural networks to encode both queries and document chunks into dense vectors.
- This allows the retrieval system to capture semantic relevance beyond mere keyword matching.

### 4. RAG Pipeline

The RAG pipeline includes:

- **Vector Encoding:** Queries and document chunks are converted into vectors using models like BERT.
- **Semantic Matching:** Dense vector embeddings are matched to find the most relevant documents.
- **Combining Data:** Retrieved documents are combined with the initial query to form a prompt for the LLM.
- **Generate Text:** The enhanced prompt is fed into the LLM to generate the final response.

### 5. Advantages of RAG

- **Utilizes External Data:** Enhances the LLM's knowledge base without retraining the model.
- **Handles Unlabeled Data:** Effective even with limited labeled data.
- **Real-Time Information Retrieval:** Ideal for applications like virtual assistants and real-time information access.

### 6. Choosing a Vector Database

- **Types:** Vector databases (e.g., using dense embeddings) and graph databases (e.g., structured knowledge bases) are compared for their efficacy in RAG.
- **Comparison:** Vector databases are good for semantic retrieval, while graph databases ensure high accuracy but require precise queries.

### 7. Building a RAG System

Three key steps: Ingestion, Retrieval, and Synthesis/Response Generation.

- **Chunking:** Divides documents into manageable segments for retrieval.
- **Embeddings:** Converts queries and document chunks into a comparable vector form.
- **Response Generation:** Combines the retrieved knowledge with the query to generate coherent and accurate responses.

### 8. Embeddings

- **Sparse vs. Dense:** Dense embeddings (e.g., Sentence Transformers) are preferred for capturing the semantics of sentences.
- **Sentence Transformers:** Effective for generating meaningful sentence-level embeddings suitable for RAG.

### Conclusion

RAG is a powerful method to leverage external knowledge, providing accurate and contextually relevant responses without requiring extensive retraining of LLMs. It is particularly useful in scenarios where access to vast, unlabeled information is necessary.

**Sources:**

- [ChatGPT Series 5: Tìm hiểu về Retrieval Augmented Generation (RAG)](https://viblo.asia/p/chatgpt-series-5-tim-hieu-ve-retrieval-augmented-generation-rag-Ny0VGRd7LPA)

---

---

---

---

---

---
```


What would you like ChatGPT to know about you?
 ● Location:
 ● Profession/Role:
 ● Background:
 ● KeyResponsibilities:
 ● Knowledge or Expertise:
 ● Jargon or Terminology:
 ● Typical Challenges:
 ● Current Projects:
 ● Goals and Objectives:
 Howwouldyou like ChatGPT to respond?
 ● Tone:
 ● Response Format: (Tabular,bulletpoints, paragraphs)
 ● Response style: (creative,precise, in the style of or act as)
 ● Level of Detail: (Howlongorshortshouldresponses generally be?)
 ● Sources: (preferred sources or cite sources)
 ● Bias: (ShouldChatGPThaveopinions on topics or remain neutral?)
 Hot Keys:
 WhenItype “5q” Provide me 5 thought-provoking questions about
 the current topic
 WhenItype “3p” please give me 3 alternative prompts I could use
 to get the results I’m looking for.

---
![[Pasted image 20250308012453.png]]