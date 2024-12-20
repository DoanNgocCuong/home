
1. summaryTruLens: Đánh giá và Theo dõi Ứng dụng LLMturn0fetch0 TruLens là một công cụ mã nguồn mở được thiết kế để đánh giá và theo dõi hiệu suất của các ứng dụng dựa trên Mô hình Ngôn ngữ Lớn (LLM). Nó cung cấp các "hàm phản hồi" giúp đánh giá chất lượng đầu vào, đầu ra và kết quả trung gian của ứng dụng, hỗ trợ phát hiện và cải thiện các điểm yếu trong quá trình phát triển. citeturn0search3

Vì TruLens là phần mềm mã nguồn mở, bạn có thể sử dụng miễn phí. Tuy nhiên, nếu bạn tích hợp TruLens với các dịch vụ bên thứ ba như OpenAI hoặc Azure OpenAI để đánh giá, có thể phát sinh chi phí từ các dịch vụ này. Do đó, việc sử dụng TruLens bản thân không mất phí, nhưng các dịch vụ liên quan có thể có chi phí tùy thuộc vào nhà cung cấp.
- [truera/trulens: Evaluation and Tracking for LLM Experiments](https://github.com/truera/trulens?utm_source=chatgpt.com)
- [Refining RAG Accuracy with TrueLens: An Evaluation Guide | by Kadam Sayali | Nov, 2024 | GoPenAI](https://blog.gopenai.com/refining-rag-accuracy-with-truelens-an-evaluation-guide-1512ab257ab3)


![[Pasted image 20241122010335.png]]

Dưới đây là bảng chi tiết giải thích 3 chỉ số **Groundedness**, **Answer Relevance**, và **Context Relevance** được đo lường trong TruLens:

|**Chỉ số**|**Định nghĩa**|**Mục tiêu**|**Cách đo lường trong TruLens**|
|---|---|---|---|
|**Groundedness**|Đo lường mức độ mà câu trả lời được hỗ trợ bởi thông tin truy xuất từ vector store hoặc tài liệu nguồn.|- Đảm bảo câu trả lời dựa vào thông tin có sẵn.- Giảm thiểu **hallucination** (thông tin không chính xác hoặc bịa đặt).|- So sánh câu trả lời với nội dung tài liệu truy xuất được.- Sử dụng hàm `Feedback` để đánh giá mức độ "grounded" của câu trả lời.|
|**Answer Relevance**|Đo lường mức độ mà câu trả lời phù hợp và đúng với câu hỏi được đặt ra.|- Đảm bảo câu trả lời đúng trọng tâm và đầy đủ.- Loại bỏ câu trả lời lạc đề hoặc không chính xác.|- So sánh giữa **prompt (câu hỏi)** và **response (câu trả lời)**.- Sử dụng mô hình hoặc độ tương đồng ngữ nghĩa (semantic similarity) để đo độ phù hợp.|
|**Context Relevance**|Đo lường mức độ mà ngữ cảnh (tài liệu truy xuất từ vector store) liên quan trực tiếp đến câu hỏi được đặt ra.|- Đảm bảo ngữ cảnh được sử dụng phù hợp với câu hỏi.- Loại bỏ các ngữ cảnh không liên quan trước khi đưa vào mô hình GPT để trả lời.|- So sánh ngữ cảnh truy xuất từ `retrieve()` với câu hỏi.- Sử dụng mô hình hoặc phép đo để đánh giá mức độ liên quan của ngữ cảnh với câu hỏi đầu vào.|

---

### **Chi tiết thêm cho mỗi chỉ số**:

#### 1. **Groundedness**

- **Ví dụ tốt**:
    - Câu trả lời: _"Starbucks represents the second wave of coffee culture."_
    - Trích dẫn được từ tài liệu: _"Starbucks is seen to be the main representation of the United States' second wave of coffee culture."_
- **Ví dụ không tốt**:
    - Câu trả lời: _"Starbucks is responsible for the third wave of coffee culture."_ (Thông tin không có trong nguồn, hallucination).

#### 2. **Answer Relevance**

- **Ví dụ tốt**:
    - **Câu hỏi**: _"What wave of coffee culture is Starbucks seen to represent?"_
    - **Câu trả lời**: _"Starbucks represents the second wave of coffee culture."_ (Đúng trọng tâm và trả lời chính xác câu hỏi).
- **Ví dụ không tốt**:
    - **Câu trả lời**: _"Starbucks is a coffee company based in Seattle."_ (Thông tin đúng nhưng không trả lời câu hỏi).

#### 3. **Context Relevance**

- **Ví dụ tốt**:
    - **Câu hỏi**: _"What wave of coffee culture is Starbucks seen to represent?"_
    - **Ngữ cảnh truy xuất**: _"Starbucks is seen to be the main representation of the United States' second wave of coffee culture."_ (Ngữ cảnh liên quan trực tiếp).
- **Ví dụ không tốt**:
    - **Ngữ cảnh truy xuất**: _"Seattle is home to a large tech industry, including Microsoft and Amazon."_ (Ngữ cảnh không liên quan đến câu hỏi).

---

Nếu bạn cần thêm ví dụ thực tế hoặc cách cải thiện các chỉ số này, mình sẵn sàng hỗ trợ!



### **Ý nghĩa và hoạt động của đoạn mã sử dụng Guardrails**

Đoạn mã bạn cung cấp triển khai **Guardrails** (tạm hiểu là "rào chắn") bằng cách sử dụng **context relevance score** làm tiêu chí lọc ngữ cảnh trước khi ngữ cảnh được đưa vào mô hình LLM (GPT). Điều này nhằm giảm hiện tượng **hallucination** và cải thiện hiệu quả xử lý.

---

### **Giải thích chi tiết các thành phần chính trong đoạn mã**

#### 1. **Guardrails là gì?**

- Guardrails được sử dụng để:
    - **Kiểm soát chất lượng** thông tin được sử dụng trước khi gửi tới LLM.
    - **Loại bỏ ngữ cảnh không liên quan**, giúp cải thiện câu trả lời.
- Trong trường hợp này, `@context_filter` được sử dụng làm decorator để lọc ngữ cảnh dựa trên **context relevance score**.

---

#### 2. **Cách Guardrails hoạt động trong đoạn mã**

##### **a. Định nghĩa chỉ số đánh giá Context Relevance**

```python
f_context_relevance_score = Feedback(
    provider.context_relevance, name="Context Relevance"
)
```

- `Feedback` định nghĩa một hàm đánh giá (feedback function) đo mức độ **liên quan của ngữ cảnh** (context relevance).
- **`provider.context_relevance`**: Được cung cấp bởi TruLens, đo lường mức độ ngữ cảnh liên quan đến câu hỏi.

---

##### **b. Bộ lọc ngữ cảnh với @context_filter**

```python
@context_filter(
    feedback=f_context_relevance_score,
    threshold=0.75,
    keyword_for_prompt="query",
)
```

- **`@context_filter`**: Decorator này áp dụng bộ lọc dựa trên feedback function `f_context_relevance_score`.
- **`threshold=0.75`**:
    - Điểm **context relevance score** phải **>= 0.75** mới được coi là ngữ cảnh liên quan.
    - Nếu không, ngữ cảnh đó sẽ bị loại bỏ.
- **`keyword_for_prompt="query"`**:
    - Chỉ định rằng ngữ cảnh được lọc dựa trên từ khóa (ở đây là "query").

---

##### **c. Tích hợp Guardrails vào hàm `retrieve`**

```python
def retrieve(self, query: str) -> list:
    results = vector_store.query(query_texts=query, n_results=4)
    if "documents" in results and results["documents"]:
        return [doc for sublist in results["documents"] for doc in sublist]
    else:
        return []
```

- **Ngữ cảnh ban đầu**: Truy xuất từ `vector_store` dựa trên `query` (câu hỏi).
- **Sau khi lọc**:
    - Chỉ các ngữ cảnh đạt điểm **context relevance >= 0.75** mới được trả về.
    - Nếu không có ngữ cảnh nào đạt yêu cầu, danh sách ngữ cảnh trả về sẽ rỗng (`[]`).

---

#### 3. **Tích hợp Guardrails với TruCustomApp**

```python
filtered_tru_rag = TruCustomApp(
    filtered_rag,
    app_name="RAG",
    app_version="filtered",
    feedbacks=[f_groundedness, f_answer_relevance, f_context_relevance],
)
```

- **`TruCustomApp`**: Đóng gói ứng dụng RAG đã lọc (FilteredRAG) để đo lường các chỉ số.
- **`feedbacks`**:
    - Kết hợp 3 chỉ số: **Groundedness**, **Answer Relevance**, **Context Relevance**.

---

#### 4. **Kết quả khi sử dụng Guardrails**

- Khi bạn thực hiện các truy vấn:
    
    ```python
    with filtered_tru_rag as recording:
        filtered_rag.query("What wave of coffee culture is Starbucks seen to represent in the United States?")
    ```
    
- **Trước khi truy vấn tới LLM**:
    - Ngữ cảnh được lọc bằng Guardrails (chỉ các ngữ cảnh phù hợp được gửi đến LLM).
- **Lợi ích**:
    - **Giảm Hallucination**: LLM sẽ không xử lý các ngữ cảnh không liên quan.
    - **Cải thiện hiệu quả**: LLM chỉ làm việc với thông tin thực sự liên quan.

---

#### 5. **Chạy Dashboard để xem kết quả**

```python
run_dashboard(session)
```

- Hiển thị kết quả đánh giá các truy vấn trên Dashboard của TruLens, bao gồm:
    - **Điểm Groundedness**.
    - **Answer Relevance**.
    - **Context Relevance**.

---

### **Tóm lại: Tại sao cần Guardrails?**

- Guardrails đóng vai trò **lọc ngữ cảnh** để đảm bảo thông tin gửi tới LLM là chất lượng, phù hợp, và giảm thiểu nguy cơ sinh ra thông tin sai lệch.
- Đoạn mã trên cho phép kiểm soát việc truy xuất ngữ cảnh từ vector store, sử dụng các tiêu chí đánh giá định lượng như context relevance.