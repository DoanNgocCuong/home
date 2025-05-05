Dựa trên mô hình perceptron trong hình, ta có các bước tính toán cụ thể cho từng ví dụ để quyết định "Goes sailing" hay "Does not go sailing".

### **Công thức đầu ra của perceptron:**

y=sign(w0⋅1+w1⋅x1+w2⋅x2+w3⋅x3)y = \text{sign}(w_0 \cdot 1 + w_1 \cdot x_1 + w_2 \cdot x_2 + w_3 \cdot x_3)

Với các trọng số đã cho:

- w0=−0.5w_0 = -0.5
- w1=0.6w_1 = 0.6
- w2=0.1w_2 = 0.1
- w3=−0.6w_3 = -0.6

**Bảng dữ liệu cho 2 ví dụ:**

- **Example 1:** (x1=0,x2=1,x3=0)(x_1 = 0, x_2 = 1, x_3 = 0)
- **Example 2:** (x1=1,x2=2,x3=1)(x_1 = 1, x_2 = 2, x_3 = 1)

---

### **Tính toán cho Example 1:**

Tổng đaˆˋu vaˋo=w0⋅1+w1⋅0+w2⋅1+w3⋅0\text{Tổng đầu vào} = w_0 \cdot 1 + w_1 \cdot 0 + w_2 \cdot 1 + w_3 \cdot 0 =−0.5⋅1+0.6⋅0+0.1⋅1+(−0.6)⋅0= -0.5 \cdot 1 + 0.6 \cdot 0 + 0.1 \cdot 1 + (-0.6) \cdot 0 =−0.5+0+0.1+0=−0.4= -0.5 + 0 + 0.1 + 0 = -0.4

Kết quả −0.4≤0-0.4 \leq 0, nên y=−1y = -1 (Does not go sailing).

---

### **Tính toán cho Example 2:**

Tổng đaˆˋu vaˋo=w0⋅1+w1⋅1+w2⋅2+w3⋅1\text{Tổng đầu vào} = w_0 \cdot 1 + w_1 \cdot 1 + w_2 \cdot 2 + w_3 \cdot 1 =−0.5⋅1+0.6⋅1+0.1⋅2+(−0.6)⋅1= -0.5 \cdot 1 + 0.6 \cdot 1 + 0.1 \cdot 2 + (-0.6) \cdot 1 =−0.5+0.6+0.2−0.6= -0.5 + 0.6 + 0.2 - 0.6 =−0.3= -0.3

Kết quả −0.3≤0-0.3 \leq 0, nên y=−1y = -1 (Does not go sailing).

---

### **Kết luận:**

- **Example 1:** Does not go sailing.
- **Example 2:** Does not go sailing.

## Bài 1.b: 

![[Pasted image 20250202194724.png]]

```python
# Given values
alpha = 0.05  # Learning rate
t = 1  # Target output for the second example
x = [1, 2, 1]  # Inputs (x1, x2, x3)
w_old = [-0.5, 0.6, 0.1, -0.6]  # (w0, w1, w2, w3) old values

# Calculate current prediction y = sign(w0 + w1 * x1 + w2 * x2 + w3 * x3)
net_input = w_old[0] + w_old[1] * x[0] + w_old[2] * x[1] + w_old[3] * x[2]
y = 1 if net_input >= 0 else -1  # Activation function (sign)

# Perceptron update rule: w_k(new) = w_k(old) + alpha * x_k * (t - y)
w_new = [w_old[0] + alpha * (t - y)]  # Start with w0 update
									 # t: goundtruth, y: predict
for i in range(3):
    w_new.append(w_old[i+1] + alpha * x[i] * (t - y))

w_new
```

Câu 1.b 

(w0, w1, w2, w3)old = (-0.5, 0.6, 0.1, -0.6)

y = -0.5 + 0.6 * 1 + 0.1 * 2 + -0.6 *1 = -0.3

w0(new)=w0(old) + alpha * (1 - -0.3) = -0.5 + 0.05 * 1.3 = 
w1(new)=w1(old) + alpha * (1 - -0.3) = 0.6 + 0.05 * 1.3 = 
w2(new)=w2(old) + alpha * (1 - -0.3) = 0.1 + 0.05 * 1.3 = 

- w0(new)=−0.4
- w1(new)=0.7
- w2(new)=0.3
- w3(new)=−0.5

---
5 features, 4 categories, 4 hidden layers, 5*7 + 7*7 + 7*7 + 7*7 + 7*4 = 210 weights. 

---
### **Cách xây dựng ma trận nhầm lẫn (Confusion Matrix):**

**Ma trận nhầm lẫn** là công cụ quan trọng trong học máy để đánh giá hiệu suất của mô hình phân loại.

---

### **Ý nghĩa của từng thành phần:**

- **P (Positive)**: Là trường hợp **malign (ác tính)**.
- **N (Negative)**: Là trường hợp **benign (lành tính)**.

|Dự đoán / Thực tế|Positive (malign)|Negative (benign)|
|---|---|---|
|**Positive (malign)**|True Positive (TP)|False Positive (FP)|
|**Negative (benign)**|False Negative (FN)|True Negative (TN)|

---

### **Giải thích các thành phần:**

1. **TP (True Positive)**:
    
    - Mô hình **dự đoán đúng** trường hợp ác tính (malign).
    - Ví dụ: Nếu bệnh nhân thật sự mắc bệnh (malign) và mô hình cũng dự đoán là mắc bệnh.
2. **FP (False Positive)**:
    
    - Mô hình **dự đoán sai** trường hợp ác tính khi thực tế là lành tính.
    - Ví dụ: Bệnh nhân không mắc bệnh (benign) nhưng mô hình dự đoán nhầm là mắc bệnh.
3. **FN (False Negative)**:
    
    - Mô hình **dự đoán sai** trường hợp lành tính khi thực tế là ác tính.
    - Ví dụ: Bệnh nhân thật sự mắc bệnh (malign) nhưng mô hình dự đoán nhầm là không mắc bệnh (benign).
4. **TN (True Negative)**:
    
    - Mô hình **dự đoán đúng** trường hợp lành tính (benign).
    - Ví dụ: Bệnh nhân không mắc bệnh (benign) và mô hình cũng dự đoán là không mắc bệnh.

---

