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