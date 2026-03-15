# Search Engine (Google) - Hệ thống tìm kiếm

## Mức độ khó: ⭐⭐⭐⭐⭐ (Rất khó)

## Giới thiệu
Search engine là one of the most complex systems. Cần crawl miliaran web pages, index them efficiently, return relevant results từ indices với latency < 100ms. Combines crawling, indexing, ranking, query processing.

## Yêu cầu Chức năng (Functional Requirements)
- Web crawling: discover and fetch web pages
- Indexing: create searchable indices of pages
- Searching: return relevant results for queries
- Ranking: order results by relevance
- Caching: cache popular queries
- Auto-complete: suggest search terms
- Spell correction: correct typos
- Filtering: filter by date, domain, type

## Yêu cầu Phi chức năng (Non-Functional Requirements)
- Low latency: < 100ms query response
- High throughput: billions of queries/day
- Scalability: index trillions of pages
- Freshness: index updates regularly
- Fault tolerance: no single point of failure
- Accuracy: return relevant results
- Cost-effective: balance storage and compute

## Các khái niệm chính
- **Crawler**: Distributed web crawler to fetch pages
- **Inverted Index**: Map from words to documents containing them
- **PageRank**: Rank pages based on link structure
- **TF-IDF**: Term frequency-inverse document frequency for relevance
- **Query Processing**: Parse and optimize queries
- **Distributed Storage**: Store indices across cluster
- **Bloom Filters**: Efficient deduplication
- **Sharding**: Partition indices by term or document

## Ước lượng
- Pages to index: 100 billion
- Daily new pages: 1 billion
- Daily queries: 5 billion
- Query latency requirement: 100ms
- Index size: ~1 petabyte
- Storage per indexed page: ~10 KB
- QPS: 60,000+ queries per second

## Kiến trúc cấp cao
```
Query Input
    ↓
Query Processor
    ├─ Tokenization
    ├─ Spell correction
    └─ Query expansion
    ↓
Search Service
    ├─ Lookup inverted index
    ├─ Apply ranking
    └─ Return top K results
    ↓
Results

Separate Pipeline:
Web Crawler → URL Frontier → Page Parser
    ↓
Inverted Index Builder
    ↓
Distributed Storage
```

## Các trade-off chính
- **Freshness vs Cost**: Update indices more frequently costs more
- **Relevance vs Diversity**: Top results may be similar
- **Latency vs Accuracy**: Simple ranking faster, complex ranking more accurate
- **Storage vs Query performance**: More data stored makes queries slower
- **Centralized vs Distributed**: Distributed more scalable but complex
- **Real-time vs Batch**: Real-time indexing slower, batch faster

## Các bài toán phân nhánh
- Personalized search results
- Spam detection
- Featured snippets extraction
- Knowledge graph construction
- Multi-language support
- Image/Video search
- News search with freshness
- Voice search support
