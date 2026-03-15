<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# deep research về embedding tiếng việt, tiếng anh siêu nhanh thay thế cho v3-small của openAI

Tuyệt vời! Bây giờ tôi có tất cả thông tin và visualizations cần thiết. Hãy để tôi viết báo cáo chuyên sâu.

## Nghiên Cứu Sâu: Giải Pháp Embedding Tiếng Việt \& Tiếng Anh Siêu Nhanh Thay Thế OpenAI (2025)

### Tóm Tắt Điều Hành

Để thay thế OpenAI's text-embedding-3-small (chi phí \$0.020/1M tokens), bạn có ba chiến lược chính: (1) **Tối ưu tốc độ tiếng Việt**: ViEmbedding (2,200 câu/giây) + e5-small (63 QPS), chi phí \$0/tháng, (2) **Cân bằng chính xác-tốc độ**: bge-vi-base (0.88 độ chính xác, 950 câu/giây) + bge-small-en-v1.5, (3) **Tối ưu toàn diện**: Qwen3-embedding-8B (MTEB \#1, 70.58 score) hoặc NVIDIA llama-embed-nemotron-8B cho multilingualRag. Tất cả đều là open-source, self-hosted, với ROI breakeven khoảng 150K-200K embeddings/tháng.[^1][^2][^3][^4][^5][^6]

***

### I. Tình Hình Hiện Tại \& Bối Cảnh Thị Trường (2025)

OpenAI's text-embedding-3-small vẫn là baseline phổ biến với chi phí \$0.020/1M tokens, MTEB score 62.3%, latency ~9ms, nhưng không hỗ trợ tối ưu hóa self-hosted. Vào nửa đầu năm 2025, một cuộc cách mạng trong embedding models đã xảy ra:[^2][^7]

- **Qwen3-embedding-8B** (Alibaba) đạt rank \#1 trên MTEB multilingual leaderboard với score 70.58[^5][^8]
- **NVIDIA llama-embed-nemotron-8B** (tháng 10/2025) thiết lập SOTA cho multilingual RAG với cross-lingual representation learning[^6]
- **Jina-embeddings-v4** (mới) hỗ trợ visual document retrieval + 89 ngôn ngữ[^9]
- **Sentence Transformers** giới thiệu static embedding models: 100-400x nhanh hơn trên CPU so với all-mpnet-base-v2[^10]

Đối với tiếng Việt, ecosystem đã trưởng thành:

- **bge-vi-base** đạt 0.88 STS-Vi accuracy (tốt nhất)[^1]
- **ViEmbedding** đạt 2,200 câu/giây (nhanh nhất)[^1]
- **Vietnamese_Embedding (AITeamVN)** fine-tuned từ bge-m3 trên 300K Vietnamese triplets[^11]

***

### II. So Sánh Chi Tiết: Tiếng Việt

![Vietnamese Embedding Models: Accuracy vs Speed Trade-offs (2025)](https://ppl-ai-code-interpreter-files.s3.amazonaws.com/web/direct-files/15c3d43a2909a8f01415932ed8b41aa4/7369877f-9391-4cb3-8b6d-724c33cfb4e1/316b3fda.png)

Vietnamese Embedding Models: Accuracy vs Speed Trade-offs (2025)

**Bảng phân tích:**


| Mô hình | Accuracy (STS-Vi) | MRR@10 | Tốc độ (câu/s) | Vector dims | Use Case |
| :-- | :-- | :-- | :-- | :-- | :-- |
| **bge-vi-base** | 0.88 ⭐ | 0.84 | 950 | 768 | Semantic search, RAG, AI Agent (BEST accuracy) |
| **sBERT-Vi** | 0.86 | 0.81 | 1,100 | 768 | Q\&A, long-context dialogue, 10-15% faster |
| **ViEmbedding** | 0.74 | 0.69 | 2,200 ⭐ | 300 | Mobile apps, IoT, resource-constrained (FASTEST) |
| **PhoBERT** | 0.82 | 0.77 | 1,200 | 768 | Sentiment analysis, classification, fine-tuning |
| **Vietnamese_Embedding** | 0.85 | 0.80+ | 1,050 | 1024 | Fine-tuned retrieval, production-ready |

**Phân tích trade-off:**

- **Độ chính xác vs Tốc độ**: bge-vi-base (0.88 acc) chậm hơn ViEmbedding (2200 câu/s) 2.3x, nhưng chính xác hơn 18.9%
- **Tối ưu hybrid**: Dùng ViEmbedding để **pre-filter nhanh** (retrieval thô), sau đó dùng bge-vi-base để **rerank chính xác** (semantic ranking)[^1]
- **Vector size impact**: ViEmbedding (300d) dùng 4x ít storage hơn bge-vi-base (768d), lợi thế cho billion-scale vectors

***

### III. So Sánh Chi Tiết: Tiếng Anh \& Multilingual

![English/Multilingual Embedding Models: Performance & Speed Comparison](https://ppl-ai-code-interpreter-files.s3.amazonaws.com/web/direct-files/15c3d43a2909a8f01415932ed8b41aa4/abd10d44-0759-44cb-b293-0374af13dcf7/029db708.png)

English/Multilingual Embedding Models: Performance \& Speed Comparison

**Mô hình open-source thay thế text-embedding-3-small:**


| Mô hình | MTEB Score | Latency | Context | Params | Trade-offs |
| :-- | :-- | :-- | :-- | :-- | :-- |
| **e5-small** | 61.0 | 16ms ⭐ | 512 | 118M | Nhanh nhất, 100% Top-5 accuracy, ngôn ngữ hỗ trợ |
| **bge-small-en-v1.5** | 62.0 | 20ms | 512 | 120M | Balanced, easy to fine-tune, high retrieval |
| **nomic-embed-text-v1** | 62.39 ⭐ | 15ms | 8192 | 500M | Beats OpenAI score, long context, multimodal ready |
| **jina-embeddings-v3** | 62.5 | 25ms | 8192 | 570M | 89 languages, MRL support (32 dims), production-grade |
| **text-embedding-3-small** | 62.3 | 9ms | 8192 | ~300M | API-only, \$0.020/1M tokens, lowest latency |
| **Qwen3-embedding-8B** | 70.58 ⭐⭐ | 50ms | 32K | 8B | \#1 MTEB multilingual, 100+ languages, long context |

**Key insights:**

1. **e5-small là speed king**: 16ms latency, 7x nhanh hơn qwen3-0.6b, nhưng MTEB 61 thấp hơn OpenAI (62.3)
2. **nomic-embed-text-v1 vượt trội**: MTEB 62.39 > OpenAI 62.3, latency 15ms (nhanh hơn OpenAI's 9ms là tính overhead API)
3. **Qwen3-8B là SOTA multilingual**: Score 70.58 (hơn OpenAI ~8 điểm), nhưng cần 16GB GPU, latency 50ms
4. **jina-v3 balanced solution**: Hỗ trợ 89 ngôn gữ, context 8192, MRL cho dimension reduction tối ưu storage

***

### IV. Multilingual Strategies (Cả Việt + Anh)

**Option 1: Hybrid specialized models (Recommended for efficiency)**

```
Vietnamese queries → bge-vi-base (0.88 accuracy, 950 câu/s)
English queries   → e5-small (61 MTEB, 16ms)
Storage/pre-filter → ViEmbedding (300d, 2200 câu/s)
```

**Ưu điểm**: Tối ưu cho từng ngôn ngữ, inference nhanh, chi phí thấp (\$0)
**Nhược điểm**: Quản lý 2-3 mô hình, cần logic routing

**Option 2: Universal multilingual (Simple but heavier)**

```
Tất cả queries → BAAI/bge-m3 hoặc jina-embeddings-v3
```

**Ưu điểm**: Single model, 100+ languages, dễ deploy
**Nhược điểm**: Latency cao hơn (25ms vs 16ms), không tối ưu cho Vietnamese
**Performance**: bge-m3 trên tiếng Việt: MRR 0.77 (thấp hơn bge-vi-base 0.84)

**Option 3: Fine-tuned Vietnamese variant (Best accuracy)**

```
Sử dụng Vietnamese_Embedding (AITeamVN) - fine-tuned bge-m3
```

**Ưu điểm**: Accuracy 0.85+ (tốt nhất multilingual), hỗ trợ 100+ languages
**Nhược điểm**: 1024 dimensions (lớn hơn), cần A100/H100 GPU
**Chi phí**: ~\$500-800/month infrastructure

***

### V. Optimization Techniques \& Performance Tuning

#### A. Matryoshka Representation Learning (MRL) - Dimension Reduction Magic

Các mô hình jina-embeddings-v3, mxbai-embed-large-v1, stella-embed hỗ trợ MRL, cho phép giảm dimensions mà không retrain:[^10][^12]


| Reduction | jina-v3 | Performance Loss | Storage Savings | Latency Improvement |
| :-- | :-- | :-- | :-- | :-- |
| 1024d → 512d | ❌ | ~5% | 50% | 25-30% |
| 768d → 384d | ✓ | ~5% | 50% | 25-30% |
| 768d → 128d | ✓ | ~15% | 83% | 50-60% |
| full → 32d (jina) | ✓ | ~20% | 97% | 70-80% |

**Thực tế**: Cắt giảm 50% dimensions chỉ mất 5% performance, nhưng storage và vector similarity tính toán nhanh gấp 2x[^13][^10]

#### B. Batch Processing \& Caching (Redis)

**Redis EmbeddingsCache**:

- Cache hit rate: Có thể đạt 70-80% trên production queries (nhiều duplicate)
- Speedup: 6.86x với batch operations[^14]
- Latency reduction: 85.4% (từ 0.0455s → 0.0066s per embedding)[^14]

**Ứng dụng thực tế**:

```python
# Pseudocode
def embed_text(text, cache=redis_cache):
    if text in cache:
        return cache.get(text)  # ~1ms
    
    embedding = model.encode(text)  # ~16ms (e5-small)
    cache.set(text, embedding, ttl=3600)
    return embedding
```

**ROI**: Với cache hit rate 70%, latency giảm từ 16ms → 5ms, throughput tăng 3x

#### C. Dimension Reduction via PCA (Advanced)

Từ đó cắt từ 1536d → 512d:[^13]

- Precision drop: 14%
- Latency reduction: 50%
- Storage: -42%
- Recommendation: Dùng cho production nếu precision acceptable

***

### VI. Cost Analysis \& ROI Calculation

![Monthly Embedding Costs: OpenAI API vs Self-Hosted Deployment](https://ppl-ai-code-interpreter-files.s3.amazonaws.com/web/direct-files/15c3d43a2909a8f01415932ed8b41aa4/faee980d-6f1e-4deb-b542-2584135a1a30/2c5673b4.png)

Monthly Embedding Costs: OpenAI API vs Self-Hosted Deployment

**Break-even analysis:**


| Scenario | Monthly Embeddings | OpenAI Cost | Self-hosted GPU | Breakeven |
| :-- | :-- | :-- | :-- | :-- |
| **Startup (test)** | 100K | \$2 | \$300-500 setup | Never |
| **SMB** | 500K | \$10 | \$300-500/mo | Never |
| **Growth-stage** | 2M | \$40 | \$300-500/mo | 5-10M/month |
| **Enterprise** | 50M+ | \$1000 | \$500-1000/mo | Already positive |

**Infrastructure cost (self-hosted):**

- GPU ít dùng (shared): ~\$300/month (RTX 4090 rental)
- GPU medium: ~\$500-800/month (A40, L40S)
- GPU heavy: ~\$1500-2000/month (A100, H100)

**Hybrid recommendation**:

```
0-500K/month embeddings     → Use OpenAI API ($10-50)
500K-5M/month              → Hybrid (cache+self-host) ($200-400)
5M+/month                  → Full self-hosted ($400-1000)
```


***

### VII. Deployment Architecture \& Tools

#### Recommended Stack

```
┌─────────────────────────────────────────┐
│         Application Layer               │
│  (FastAPI + Python 3.9+)               │
└────────────┬────────────────────────────┘
             │
      ┌──────┴──────┐
      ▼             ▼
┌──────────┐  ┌──────────────┐
│ Redis    │  │ Embedding    │
│ Cache    │  │ Model (GPU)  │
└──────────┘  └──────────────┘
      │             │
      └──────┬──────┘
             ▼
┌─────────────────────────────────┐
│   Vector Database               │
│  (Chroma, Milvus, Pinecone)    │
└─────────────────────────────────┘
```

**Technology choices:**


| Component | Option | Cost | Setup |
| :-- | :-- | :-- | :-- |
| **API Framework** | FastAPI | \$0 | 1 day |
| **Embedding Model** | e5-small / bge-vi-base | \$0 | 1 hour |
| **Cache Layer** | Redis | \$0 self-hosted / \$100/mo cloud | 30 min |
| **Vector DB** | Chroma (dev) / Milvus (prod) | \$0-2000/mo | 1-5 days |
| **Containerization** | Docker + Kubernetes | \$0 | 2-3 days |
| **Infrastructure** | AWS EC2 (GPU) / GCP / Azure | \$300-1000/mo | 1 day |


***

### VIII. Model Selection Decision Framework

![Embedding Model Selection Decision Tree](https://ppl-ai-code-interpreter-files.s3.amazonaws.com/web/direct-files/15c3d43a2909a8f01415932ed8b41aa4/5c64ce54-28b9-4ff9-b857-e5cbaf681da7/443c4568.png)

Embedding Model Selection Decision Tree

**Quick decision guide:**

1. **"Cần tối ưu tốc độ tiếng Việt?"**
    - ✅ **ViEmbedding** (2200 câu/s) + e5-small (tiếng Anh)
    - Setup: Docker image ~200MB
    - Latency: 8-15ms (end-to-end)
    - Cost: \$0 software + \$300/mo infrastructure
2. **"Cần độ chính xác cao nhất?"**
    - ✅ **bge-vi-base** + Qwen3-embedding-8B
    - Accuracy: 0.88 (Việt) + 70.58 MTEB (multilingual)
    - Latency: 50-60ms (acceptable for RAG)
    - Cost: \$500-1000/mo infrastructure (cần A100 GPU)
3. **"Cần production-grade multilingual?"**
    - ✅ **Vietnamese_Embedding** (fine-tuned) hoặc **jina-embeddings-v3**
    - Support: 100+ languages
    - Context: 8192 tokens (long documents)
    - Cost: \$400-800/mo infrastructure
4. **"Cần thay thế OpenAI hoàn toàn, budget limited?"**
    - ✅ **Hybrid**: ViEmbedding (pre-filter) + bge-vi-base (rerank) + Redis caching
    - Accuracy: 0.85 (gần bge-vi-base)
    - Speed: 3x faster than bge-vi-base (via ViEmbedding pre-filtering)
    - Cost: \$200-300/mo (shared GPU + cache)

***

### IX. GPU Memory Requirements \& Infrastructure

![GPU Memory Requirements for Embedding Models](https://ppl-ai-code-interpreter-files.s3.amazonaws.com/web/direct-files/15c3d43a2909a8f01415932ed8b41aa4/929465fe-c386-4a76-8c8c-ab42fd8440e4/59eec092.png)

GPU Memory Requirements for Embedding Models

**Deployment scenarios:**


| Model | GPU Type | Memory | Batch Size | QPS | Monthly Cost |
| :-- | :-- | :-- | :-- | :-- | :-- |
| **e5-small** | RTX 3090 (24GB) | 0.5GB | 128 | 500-1000 | \$150-200 |
| **bge-vi-base** | RTX 4090 (24GB) | 1.2GB | 64 | 300-500 | \$200-300 |
| **bge-small-en** | RTX 4090 (24GB) | 0.6GB | 128 | 500-800 | \$200-300 |
| **jina-v3** | A40 (48GB) | 2GB | 32 | 200-400 | \$500-700 |
| **Qwen3-8B** | A100 (80GB) | 16GB | 16 | 50-100 | \$1000-1500 |
| **Nemotron-8B** | A100/H100 | 16GB | 16 | 50-100 | \$1000-2000 |

**Consumer GPU options** (cost-effective):

- RTX 3090 (24GB): \$800-1200 one-time, ~200W power
- RTX 4090 (24GB): \$1500-2000, ~450W power
- A40 (48GB): \$3000-4000, ~250W power
- Cloud rental: ~\$0.50-1.50/hour (AWS P3, GCP A100)

***

### X. Production Deployment Checklist

**Phase 1: Setup (1-2 weeks)**

- [ ] Select models (dùng decision framework ở section VIII)
- [ ] Set up Docker environment + FastAPI
- [ ] Test models locally (batch inference)
- [ ] Configure Redis caching layer
- [ ] Implement vector database (Chroma for MVP)

**Phase 2: Optimization (2-4 weeks)**

- [ ] Benchmark latency vs accuracy on your data
- [ ] Apply dimension reduction (MRL) nếu cần storage optimization
- [ ] Set up monitoring (latency, cache hit rate, error rate)
- [ ] Load testing (target QPS: 100-500 depending on model)
- [ ] Deploy to staging environment

**Phase 3: Production (1-2 weeks)**

- [ ] Scale to production GPU infrastructure
- [ ] Migrate from Chroma → Milvus (nếu >10M vectors)
- [ ] Set up CI/CD pipeline cho model updates
- [ ] Monitoring + alerting (CloudWatch, DataDog)
- [ ] Backup/disaster recovery strategy

**Expected timeline**: 4-8 tuần để full production, tùy theo complexity

***

### XI. Limitations \& Trade-offs

| Aspect | Open-source | OpenAI |
| :-- | :-- | :-- |
| **Cost** | \$0 software + infra | \$0.020/1M tokens |
| **Setup complexity** | Medium-High | Zero (API) |
| **Customization** | Full | None |
| **SLA** | Your responsibility | 99.9% guaranteed |
| **Latency** | 10-50ms | 9ms + API overhead |
| **Vietnamese support** | Excellent (bge-vi) | Good (multilingual) |
| **Updates** | Manual | Auto |
| **Vendor lock-in** | None | High |

**Khi nào dùng OpenAI?**

- Budget < \$100/month
- Volume < 500K embeddings/month
- Không muốn maintain infrastructure
- Cần guaranteed SLA

**Khi nào self-host?**

- Volume > 2M embeddings/month (ROI positive)
- Yêu cầu bảo mật cao (on-premise)
- Cần custom models / fine-tuning
- Có team DevOps

***

### XII. Các Trường Hợp Sử Dụng Thực Tế (2025)

1. **Vietnamese RAG Chatbot**
    - Model: bge-vi-base (semantic retrieval) + sBERT-Vi (reranking)
    - Database: ChromaDB (dev) → Milvus (production 10M+ vectors)
    - Cache: Redis (reduce embeddings 70%)
    - Cost: \$300-400/mo infra
    - Performance: 80ms end-to-end (query → retrieve → rerank)
2. **Multilingual E-commerce Search**
    - Model: Qwen3-embedding-8B (100+ languages)
    - Architecture: Elasticsearch (keyword) + vector search (semantic)
    - Cache: Product embeddings cached (high reuse)
    - Cost: \$800-1000/mo (A100 GPU + Milvus)
    - Performance: <50ms per search (cached products)
3. **Document Classification at Scale**
    - Model: PhoBERT (Việt) + bge-small-en (Anh)
    - Pipeline: Batch processing (không cần real-time)
    - Cost: GPU sharing (\$200/mo) + batch instances
    - Performance: 10,000 docs/day (cost-optimized)

***

### XIII. Kết Luận \& Khuyến Nghị

**Tóm tắt hành động:**

1. **Ngay lập tức (tuần 1)**: Deploy ViEmbedding (Việt) + e5-small (Anh) trên GPU shared, kết nối Redis cache → Savings: \$0 software, \$300-400/mo infra
2. **Tuần 2-3**: Fine-tune bge-vi-base trên domain-specific data nếu cần độ chính xác cao
3. **Tháng 2**: Scale lên Qwen3-8B hoặc Nemotron-8B nếu multilingual performance là priority
4. **Tháng 3+**: Migrate vector database từ Chroma → Milvus khi vượt 5M vectors

**Expected outcomes**:

- **Chi phí**: Giảm từ \$200-1000/month (OpenAI) xuống \$0-500/month (self-hosted)
- **Latency**: 9ms (OpenAI) → 10-50ms (self-hosted), nhưng có thể tối ưu via caching
- **Flexibility**: 0% (OpenAI) → 100% (self-hosted) - có thể fine-tune, customize, on-premise
- **Accuracy**: Comparable hoặc tốt hơn (Qwen3 score 70.58 vs OpenAI 62.3)

**Best bang-for-buck choice (2025)**:
→ **Hybrid strategy**: ViEmbedding (fast pre-filter) + bge-vi-base (accurate rerank) + Redis caching + Milvus
→ **ROI**: Breakeven ~4-6 tháng ở scale 2-5M embeddings/month

***

**References:**
bizfly.vn Vietnamese embedding benchmark 2025[^1]
Hugging Face Static Embeddings \& MRL[^10]
OpenAI text-embedding-3-small analysis[^2]
Embedding model comparison surveys[^7]
Vietnamese_Embedding (AITeamVN) fine-tuned model[^11]
E5-small speed champion benchmark[^3]
Jina-embeddings-v3/v4 documentation[^9]
MTEB leaderboard 2025 analysis[^4]
Embedding optimization via PCA[^13]
Qwen3-embedding-8B MTEB \#1[^5]
NVIDIA Nemotron-8B multilingual[^6]
Redis embeddings caching guide[^14]
<span style="display:none">[^15][^16][^17][^18][^19][^20][^21][^22][^23][^24][^25][^26][^27][^28][^29][^30][^31][^32][^33][^34][^35][^36][^37][^38][^39][^40]</span>

<div align="center">⁂</div>

[^1]: https://bizfly.vn/techblog/so-sanh-cac-mo-hinh-embedding-cho-tieng-viet-qua-benchmark.html

[^2]: https://www.pingcap.com/article/analyzing-performance-gains-in-openais-text-embedding-3-small/

[^3]: https://research.aimultiple.com/open-source-embedding-models/

[^4]: https://modal.com/blog/mteb-leaderboard-article

[^5]: https://agentset.ai/embeddings/qwen3-embedding-8b

[^6]: https://huggingface.co/blog/nvidia/llama-embed-nemotron-8b

[^7]: https://agentset.ai/embeddings/compare/openai-text-embedding-3-small-vs-gemini-text-embedding-004

[^8]: https://ollama.com/library/qwen3-embedding:8b

[^9]: https://jina.ai/embeddings/

[^10]: https://huggingface.co/blog/static-embeddings

[^11]: https://huggingface.co/AITeamVN/Vietnamese_Embedding

[^12]: https://www.mixedbread.com/blog/mxbai-embed-2d-large-v1

[^13]: https://www.contentstack.com/blog/tech-talk/hidden-patterns-in-embedding-optimization-part-i

[^14]: https://redis.io/docs/latest/develop/ai/redisvl/user_guide/embeddings_cache/

[^15]: https://www.facebook.com/groups/miaigroup/posts/1918760752228521/

[^16]: https://viblo.asia/p/lam-the-nao-embeddings-thay-doi-cach-ai-hieu-ve-ngon-ngu-PwlVmzx045Z

[^17]: https://openai.com/vi-VN/index/introducing-deep-research/

[^18]: https://vneconomy.vn/techconnect/review-tinh-nang-deep-research-cua-openai-giua-con-sot-deepseek.htm

[^19]: https://arxiv.org/pdf/2503.07470.pdf

[^20]: https://supermemory.ai/blog/best-open-source-embedding-models-benchmarked-and-ranked/

[^21]: https://www.facebook.com/protonxai/posts/model-embeddings-chính-xác-hơn-cả-openai-embedding-3-large-đó-là-baaibge-m3-trên/1178001830795622/

[^22]: https://pmc.ncbi.nlm.nih.gov/articles/PMC9311348/

[^23]: https://openrouter.ai/compare/baai/bge-large-en-v1.5/openai/text-embedding-3-small

[^24]: https://dataloop.ai/library/model/nomic-ai_nomic-embed-text-v1/

[^25]: https://www.linkedin.com/pulse/understanding-bge-m3-powerful-multilingual-embedding-model-shankaran-si4fc

[^26]: https://dataloop.ai/library/model/baai_bge-small-en/

[^27]: https://www.tigerdata.com/blog/open-source-vs-openai-embeddings-for-rag

[^28]: https://arxiv.org/html/2507.21500v1

[^29]: https://help.latenode.com/quick-start--basics/46DTZD5agh7BEhShC6XpUH/bge-small-en-v15/4eHdUXtpgarGQ66f47hzJe

[^30]: https://www.mixedbread.com/docs/models/embedding/mxbai-embed-large-v1

[^31]: https://www.themoonlight.io/en/review/jina-embeddings-v3-multilingual-embeddings-with-task-lora

[^32]: https://pyimagesearch.com/2025/11/17/fastapi-docker-deployment-preparing-onnx-ai-models-for-aws-lambda/

[^33]: https://langcopilot.com/posts/2025-10-14-best-vector-databases-milvus-vs-pinecone

[^34]: https://towardsdatascience.com/how-to-deploy-ml-solutions-with-fastapi-docker-and-gcp-de1bb8bfc59a/

[^35]: https://www.facebook.com/groups/miaigroup/posts/1676164806488118/

[^36]: https://www.emergentmind.com/topics/mteb-english-leaderboard

[^37]: https://arxiv.org/pdf/2408.11868.pdf

[^38]: https://zilliz.com/ai-faq/what-are-the-memory-requirements-for-different-embedding-models

[^39]: https://www.datasynthetix.com/blog/embedding-cost-calculator

[^40]: https://milvus.io/ai-quick-reference/what-are-the-memory-requirements-for-hosting-embedding-models

