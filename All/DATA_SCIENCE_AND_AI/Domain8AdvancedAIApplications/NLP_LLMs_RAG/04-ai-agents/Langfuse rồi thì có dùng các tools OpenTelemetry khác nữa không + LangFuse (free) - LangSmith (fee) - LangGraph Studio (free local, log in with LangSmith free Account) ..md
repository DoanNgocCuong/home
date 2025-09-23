Trong lúc làm, với con mắt của 1 lính mới. Em đi hỏi và hỏi: hỏi người anh trong công ty, hỏi các sếp trong Discord FSDS, hỏi AI. 

Và 1 vài summary lại. 

---

# 1. Dùng Langfuse rồi thì có dùng các tools OpenTelemetry khác nữa không?

┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐  
│   Application   │───▶│  OpenTelemetry   │───▶│  Export & Store│  
│  (AI Robot) │   │    |   (Collector)    │    │                 │  
└─────────────────┘    └──────────────────┘    └─────────────────┘  
                                │  
                    ┌───────────┼───────────┐  
                    ▼           ▼           ▼  
            ┌───────────┐ ┌──────────┐ ┌──────────┐  
            │  Metrics  │ │   Logs   │ │  Traces  │  
            │Prometheus │ │ELK Stack │ │ Jaeger   │  
            └─────┬─────┘ └────┬─────┘ └────┬─────┘  
                  ▼            ▼            ▼  
            ┌──────────┐ ┌──────────┐ ┌──────────┐  
            │ Grafana  │ │  Kibana  │ │ Jaeger   │  
            │Dashboard │ │Dashboard │ │   UI     │  
            └──────────┘ └──────────┘ └──────────┘  
  
# 2. LangFuse (free) - LangSmith (fee) - LangGraph Studio (free local).

- Trong lúc làm, em tình cờ thấy cái: UI Graph nó được hiển thị trên LangSmith (fee) bằng lệnh `langgraph dev` trong khi LangFuse lại không có, LangSmith thì lại mất tiền :3 

Tìm hiểu ra mới biết: hoàn toàn có thể dùng: LangFuse + LangGraph Studio (free) hoàn toàn với UI trên LangSmith nhưng không mất tiền. :D

- **LangGraph Studio** (FREE) = Visual + UI testing  - cần log in vào **LangSmith Free Account** 
- **Langfuse** (FREE self-host) = Production monitoring
- **LangSmith** (PAID) = Advanced evaluation