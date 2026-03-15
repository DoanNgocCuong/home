```
đóng gói lại thành 1 tài liệu tên là SKILL.md cho việc triển khai cái X_API_KEY với alert này ko nhỉ :  file đều có: Overview → Core Principles → Best Practices (What/Why/How/Anti-pattern) → Decision Frameworks → Checklist → Common Mistakes → Tools & References. Code examples thực tế (Python, Docker, Terraform, K8s).
```




---



# Ví dụ 1 

```
Ở mỗi folder trong 20 folders 
1. Cậu deep research về domain đó, SKILL domain đó, dùng những cái đã được đóng gói và dùng cho các agents từ các repo lớn mọi người chia sẻ về SKILL agent
2. mỗi folder tạo 1 file SKILL.md nhé 
3. DEEP RESEARCH ĐỂ TẠO RA   MỖI FILE SKILL.md đều là BEST PRACTICES
```

Đây là task lớn — 20 file SKILL.md, mỗi file cần deep research. Tớ triển song song cho nhanh:

**Used 5 tools, updated todo list, ran a command**

Used 5 tools, updated todo list, ran a command

Done bro. **20/20 SKILL.md** đã tạo xong, tổng cộng **~11,000 dòng, ~380KB** knowledge base:

| Group                 | Domain                 | Lines | Nội dung chính                                        |
| --------------------- | ---------------------- | ----- | ------------------------------------------------------- |
| **DESIGN**      | 5.01 Architecture      | 448   | Clean Architecture, DDD, 12-Factor, Scalability         |
|                       | 5.02 API Design        | 788   | REST/GraphQL/gRPC, Pagination, Versioning, Stripe-style |
|                       | 5.03 Database          | 780   | PostgreSQL, Indexing, Connection Pooling, Sharding      |
| **BUILD**       | 5.04 Deployment        | 848   | Blue-green, Canary, Feature Flags, GitHub Actions       |
|                       | 5.05 Testing           | 979   | Test Pyramid, Contract Testing, Locust, Chaos           |
|                       | 5.06 Code Quality      | 1,221 | Clean Code, SonarQube, Refactoring, CODEOWNERS          |
| **RUN**         | 5.07 Reliability       | 341   | Circuit Breaker, Retry, Timeout, Error Budgets          |
|                       | 5.08 Observability     | 404   | Logs/Metrics/Traces, Langfuse, OpenTelemetry            |
|                       | 5.09 Error Handling    | 476   | RFC 7807, Dead Letter Queue, Saga Pattern               |
|                       | 5.10 Prod Readiness    | 589   | PRR Checklist, On-call, Google SRE Book                 |
| **CROSS**       | 5.11 Security          | 275   | OWASP, OAuth2, Secret Management, mTLS                  |
|                       | 5.12 Config & Secrets  | 383   | Vault, 12-Factor, Secret Rotation, Feature Flags        |
|                       | 5.13 Infrastructure    | 536   | Docker Best Practices, Terraform, K8s, Nginx            |
|                       | 5.14 Documentation     | 627   | ADR, Runbooks, Mermaid, Postmortem Templates            |
| **SPECIALIZED** | 5.15 MLOps             | 437   | vLLM, MLflow, Langfuse, RAG, Guardrails                 |
|                       | 5.16 Caching           | 508   | Redis, CDN, Cache Stampede, N+1 Query                   |
|                       | 5.17 Async/MQ          | 622   | RabbitMQ vs Kafka, DLQ, Saga, Stream Processing         |
|                       | 5.18 Compliance        | 793   | GDPR, PII, SOC 2, Data Breach Response                  |
|                       | 5.19 Chaos Engineering | 758   | Chaos Monkey, Game Days, Failure Injection              |
|                       | 5.20 Cost Optimization | 1,179 | FinOps, Right-sizing, Spot Instances, Tagging           |

Mỗi file đều có: Overview → Core Principles → Best Practices (What/Why/How/Anti-pattern) → Decision Frameworks → Checklist → Common Mistakes → Tools & References. Code examples thực tế (Python, Docker, Terraform, K8s).



---



# Ví dụ 2 Đã tạo tài liệu SKILL tại: `.claude/skills/api-key-auth/SKILL.md`

```
Có thể giúp mình đóng gói lại thành 1 tài liệu tên là SKILL.md cho việc triển khai cái X_API_KEY với alert này ko nhỉ :  file đều có: Overview → Core Principles → Best Practices (What/Why/How/Anti-pattern) → Decision Frameworks → Checklist → Common Mistakes → Tools & References. Code examples thực tế (Python, Docker, Terraform, K8s).
```

Nội dung bao gồm:

* **Overview** : Giới thiệu về API Key Auth
* **Core Principles** : Các nguyên tắc cốt lõi
* **Best Practices (What/Why/How/Anti-pattern)** :
* API Key Middleware Pattern
* Toggle Environment Pattern
* Security Alert Integration
* **Decision Frameworks** : Khi nào dùng API Key vs OAuth2/JWT
* **Checklist** : Implementation, Security, Monitoring, Testing
* **Common Mistakes** : 4 lỗi thường gặp (Circular Import, Hardcode, etc.)
* **Tools & References** : Code files, env vars, testing commands
* **Quick Reference Card** : Summary dạng card
