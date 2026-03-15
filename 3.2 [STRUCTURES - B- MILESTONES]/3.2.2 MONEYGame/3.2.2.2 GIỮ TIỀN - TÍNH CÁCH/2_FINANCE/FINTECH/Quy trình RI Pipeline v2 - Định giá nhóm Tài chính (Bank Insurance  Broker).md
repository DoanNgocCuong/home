
---

# Quy trình RI Pipeline v2: Định giá nhóm Tài chính (Bank / Insurance / Broker)

Tài liệu này mô tả phiên bản v2 của mô hình Residual Income (RI), được thiết kế để tự động hóa việc định giá cho các công ty tài chính1.

**Điểm khác biệt so với bản v1 (Baseline):**

- **Tính thêm Payout Ratio:** Dựa trên trung bình 3–5 năm từ Báo cáo tài chính (BCTC)2.
    
- **Giá trị sổ sách ($BV_t$) "động":** $BV_t$ sẽ thay đổi theo ROE và tỷ lệ chi trả cổ tức (Payout), phản ánh đúng logic lợi nhuận giữ lại thay vì cố định $BV_0$3333.
    
- **Cấu trúc cốt lõi:** Vẫn giữ nguyên nguyên lý RI: $BV_0 + PV(RI_{1..5}) + PV(CV_5)$4.
    

---

## Bước 0: Mục tiêu & Output

**Mục tiêu:** Tính giá trị nội tại trên mỗi cổ phiếu (Intrinsic Value Per Share) theo mô hình RI5.

**Output chuẩn đầu ra:**

1. **Payout Ratio:** Tỷ lệ chi trả cổ tức tiền mặt bình quân 3–5 năm6.
    
2. **ROE Forecast:** Dự báo ROE cho các năm $Y_1$ đến $Y_5$7.
    
3. **Đường $BV_t$ động:** Chuỗi giá trị sổ sách từ $BV_0$ đến $BV_5$8.
    
4. **RI từng năm:** Các giá trị thu nhập thặng dư $RI_1$ đến $RI_5$9.
    
5. **Terminal RI Value:** Giá trị tại điểm cuối $CV_5$10.
    
6. **Giá trị nội tại ($V_0$):** Tổng hợp từ $BV_0 + PV(RI_{1..5}) + PV(CV_5)$11.
    

---

## Bước 1: Input tối thiểu

### 1.1.

Từ Báo cáo tài chính 12

- $BV_0$ (Giá trị sổ sách tại thời điểm hiện tại):
    
    $$BV_0 = \frac{\text{Vốn chủ sở hữu thuộc cổ đông công ty mẹ}}{\text{Số cổ phiếu lưu hành}}$$
    
    13
    
- **Dữ liệu quá khứ:** Lợi nhuận sau thuế ($NI_t$) và Cổ tức tiền mặt đã trả ($DivPaid_t$).
    
    - $NI_t = \frac{\text{LNST thuộc cổ đông công ty mẹ (năm t)}}{\text{Số cổ phiếu}}$ 14
        
    - $DivPaid_t$: Lấy từ mục "Cổ tức, lợi nhuận đã trả cho chủ sở hữu" trong Lưu chuyển tiền tệ (hoạt động tài chính)15.
        
- **ROE lịch sử:** $ROE_0, ROE_{-1}, \dots$ (tính bằng LNST / Vốn chủ bình quân)16.
    

### 1.2.

Dữ liệu ngành 17

- **$ROE_{anchor}$:** Median ROE của ngành trong 5 năm18.
    

### 1.3.

Tham số mô hình 19

- **$K_e$ (Cost of Equity):** Chi phí vốn chủ sở hữu (ví dụ: 12%)20.
    
- **$\omega$ (Omega):** Hệ số bền vững (persistence), tra từ bảng ngành theo tier21.
    
- **$\Delta_{cap}$:** Giới hạn biến động ROE năm-năm (mặc định 5%)22.
    
- **$\alpha$:** Hệ số xu hướng cho ROE năm 1 (mặc định 0.4)23.
    
- **$\lambda$:** Tốc độ hoàn về trung bình (Mean-reversion speed): Bank (0.25), Insurance (0.30), Broker (0.40)24.
    

---

## Bước 2: Tính Payout Ratio từ BCTC

1. Payout từng năm (chỉ tính tiền mặt):
    
    $$Payout_t = \frac{DivPaid_t}{NI_t}$$
    
    25
    
2. Payout bình quân ($N = 3 \text{ đến } 5$ năm):
    
    $$Payout_{avg} = \text{Average}(Payout_{t-1}, \dots, Payout_{t-N})$$
    
    26
    
3. Tỷ lệ giữ lại (Retention Ratio):
    
    $$Retention = 1 - Payout_{avg}$$
    
    27
    

---

## Bước 3: Guardrails (Bộ lọc an toàn) cho ROE

1. **Giới hạn trần/sàn theo ngành (Clip ROE):**
    
    - Ngân hàng: $[-5\%, 30\%]$ 28
        
    - Bảo hiểm: $[-10\%, 25\%]$ 29
        
    - Chứng khoán: $[-20\%, 35\%]$ 30
        
2. Giới hạn biến động năm-năm:
    
    $$\Delta = \text{Clip}(ROE_0 - ROE_{-1}, -\Delta_{cap}, +\Delta_{cap})$$
    
    31
    

---

## Bước 4: Dự báo ROE ($Y_1 \dots Y_5$)

1. Năm 1 (Theo xu hướng ngắn hạn):
    
    $$ROE_1 = ROE_0 + \alpha \times \Delta$$
    
    32
    
2. Năm 2 – 5 (Hoàn về trung bình ngành):
    
    $$ROE_{t+1} = ROE_t + \lambda \times (ROE_{anchor} - ROE_t)$$
    
    _(Áp dụng cho $t = 1 \dots 4$)_ 33
    

---

## Bước 5: Dự báo $BV_t$ (Book Value) động

Đây là bước quan trọng cập nhật $BV$ dựa trên lợi nhuận giữ lại34. Với mỗi năm $t = 1 \dots 5$:

1. Tính Lợi nhuận ($NI_t$):
    
    $$NI_t = ROE_t \times BV_{t-1}$$
    
    35
    
2. Tính Cổ tức ($Div_t$):
    
    $$Div_t = Payout_{avg} \times NI_t$$
    
    36
    
3. Cập nhật Giá trị sổ sách ($BV_t$):
    
    $$BV_t = BV_{t-1} + NI_t - Div_t$$
    
    Hoặc viết gọn:
    
    $$BV_t = BV_{t-1} \times [1 + ROE_t \times (1 - Payout_{avg})]$$
    
    37
    

_Khởi tạo $BV_0$ là giá trị sổ sách hiện tại_38.

---

## Bước 6, 7, 8, 9: Tính toán định giá

Bước 6: Tính Residual Income ($RI$) 39

$$RI_t = (ROE_t - K_e) \times BV_{t-1}$$

40

Bước 7: Chiết khấu dòng RI 41

$$PV(RI_t) = \frac{RI_t}{(1 + K_e)^t}$$

42

Bước 8: Tính giá trị cuối (Terminal Value) 43

Giả định thu nhập thặng dư suy giảm theo hệ số $\omega$: $RI_{t+1} = \omega \times RI_t$44.

- Giá trị tiếp diễn tại cuối năm 5 ($CV_5$):
    
    $$CV_5 = RI_5 \times \frac{\omega}{(1 + K_e) - \omega}$$
    
    45
    
- Chiết khấu về hiện tại:
    
    $$PV(CV_5) = \frac{CV_5}{(1 + K_e)^5}$$
    
    46
    

Bước 9: Tổng hợp Giá trị nội tại ($V_0$) 47

$$V_0 = BV_0 + \sum_{t=1}^{5} PV(RI_t) + PV(CV_5)$$

48

---

## Ví dụ minh họa: Ngân hàng X

**Giả định đầu vào:** 49

- $BV_0 = 20.000$ đ/cp
    
- $K_e = 12\%$
    
- $\omega = 0.72$
    
- $Payout_{avg} = 40\%$ (Suy ra Retention = $60\%$)
    
- $ROE_0 = 20\%$, $ROE_{-1} = 18\%$
    
- $ROE_{anchor} = 15\%$
    
- $\Delta_{cap} = 5\%$, $\alpha = 0.4$, $\lambda = 0.25$
    

1. Tính ROE Forecast: 50

- $\Delta = \text{Clip}(20\% - 18\%, \pm5\%) = 2\%$
    
- $ROE_1 = 20\% + 0.4 \times 2\% = 20,8\%$
    
- $ROE_2 = 20,8\% + 0.25 \times (15\% - 20,8\%) = 19,35\%$
    
- $ROE_3 \approx 18,26\%$
    
- $ROE_4 \approx 17,45\%$
    
- $ROE_5 \approx 16,84\%$
    

2. Tính $BV_t$ (Book Value động): 51

|**Năm**|**BVt−1​ (đầu kỳ)**|**NIt​ (Lợi nhuận)**|**Divt​ (Cổ tức 40%)**|**BVt​ (cuối kỳ)**|
|---|---|---|---|---|
|**Y1**|20.000|4.160|1.664|**22.496**|
|**Y2**|22.496|~4.353|~1.741|**~25.108**|
|**Y3**|25.108|~4.585|~1.834|**~27.859**|
|**Y4**|27.859|~4.861|~1.944|**~30.775**|
|**Y5**|30.775|~5.181|~2.072|**~33.884**|

3. Tính RI và Chiết khấu ($K_e = 12\%$): 52

|**Năm**|**RIt​=(ROEt​−12%)×BVt−1​**|**PV(RIt​)**|
|---|---|---|
|**Y1**|$(20,8\% - 12\%) \times 20.000 = 1.760$|**1.571,43**|
|**Y2**|$(19,35\% - 12\%) \times 22.496 \approx 1.653$|**1.318,13**|
|**Y3**|$(18,26\% - 12\%) \times 25.108 \approx 1.572$|**1.119,19**|
|**Y4**|$(17,45\% - 12\%) \times 27.859 \approx 1.517$|**964,36**|
|**Y5**|$(16,84\% - 12\%) \times 30.775 \approx 1.488$|**844,35**|
|**Tổng**||**5.817,45**|

4. Giá trị cuối (Terminal Value): 53

- $CV_5 \approx 1.488 \times \frac{0,72}{(1,12 - 0,72)} \approx 2.678,46$
    
- $PV(CV_5) \approx \frac{2.678,46}{1,12^5} \approx \mathbf{1.519,83}$
    

5. Kết quả định giá ($V_0$): 54

$$V_0 \approx 20.000 + 5.817,45 + 1.519,83 \approx \mathbf{27.337} \text{ đ/cp}$$

_(Tương đương P/B theo định giá $\approx 1.37$ lần)_