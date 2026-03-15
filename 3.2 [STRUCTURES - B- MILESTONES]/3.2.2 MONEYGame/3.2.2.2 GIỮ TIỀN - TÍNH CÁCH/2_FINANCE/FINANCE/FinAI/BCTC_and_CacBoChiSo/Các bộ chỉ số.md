## Giải đáp về Sự Khác Biệt Công Thức

Ngoài các mã đặc biệt như BVH (sử dụng báo cáo tài chính riêng do đặc thù ngành bảo hiểm), hầu hết mã chứng khoán trên HOSE tuân thủ chuẩn báo cáo tài chính thống nhất theo Thông tư 200/2014/TT-BTC và các sửa đổi (VAS/IFRS cơ bản), nên công thức tính toán tỷ lệ tài chính (như ROE, ROA) thường giống nhau. Tuy nhiên, sự khác biệt chủ yếu nằm ở mã đặc biệt và bộ luật báo cáo riêng theo ngành. Điều này phù hợp với kiến trúc engine generic + JSON config bạn đang build, tránh if/elif explosion.[aceacademy+1](https://aceacademy.vn/mece-la-gi-cach-su-dung-mece-framework-chuan/)​

## MECE Mã Đặc Biệt Như BVH

Áp dụng nguyên tắc MECE (Mutually Exclusive - loại trừ lẫn nhau; Collectively Exhaustive - bao quát toàn bộ), phân loại mã đặc biệt trên HOSE dựa trên báo cáo tài chính riêng biệt:[ocd+1](https://ocd.vn/nguyen-tac-mece/)​

- **Nhóm 1: Bảo hiểm** (BVH, BIC, PTI, PGI): Sử dụng mẫu báo cáo riêng (Thông tư 50/2021/TT-BTC), với chỉ số đặc thù như combined ratio, doanh thu phí bảo hiểm gốc.
    
- **Nhóm 2: Ngân hàng** (VCB, BID, CTG): Báo cáo theo Thông tư 19/2021/TT-NHNN, thêm tỷ lệ CAR, NIM, LDR.
    
- **Nhóm 3: Chứng khoán** (SSI, HCM, VND): Theo Thông tư 121/2020/TT-BTC, tập trung margin, phí giao dịch.
    
- **Nhóm 4: Khác** (VIC - quỹ đầu tư, POW - năng lượng với báo cáo môi trường): Ít hơn, override riêng.
    

## MECE Bộ Luật Báo Cáo Trên HOSE

Phân loại toàn bộ theo khung pháp lý (MECE đảm bảo không trùng lặp, bao quát 100% mã HOSE ~400 mã):[vietnammanagementconsulting+1](https://www.vietnammanagementconsulting.com/2024/10/16/nguyen-tac-mece-luat-bat-thanh-van-trong-case-interview/)​

- **Chuẩn chung (80% mã)**: Thông tư 200/2014/TT-BTC (công ty thường), VAS cơ bản - công thức chuẩn (KQKD / CDKT).
    
- **Ngành đặc thù (15%)**: Bảo hiểm (50/2021), Ngân hàng (19/2021), Chứng khoán (121/2020), Bất động sản (VIC-like theo 96/2020).
    
- **Quỹ/Đặc biệt (5%)**: ETF, quỹ mở (Thông tư 98/2020), Reits - báo cáo NAV riêng.  
    Tổng MECE: Các nhóm loại trừ lẫn nhau (mỗi mã chỉ 1 khung), bao quát toàn bộ.
    

## Prompt Để Xây Engine Config

text

`Bạn là AI Engineer chuyên FinTech, xây engine Python generic phân tích báo cáo tài chính chứng khoán HOSE (scale 400+ mã). Nhiệm vụ:  1. Thiết kế JSON config schema MECE cho các mã đặc biệt (BVH-like: bảo hiểm, ngân hàng, chứng khoán) + chuẩn chung. 2. Mini DSL parse công thức (e.g., "KQKD_60 / CDKT_410_avg * 100" → engine eval dynamic). 3. Code mẫu engine: Load JSON per mã → routing theo legal_framework → compute ratios → output dict. 4. Đảm bảo scalable: Thêm mã mới chỉ edit JSON, không code if/elif. Input mẫu JSON: {   "ticker": "BVH",  "framework": "insurance_50_2021",  "ratios": {    "ROE": "LNST_60 / VON_410_avg",    "CombinedRatio": "ChiPhiBH / DoanhThuPhiGoc"  },  "overrides": {...} } Output: Code Python + JSON samples cho BVH/VCB/standard + test cases.`

Prompt này giúp phác thảo mini DSL ngay, align với chiến lược đại dương xanh + tích lũy system dài hạn của bạn.

Add to follow-up

Check sources

1. [https://aceacademy.vn/mece-la-gi-cach-su-dung-mece-framework-chuan/](https://aceacademy.vn/mece-la-gi-cach-su-dung-mece-framework-chuan/)
2. [https://ocd.vn/nguyen-tac-mece/](https://ocd.vn/nguyen-tac-mece/)
3. [https://tapchikinhtetaichinh.vn/nhom-co-phieu-nao-se-thu-hut-dong-tien.html](https://tapchikinhtetaichinh.vn/nhom-co-phieu-nao-se-thu-hut-dong-tien.html)
4. [https://acadummy21.wordpress.com/2021/09/01/5-mece-framework-duy-nhat-ban-can-phai-biet/](https://acadummy21.wordpress.com/2021/09/01/5-mece-framework-duy-nhat-ban-can-phai-biet/)
5. [https://analytics.tomorrowmarketers.org/p/mece](https://analytics.tomorrowmarketers.org/p/mece)
6. [https://athenacorp.vn/mece-06-loi-ich-ap-dung-nguyen-tac-phan-tich-ro-rang/](https://athenacorp.vn/mece-06-loi-ich-ap-dung-nguyen-tac-phan-tich-ro-rang/)
7. [https://viec.co/bai-viet/phuong-phap-giai-quyet-van-de-mece-o-viec-co/1462](https://viec.co/bai-viet/phuong-phap-giai-quyet-van-de-mece-o-viec-co/1462)
8. [https://www.vietnammanagementconsulting.com/2024/10/16/nguyen-tac-mece-luat-bat-thanh-van-trong-case-interview/](https://www.vietnammanagementconsulting.com/2024/10/16/nguyen-tac-mece-luat-bat-thanh-van-trong-case-interview/)
9. [https://finance.vietstock.vn/bvh/phan-tich-ky-thuat.htm](https://finance.vietstock.vn/bvh/phan-tich-ky-thuat.htm)
10. [https://www.facebook.com/thetraineeclub/posts/-mece-framework-b%C3%AD-k%C3%ADp-kinh-%C4%91i%E1%BB%83n-cho-b%C3%A0i-to%C3%A1n-h%E1%BB%87-th%E1%BB%91ng-th%C3%B4ng-tinmece-%C4%91%E1%BB%8Dc-l%C3%A0-me-s/172975604365716/](https://www.facebook.com/thetraineeclub/posts/-mece-framework-b%C3%AD-k%C3%ADp-kinh-%C4%91i%E1%BB%83n-cho-b%C3%A0i-to%C3%A1n-h%E1%BB%87-th%E1%BB%91ng-th%C3%B4ng-tinmece-%C4%91%E1%BB%8Dc-l%C3%A0-me-s/172975604365716/)