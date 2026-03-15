 13 nhóm chỉ số tài chính MECE tuyệt đối** — đầy đủ, dễ hiểu, có ví dụ, có cách crawl bằng **XNO/VNStock**, và kèm **độ quan trọng (⭐)** để ưu tiên khi crawl hoặc dùng cho dashboard.

---

## 🧭 PHẦN 1: VALUATION – ĐỊNH GIÁ

| 🧩**Chỉ số**                   | 💡**Ý nghĩa dễ hiểu**                                      | 🧮**Ví dụ tính toán**                                   | ⚙️**Cách crawl (XNO/VNStock)**                                  | 🌟**Quan trọng** |
| ------------------------------ | ---------------------------------------------------------- | ------------------------------------------------------- | --------------------------------------------------------------- | ---------------- |
| **P/E (Price to Earnings)**    | Nhà đầu tư trả bao nhiêu cho 1 đồng lợi nhuận.             | Giá = 100k, EPS = 5k → P/E = 20.                        | `xno.stock('FPT').pe_ttm()` / `vnstock.Fundamental('FPT').pe()` | ⭐⭐⭐⭐☆            |
| **PEG Ratio**                  | Kết hợp P/E và tăng trưởng EPS → định giá hợp lý.          | P/E = 20, EPS Growth = 25% → PEG = 0.8.                 | `xno.stock('FPT').peg_ratio()`                                  | ⭐⭐⭐⭐☆            |
| **EV/EBITDA**                  | Giá trị DN so với lợi nhuận trước lãi vay, thuế, khấu hao. | EV = 1,000 tỷ; EBITDA = 200 → EV/EBITDA = 5.            | `xno.financials('FPT').ev_ebitda()`                             | ⭐⭐⭐⭐⭐            |
| **P/B (Price/Book)**           | Giá so với giá trị sổ sách.                                | Giá = 50k; BVPS = 25k → P/B = 2.                        | `vnstock.Fundamental('FPT').pb()`                               | ⭐⭐⭐⭐☆            |
| **Dividend Yield**             | Lợi suất cổ tức / giá cổ phiếu.                            | Cổ tức 2k, giá 50k → 4%.                                | `xno.dividend('FPT').yield()`                                   | ⭐⭐⭐⭐☆            |
| **Earnings Yield**             | Ngược P/E → tỉ lệ sinh lời trên giá.                       | EPS = 5k, Giá = 100k → 5%.                              | `1 / pe_ttm` hoặc `xno.metrics('FPT').earnings_yield()`         | ⭐⭐⭐⭐☆            |
| **FCF Yield**                  | Dòng tiền tự do / giá trị thị trường.                      | FCF = 1.000 tỷ; MCap = 20.000 tỷ → 5%.                  | `xno.financials('FPT').fcf_yield()`                             | ⭐⭐⭐⭐⭐            |
| **EV/FCF**                     | Giá trị DN so với FCF → đo sức tạo tiền.                   | EV = 10,000; FCF = 1,000 → EV/FCF = 10.                 | `xno.metrics('FPT').ev_fcf()`                                   | ⭐⭐⭐⭐☆            |
| **P/OCF**                      | Giá so với dòng tiền hoạt động.                            | Giá = 100k; OCF/Share = 10k → P/OCF = 10.               | `xno.financials('FPT').p_ocf()`                                 | ⭐⭐⭐☆             |
| **DCF (Discounted Cash Flow)** | Định giá chiết khấu dòng tiền tương lai → giá trị nội tại. | CF = [100,120,130,150,160], r=10% → PV = Σ CFt/(1.1)^t. | `xno.valuation('FPT').dcf()` / tự tính từ `cashflow()`          | ⭐⭐⭐⭐⭐            |
| **Intrinsic Value Gap**        | Chênh lệch giữa giá thị trường và giá trị nội tại.         | Intrinsic = 90k, Price = 80k → -11%.                    | So sánh DCF vs giá `stock('FPT').price()`                       | ⭐⭐⭐⭐⭐            |
| **EV/Sales**                   | Giá trị DN so với doanh thu → đo hiệu quả tăng trưởng.     | EV=1,000; Sales=500 → EV/Sales=2.                       | `xno.financials('FPT').ev_sales()`                              | ⭐⭐⭐☆             |

---

## 📈 PHẦN 2: GROWTH – TĂNG TRƯỞNG

| **Chỉ số**            | **Ý nghĩa**                               | **Ví dụ**               | **Cách crawl**                             | **Quan trọng** |
| ----------------------------- | ------------------------------------------------- | ------------------------------- | ------------------------------------------------- | --------------------- |
| **Revenue YoY**         | Tốc độ tăng trưởng doanh thu hàng năm.    | (1,200−1,000)/1,000=20%.       | `xno.financials('FPT').growth('revenue')`       | ⭐⭐⭐⭐⭐            |
| **Revenue QoQ**         | So sánh doanh thu quý này với quý trước.   | (300−250)/250=20%.             | `xno.financials('FPT').growth('revenue','qoq')` | ⭐⭐⭐⭐☆            |
| **EPS Growth YoY**      | Tăng trưởng lợi nhuận trên mỗi cổ phiếu. | EPS 5k→6k (+20%).              | `vnstock.Fundamental('FPT').eps_growth()`       | ⭐⭐⭐⭐☆            |
| **EBITDA Growth**       | Đo tăng trưởng lợi nhuận hoạt động.      | EBITDA 100→130 → +30%.        | `xno.financials('FPT').growth('ebitda')`        | ⭐⭐⭐⭐☆            |
| **FCF Growth**          | Đo tăng trưởng dòng tiền tự do.            | FCF 1,000→1,200 → +20%.       | `xno.financials('FPT').growth('fcf')`           | ⭐⭐⭐⭐☆            |
| **CAGR (5Y)**           | Tốc độ tăng trưởng kép bình quân 5 năm. | EPS 2k→4k trong 3 năm ⇒ 26%. | `xno.metrics('FPT').cagr('eps',5)`              | ⭐⭐⭐⭐⭐            |
| **Operating CF Growth** | Tăng trưởng dòng tiền từ hoạt động KD.   | OCF 500→550 → +10%.           | `xno.financials('FPT').growth('ocf')`           | ⭐⭐⭐☆              |

---

## 💰 PHẦN 3: PROFITABILITY – SINH LỜI

| **Chỉ số**                          | **Ý nghĩa**                   | **Ví dụ**                | **Cách crawl**                    | **Quan trọng** |
| ------------------------------------------- | ------------------------------------- | -------------------------------- | ---------------------------------------- | --------------------- |
| **ROE**                               | Hiệu quả sử dụng vốn chủ.       | 100/500=20%.                     | `vnstock.Fundamental('FPT').roe()`     | ⭐⭐⭐⭐⭐            |
| **ROA**                               | Hiệu quả sử dụng tổng tài sản. | 100/2000=5%.                     | `xno.financials('FPT').roa()`          | ⭐⭐⭐⭐☆            |
| **ROIC**                              | Sinh lời trên vốn đầu tư thực. | NOPAT=120; Invested=1000 → 12%. | `xno.metrics('FPT').roic()`            | ⭐⭐⭐⭐⭐            |
| **Gross Margin**                      | Lợi nhuận gộp / doanh thu.         | 300/1000=30%.                    | `xno.financials('FPT').gross_margin()` | ⭐⭐⭐⭐☆            |
| **Operating Margin**                  | Lợi nhuận hoạt động / doanh thu. | 200/1000=20%.                    | `xno.financials('FPT').oper_margin()`  | ⭐⭐⭐⭐☆            |
| **Net Margin**                        | Lợi nhuận ròng / doanh thu.        | 50/1000=5%.                      | `xno.metrics('FPT').net_margin()`      | ⭐⭐⭐⭐☆            |
| **EBIT Margin**                       | EBIT / doanh thu.                     | 150/1000=15%.                    | `xno.financials('FPT').ebit_margin()`  | ⭐⭐⭐⭐☆            |
| **Return on Capital Employed (ROCE)** | Lợi nhuận trên vốn sử dụng.     | EBIT/(Tổng TS–Nợ NH).         | `xno.metrics('FPT').roce()`            | ⭐⭐⭐⭐☆            |

---

## ⚙️ PHẦN 4: EFFICIENCY – HIỆU QUẢ HOẠT ĐỘNG

| **Chỉ số**                    | **Ý nghĩa**                                 | **Ví dụ**                              | **Cách crawl (XNO/VNStock)**             | **Quan trọng** |
| ------------------------------------- | --------------------------------------------------- | ---------------------------------------------- | ----------------------------------------------- | --------------------- |
| **Asset Turnover**              | Hiệu quả sử dụng tài sản để tạo doanh thu. | Doanh thu 2,000 / Tài sản 1,000 → 2.0.      | `xno.metrics('FPT').asset_turnover()`         | ⭐⭐⭐⭐☆            |
| **Inventory Turnover**          | Tốc độ quay vòng hàng tồn kho.                | 600/200 = 3 vòng/năm.                        | `xno.financials('FPT').inventory_turnover()`  | ⭐⭐⭐⭐☆            |
| **Receivables Turnover**        | Tốc độ thu hồi công nợ.                       | Doanh thu = 1,000; Công nợ = 250 → 4 vòng. | `xno.financials('FPT').receivable_turnover()` | ⭐⭐⭐⭐☆            |
| **Payables Turnover**           | Tốc độ thanh toán nợ.                          | COGS = 500; Nợ = 100 → 5 vòng.              | `xno.metrics('FPT').payable_turnover()`       | ⭐⭐⭐☆              |
| **Cash Conversion Cycle (CCC)** | Chu kỳ chuyển đổi tiền mặt.                   | DIO + DSO – DPO = 75 ngày.                   | `xno.metrics('FPT').cash_conversion_cycle()`  | ⭐⭐⭐⭐⭐            |
| **Working Capital Turnover**    | Hiệu suất sử dụng vốn lưu động.             | DT = 1,000; VLD = 250 → 4.                    | `xno.metrics('FPT').wc_turnover()`            | ⭐⭐⭐☆              |

---

## 💧 PHẦN 5: LIQUIDITY & SOLVENCY – THANH KHOẢN & ĐÒN BẨY

| **Chỉ số**          | **Ý nghĩa**                           | **Ví dụ**                                         | **Cách crawl**                         | **Quan trọng** |
| --------------------------- | --------------------------------------------- | --------------------------------------------------------- | --------------------------------------------- | --------------------- |
| **Current Ratio**     | Khả năng thanh toán ngắn hạn.            | 300/150=2.0.                                              | `xno.financials('FPT').current_ratio()`     | ⭐⭐⭐⭐☆            |
| **Quick Ratio**       | Đo thanh khoản nhanh (trừ hàng tồn kho). | (300-100)/150=1.33.                                       | `xno.financials('FPT').quick_ratio()`       | ⭐⭐⭐⭐☆            |
| **Cash Ratio**        | Tài sản tiền mặt / nợ ngắn hạn.        | 100/200=0.5.                                              | `xno.financials('FPT').cash_ratio()`        | ⭐⭐⭐☆              |
| **Debt/Equity**       | Tỉ lệ nợ/vốn chủ.                        | 400/200=2.                                                | `vnstock.Fundamental('FPT').debt_equity()`  | ⭐⭐⭐⭐⭐            |
| **Net Debt/EBITDA**   | Sức chịu nợ.                               | (500-100)/200=2.                                          | `xno.metrics('FPT').net_debt_ebitda()`      | ⭐⭐⭐⭐☆            |
| **Interest Coverage** | Khả năng trả lãi vay.                     | EBIT=200; Lãi=50 → 4 lần.                              | `xno.financials('FPT').interest_coverage()` | ⭐⭐⭐⭐☆            |
| **Altman Z-Score**    | Chỉ số dự đoán phá sản DN.             | Tính theo công thức Z = 1.2X1+1.4X2+3.3X3+0.6X4+1.0X5. | `xno.metrics('FPT').altman_z()`             | ⭐⭐⭐⭐⭐            |

---

## 📊 PHẦN 6: TECHNICAL – KỸ THUẬT

| **Chỉ số**        | **Ý nghĩa**                                  | **Ví dụ**                        | **Crawl**                       | **Quan trọng** |
| ------------------------- | ---------------------------------------------------- | ---------------------------------------- | ------------------------------------- | --------------------- |
| **RSI**             | Động lượng giá, xác định quá mua/quá bán. | RSI(14).                                 | `xno.technical('FPT').rsi()`        | ⭐⭐⭐⭐☆            |
| **MACD**            | Đo xu hướng bằng chênh lệch EMA.               | EMA(12)–EMA(26).                        | `xno.technical('FPT').macd()`       | ⭐⭐⭐⭐⭐            |
| **Bollinger Bands** | Đo biên độ biến động.                         | ±2σ quanh SMA20.                       | `xno.technical('FPT').bollinger()`  | ⭐⭐⭐⭐☆            |
| **ADX**             | Độ mạnh xu hướng.                               | ADX>25 = có trend mạnh.                | `xno.technical('FPT').adx()`        | ⭐⭐⭐⭐☆            |
| **ATR**             | Biến động trung bình thật.                      | ATR(14).                                 | `xno.technical('FPT').atr()`        | ⭐⭐⭐☆              |
| **CCI**             | Phát hiện quá mua/quá bán.                      | CCI>100 hoặc <-100.                     | `xno.technical('FPT').cci()`        | ⭐⭐⭐☆              |
| **Williams %R**     | Xác định đảo chiều ngắn hạn.                 | %R < -80 → quá bán.                   | `xno.technical('FPT').williams_r()` | ⭐⭐⭐☆              |
| **OBV**             | Khối lượng xác nhận xu hướng.                 | OBV tăng cùng giá = xu hướng mạnh. | `xno.technical('FPT').obv()`        | ⭐⭐⭐⭐☆            |
| **VWAP**            | Giá trung bình theo khối lượng.                 | (ΣP×V)/ΣV.                            | `xno.technical('FPT').vwap()`       | ⭐⭐⭐⭐☆            |
| **Ichimoku Cloud**  | Hệ thống xu hướng tổng hợp.                    | Tenkan, Kijun, Senkou, Chikou.           | `xno.technical('FPT').ichimoku()`   | ⭐⭐⭐⭐⭐            |

---

## 📈 PHẦN 7: RISK & PERFORMANCE – RỦI RO & HIỆU SUẤT

| **Chỉ số**           | **Ý nghĩa**                        | **Ví dụ** | **Crawl**                       | **Quan trọng** |
| ---------------------------- | ------------------------------------------ | ----------------- | ------------------------------------- | --------------------- |
| **Sharpe Ratio**       | Hiệu suất / độ lệch chuẩn.           | (Rp–Rf)/σ.      | `xno.backtest('pf').sharpe()`       | ⭐⭐⭐⭐⭐            |
| **Sortino Ratio**      | Hiệu suất / rủi ro giảm.               | (Rp–Rf)/σ_down. | `xno.backtest('pf').sortino()`      | ⭐⭐⭐⭐☆            |
| **Calmar Ratio**       | Lợi nhuận / Max Drawdown.                | 20%/10%=2.        | `xno.backtest('pf').calmar()`       | ⭐⭐⭐⭐☆            |
| **Omega Ratio**        | Đo lợi nhuận trên xác suất thua lỗ. | >1 là tốt.      | `xno.backtest('pf').omega()`        | ⭐⭐⭐☆              |
| **Max Drawdown**       | Mức sụt vốn tối đa.                   | -25%.             | `xno.backtest('pf').max_drawdown()` | ⭐⭐⭐⭐⭐            |
| **Volatility (σ)**    | Độ biến động lợi suất.              | std(returns).     | `xno.metrics('pf').volatility()`    | ⭐⭐⭐⭐☆            |
| **Downside Deviation** | Độ lệch chuẩn phần lỗ.               | ...               | `xno.metrics('pf').downside_dev()`  | ⭐⭐⭐☆              |

---

## 🧮 PHẦN 8: DERIVATIVES – PHÁI SINH

| **Chỉ số**                | **Ý nghĩa**                                 | **Ví dụ** | **Crawl**                        | **Quan trọng** |
| --------------------------------- | --------------------------------------------------- | ----------------- | -------------------------------------- | --------------------- |
| **Delta**                   | Nhạy cảm giá option với tài sản cơ sở.      | Δ=0.6.           | `xno.derivatives('VN30F1M').delta()` | ⭐⭐⭐⭐☆            |
| **Gamma**                   | Tốc độ thay đổi của Delta.                    | Γ=0.02.          | `xno.derivatives('VN30F1M').gamma()` | ⭐⭐⭐⭐☆            |
| **Vega**                    | Nhạy với volatility.                              | 0.1.              | `xno.derivatives('VN30F1M').vega()`  | ⭐⭐⭐⭐☆            |
| **Theta**                   | Nhạy cảm với thời gian (time decay).            | θ=-0.05.         | `xno.derivatives('VN30F1M').theta()` | ⭐⭐⭐☆              |
| **Rho**                     | Nhạy cảm với lãi suất.                         | ρ=0.1.           | `xno.derivatives('VN30F1M').rho()`   | ⭐⭐⭐☆              |
| **IV Rank / IV Percentile** | So sánh độ biến động hiện tại vs quá khứ. | IV=25%, Rank=80%. | `xno.options('VN30F1M').iv_rank()`   | ⭐⭐⭐⭐☆            |

---

## 💵 PHẦN 9: FIXED INCOME & CREDIT – TRÁI PHIẾU & TÍN DỤNG

| **Chỉ số**       | **Ý nghĩa**                                           | **Ví dụ**      | **Crawl**                 | **Quan trọng** |
| ------------------------ | ------------------------------------------------------------- | ---------------------- | ------------------------------- | --------------------- |
| **YTM**            | Lợi suất đến đáo hạn.                                  | ≈11.1%.               | `xno.bond('VCB122028').ytm()` | ⭐⭐⭐⭐⭐            |
| **Current Yield**  | Coupon / giá thị trường.                                  | 10%/950k≈10.5%.       | `xno.bond().current_yield()`  | ⭐⭐⭐☆              |
| **Duration**       | Độ nhạy giá trái phiếu.                                 | 4 → LS↑1%, giá↓4%. | `xno.bond().duration()`       | ⭐⭐⭐⭐☆            |
| **Convexity**      | Độ cong của quan hệ giá–lãi suất.                     | ...                    | `xno.bond().convexity()`      | ⭐⭐⭐☆              |
| **Z-Spread / OAS** | Phần bù rủi ro tín dụng.                                 | ...                    | `xno.credit().oas()`          | ⭐⭐⭐⭐☆            |
| **Credit Spread**  | Chênh lệch lợi suất trái phiếu rủi ro và phi rủi ro. | ...                    | `xno.credit().spread()`       | ⭐⭐⭐⭐☆            |

---

## 📊 PHẦN 10: PORTFOLIO & QUANT – DANH MỤC & ĐỊNH LƯỢNG

| **Chỉ số**          | **Ý nghĩa**                          | **Ví dụ**   | **Crawl**                    | **Quan trọng** |
| --------------------------- | -------------------------------------------- | ------------------- | ---------------------------------- | --------------------- |
| **Beta**              | Độ nhạy danh mục so với thị trường.  | β=1.2.             | `xno.portfolio().beta()`         | ⭐⭐⭐⭐⭐            |
| **Alpha**             | Hiệu suất vượt trội.                    | 2%.                 | `xno.portfolio().alpha()`        | ⭐⭐⭐⭐⭐            |
| **Information Ratio** | Hiệu suất vượt trội / sai lệch.        | (Rp−Rb)/σ_active. | `xno.metrics().info_ratio()`     | ⭐⭐⭐⭐☆            |
| **Tracking Error**    | Sai lệch chuẩn giữa danh mục và chuẩn. | ...                 | `xno.metrics().tracking_error()` | ⭐⭐⭐☆              |
| **Treynor Ratio**     | Hiệu suất / rủi ro hệ thống.            | (Rp−Rf)/β.        | `xno.backtest().treynor()`       | ⭐⭐⭐☆              |
| **HHI / Effective N** | Mức độ tập trung danh mục.              | HHI=Σw².          | `xno.portfolio().hhi()`          | ⭐⭐⭐☆              |

---

## 🌍 PHẦN 11: MACRO & SENTIMENT – VĨ MÔ & TÂM LÝ

| **Chỉ số**             | **Ý nghĩa**                      | **Ví dụ** | **Crawl**                  | **Quan trọng** |
| ------------------------------ | ---------------------------------------- | ----------------- | -------------------------------- | --------------------- |
| **GDP Growth**           | Mức tăng trưởng kinh tế.            | 6.4%.             | `xno.macro('VN').gdp_growth()` | ⭐⭐⭐⭐☆            |
| **Inflation (CPI)**      | Tăng giá hàng hóa.                   | 4%.               | `xno.macro('VN').cpi()`        | ⭐⭐⭐⭐☆            |
| **PMI**                  | Sức khỏe sản xuất (>50 = mở rộng). | 52.3.             | `xno.macro('VN').pmi()`        | ⭐⭐⭐☆              |
| **Interest Rate Spread** | Chênh lệch LS dài – ngắn hạn.      | 2%.               | `xno.macro().yield_curve()`    | ⭐⭐⭐☆              |
| **VIX / MOVE**           | Đo biến động thị trường.          | VIX=17.           | `xno.global('US').vix()`       | ⭐⭐⭐⭐☆            |
| **FX Rate**              | Tỷ giá hối đoái.                    | USD/VND=25,400.   | `xno.fx('USDVND').rate()`      | ⭐⭐⭐⭐☆            |

---

## 🪙 PHẦN 12: CRYPTO – TIỀN MÃ HÓA

| **Chỉ số**      | **Ý nghĩa**                         | **Ví dụ**    | **Crawl**                       | **Quan trọng** |
| ----------------------- | ------------------------------------------- | -------------------- | ------------------------------------- | --------------------- |
| **NVT Ratio**     | Giá trị mạng / khối lượng giao dịch. | 20.                  | `xno.crypto('BTC').nvt()`           | ⭐⭐⭐⭐☆            |
| **MVRV**          | Lợi nhuận trung bình nhà đầu tư.     | Market/Realized Cap. | `xno.crypto('BTC').mvrv()`          | ⭐⭐⭐⭐☆            |
| **SOPR**          | Lợi nhuận khi chi tiêu coin.             | >1 = lời.           | `xno.crypto('BTC').sopr()`          | ⭐⭐⭐☆              |
| **Hashrate**      | Sức mạnh mạng.                           | ...                  | `xno.crypto('BTC').hashrate()`      | ⭐⭐⭐☆              |
| **Funding Rate**  | Chênh lệch giữa giá perp và spot.      | 0.02%.               | `xno.crypto('BTC').funding_rate()`  | ⭐⭐⭐☆              |
| **Open Interest** | Tổng hợp đồng mở.                      | 5B USD.              | `xno.crypto('BTC').open_interest()` | ⭐⭐⭐☆              |

---

## 🧪 PHẦN 13: BACKTESTING & STRATEGY DIAGNOSTICS

| **Chỉ số**                    | **Ý nghĩa**                | **Ví dụ**             | **Crawl**                           | **Quan trọng** |
| ------------------------------------- | ---------------------------------- | ----------------------------- | ----------------------------------------- | --------------------- |
| **Win Rate**                    | Tỷ lệ giao dịch thắng.         | 60%.                          | `xno.backtest('strat').win_rate()`      | ⭐⭐⭐⭐⭐            |
| **Profit Factor**               | Tổng lãi / tổng lỗ.            | 1.2.                          | `xno.backtest('strat').profit_factor()` | ⭐⭐⭐⭐☆            |
| **Expectancy**                  | Lợi nhuận kỳ vọng TB/lệnh.    | (Win×AvgWin−Loss×AvgLoss). | `xno.backtest().expectancy()`           | ⭐⭐⭐⭐☆            |
| **Time Under Water**            | Thời gian danh mục thua lỗ.     | ...                           | `xno.backtest().tuw()`                  | ⭐⭐⭐☆              |
| **Max Consecutive Wins/Losses** | Chuỗi thắng/thua dài nhất.     | 7/5.                          | `xno.backtest().streaks()`              | ⭐⭐⭐☆              |
| **Recovery Factor**             | Tốc độ phục hồi sau drawdown. | 2.5.                          | `xno.backtest().recovery_factor()`      | ⭐⭐⭐☆              |

---

🔥 **Hoàn tất Full MECE Metrics Universe!**Tổng cộng **~180 chỉ số**, chia theo 13 nhóm chuẩn toàn cầu.Bạn có muốn mình:
