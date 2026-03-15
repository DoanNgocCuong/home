# Quy trình 8 Bước Xây Dựng Mô Hình Định Giá DCF/FCFF

## Bước 1 – Thu thập & chuẩn hóa dữ liệu
- Thu thập **10 năm dữ liệu tài chính** của doanh nghiệp (BCTC) + **dữ liệu ngành** (tăng trưởng, biên lợi nhuận, rủi ro, hệ số định giá).  
- Làm sạch số liệu: loại bỏ **sự kiện bất thường**, tách **hoạt động kinh doanh chính** khỏi **tài sản phi hoạt động**.  
- Điều chỉnh IFRS 16 (thuê tài chính) và SBC (cổ phiếu thưởng).  

**Chú thích:**  
- *BCTC*: Báo cáo tài chính.  
- *EBIT/EBITDA*: Lợi nhuận trước lãi vay & thuế / trước lãi vay, thuế & khấu hao.  
- *IFRS 16*: Chuẩn kế toán vốn hóa thuê tài chính.  
- *SBC*: Cổ phiếu thưởng cho nhân viên.

---

## Bước 2 – Ước lượng giả định nền (Priors)
- Xác định phạm vi hợp lý (bands) cho biến:  
  - **g_base**: Tăng trưởng trung hạn.  
  - **g∞**: Tăng trưởng dài hạn ≤ tăng trưởng GDP.  
  - **Margin band**, **CAPEX/Sales**, **D&A/Sales**, **NWC/Sales**, **Beta**, **D/V**, **Tax**.  

**Chú thích:**  
- *GDP*: Tổng sản phẩm quốc nội.  
- *CAPEX*: Chi đầu tư tài sản cố định.  
- *D&A*: Khấu hao.  
- *NWC*: Vốn lưu động ròng.  
- *Beta (β)*: Độ nhạy cổ phiếu so với thị trường.  
- *D/V*: Nợ trên tổng vốn.  

---

## Bước 3 – Dự phóng (Projection)
- Dự phóng **5–10 năm tương lai**: Doanh thu, EBIT margin, D&A, CAPEX, ΔNWC.  
- Cập nhật tài sản cố định: PPEₜ = PPEₜ₋₁ + CAPEX – D&A.  
- Duy trì quan hệ **ROIC–Tăng trưởng–Tái đầu tư**: Reinvestment_rate ≈ g / ROIC.  

**Chú thích:**  
- *PPE*: Tài sản cố định hữu hình.  
- *ROIC*: Lợi nhuận sau thuế trên vốn đầu tư.  
- *Reinvestment rate*: Tỷ lệ tái đầu tư lợi nhuận để tăng trưởng.

---

## Bước 4 – Tính FCFF, WACC, EV & TV
- **FCFF** = NOPAT + D&A – CAPEX – ΔNWC.  
- **WACC** = Chi phí vốn bình quân của nợ & vốn chủ.  
- **EV** = ∑(FCFF / (1+WACC)^t) + **TV**.  
- **TV**: Gordon (FCFFₙ₊₁ / (WACC – g∞)) hoặc Exit Multiple (EBITDAₙ × Multiple ngành).  
- **Equity** = EV – Net Debt ± Non-operating Items.  

**Chú thích:**  
- *NOPAT*: Lợi nhuận hoạt động sau thuế.  
- *WACC*: Weighted Average Cost of Capital – chi phí vốn bình quân.  
- *EV*: Enterprise Value – giá trị doanh nghiệp.  
- *TV*: Terminal Value – giá trị vĩnh viễn.  
- *Net Debt*: Nợ ròng.

---

## Bước 5 – Áp ràng buộc (Constraints)
- **Kinh tế:** g∞ < WACC; ROIC∞ ≥ g∞.  
- **Cấu trúc vốn:** K_d < K_e.  
- **Rủi ro tài chính:** Interest coverage ≥ 3×; Debt/EBITDA ≤ 4×.  
- **Kế toán:** CFO + CFI + CFF ≈ ΔCash; Cash ≥ 0.  

**Chú thích:**  
- *Interest coverage*: EBIT/Lãi vay.  
- *Debt/EBITDA*: Đòn bẩy tài chính.  
- *CFO/CFI/CFF*: Dòng tiền hoạt động/đầu tư/tài chính.

---

## Bước 6 – Kiểm định mô hình (Validation)
- **Backtest**: So sánh DCF 3–5 năm quá khứ với giá thị trường → MAPE, RMSE, bias.  
- **Sensitivity**: Độ nhạy WACC, g∞, margin.  
- **Scenario**: Base / Optimistic / Pessimistic.  
- **Monte Carlo**: Mô phỏng xác suất EV.  
- **Comparative**: FCFE & multiples (P/E, EV/EBITDA).  

**Chú thích:**  
- *MAPE*: Sai lệch trung bình theo %.  
- *RMSE*: Sai số bình phương trung bình.  
- *Bias*: Xu hướng sai lệch.  
- *Monte Carlo*: Mô phỏng xác suất.  

---

## Bước 7 – Hiệu chỉnh (Refinement)
- Nếu bias hệ thống → chỉnh WACC, g∞, ROIC logic.  
- Nếu sensitivity quá lớn → nới giả định, đưa về chuẩn ngành.  
- Lặp kiểm định đến khi sai số < 10–15%.  

---

## Bước 8 – Báo cáo & Giải thích (Attribution)
- Trình bày **Value Bridge**: yếu tố nào làm thay đổi giá trị (doanh thu, margin, CAPEX, WACC).  
- Làm **Reverse DCF**: Tính ngược tăng trưởng mà thị trường ngầm giả định.  
- Đưa **Scorecard**: chấm điểm độ tin cậy mô hình.  

**Chú thích:**  
- *Attribution / Value Bridge*: Phân rã giá trị theo yếu tố.  
- *Reverse DCF*: Định giá ngược.  

---

## Triết lý tổng kết
> “DCF tốt không phải là mô hình đoán giá, mà là mô hình giải thích giá trị —  
> có logic kinh tế, có ràng buộc, có kiểm chứng thống kê.”
