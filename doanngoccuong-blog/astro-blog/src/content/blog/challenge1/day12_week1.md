---
title: "Buổi 1: FastAPI + Docker Compose"
description: "Học cách triển khai dịch vụ backend cơ bản với FastAPI và Docker Compose."
pubDate: "2026-03-02"
updatedDate: "2026-03-03"
tags: ["FastAPI", "Docker", "Backend", "challenge-1"]
---

# 🚀 BUỔI 1: FASTAPI + DOCKER COMPOSE — Production Service Foundation

**Deadline nộp:** **Thứ 3, 11:59PM** — 
Ae nộp bài dưới bài đăng này nhé
-----

## 1. Tầm quan trọng
- Ngày 1, mình muốn anh chị em tập trung vào 2 kỹ năng căn bản của AI Engineer nói riêng và Engineer nói chung: bảo gồm 'Viết API' và 'Đóng Gói Docker'


### FastAPI — Backend Framework #1 cho Python AI

**Tại sao quan trọng?**
Hầu hết các dự án Python và AI hiện nay sử dụng FastAPI do ba lợi thế cốt lõi: async native, tự động sinh Swagger docs tại `/docs`, và Pydantic validation tích hợp sẵn.

Trước đây, khi mới bắt đầu với Flask, việc cấu hình CORS thủ công, tự viết tài liệu API dạng HTML, và validate request bằng chuỗi if-else là điều bình thường. Sau khi chuyển sang FastAPI, chỉ cần chạy `uvicorn main:app` là hiển thị Swagger UI như Swagger trong hệ sinh thái JavaScript nhưng được tối ưu tốt hơn cho Python.

### Docker + Docker Compose — Đóng Gói Production

**Tại sao quan trọng?**
Sau khi hoàn thiện code, việc chuyển giao cho thành viên khác hoặc deploy lên server chỉ cần một lệnh `docker-compose up` — không lo sai lệch môi trường, không mất thời gian debug dependency. *Build once, run everywhere.*
Câu quen thuộc ae sẽ được nghe: Đã đóng docker chưa.

Khi push repo lên mà không có Docker, các câu hỏi thường gặp là: “Python version nào?”, “pip install lỗi?”, “DB config thế nào?”. Docker Compose giải quyết toàn bộ — clone + up là chạy được ngay. -----

## 2. Sai Lầm Phổ Biến — Bảng Chi Tiết

|#|Sai lầm                                                                      |Ví dụ code sai / config sai                                                                                                                    |Hậu quả thực tế (khi deploy)                                                                                                                                                                                                                           |Cách sửa đúng trong buổi 1                                                                                                                                                                                                                                   |Dẫn chứng                                                                                                                           |
|-|-----------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
|1|**Dùng `python:latest` làm base image**                                      |`FROM python:latest` trong Dockerfile, không chỉ định version, không dùng bản slim                                                             |Image build ra nặng ~1–1.2GB, thời gian build có thể 5–10 phút. Khi push lên registry hoặc chạy CI/CD (GitHub Actions, Render…), pipeline dễ timeout, tốn băng thông và storage. Việc debug trở nên chậm vì mỗi lần chỉnh sửa là phải build lại từ đầu.|Chỉ định bản **cụ thể + slim**: `FROM python:3.11-slim AS builder` cho stage build, sau đó `FROM python:3.11-slim` cho runtime. Kết hợp multi-stage build để image cuối chỉ chứa runtime cần thiết, giảm size xuống ~150–250MB.                              |[Docker Python Official Images](https://hub.docker.com/_/python) — so sánh kích thước `latest` vs `3.11-slim`.                      |
|2|**Không có `.dockerignore`**                                                 |Không tạo file `.dockerignore`, hoặc file rỗng → toàn bộ thư mục (kể cả `.git/`, `.venv/`, `__pycache__/`, file nặng) bị đưa vào build context.|Build context phình to 300–800MB+, mỗi lần `docker build` là copy lượng dữ liệu lớn. Thời gian build kéo dài, CI/CD chậm, ảnh hưởng trực tiếp đến năng suất của cả team.                                                                               |Tạo `.dockerignore` với các mục cơ bản: `__pycache__/`, `*.pyc`, `.git/`, `.venv/`, `node_modules/`, file data nặng. Kiểm tra lại bằng `docker build` để xác nhận build context đã giảm đáng kể.                                                             |[Docker docs — dockerignore](https://docs.docker.com/build/context/#dockerignore-files).                                            |
|3|**Hardcode connection string / password trong code**                         |Trong code: `DB_URL = "postgresql://user:password@localhost:5432/mydb"` hoặc viết thẳng user/pass trong `settings.py`.                         |Commit lên GitHub → password xuất hiện trên public repo. Các công cụ scan secrets (GitHub, security scanner) sẽ flag lỗi. Trong môi trường thực tế, đây là vấn đề bảo mật nghiêm trọng — có thể phải rotate toàn bộ credential.                        |Đưa toàn bộ secret vào **environment variables**. Trong `docker-compose.yml` cấu hình: `DATABASE_URL=postgresql://user:${POSTGRES_PASSWORD}@db:5432/mydb`. Trong code, đọc bằng `os.getenv("DATABASE_URL")`. Không commit file `.env` (đưa vào `.gitignore`).|[Render community thread về env vars](https://community.render.com/t/trouble-deploying-fastapi-app/26721).                          |
|4|**Không cấu hình healthcheck cho PostgreSQL, chỉ dùng `depends_on` mặc định**|`depends_on: - db` mà không có `healthcheck` và `condition: service_healthy`.                                                                  |Docker Compose sẽ khởi động API ngay khi container DB *bắt đầu chạy*, nhưng PostgreSQL chưa sẵn sàng nhận connection. Kết quả: FastAPI connect lần đầu bị `Connection refused`, app crash hoặc phải retry liên tục.                                    |Thêm `healthcheck` cho service `db` (dùng `pg_isready`) và cấu hình `depends_on` theo dạng: `db: { condition: service_healthy }`. Container API chỉ khởi động sau khi DB báo healthy.                                                                        |[StackOverflow — Unable to start FastAPI server with PostgreSQL using docker-compose](https://stackoverflow.com/questions/69381579).|
|5|**Nhét toàn bộ logic vào 1 file `main.py` (monolith)**                       |`main.py` chứa tất cả: khởi tạo app, router, Pydantic model, business logic, DB connection… thường dài 300–500 dòng.                           |Ban đầu chạy được, nhưng sau 1–2 tuần mở rộng là bắt đầu rối. Khó test, khó đọc, khó refactor. Trong buổi phỏng vấn kỹ thuật, cấu trúc repo kiểu này cho thấy thiếu kinh nghiệm tổ chức code production.                                               |Tách cấu trúc theo FastAPI best practice: `app/main.py` (khởi tạo app), `app/routers/api.py` (endpoints), `app/models/schemas.py` (Pydantic models), `app/services/` (business logic). Code rõ ràng, dễ mở rộng, đúng với tài liệu chính thức.               |[FastAPI — Bigger Applications, Multiple Files](https://fastapi.tiangolo.com/tutorial/bigger-applications/).                        |
|6|**Không dùng Pydantic để validate input/output**                             |Định nghĩa endpoint nhận `dict` rồi tự kiểm tra bằng `if 'text' not in ...`; không khai báo model rõ ràng.                                     |Với dữ liệu không hợp lệ (ví dụ: `{}` hoặc `{"text": null}`), code ném `KeyError` hoặc `TypeError`, trả về lỗi 500 không có giải thích. Log khó đọc, người dùng API không biết mình sai ở đâu.                                                         |Khai báo rõ ràng request/response bằng Pydantic: `class ItemRequest(BaseModel): text: str`. FastAPI tự validate và trả 422 kèm message chi tiết khi input thiếu hoặc sai type. Output cũng nên dùng model để đảm bảo schema nhất quán.                       |[FastAPI — Request Body](https://fastapi.tiangolo.com/tutorial/body/).                                                              |
|7|**Cấu hình CORS wildcard `allow_origins=["*"]` trong production**            |Trong app: `allow_origins=["*"]` vì “cho tiện test front-end”.                                                                                 |Ở môi trường production, bất kỳ origin nào cũng có thể gọi API. Các công cụ security scan thường đánh giá mức độ **high risk**. Một số tổ chức có policy từ chối service có CORS `*`.                                                                  |Chỉ cho phép origin cụ thể: `["http://localhost:3000"]` cho môi trường dev. Khi lên production, cấu hình domain rõ ràng, ví dụ: `["https://frontend.mydomain.com"]`.                                                                                         |[FastAPI — CORS docs](https://fastapi.tiangolo.com/tutorial/cors/).                                                                 |
|8|**Chạy container với user root**                                             |Không set `USER`, để mặc định root trong Dockerfile.                                                                                           |Security scan sẽ báo lỗi “container running as root”. Nếu có lỗ hổng trong ứng dụng, attacker có thể lợi dụng quyền root trong container. Một số nền tảng (Kubernetes cluster với hardened policy) từ chối chạy container root.                        |Tạo user không phải root và chuyển sang user đó: `RUN useradd -m aiuser && chown -R aiuser /app` rồi `USER aiuser`. Quyền trong container bị giới hạn, giảm đáng kể bề mặt tấn công.                                                                         |[Docker best practices / FastAPI in Docker](https://fastapi.tiangolo.com/deployment/docker/).                                       |


Cấu trúc thư mục best practices ( anh sẽ gửi sau, đang bị hỏng sạc laptop phải dùng IPad soạnbài) 

----
### Yêu Cầu Kỹ Thuật Bắt Buộc


> **Lưu ý:** Không có hướng dẫn code chi tiết — các bạn tự implement, có thể sử dụng AI hoặc tham khảo tài liệu chính thức. Output bao gồm **1 video quay màn hình ~5 phút** trình bày toàn bộ demo. Các bạn chấm điểm theo vòng tròn.

-----

## 3. Hướng dẫn làm bài tập

Cấu trúc thư mục tham khảo
```
ai-service/                          # Tên repo tự đặt
├── app/                             # Toàn bộ FastAPI code
│   ├── __init__.py                  # File rỗng: touch __init__.py
│   ├── main.py                      # FastAPI app + include routers
│   ├── routers/
│   │   └── api.py                   # 3 endpoints theo đề bài
│   ├── models/
│   │   └── schemas.py               # Request/Response BaseModel
│   └── services/
│       └── core.py                  # Business logic
├── docker/
│   ├── Dockerfile                   # Multi-stage build
│   └── docker-compose.yml           # FastAPI + PostgreSQL
├── utils/                           # vài ảnh dẫn chứng làmìnhđãchạy thành công, ví dụ) 
│   ├── 1-swagger-docs.png           # Screenshot localhost:8000/docs
│   ├── 2-health-curl.png            # curl /health → JSON OK
│   ├── 3-post-success.png           # curl POST endpoint-1 success
│   ├── 4-bad-input.png              # curl bad input → 422 error
… tùy ae
├── requirements.txt                 # fastapi uvicorn pydantic numpy
├── .dockerignore                    # Tối thiểu 8 dòng ignore
└── AVOIDANCE_TABLE.md               # Proof tránh ≥ 6/8 lỗi
```

-----
- **3 endpoints** theo đề bài — Swagger `/docs` hiển thị đầy đủ, rõ ràng
- **Pydantic validation** cho input (max_length, required fields)
- **HTTPException 422** trả về khi input không hợp lệ
- **Docker Compose** với 2 services (api + db) — cả hai healthy


## 4. Output Nộp Bắt Buộc — 4 Output 

Hoàn thành đủ 4 output dưới đây là hoàn thành bài. Deadline: **Thứ 3, 11:59PM**.

### Output 1: Chọn Đề Để Thực Hành & Push Code GitHub Public (sau mang đi phỏng vấn show được) + ĐẶT TÊN THEO FORMAT: "... - challenge1-weaction" để dễ nhận diện nhau + đầy đủ với README.md
+, docs/RUNBOOK.md Trong Repo ghi rõ các sai lầm đã tránh được

Ví dụ: github/DoanNgocCuong/fastapi_dockercompose_challenge1_weaction.git


Tự chọn 1 chủ đề (có thể nhờ AI gợi ý nếu chưa có ý tưởng), hoặc tham khảo 5 đề AI Engineer thực tế dưới đây:

1. **Đóng gói mô hình AI local thành API**: Sau khi train mô hình classification (HuggingFace), wrap thành `POST /predict(text)` → trả về tags/probability. Lưu kết quả vào DB để tracking.
1. **Proxy & cache API bên thứ ba**: Nhận request từ OpenAI/Groq → FastAPI cache kết quả vào Postgres + rate limiting. `GET /chat/cached/{id}` trả về kết quả đã cache.
1. **AI Agent tool wrapper service**: Đóng gói backend DB query thành tool cho LangChain agent: `POST /agent-tool(query)` → thực thi SQL an toàn + trả về JSON result.
1. **RAG pipeline mini-API**: Embed text → lưu vector DB (mock Postgres). `POST /rag-query` → retrieve context + mock LLM answer.
1. **MLOps inference server**: Deploy fine-tuned model → `POST /infer(image/text)`. Scale với uvicorn workers, có healthcheck kiểm tra model loaded.

Implement **3 endpoints** (POST create/use, GET result, /health) + Pydantic + Postgres + Docker theo đúng best practice. Push lên **GitHub public** (đặt tên `ai-service-[ten-ban]`), đảm bảo `docker-compose up` chạy thành công.




-----

### Output 2: AVOIDANCE_TABLE.md Trong Repo

File Markdown **chứng minh đã tránh≥cáclỗitrong8lỗi ** trong bảng ở mục 2. Mỗi lỗi cần có: mô tả cách xử lý + **Ví dụ formatngắngọn :**

```maảkdown
Tôi đã tránh các lỗi thường gặp. ….
(Tùy ae viết file) 
**Lỗi #1 — Base image**: Sử dụng python:3.11-slim với multi-stage build → image cuối 180MB (xem utils/6-docker-images.png).

**Lỗi #3 — Hardcode secrets**: DB_URL đọc từ os.getenv(), biến môi trường inject qua docker-compose.

Snippet docker-compose.yml:
[paste code tại đây]
```

-----

### Output 3: Video Demo ~5 Phút (YouTubeDemo)

Quay **live màn hình**, trình bày theo thứ tự:

1. Giới thiệu đề bài đã chọn và lý do chọn (liên hệ thực tế công việc AI Engineer).
1. Clone repo → `docker-compose up` → `docker ps` → `curl POST` endpoint chính → test 422 bad input qua `/docs`, mở swagger 

2. Giải thích cách tổ chức routers theo folder (tránh monolith) và cấu hình healthcheck cho DB (tránh lỗi kết nối khi khởi động).

Nộp **link GitHub + link YouTube unlisted** lên /Facebook dưới bài đăng

-----

### Output 4: Review Vòng Tròn

Quy trình: **Người 1 review Người 2, Người 2 review Người 3, … người cuối review Người 1**.

Nội dung comment cần kiểm tra:

- GitHub link có public không?
- `AVOIDANCE_TABLE.md` đủ chưa không?
- Video đã upload chưa?
- `docker-compose up` chạy thành công không?
- Sau đó điền link Github và Video của đồng đội vào đây: https://docs.google.com/spreadsheets/d/18RGv8EJW-A-2yWYV2y0-9oiWEXVt-r2GW1qTXJ_GF6k/edit?gid=22262218#gid=22262218

Nhắc nhở thành viên chưa nộp → tag anh nếu cần. Sau khi hoàn thành báo cáo “review done”.

### Output 5
Ace điền giúp Cường form feedback này để Cường hỗ trợ ace tốt nhất nhé. Thanks: [https://forms.gle/pHYsYKELCFptRKN9A](https://forms.gle/pHYsYKELCFptRKN9A)

-----

> **4 output hoàn thành = bài nộp đạt chuẩn.** Repo chạy thực tế, bảng tránh lỗi chứng minh tư duy kỹ thuật, video là tài liệu CV có giá trị thực.

** Hoàn thành buổi 1 là nền tảng vững chắc cho lộ trình AI Engineering.
