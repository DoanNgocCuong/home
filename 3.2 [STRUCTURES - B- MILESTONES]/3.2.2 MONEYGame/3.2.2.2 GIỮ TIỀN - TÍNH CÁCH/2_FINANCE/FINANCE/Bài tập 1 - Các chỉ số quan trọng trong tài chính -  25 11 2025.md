

Yêu cầu của bạn là vẽ sơ đồ luồng đi (flow diagram) của các chỉ số tài chính, định giá và hoạt động được liệt kê, cùng với mối quan hệ giữa chúng. Dựa trên các nguồn tài liệu về mô hình tài chính 3 Báo cáo (3-Statement Model), Định giá Dòng tiền Chiết khấu (DCF), và Phân tích Tương đối (Multiples), tôi sẽ xây dựng sơ đồ luồng đi dưới dạng các giai đoạn tính toán chính.

Sơ đồ này đi từ **Hiệu suất Hoạt động** (Báo cáo Kết quả Kinh doanh - P&L), chuyển sang **Tạo ra Tiền mặt** (Dòng tiền Tự do - FCFF), và kết thúc bằng **Định giá Doanh nghiệp** (Enterprise Value/Market Cap).

--------------------------------------------------------------------------------

# 1. Sơ Đồ Luồng Đi Của Các Chỉ Số Tài Chính và Định Giá

Cơ sở của luồng đi này là Mô hình 3 Báo cáo (3-Statement Model), yêu cầu sự liên kết chặt chẽ giữa Báo cáo Kết quả Kinh doanh, Bảng Cân đối Kế toán, và Báo cáo Lưu chuyển Tiền tệ.

Giai Đoạn 1: Hiệu Suất Hoạt Động & Lợi Nhuận (Income Statement Flow)

Giai đoạn này xác định khả năng sinh lời từ hoạt động cốt lõi của doanh nghiệp.

|   |   |   |   |
|---|---|---|---|
|Chỉ số|Mối quan hệ/Công thức (Dựa trên Nguồn)|Vai trò|Nguồn tham chiếu|
|**Revenue**|Là điểm khởi đầu của P&L. Dữ liệu này được sử dụng để dự báo các tài khoản khác.|Đo lường quy mô doanh thu.||
|**Gross Profit**|**Revenue** - Giá vốn hàng bán (COGS).|Lợi nhuận sau khi trừ chi phí trực tiếp của sản phẩm/dịch vụ.||
|**Gross Margin**|**Gross Profit** ÷ **Revenue**.|Tỷ suất sinh lời gộp, là một trong 4 lĩnh vực trọng tâm của CFO Dashboard.||
|**EBITDA**|Gross Profit - Chi phí hoạt động (trừ **D&A**). EBIT + **D&A**.|Đại diện cho dòng tiền hoạt động trước lãi vay, thuế và **D&A**.||
|**D&A**|Thường được sử dụng để tính từ EBITDA sang EBIT, và được trừ khỏi PP&E trên Bảng Cân đối Kế toán.|Chi phí không dùng tiền mặt (non-cash expense) liên quan đến **Capex**.||
|**EBIT**|**EBITDA** - **D&A**. (Hoặc Lợi nhuận hoạt động).|Thu nhập từ hoạt động trước lãi vay và thuế (Operating Income).||
|**Effective Tax Rate**|Được sử dụng để tính thuế phải trả.|Tỷ lệ thuế thực tế áp dụng cho thu nhập chịu thuế.||
|**NOPAT**|Thường là EBIT × (1 - **Effective Tax Rate**).|Lợi nhuận ròng từ hoạt động sau thuế (Net Operating Profit After Tax).||
|**Net Income (NI)**|Thu nhập ròng (lãi ròng) sau khi trừ chi phí lãi vay và thuế. Là một trong những chỉ số quan trọng trên CFO Dashboard.|Cơ sở để tính toán **FCFE**, **P/E Ratio** và thay đổi **Equity**.||

--------------------------------------------------------------------------------

Giai Đoạn 2: Dòng Tiền & Vốn Lưu Động (Cash Flow Flow)

Giai đoạn này điều chỉnh lợi nhuận kế toán (**NI**) thành tiền mặt thực sự tạo ra (**FCFF**).

|   |   |   |   |
|---|---|---|---|
|Chỉ số|Mối quan hệ/Công thức (Dựa trên Nguồn)|Vai trò|Nguồn tham chiếu|
|**CFO**|NI + D&A ± Δ**Working Capital** (và các điều chỉnh khác).|Dòng tiền từ hoạt động kinh doanh (Operating Cash Flow).||
|**Working Capital (WC)**|Tài sản ngắn hạn trừ đi Nợ ngắn hạn.|Tình trạng vốn lưu động.||
|**Accounts Receivable (AR)**|Là một thành phần của WC, được dự báo dựa trên Doanh thu (sử dụng DSO).|Các khoản phải thu khách hàng.||
|**Accounts Payable (AP)**|Là một thành phần của WC, được dự báo dựa trên COGS (sử dụng DPO).|Các khoản phải trả nhà cung cấp.||
|Δ**Working Capital**|Thay đổi WC từ năm trước đến năm hiện tại.|Việc tăng Δ**Working Capital** làm giảm tiền mặt (Cash Outflow).||
|**Capex**|Chi phí vốn. **Capex** làm giảm giá trị tài sản PP&E (trên BCĐKT) theo công thức: Old Balance - CapEx - D&A (do dấu trên CFS).|Chi phí đầu tư tài sản dài hạn. Capex - D&A là **Net Capital Expenditures**.||
|**FCFF (Free Cash Flow to Firm)**|Dòng tiền tự do cho toàn bộ công ty (cả chủ nợ và cổ đông). FCFF là tiền mặt sau khi công ty đã tái đầu tư (Net Capex và Δ**Working Capital**).|Là cơ sở cốt lõi để tính **Giá trị Doanh nghiệp (Firm Value)** trong mô hình DCF.||

--------------------------------------------------------------------------------

Giai Đoạn 3: Chi Phí Vốn và Cấu Trúc Vốn (Cost of Capital & Capital Structure)

Giai đoạn này xác định **tỷ lệ chiết khấu (WACC)** và các thành phần cấu trúc vốn, cần thiết cho việc định giá DCF.

|   |   |   |   |
|---|---|---|---|
|Chỉ số|Mối quan hệ/Công thức (Dựa trên Nguồn)|Vai trò|Nguồn tham chiếu|
|**Cost of Debt (CoD)**|Chi phí vay nợ. Thường được ước tính dựa trên xếp hạng tín dụng và lợi suất trái phiếu (default spreads).|Lãi suất dùng để chiết khấu dòng tiền cho chủ nợ, là thành phần của WACC.||
|**Cost of Equity (CoE)**|Chi phí vốn chủ sở hữu. Thường được ước tính bằng mô hình CAPM, bao gồm Phần bù rủi ro vốn chủ sở hữu (ERP).|Lãi suất dùng để chiết khấu dòng tiền cho cổ đông (FCFE).||
|**Equity**|Giá trị vốn chủ sở hữu (trên Bảng Cân đối Kế toán). Thay đổi do Old Equity + **Net Income** + Dividends + Other Items.|Một thành phần trong tỷ trọng tính WACC.||
|**Interest-bearing Debt**|Tổng nợ chịu lãi (Total Debt). Thay đổi do Old Debt + Change in Debt (từ CFS).|Một thành phần trong tỷ trọng tính WACC.||
|**WACC**|Chi phí Vốn Bình quân Gia quyền (Weighted Average Cost of Capital). Được tính toán bằng cách cân đối **CoE** và **CoD** theo tỷ trọng vốn chủ sở hữu và nợ vay.|**Là tỷ lệ chiết khấu (Discount Rate)** quan trọng nhất, dùng để chiết khấu **FCFF** về Giá trị Doanh nghiệp (Firm Value).||
|**Cash & Short-term Investments**|Tiền mặt và các khoản đầu tư ngắn hạn.|Được trừ khỏi tổng nợ để tính **Net Debt**.||
|**Net Debt**|**Interest-bearing Debt** - **Cash & Short-term Investments**.|Được sử dụng để tính **Enterprise Value (EV)**.||

--------------------------------------------------------------------------------

Giai Đoạn 4: Định Giá & Các Bội Số Thị Trường (Valuation)

Giai đoạn này chuyển dòng tiền và các chỉ số hoạt động thành Giá trị Doanh nghiệp và Giá trị Vốn Chủ sở hữu, sử dụng cả DCF và phương pháp tương đối (Multiples).

|   |   |   |   |
|---|---|---|---|
|Chỉ số|Mối quan hệ/Công thức (Dựa trên Nguồn)|Vai trò|Nguồn tham chiếu|
|**Base-year FCFF**|**FCFF** tại năm cơ sở (năm cuối cùng của dữ liệu lịch sử hoặc năm đầu của dự báo).|Dòng tiền để bắt đầu quá trình chiết khấu.||
|**FCFF** (Future)|**FCFF** được dự phóng trong tương lai, thường dựa trên **Revenue Growth** và **Earnings Growth**.|Các dòng tiền được **WACC** chiết khấu về hiện tại.||
|**Enterprise Value (EV)**|Tổng giá trị nội tại được xác định bằng cách chiết khấu tất cả các luồng **FCFF** trong tương lai (bao gồm Terminal Value) về hiện tại bằng **WACC**. Cũng bằng **Market Cap** + **Net Debt**.|Giá trị toàn bộ doanh nghiệp, không phụ thuộc vào cấu trúc vốn.||
|**Market Capitalization**|**Shares Outstanding** × **Stock Price**. Cũng bằng **EV** - **Net Debt**.|Tổng giá trị thị trường của vốn chủ sở hữu.||
|**Stock Price**|Giá cổ phiếu.|Yếu tố đầu vào để tính Market Cap và là kết quả của định giá trên mỗi cổ phiếu.||
|**Shares Outstanding**|Số lượng cổ phiếu đang lưu hành.|Dùng để tính Market Cap.||
|**P/E Ratio**|**Market Capitalization** ÷ **Net Income**.|Bội số định giá vốn chủ sở hữu phổ biến.||
|**P/B Ratio**|Price-to-Book Ratio (Giá/Giá trị Sổ sách Vốn Chủ sở hữu).|Bội số định giá vốn chủ sở hữu khác.||
|**EV/EBITDA**|**Enterprise Value** ÷ **EBITDA**.|Bội số định giá doanh nghiệp phổ biến nhất (thường dùng làm giả định Terminal Value trong DCF).||
|**Peer Multiples Snapshot**|**5Y Mean Multiple, 5Y Std Multiple, Peer Percentile Rank**|Các bội số của các công ty cùng ngành (Peer Group) được sử dụng để so sánh tương đối và kiểm tra tính hợp lý của mô hình DCF.||

--------------------------------------------------------------------------------

Giai Đoạn 5: Các Chỉ Số Chuyên Biệt và Rủi Ro (Specialized & Risk Indicators)

Các chỉ số này cung cấp thông tin về tăng trưởng, chất lượng quản trị và rủi ro, ảnh hưởng đến các giả định đầu vào trong các giai đoạn trước (ví dụ: Tốc độ tăng trưởng, CoE, Effective Tax Rate).

|   |   |   |   |
|---|---|---|---|
|Chỉ số|Mối quan hệ/Tính chất|Ứng dụng/Mối quan hệ chính|Nguồn tham chiếu|
|**Revenue Growth**|Tốc độ tăng trưởng doanh thu.|Là đầu vào quan trọng để dự phóng **Revenue** trong mô hình DCF và đánh giá tiềm năng tăng trưởng.||
|**Earnings Growth**|Tốc độ tăng trưởng thu nhập.|Dùng để tính toán **P/E Ratio** (PEG Ratio) và dự phóng **Net Income**.||
|**Auditor Name / is_Big4 Auditor**|Thông tin về kiểm toán viên.|Đánh giá tính minh bạch và độ tin cậy của **Financial Statements** (**Revenue**, **NI**, **Total Assets**).||
|**Audit Opinion Severity Score**|Mức độ nghiêm trọng của ý kiến kiểm toán.|Đánh giá rủi ro tài chính và quản trị, ảnh hưởng đến chi phí vốn (**CoE/WACC**).||
|**Related-party Transaction Size**|Quy mô giao dịch với bên liên quan.|Đánh giá rủi ro quản trị và tính minh bạch của các giao dịch (có thể làm sai lệch **Revenue** hoặc **EBITDA**).||
|**Embedded Value (EV_life), Value of New Business (VNB), VNB Margin, Solvency Margin Ratio (RBC), Persistency Ratio (13th month)**|Các chỉ số chuyên biệt cho ngành bảo hiểm.|Các chỉ số quan trọng trong việc định giá và đánh giá rủi ro tài chính của các công ty bảo hiểm.||
|**Total Assets**|Tổng tài sản.|Là cơ sở để tính toán tỷ suất sinh lời trên tài sản (ROA) và là thành phần chính của Bảng Cân đối Kế toán.||
|**Newly Issued Shares (3y), Convertible Securities, ESOP Shares**|Các yếu tố có thể gây pha loãng vốn chủ sở hữu (Dilution).|Ảnh hưởng đến **Shares Outstanding** và **Stock Price**.||

--------------------------------------------------------------------------------

Mối Quan Hệ Cốt Lõi Trên Luồng Đi

Mối quan hệ giữa các chỉ số được xây dựng dựa trên các công thức tài chính cơ bản và các mô hình định giá:

1. **Từ Doanh thu đến Tiền mặt (FCFF):**

    ◦ **Revenue** là nền tảng, quyết định **Gross Profit**.

    ◦ **Gross Profit** (sau khi trừ chi phí vận hành) tạo ra **EBITDA**.

    ◦ **EBITDA** là thước đo dòng tiền hoạt động trước D&A, thường được sử dụng trong các tỷ lệ đòn bẩy như **Net Debt/EBITDA**.

    ◦ **EBIT** (Thu nhập hoạt động) được tính bằng **EBITDA - D&A**.

    ◦ **Net Income** là kết quả cuối cùng của P&L, bị ảnh hưởng bởi **EBIT** và **Effective Tax Rate**.

    ◦ **FCFF** là kết quả của việc điều chỉnh **NOPAT** hoặc **NI** cho các khoản phi tiền mặt (**D&A**) và các khoản tái đầu tư như **Capex** và Δ**Working Capital**.

2. **Mối quan hệ giữa Dòng tiền và Định giá Nội tại (DCF):**

    ◦ Giá trị Nội tại (**EV**) được xác định bằng cách chiết khấu **FCFF** trong tương lai về hiện tại.

    ◦ Tỷ lệ chiết khấu được sử dụng là **WACC**, được tính toán từ **CoE** và **CoD**.

    ◦ Việc dự phóng **FCFF** phụ thuộc vào các giả định về tăng trưởng, như **Revenue Growth** và **Earnings Growth**.

3. **Mối quan hệ giữa Giá trị Thị trường và Định giá Tương đối:**

    ◦ **Market Capitalization** được xác định bằng **Stock Price** × **Shares Outstanding**.

    ◦ **Enterprise Value (EV)** liên kết Giá trị Thị trường với Cấu trúc Vốn thông qua **Net Debt** (**EV** = Market Cap + **Net Debt**).

    ◦ Các bội số định giá như **P/E Ratio** (Market Cap / **Net Income**) và **EV/EBITDA** (**EV** / **EBITDA**) thiết lập mối quan hệ giữa giá trị thị trường/doanh nghiệp và hiệu suất hoạt động (**EBITDA**, **NI**).

4. **Kiểm soát và Điều chỉnh Kế toán:**

    ◦ **Working Capital** và sự thay đổi của nó (Δ**Working Capital**) được chi phối bởi các chỉ số quản lý hoạt động như **Accounts Receivable** và **Accounts Payable**.

    ◦ Các chỉ số về kiểm toán và tuân thủ (**Auditor Name**, **Audit Opinion Severity Score**) đóng vai trò là cơ chế kiểm soát nội bộ (Internal Controls), đảm bảo tính chính xác và minh bạch của toàn bộ dữ liệu đầu vào (**Revenue, NI, Total Assets**) được sử dụng trong mô hình.

**Tóm lại:** Luồng đi tài chính khởi nguồn từ **Revenue** (Thu) và giảm dần qua các cấp lợi nhuận, chuyển đổi thành **FCFF** (Tiền mặt), được chiết khấu bằng **WACC** (Chi phí) để tìm ra **Enterprise Value** (Giá trị). Các bội số như **EV/EBITDA** và **P/E** được sử dụng để kiểm tra tính hợp lý của giá trị này trong mối tương quan với thị trường.

Để hình dung, có thể coi hệ thống này như một cỗ máy sản xuất nước:

• **Revenue** là lượng nước thô đi vào.

• **EBITDA/NI** là lượng nước đã được lọc sơ bộ (lợi nhuận).

• **Capex** và Δ**Working Capital** là chi phí bảo trì và nâng cấp máy móc (tái đầu tư).

• **FCFF** là lượng nước sạch (tiền mặt tự do) có thể phân phối.

• **WACC** là lãi suất vay vốn cho cỗ máy này (chi phí cơ hội).

• **EV** là giá trị của toàn bộ cỗ máy này nếu xét đến dòng nước sạch nó có thể tạo ra trong tương lai.

• **P/E** và **EV/EBITDA** là giá bán cỗ máy dựa trên giá thị trường của các cỗ máy tương tự.



# 2. Các phương pháp định giá 

| Lĩnh vực Cốt lõi                               | Cấp 1 (Loại Hình Phân Tích)                                           | Chỉ số/Phương pháp                                                                                                     | Vai trò và Bối cảnh                                                                                                                                                                        | Nguồn hỗ trợ |
| :--------------------------------------------- | :-------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------- |
| **I. ĐỊNH GIÁ CỐT LÕI (CORE VALUATION)**       | **I.A. Dựa trên Giá trị Nội tại (Intrinsic Value)**                   | DCF Model (FCFF/FCFE), NPV                                                                                             | Ước tính Giá trị Nội tại bằng cách chiết khấu dòng tiền tương lai. DCF/NPV phản ánh Giá trị Doanh nghiệp Hoạt động (Going Concern Value).                                                  |              |
|                                                | **I.B. Dựa trên Tương đối Thị trường (Relative Valuation - Pricing)** | CCA (Comps), PTA                                                                                                       | **CCA:** So sánh bội số với các công ty cùng ngành giao dịch công khai. **PTA:** Dựa trên bội số của các giao dịch M&A lịch sử. CCA/PTA được dùng để kiểm tra tính hợp lý của kết quả DCF. |              |
| **II. QUẢN TRỊ HIỆU SUẤT & ĐO LƯỜNG LỢI SUẤT** | **II.A. Đo lường Hiệu suất/Lợi suất**                                 | IRR (Tỷ suất Hoàn vốn Nội bộ)                                                                                          | Chỉ số lợi suất dùng để đánh giá mức độ khả thi của dự án và sắp xếp thứ tự ưu tiên đầu tư.                                                                                                |              |
|                                                | **II.B. Công cụ Kiểm định Mô hình**                                   | Phân tích Độ nhạy (Sensitivity Analysis), Phân tích Kịch bản (Scenario Analysis), Kiểm tra Căng thẳng (Stress Testing) | Kiểm tra rủi ro bằng cách thay đổi các biến số đầu vào (ví dụ: WACC, Tốc độ Tăng trưởng) để xác định mức độ ảnh hưởng đến kết quả cuối cùng (NPV/Giá Mục tiêu).                            |              |
| **III. ĐỊNH GIÁ CHUYÊN NGÀNH**                 | **III.A. Định giá Bảo hiểm**                                          | Embedded Value (EV_life), VNB, VNB Margin, Solvency Margin Ratio (RBC)                                                 | Các chỉ số định giá và rủi ro đặc thù, bổ sung cho DCF.                                                                                                                                    |              |
| **IV. KHUNG QUẢN TRỊ RỦI RO (GRC)**            | **IV.A. Tuân thủ và Thẩm định**                                       | DD Reports (FDD), Compliance Risk Register, Yêu cầu AML/CFT (KYC/CDD)                                                  | Đảm bảo dữ liệu đầu vào (từ các chỉ số P&L/CFS) là chính xác. Xác định rủi ro pháp lý và quản trị, ảnh hưởng đến Chi phí Vốn (WACC).                                                       |              |

---
# 1 Vài câu hỏi: 
## 1. Trong mô hình ba báo cáo tài chính (3-statement model), khoản mục nào trên Bảng cân đối kế toán (Balance Sheet) được liên kết trực tiếp với Lợi nhuận ròng (Net Income) từ Báo cáo kết quả kinh doanh (Income Statement)?

=> "Lợi nhuận giữ lại (Retained Earnings)" = Lợi nhuận giữ lại của kì trước + lợi nhuận ròng - Cổ tức đã trả. 


## 2. Khi xây dựng biểu đồ "Sân bóng đá" (Football Field Chart) để trình bày kết quả định giá, mục đích chính là gì?
- So sánh trực quan khoảng định giá của nhiều phương pháp khác nhau. 
- DCF, CCA, PTA, ... cho phép so sánh xác định 1 vùng giá trị hợp lý. 
- **Tổng hợp kết quả:** Biểu đồ này được sử dụng để **tổng hợp và trực quan hóa phạm vi định giá từ tất cả các phương pháp** định giá đã sử dụng. Các phương pháp này thường bao gồm Định giá Dòng tiền Chiết khấu (DCF), Phân tích Công ty So sánh (Comparable Company Analysis - CCA), và Phân tích Giao dịch Tiền lệ (Precedent Transaction Analysis - PTA).


## 2.1 DCP và NPV 

**Có mối liên hệ công thức giữa DCF và NPV không?**

---

**3. Diễn giải:**

- DCF đưa ra tổng giá trị hiện tại của tất cả dòng tiền thu (thường là dương).
    
- NPV là giá trị còn lại cho nhà đầu tư sau khi đã bỏ ra vốn đầu tư ban đầu.
    
- Nếu DCF (tổng dòng tiền chiết khấu) lớn hơn đầu tư ban đầu, thì NPV > 0 → đầu tư hiệu quả.
    

---

**4. Minh họa số liệu:**

- Đầu tư ban đầu (C0C_0C0): -100
    
- DCF (tổng dòng tiền đã chiết khấu): 103.3
    
- NPV=103.3−100=3.3NPV = 103.3 - 100 = 3.3NPV=103.3−100=3.3
    

---

**Kết luận:**  
Công thức **NPV = DCF – Đầu tư ban đầu** chính là mối liên hệ trực tiếp giữa 2 khái niệm này.  
Bạn cần minh họa Excel template hoặc ứng dụng thực tế cụ thể không?

1. [https://notebooklm.google.com/notebook/94557a2a-c2c8-4054-b38c-205b4dffa315](https://notebooklm.google.com/notebook/94557a2a-c2c8-4054-b38c-205b4dffa315)


---

Biểu đồ "Sân bóng đá" (Football Field Chart) có mục đích chính là **so sánh trực quan các khoảng định giá** từ nhiều phương pháp khác nhau, nhằm xác định phạm vi giá mục tiêu hợp lý. Các phương pháp bạn liệt kê (DCF, CCA, PTA) là ba trụ cột định giá phổ biến nhất trong phân tích cơ bản.

Dựa trên các nguồn tài liệu, ngoài ba phương pháp cốt lõi đó, còn tồn tại các phương pháp định giá chuyên biệt, các biến thể của DCF, và các công cụ quản lý rủi ro đi kèm đóng vai trò quyết định tính chính xác của kết quả định giá.

### I. Các Phương pháp Định giá Khác được Đề cập

Các nguồn tài liệu có đề cập đến các phương pháp hoặc biến thể định giá sau:

#### 1. Các Biến thể của Mô hình Chiết khấu Dòng tiền (DCF)

DCF là phương pháp xác định **Giá trị Nội tại (Intrinsic Value)** của một tài sản bằng cách chiết khấu Dòng tiền Tự do (FCF) dự kiến về giá trị hiện tại.

- **FCFE (Free Cash Flow to Equity):** Đây là một mô hình DCF chính, chiết khấu Dòng tiền Tự do cho Cổ đông (FCFE) bằng **Chi phí Vốn Chủ Sở Hữu (Cost of Equity)** để tìm ra Giá trị Vốn Chủ Sở Hữu (Equity Value).
- **FCFF (Free Cash Flow to Firm):** Mô hình này chiết khấu Dòng tiền Tự do cho Toàn bộ Công ty (FCFF) bằng **Chi phí Vốn Bình quân Gia quyền (WACC)** để tìm ra Giá trị Doanh nghiệp (Firm Value). FCFF là mô hình được sử dụng phổ biến hơn trong bối cảnh M&A hoặc phân tích doanh nghiệp tổng thể.
- **NPV (Net Present Value):** Mặc dù NPV là kết quả của việc chiết khấu dòng tiền, nó được coi là một công cụ định lượng cốt lõi để đánh giá khả năng sinh lời, rủi ro và mức độ phù hợp của một khoản đầu tư. NPV được sử dụng rộng rãi để đánh giá tính khả thi của các dự án đầu tư (như bất động sản, dầu khí, R&D dược phẩm).

#### 2. Các Chỉ số Định giá Liên quan

- **IRR (Internal Rate of Return):** Tỷ suất Hoàn vốn Nội bộ (IRR) là một chỉ số được sử dụng rộng rãi để đánh giá mức độ khả thi và lợi tức kỳ vọng của các dự án hoặc cổ phiếu/trái phiếu. IRR được so sánh với một tỷ suất hoàn vốn tối thiểu. Cùng với NPV, IRR là một trong những công cụ phân tích định lượng cốt lõi.

#### 3. Phương pháp Định giá Chuyên ngành (Đã được đề cập trước đó)

Các chỉ số chuyên biệt cho ngành bảo hiểm—vốn không áp dụng DCF hay CCA truyền thống—cũng được sử dụng để xác định giá trị, dựa trên thông tin về **Bao mua và phân phối bán ra bảo hiểm nhân thọ và đầu tư khác liên quan đến bảo hiểm**:

- **Embedded Value (EV_life):** Giá trị nội tại tiềm ẩn (đặc thù cho ngành bảo hiểm).
- **Value of New Business (VNB):** Giá trị kinh doanh mới.
- **VNB Margin:** Biên lợi nhuận kinh doanh mới.

### II. Cấu trúc MECE các Phương pháp Định giá và Khung Phân tích

Để có cái nhìn tổng quan theo cấu trúc MECE (Mutually Exclusive, Collectively Exhaustive), tôi sẽ phân loại các chỉ số và phương pháp này theo vai trò của chúng trong chu trình phân tích đầu tư, mở rộng từ các mô hình định giá cốt lõi sang các công cụ kiểm soát và quản trị rủi ro.

| Lĩnh vực Cốt lõi                               | Cấp 1 (Loại Hình Phân Tích)                                           | Chỉ số/Phương pháp                                                                                                     | Vai trò và Bối cảnh                                                                                                                                                                        | Nguồn hỗ trợ |
| :--------------------------------------------- | :-------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------- |
| **I. ĐỊNH GIÁ CỐT LÕI (CORE VALUATION)**       | **I.A. Dựa trên Giá trị Nội tại (Intrinsic Value)**                   | DCF Model (FCFF/FCFE), NPV                                                                                             | Ước tính Giá trị Nội tại bằng cách chiết khấu dòng tiền tương lai. DCF/NPV phản ánh Giá trị Doanh nghiệp Hoạt động (Going Concern Value).                                                  |              |
|                                                | **I.B. Dựa trên Tương đối Thị trường (Relative Valuation - Pricing)** | CCA (Comps), PTA                                                                                                       | **CCA:** So sánh bội số với các công ty cùng ngành giao dịch công khai. **PTA:** Dựa trên bội số của các giao dịch M&A lịch sử. CCA/PTA được dùng để kiểm tra tính hợp lý của kết quả DCF. |              |
| **II. QUẢN TRỊ HIỆU SUẤT & ĐO LƯỜNG LỢI SUẤT** | **II.A. Đo lường Hiệu suất/Lợi suất**                                 | IRR (Tỷ suất Hoàn vốn Nội bộ)                                                                                          | Chỉ số lợi suất dùng để đánh giá mức độ khả thi của dự án và sắp xếp thứ tự ưu tiên đầu tư.                                                                                                |              |
|                                                | **II.B. Công cụ Kiểm định Mô hình**                                   | Phân tích Độ nhạy (Sensitivity Analysis), Phân tích Kịch bản (Scenario Analysis), Kiểm tra Căng thẳng (Stress Testing) | Kiểm tra rủi ro bằng cách thay đổi các biến số đầu vào (ví dụ: WACC, Tốc độ Tăng trưởng) để xác định mức độ ảnh hưởng đến kết quả cuối cùng (NPV/Giá Mục tiêu).                            |              |
| **III. ĐỊNH GIÁ CHUYÊN NGÀNH**                 | **III.A. Định giá Bảo hiểm**                                          | Embedded Value (EV_life), VNB, VNB Margin, Solvency Margin Ratio (RBC)                                                 | Các chỉ số định giá và rủi ro đặc thù, bổ sung cho DCF.                                                                                                                                    |              |
| **IV. KHUNG QUẢN TRỊ RỦI RO (GRC)**            | **IV.A. Tuân thủ và Thẩm định**                                       | DD Reports (FDD), Compliance Risk Register, Yêu cầu AML/CFT (KYC/CDD)                                                  | Đảm bảo dữ liệu đầu vào (từ các chỉ số P&L/CFS) là chính xác. Xác định rủi ro pháp lý và quản trị, ảnh hưởng đến Chi phí Vốn (WACC).                                                       |              |

---

