# MINDGame — MASTER MAP

> Hệ thống phát triển bản thân của Đoàn Ngọc Cường
> Cập nhật: 15/03/2026

---

## TỔNG QUAN CẤU TRÚC

```
MINDGame/
│
├── 01-NHẤT HƯỚNG/              ← Triết lý cốt lõi + Tu tập
│   ├── P1 (Tâm Lý Học 6 Góc)        ← cần copy thủ công
│   ├── P2 (THE ROAD + Mental Models)  ← cần copy thủ công
│   ├── P3 (Tứ Niệm Xứ + Networking)  ← cần copy thủ công
│   ├── GOSINGA/ (sách PDF + đúc kết pháp)
│   └── Tứ-Niệm-Xứ/ (thực hành)
│
├── 02-TÂM TRÍ-MINDSET/        ← Inner Game (12 files ✓)
│   ├── Nỗi-Sợ-Niềm-Tin-Giới-Hạn/
│   ├── Mental-Models/ (Munger, Tư duy hệ thống)
│   ├── Coaching-Tâm-Lý-Học/ (NLP, Coach Mai Anh) + CKP/
│   └── Growth-Mindset-10x/ (10x>2x, Dan Koe, Wecommit)
│
├── 03-PROBLEM SOLVING & LEARNING/ ← Framework + Phương pháp (26 files ✓)
│   ├── Problem-Solving-Framework/ (Mô hình 6 tầng)
│   ├── Decision-Making/ (Bí Ngô, IMPORTANT)
│   ├── PP-Học-Tập/ (Thiên tài, Ultralearning, Context Eng)
│   └── Habits-Time-Productivity/ (4000 Weeks, Goggins, Habits)
│
├── 04-CAREER-TIỀN/             ← Sự nghiệp + Tài chính (6 files + cần bổ sung)
│   ├── Career-Strategy/
│   ├── Tiền-Bạc/
│   └── Networking-Người/
│
├── NHẬT KÝ/                    ← (171 files ✓)
│   ├── 2025/ (theo tháng 03→12)
│   └── 2026/ (merged từ DailyNote)
│
├── SHARING/                    ← (4 files ✓)
│
├── NOTE-TECH/                  ← Đã phân bổ vào DataScienceAndAI, cần xóa
│
└── 0_CKP/                     ← Archive (6 files ✓)
```

---

## NOTE-TECH ĐÃ PHÂN BỔ VÀO DataScienceAndAI

| File | → Đích trong DataScienceAndAI |
|------|-------------------------------|
| System Design - Youtube Mini | 2 - SDD/ |
| Lập trình song song C | 2 - SDD/06-PROGRAMMING-FUNDAMENTALS/ |
| CI CD | 5 - Production/5.04 - BUILD - Deployment & CI-CD/ |
| Docker | 5 - Production/5.13 - CROSS - Infrastructure/ |
| Cloud | 5 - Production/5.13 - CROSS - Infrastructure/ |
| GKE Hackathon | 5 - Production/5.13 - CROSS - Infrastructure/ |
| Kiểm tra port/log | 5 - Production/5.08 - RUN - Observability/ |
| Response time debug | 5 - Production/5.08 - RUN - Observability/ |
| MAX WORKS Threading | 5 - Production/5.16 - SPECIALIZED - Performance/ |
| Bash Scripts/Airflow | 5 - Production/5.15 - SPECIALIZED - MLOps/ |
| FastAPI | 5 - Production/5.02 - DESIGN - API Design/ |
| DevOps Group + Khoá | 5 - Production/5.04 - BUILD - Deployment/ |
| FSDS course notes (5 files) | DataScienceAndAI/CKP/ |

Non-tech files đã redirect về MINDGame: Meditation → 01, Wecommit Mindset → 02, Career/Networking → 04, FB posts → SHARING

---

## CẦN LÀM THỦ CÔNG TRÊN WINDOWS

### Bước 1: Copy files vào 01-NHẤT HƯỚNG (bị mất do overlay)

Từ `0. NHẤT HƯỚNG\` (folder cũ trên Windows):
```
copy  1.MD         → 01-NHẤT HƯỚNG\P1-Tâm-Lý-Học-6-Góc.md
copy  2.mD         → 01-NHẤT HƯỚNG\P2-THE-ROAD-Mental-Models.md
copy  3.md         → 01-NHẤT HƯỚNG\P3-Tứ-Niệm-Xứ-Networking.md
copy  Vọc.md       → 01-NHẤT HƯỚNG\Vọc.md
```

Từ `NOTE\1.2 Đã đúc kết...\Đoàn Ngọc Cường...\`:
```
copy  1_Nhất Hướng - Lark.md   → 01-NHẤT HƯỚNG\Nhất-Hướng-Lark.md
copy  GOSINGA\*                 → 01-NHẤT HƯỚNG\GOSINGA\
```

Từ `NOTE\1.2 Đoàn Ngọc Cường - CKP...\`:
```
copy  "2. NGOẠI LỰC...TỨ NIỆM XỨ...md"  → 01-NHẤT HƯỚNG\Tứ-Niệm-Xứ\
```

### Bước 2: Bổ sung files vào 02-TÂM TRÍ-MINDSET (từ NOTE đã mất)

Từ `NOTE\1.1 Đang Nghiên Cứu\`:
```
copy  "20-11-2025 CHARLIE MUNGERS MENTAL MODELS.md"  → 02-TÂM TRÍ-MINDSET\Mental-Models\
```

Từ `NOTE\1.1 Đang Không Nghiên Cứu\`:
```
copy  "2025 - 08 - 31 DOPAMINE..."     → 02-TÂM TRÍ-MINDSET\Nỗi-Sợ-Niềm-Tin-Giới-Hạn\
copy  "2025-08-24 Chế độ sinh tồn.md"  → 02-TÂM TRÍ-MINDSET\Nỗi-Sợ-Niềm-Tin-Giới-Hạn\
copy  "2025-10-04 Não.md"              → 02-TÂM TRÍ-MINDSET\Mental-Models\
copy  "6 TƯ DUY CỦA MỘT SENIOR.md"    → 02-TÂM TRÍ-MINDSET\Growth-Mindset-10x\
copy  "2025-08-29 Bất công...game.md"  → 02-TÂM TRÍ-MINDSET\Growth-Mindset-10x\
```

### Bước 3: Bổ sung files vào 04-CAREER-TIỀN (từ NOTE đã mất)

Từ `NOTE\1.1 Đang Không NC\`:
```
copy  "-7. Chiến lược Job nước ngoài.md"            → 04-CAREER-TIỀN\Career-Strategy\
copy  "2. NGHIÊN CỨU XU HƯỚNG..."                   → 04-CAREER-TIỀN\Career-Strategy\
copy  "2. DANH SÁCH TOÀN DIỆN CÔNG TY FINTECH..."   → 04-CAREER-TIỀN\Career-Strategy\
copy  "3. Product Engineering..."                    → 04-CAREER-TIỀN\Career-Strategy\
copy  "2025-08-24 Naval Ravikant.md"                 → 04-CAREER-TIỀN\Career-Strategy\
copy  "2025_08_24 Walter Isaacson..."                → 04-CAREER-TIỀN\Career-Strategy\
```

Từ `NOTE\1.2 Đoàn Ngọc Cường - CKP...\`:
```
copy  "1. Cuối 2024..."                             → 04-CAREER-TIỀN\Career-Strategy\
copy  "7. Định nghĩa về Finance..."                 → 04-CAREER-TIỀN\Tiền-Bạc\
copy  "7_1. Từ AI đến Investor..."                  → 04-CAREER-TIỀN\Tiền-Bạc\
copy  "7_2. Edu và Fin.md"                          → 04-CAREER-TIỀN\Tiền-Bạc\
copy  "7_3. Phản biện...Domain.md"                  → 04-CAREER-TIỀN\Tiền-Bạc\
```

Từ `NOTE\1.2 Đã đúc kết...\Đoàn Ngọc Cường...\`:
```
copy  "ROADMAP FIRE 15 NĂM..."                      → 04-CAREER-TIỀN\Tiền-Bạc\
copy  "3.2 Chiến Lược Bí Ngô..."                    → (đã có trong 03-PROBLEM SOLVING)
```

Từ `NOTE\3_Networking\`:
```
copy  *                                              → 04-CAREER-TIỀN\Networking-Người\
```

Từ `NOTE\1. DailyNote\1.2 Tính theo Dự Án\`:
```
copy  *                                              → 04-CAREER-TIỀN\Career-Strategy\
```

### Bước 4: Xóa folders cũ

Sau khi copy xong, xóa:
1. `0. NHẤT HƯỚNG\`
2. `3.2 NỖI SỢ, NIỀM TIN GIỚI HẠN, MINDSET SAI TRONG TÂM TRÍ\`
3. `NOTE\` (toàn bộ)
4. `NOTE-TECH\` (đã phân bổ hết)
5. Loose files: `TIỀN BẠC TRONG TÂM TRÍ.md`, `Cách xin nghỉ...md`, `Điểm đi chơi.md`
