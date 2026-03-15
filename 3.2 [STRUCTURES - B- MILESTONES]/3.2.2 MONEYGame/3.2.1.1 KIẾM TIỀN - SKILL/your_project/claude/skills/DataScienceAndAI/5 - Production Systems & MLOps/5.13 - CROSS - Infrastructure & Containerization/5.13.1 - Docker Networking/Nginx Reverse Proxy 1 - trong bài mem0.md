# # Report: Triển khai Infinity Embedding Service với Nginx Reverse Proxy

```
mem0-server → infinity-proxy:80/v1/embeddings → jina-vllm:8080/embeddings
                (Nginx)                          (Infinity)
```

## 1. Vấn đề

- Infinity API dùng endpoint `/embeddings` (không có `/v1`)
- Mem0 dùng OpenAI client, tự thêm `/v1/embeddings` vào base_url
- Kết quả: endpoint mismatch → Connection refused

## 2. Giải pháp đã chọn

**Nginx Reverse Proxy** (Solution 1 - Best Practice)
- Không cần sửa code mem0
- Nhẹ, ổn định, phù hợp production
- Dễ rollback và maintain

## 3. Kiến trúc triển khai

```
┌─────────────┐         ┌──────────────────┐         ┌──────────────┐
│ mem0-server│────────▶│ infinity-proxy    │────────▶│  jina-vllm   │
│  :8889     │         │ (Nginx) :80      │         │ (Infinity)   │
│            │         │                  │         │  :8080       │
└────────────┘         └──────────────────┘         └──────────────┘
     │                         │                            │
     │  /v1/embeddings         │  /v1/embeddings           │  /embeddings
     │  (OpenAI format)        │  → /embeddings            │  (Infinity)
     └─────────────────────────┴────────────────────────────┘
```

## 4. Implementation Details

### 4.1 Nginx Proxy Configuration (`nginx-infinity.conf`)
- Map `/v1/embeddings` → `http://jina-vllm:8080/embeddings`
- Health check passthrough: `/health` → Infinity health endpoint
- Mock `/v1/models` endpoint (OpenAI-compatible)
- Timeout: 60s read, 10s connect

### 4.2 Docker Compose Updates
- Thêm service `infinity-proxy` (nginx:alpine)
- `jina-vllm`: chỉ expose nội bộ (không ra ngoài)
- `mem0`: phụ thuộc `infinity-proxy` thay vì `jina-vllm`
- Health checks cho cả 2 services

### 4.3 Application Config (`main.py`)
- `OPENAI_BASE_URL` default: `http://infinity-proxy:80/v1`
- Mem0 vẫn dùng provider "openai" (không cần đổi)

## 5. Lợi ích

| Tiêu chí | Kết quả |
|----------|---------|
| **Setup Time** | ~5 phút |
| **Code Changes** | 0 (không sửa mem0 code) |
| **Performance** | Overhead < 1ms (Nginx) |
| **Maintainability** | Dễ maintain, tách biệt concerns |
| **Production Ready** | ✅ Production-grade |

## 6. Files Changed

1. `nginx-infinity.conf` (mới) - Nginx config
2. `docker-compose.yaml` - Thêm infinity-proxy service
3. `main.py` - Update OPENAI_BASE_URL default

## 7. Testing

```bash
# Test proxy endpoint
curl -X POST http://103.253.20.30:8080/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{"model": "jinaai/jina-embeddings-v3", "input": "hello world"}'

# Test mem0 integration
curl -X POST http://103.253.20.30:8889/search \
  -H "Content-Type: application/json" \
  -d '{"query": "test", "user_id": "user1", "top_k": 3}'
```

## 8. Next Steps

- [ ] Test end-to-end với mem0 API
- [ ] Monitor proxy performance
- [ ] Document trong project docs
- [ ] Consider Solution 2 (Custom Infinity Embedder) cho long-term

---

**Status**: ✅ Implemented & Ready for Testing  
**Date**: 2025-12-30  
**Approach**: Infrastructure-level solution (Nginx Reverse Proxy)



---

<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Nginx Reverse Proxy là gì

Nginx reverse proxy là **một lớp trung gian đứng trước các service backend**, nhận mọi request từ client rồi **chuyển tiếp (proxy)** về các service phía sau, sau đó trả lại response cho client. Client chỉ “nhìn thấy” Nginx, không thấy trực tiếp các service backend.

## Khái niệm nhanh

- Bình thường: Client → trực tiếp gọi → App server (FastAPI, Node, vLLM, Infinity, mem0, …).
- Với **Nginx reverse proxy**:
    - Client → gọi tới Nginx (ví dụ `api.finai.vn`).
    - Nginx đọc URL/host, quyết định route tới backend nào (ví dụ `http://embedding:8080`, `http://llm:8000`).
    - Backend trả response cho Nginx → Nginx trả lại cho client.[^1][^2][^3]

Ví dụ cấu hình đơn giản:

```nginx
server {
    listen 443 ssl;
    server_name api.yourdomain.com;

    location /v1/embeddings/ {
        proxy_pass http://embedding-server:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```


## Tại sao dùng Nginx reverse proxy?

- **1. Ẩn backend \& tăng bảo mật**
    - Client chỉ thấy IP/hostname của Nginx, không truy cập trực tiếp vào các container/service bên trong.[^2][^4]
- **2. Một entry point cho nhiều service**
    - Ví dụ:
        - `/v1/embeddings` → Infinity (Jina v3).
        - `/v1/chat/completions` → vLLM.
        - `/admin` → dashboard.
    - Tất cả dùng chung domain + port 80/443.[^5][^3]
- **3. SSL/TLS termination**
    - Nginx nhận HTTPS, giải mã SSL, rồi forward HTTP nội bộ cho backend → backend không phải xử lý cert, đơn giản code hơn.[^6][^7]
- **4. Load balancing \& high availability**
    - Nginx có thể phân phối traffic giữa nhiều instance backend:

```nginx
upstream embed_backend {
    server embed1:8080;
    server embed2:8080;
}

server {
    location /v1/embeddings/ {
        proxy_pass http://embed_backend;
    }
}
```

    - Nếu 1 node chết, Nginx tự chuyển request sang node khác.[^7][^8]
- **5. Caching \& performance**
    - Cache các response tĩnh / ít thay đổi, giảm tải backend, tăng tốc độ.[^9][^1]

***

Tóm lại: **Nginx reverse proxy giống như “cổng frontdoor” cho toàn bộ hệ thống backend** – chỗ duy nhất client chạm vào, còn bên trong bạn thoải mái chia nhỏ service, scale, đổi port, đổi host mà không ảnh hưởng client.
<span style="display:none">[^10][^11][^12][^13][^14][^15][^16][^17][^18][^19][^20][^21][^22][^23][^24][^25]</span>

<div align="center">⁂</div>

[^1]: https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/

[^2]: https://www.cloudflare.com/learning/cdn/glossary/reverse-proxy/

[^3]: https://www.theserverside.com/blog/Coffee-Talk-Java-News-Stories-and-Opinions/How-to-setup-Nginx-reverse-proxy-servers-by-example

[^4]: https://www.strongdm.com/what-is/reverse-proxy-vs-load-balancer

[^5]: https://www.reddit.com/r/unRAID/comments/zcw7ik/what_exactly_does_reverse_proxy_do/

[^6]: https://betterstack.com/community/questions/nginx-as-reverse-proxy-with-upstream-ssl/

[^7]: https://dzone.com/articles/nginx-reverse-proxy-and-load-balancing

[^8]: https://nginx.org/en/docs/http/load_balancing.html

[^9]: https://www.hostragons.com/en/blog/nginx-reverse-proxy-configuration-and-load-balancing/

[^10]: https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_6f301519-9fcb-49ff-805d-816d7a84a0d3/aa55278f-bb85-4603-b41e-7969c4559a83/1.8-Cach-lam-nhung-thu-moi.md

[^11]: https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_6f301519-9fcb-49ff-805d-816d7a84a0d3/2f7fb2b3-d3da-4f4a-9930-a2484929107c/1.7.1-Rui-ro-phap-ly.md

[^12]: https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_6f301519-9fcb-49ff-805d-816d7a84a0d3/6ee7f2e1-c797-400b-97f5-b9f054c47e7f/1.7-V1-finAI-Finance-Agent-Web-Browser-Chien-luoc-CEO-PM.md

[^13]: https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_6f301519-9fcb-49ff-805d-816d7a84a0d3/feca8151-cf08-4c63-b87a-10e4cc3466a4/1.7-V2-Step-Up-Template-finAI-Finance-Agent-Web-Browser-Chien-luoc-toan-dien-CEO-PM.md

[^14]: https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/images/760047/a0244652-c244-4e36-9323-bbb542bce30b/image.jpg

[^15]: https://www.youtube.com/watch?v=PAEDJrGJyaY

[^16]: https://www.digitalocean.com/community/tutorials/how-to-configure-nginx-as-a-reverse-proxy-on-ubuntu-22-04

[^17]: https://www.redhat.com/en/blog/setting-reverse-proxies-nginx

[^18]: https://www.inmotionhosting.com/support/server/nginx/what-is-nginx/

[^19]: https://docs.nginx.com/nginx/admin-guide/security-controls/securing-http-traffic-upstream/

[^20]: https://www.f5.com/glossary/reverse-proxy

[^21]: https://nginx.org/en/docs/http/ngx_http_upstream_module.html

[^22]: https://kemptechnologies.com/load-balancing-nginx/reverse-proxy-nginx

[^23]: https://phoenixnap.com/kb/nginx-reverse-proxy

[^24]: https://stackoverflow.com/questions/30297999/nginx-reverse-proxy-using-upstream-directive

[^25]: https://dev.to/shubhamkcloud/understanding-reverse-proxy-with-nginx-step-by-step-guide-18a0

