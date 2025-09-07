
### **1. Mean Reciprocal Rank (MRR) là gì?**

**MRR** là một chỉ số đánh giá hiệu suất của hệ thống truy xuất thông tin hoặc hệ thống gợi ý. Nó đo lường mức độ mà kết quả đầu tiên **có liên quan** xuất hiện trong danh sách các kết quả.

#### **Công thức MRR**

MRR=1N∑i=1N1ranki\text{MRR} = \frac{1}{N} \sum_{i=1}^N \frac{1}{\text{rank}_i}

- NN: Tổng số truy vấn (queries).
- ranki\text{rank}_i: Vị trí (rank) của tài liệu liên quan đầu tiên trong danh sách kết quả cho truy vấn thứ ii.

#### **Cách hiểu MRR**

- Nếu tài liệu liên quan nhất xuất hiện ở **đầu tiên**, MRR = 1.
- Nếu tài liệu liên quan xuất hiện ở **vị trí thứ 3**, giá trị reciprocal rank là 13\frac{1}{3}.
- MRR là trung bình của các reciprocal rank trên toàn bộ truy vấn.

#### **Ví dụ**

Hệ thống trả về kết quả cho 3 truy vấn:

- Truy vấn 1: Tài liệu liên quan ở vị trí **1** → Rank =1= 1.
- Truy vấn 2: Tài liệu liên quan ở vị trí **3** → Rank =13= \frac{1}{3}.
- Truy vấn 3: Tài liệu liên quan không xuất hiện → Rank =0= 0.

MRR=13(1+13+0)=49≈0.444\text{MRR} = \frac{1}{3} \left( 1 + \frac{1}{3} + 0 \right) = \frac{4}{9} \approx 0.444

---

### **2. Hit Rate và Recall có giống nhau không?**

**Hit Rate** và **Recall** là hai khái niệm tương tự nhau nhưng có những điểm khác biệt nhỏ, tùy thuộc vào ngữ cảnh sử dụng.

#### **Hit Rate**

- **Hit Rate** đo lường tần suất mà hệ thống tìm thấy ít nhất **một tài liệu liên quan** trong danh sách trả về.
- Công thức:

Hit Rate=Soˆˊ truy vaˆˊn coˊ ıˊt nhaˆˊt một taˋi liệu lieˆn quanTổng soˆˊ truy vaˆˊn\text{Hit Rate} = \frac{\text{Số truy vấn có ít nhất một tài liệu liên quan}}{\text{Tổng số truy vấn}}

- **Ý nghĩa**:
    - Nếu danh sách kết quả chứa ít nhất một tài liệu liên quan cho truy vấn, đó là một "hit".
    - **Không quan tâm đến vị trí** hoặc số lượng tài liệu liên quan.

#### **Recall**

- **Recall** đo lường tỷ lệ giữa số tài liệu liên quan được truy xuất và tổng số tài liệu liên quan.
- Công thức:

Recall=Soˆˊ taˋi liệu lieˆn quan được trả veˆˋTổng soˆˊ taˋi liệu lieˆn quan trong hệ thoˆˊng\text{Recall} = \frac{\text{Số tài liệu liên quan được trả về}}{\text{Tổng số tài liệu liên quan trong hệ thống}}

- **Ý nghĩa**:
    - Xem xét toàn bộ tài liệu liên quan trong tập dữ liệu.
    - Chú ý đến số lượng tài liệu liên quan được trả về.

---

### **So sánh Hit Rate và Recall**

|**Thuộc tính**|**Hit Rate**|**Recall**|
|---|---|---|
|**Quan tâm**|Có tài liệu liên quan xuất hiện hay không|Số lượng tài liệu liên quan được tìm thấy|
|**Công thức đơn giản**|Phần trăm truy vấn có tài liệu liên quan|Phần trăm tài liệu liên quan được tìm thấy|
|**Phạm vi sử dụng**|Đánh giá danh sách kết quả (top-k items)|Đánh giá toàn bộ tài liệu liên quan|

---

### **Tóm tắt**

- **MRR**: Tập trung vào vị trí của tài liệu liên quan đầu tiên.
- **Hit Rate**: Chỉ cần biết có tài liệu liên quan hay không, không quan tâm số lượng.
- **Recall**: Đánh giá tỷ lệ tài liệu liên quan được tìm thấy trong tổng số tài liệu liên quan.

Nếu bạn cần giải thích thêm hoặc muốn ví dụ chi tiết, hãy cho tôi biết! 😊

