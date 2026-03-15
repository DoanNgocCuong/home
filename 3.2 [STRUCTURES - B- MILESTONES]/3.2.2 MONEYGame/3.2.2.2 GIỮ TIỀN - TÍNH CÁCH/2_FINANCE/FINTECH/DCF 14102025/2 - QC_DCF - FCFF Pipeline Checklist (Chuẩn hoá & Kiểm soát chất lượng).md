# DCF / FCFF Pipeline Checklist (Chuẩn hoá & Kiểm soát chất lượng)

> Tài liệu này mô tả pipeline không-code để tính **FCFF** bằng **hai đường** (P&L+BS và CFO), **reconcile**, và **gắn cờ rủi ro phân loại**, đảm bảo kết quả **nhất quán, sạch, và kiểm toán được**. Áp dụng cho **doanh nghiệp phi tài chính**.

---

## A) Chuẩn hóa kế toán (Accounting normalization)

1. **Phạm vi áp dụng**
   - Chỉ cho doanh nghiệp **phi tài chính**. Nếu ngành bank/insurance/broker → chuyển sang **Excess Return / FCFE đặc thù** *(flag `FINANCIAL_INSTITUTION`)*.

2. **IFRS 16 (thuê tài sản)** — chọn 1 “view” và nhất quán:
   - **View mặc định (khuyến nghị)**: giữ IFRS16 *as-is*  
     - EBIT đã gồm khấu hao ROU.  
     - **Interest** gồm lãi lease → cộng lại trong công thức CFO-route (sau thuế).  
     - Nợ thuê tính vào **Debt** trong WACC.  
     - Trả **gốc lease** ở CFF → **không** trừ riêng vào FCFF.
   - Nếu cần **pre-IFRS16 view** để so sánh dài hạn → áp dụng lại cho **toàn bộ lịch sử** (không trộn hai view).

3. **Lãi vay vốn hóa (capitalized interest)**
   - Xác định `capitalized_interest` trong thuyết minh CAPEX.
   - **Không** cộng phần này vào `Interest×(1−t)` lần nữa *(tránh double count)*.
   - *Flag:* `CAPITALIZED_INTEREST` nếu >5% Interest.

4. **M&A và tài sản không vận hành**
   - Loại **acquisitions/disposals of subsidiaries** khỏi CAPEX; xử lý **ngoài FCFF**.
   - Tài sản không vận hành (đất trống, đầu tư tài chính…): định giá riêng → cộng/trừ ở cầu **EV→Equity**.
   - *Flag:* `M&A_IN_CAPEX` nếu dòng M&A nằm trong CAPEX báo cáo.

5. **Cổ phiếu thưởng (SBC)**
   - Là non-cash ⇒ giữ nguyên trong CFO; **không** chỉnh FCFF.
   - Tác động kinh tế xử ở **vốn chủ** (pha loãng số cổ phiếu). *Flag* nếu `SBC/EBITDA > 10%`.

6. **Công ty liên kết/liên doanh (equity method)**
   - Loại lãi/lỗ từ associates khỏi EBIT/EBITDA “operating”.
   - Cổ tức nhận từ associates **không** coi là FCFF vận hành. Định giá associates riêng/cộng lại sau.
   - *Flag:* `ASSOCIATES_PRESENT`.

7. **Lương hưu (pension) – nếu trọng yếu**
   - Tách **service cost** (operating) vs **interest cost** (tài chính).
   - Thiếu dữ liệu → *flag* `PENSION_UNCERTAIN`.

8. **Thuế**
   - Dùng **thuế suất mục tiêu dài hạn** `t*` cho NOPAT và cho `Interest×(1−t*)`.
   - Nếu **cash tax rate** lệch `t*` > ±5pp trong ≥2 kỳ → *flag* `TAX_MISMATCH` và ghi chú (ưu đãi thuế, NOL, timing).

9. **Đơn vị tiền tệ & lạm phát**
   - Nếu có **hyperinflation (IAS 29)** hoặc tái định giá lớn → *flag* `INFLATION_ACCOUNTING` và chuẩn hóa.
   - Báo cáo nhiều đồng tiền → chuyển đổi về 1 currency, cố định tỷ giá kỳ báo cáo.

---

## B) Định nghĩa & đo lường chuẩn (Economic normalization)

10. **CAPEX chuẩn**
    - `CAPEX_net = PP&E additions − Proceeds from sale ± capitalized R&D/software` (nếu có, dựa thuyết minh).
    - *Flag* `CAPEX_MAPPING_ISSUE` nếu CAPEX báo cáo khác định nghĩa >15%.

11. **Tách Maintenance vs Growth CAPEX** *(để dự báo chính xác)*
    - Heuristic A: `Maintenance ≈ Depreciation × k_sector` (k≈0.8–1.2 theo ngành).
    - Heuristic B: dựa **Asset age** (gross PP&E/Depreciation) & **khả năng giữ sản lượng**.
    - Heuristic C: mô hình “Giữ EBIT không tăng” → back-solve maintenance CAPEX.
    - Lưu ước số, *flag* `MAINT_GROWTH_SPLIT_WEAK` nếu không đáng tin.

12. **NWC vận hành**
    - `NWC = (AR + Inventory + Op. other CA − Cash) − (AP + Op. other CL − Short-term debt)`
    - Bao gồm **Deferred revenue (operating)** trong **CL vận hành** (giảm NWC).
    - Loại **interest payable/receivable** (tài chính), **tax payable** giữ lại (operating).
    - *Flag* `NWC_MAPPING_ISSUE` nếu ΔNWC từ BS lệch delta WC trong CFO > 10%.

13. **CFO-route**
    - `FCFF = CFO + Interest_expense × (1−t*) − CAPEX`
    - Nếu **interest paid/received** được phân loại khác chuẩn (IFRS/US GAAP) → ghi điều chỉnh chuẩn hóa, *flag* `NONTYPICAL_CLASSIFICATION`.

---

## C) Reconcile nhiều lớp (Multi-bridge reconciliation)

14. **Hai cách tính FCFF**
    - A: `EBIT(1−t*) + D&A − ΔNWC − CAPEX`
    - B: `CFO + Interest(1−t*) − CAPEX`
    - Chênh lệch `Gap = A − B` với ngưỡng:
      - `|Gap| ≤ min(5% revenue, 10% avg FCFF)` ⇒ OK.
      - Nếu vượt → chạy **bridge** theo thứ tự:
        1) Capitalized interest
        2) Lease classification
        3) M&A lẫn vào CAPEX/CFI
        4) One-off trong CFO (kiện tụng, bảo hiểm, thuế bất thường)
        5) Thuế tiền vs t*
        6) Mapping NWC
        7) Associates/FX remeasurement

15. **Bridge công thức chéo (sanity algebra)**
    - Từ EBITDA:  
      `FCFF ≈ EBITDA − Cash taxes_on_EBIT − ΔNWC − CAPEX ± other_op_adjustments`
    - Từ lợi nhuận ròng (NI):  
      `FCFF ≈ NI + D&A + Interest(1−t*) − ΔNWC − CAPEX − NonOpAfterTax`
    - Các đường chéo phải hội tụ về cùng ± ngưỡng; nếu không → `RECONCILE_FAIL`.

---

## D) Kiểm tra thống kê & biên hợp lý (Plausibility & robustness)

16. **Biên hợp lý theo ngành** (flag nếu vượt ngưỡng 3 năm liền hoặc spike >2σ):
    - `CAPEX/Depreciation` trong **[0.6, 3.0]** (đa số ngành sản xuất).
    - `D&A/Revenue` ổn định theo cấu hình tài sản; spike → đổi đời tài sản.
    - `ΔNWC/Revenue` không “saw-tooth” quá lớn trừ ngành mùa vụ.
    - **Cash Conversion Cycle (CCC)** hợp lý với mô hình kinh doanh (retail CCC âm; project-based CCC dương lớn).
    - `FCFF/EBITDA` không âm kéo dài trừ khi **CAPEX growth** cực lớn (flag `CAPINT_HEAVY`).
    - `Interest coverage = EBIT/Interest > 2×` (nếu <1× → WACC phải cao; *flag* `LEVERAGE_STRESS`).

17. **Chất lượng lợi nhuận & dòng tiền**
    - **Accruals ratio**: `(NI − CFO)/Total assets` cao kéo dài → chất lượng dòng tiền kém (*flag* `LOW_CASH_QUALITY`).  
    - **CFO margin** vs **EBITDA margin**: gap lớn → `ONE_OFF_IN_CFO` hoặc cấu trúc working capital bất thường.

18. **Thuế**
    - `Cash tax paid / EBIT` nên quanh `t*` (trừ ưu đãi/NOL). Sai khác có lý do → note; không có → *flag* `TAX_MISMATCH`.

19. **WACC sanity**
    - WACC không được **< lạm phát danh nghĩa dài hạn**.
    - `g_terminal ≤ min(real_GDP_potential + inflation, guardrail_sector)`; nếu g > WACC → *flag* `TERMINAL_G_TOO_HIGH`.

20. **Độ nhạy & đóng góp rủi ro**
    - Bảng nhạy 2D: **WACC × g**.
    - **Variance decomposition** (thô): ước tính % biến động EV do (biên EBIT, CAPEX/Rev, ΔNWC/Rev, t*, WACC, g).  
      Nhãn `PRIMARY_SENSITIVITY = {WACC|g|CAPEX|Margin}`.

21. **Bất định (uncertainty)**
    - Monte-Carlo nhẹ (1–2k lần) trên 5–7 tham số chính với phân phối hợp lý (truncated normal/beta).
    - Báo **EV/Equity 5–95%**. *Flag* `VALUATION_UNCERT_HIGH` nếu IQR/Median > 50%.

---

## E) Nhất quán cấu trúc vốn & NCI (minority)

22. **Non-controlling interests (NCI)**
    - FCFF dựa trên **báo cáo hợp nhất** ⇒ định giá **firm** bao gồm phần của NCI.
    - Khi từ EV → Equity cho cổ đông công ty mẹ: **trừ** `NCI (fair value)` + **trừ** nợ ròng + **cộng** tài sản không vận hành.
    - Không trừ NCI trong FCFF; làm ở **cầu EV→Equity** để nhất quán.

---

## F) Dữ liệu, kiểm thử & audit

23. **Data hygiene**
    - Chuẩn hóa đơn vị (đồng/triệu/billion), tần suất (annual/quý), TTM khi cần nhưng không trộn TTM với annual trong cùng cột.
    - Track **provenance** (file→sheet→cell/thuyết minh). Mỗi chỉnh sửa phải có “note & reason”.

24. **Kiểm thử tự động (machine-checkable rules)**
    - `assert` mapping: tổng biến động WC trên BS ≈ “changes in working capital” trên CFO (±5%).
    - `assert` `CFO = NI + noncash + ΔWC + other` (công thức khôi phục).
    - `assert` A-route vs B-route trong ngưỡng; nếu fail → bridge bắt buộc.
    - `assert` `CAPEX_net` không âm trừ kỳ thanh lý lớn (có proceeds).
    - `assert` không double-count interest vốn hóa.
    - `assert` phân loại dividends received/paid theo chuẩn (không để lẫn CFO vận hành).
    - Mỗi assert gán **severity**: `ERROR` (dừng), `WARN`, `INFO`.

25. **Mức nghiêm trọng & hành động**
    - `ERROR`: `RECONCILE_FAIL`, `DATA_INCONSISTENT`, `FINANCIAL_INSTITUTION` (khi dùng sai mô hình).
    - `WARN`: `CAPITALIZED_INTEREST`, `LEASE_CLASSIFICATION`, `M&A_IN_CAPEX`, `TAX_MISMATCH`, `NWC_MAPPING_ISSUE`, `SBC_MATERIAL`, `ASSOCIATES_PRESENT`.
    - `INFO`: `SEASONALITY_SPIKE`, `SUPPLY_CHAIN_FINANCING`, `CAPINT_HEAVY`, `LOW_CASH_QUALITY`.

26. **Báo cáo đầu ra (schema đề xuất)**
```json
{
  "meta": {"currency": "VND", "freq": "annual|quarterly", "ttm_used": false},
  "drivers": {"revenue": [], "ebit_margin": [], "tax_rate_target": [], "capex_sales": [], "dna_sales": [], "dso_dio_dpo": []},
  "fcff": {
    "method_A": [{"year": 2021, "nopat": 0, "dna": 0, "capex": 0, "delta_nwc": 0, "fcff": 0}],
    "method_B": [{"year": 2021, "cfo": 0, "interest": 0, "capex": 0, "fcff": 0}],
    "reconcile_gap": [{"year": 2021, "gap": 0, "status": "OK|RECONCILE_FAIL"}]
  },
  "wacc": {"rd_after_tax": 0, "re": 0, "wd": 0, "we": 0, "wacc": 0},
  "terminal": {"method": "gordon|exit_multiple", "g": 0, "tv": 0},
  "flags": ["CAPITALIZED_INTEREST", "LEASE_CLASSIFICATION"],
  "diagnostics": ["asserts pass/fail...", "bridges applied..."],
  "uncertainty": {"EV_p5": 0, "EV_p50": 0, "EV_p95": 0, "PRIMARY_SENSITIVITY": "WACC"},
  "notes": ["text explanations..."]
}
```

---

## G) Mini-playbook xử lý tình huống “khó chịu”

- **Mùa vụ cực mạnh**: dùng rolling-TTM cho NOPAT/D&A/ΔNWC/CAPEX; so sánh FCFF_TTM vs annual.
- **Factoring/Reverse Factoring**: điều chỉnh lại AR/AP về “không factoring” nếu thuyết minh đủ; nếu không, *flag* `SUPPLY_CHAIN_FINANCING` và nâng biên sai số khi dự báo ΔNWC.
- **Thay đổi chính sách ghi nhận doanh thu**: tái lập chuỗi “pro forma” trước/sau, không trộn lẫn.
- **PP&E revaluation gains**: loại khỏi EBIT/EBT; chỉ ảnh hưởng vốn chủ, không FCFF.

---

### Ghi chú nhanh về hai công thức FCFF (để tra cứu)
- **Route A (P&L + BS):**  
  `FCFF = EBIT(1−t*) + D&A − ΔNWC − CAPEX`
- **Route B (CFO-route):**  
  `FCFF = CFO + Interest×(1−t*) − CAPEX`

> Thực hành tốt: tính **cả hai route**, chạy **reconcile** và ghi lại **bridge**. Nếu chênh lệch vượt ngưỡng, kích hoạt điều tra theo các flag ở trên.
