# vLLM Production Stack - Reference Stack cho Production

## Tổng quan

**vLLM Production Stack** là một hệ thống tham chiếu (reference stack) được xây dựng trên nền tảng vLLM, giúp bạn triển khai các mô hình ngôn ngữ lớn (LLM) ở quy mô production.

## Tính năng chính

Hệ thống này cho phép bạn:

- **Scale linh hoạt**: Mở rộng từ một instance vLLM đơn lẻ lên hệ thống phân tán mà không cần thay đổi code ứng dụng
- **Giám sát toàn diện**: Theo dõi metrics qua dashboard Grafana với các thông số như latency, TTFT (Time-to-First-Token), GPU KV cache usage
- **Tối ưu hiệu năng**: Hưởng lợi từ request routing thông minh và KV cache offloading

## Kiến trúc hệ thống

Stack được triển khai qua Helm và bao gồm:

- **Serving engine**: Các vLLM engines chạy các LLM khác nhau
- **Request router**: Điều hướng requests tới backends phù hợp dựa trên routing keys hoặc session IDs để tối đa hóa KV cache reuse
- **Observability stack**: Giám sát metrics qua Prometheus + Grafana

## Phù hợp với profile AI Engineering

Với background AI Engineering về NLP, LLMs, RAG và MLOps, đây là một công cụ rất hữu ích để:

- Triển khai LLM production trên Kubernetes (liên quan đến Docker, system design)
- Scale hệ thống AI từ prototype lên production
- Tích hợp vào các dự án RAG và AI Agents

## Tài liệu và Tutorials

Repository này cung cấp các [tutorials chi tiết](https://github.com/vllm-project/production-stack/tree/main/tutorials) về cách triển khai trên các cloud platforms như:

- AWS EKS
- GCP
- Lambda Labs

Rất hữu ích cho định hướng fintech và startup.

## Liên kết

- **Repository chính**: [vllm-project/production-stack](https://github.com/vllm-project/production-stack)
- **Fork tham khảo**: [DoanNgocCuong/vLLM-Production-Stack---production-stack](https://github.com/DoanNgocCuong/vLLM-Production-Stack---production-stack)

## Mối liên hệ với các chủ đề khác

- **Domain 6 - Production Systems & MLOps**: Model deployment, orchestration, monitoring
- **Domain 8 - Advanced AI Applications**: LLM serving, RAG systems, AI Agents
- **Kubernetes & Containerization**: Helm charts, container orchestration
- **Observability**: Prometheus, Grafana, metrics collection

