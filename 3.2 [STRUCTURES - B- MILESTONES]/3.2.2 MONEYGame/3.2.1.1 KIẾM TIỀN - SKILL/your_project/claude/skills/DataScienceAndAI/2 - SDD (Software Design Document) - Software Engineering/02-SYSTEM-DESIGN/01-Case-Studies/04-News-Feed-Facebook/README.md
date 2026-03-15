# News Feed (Facebook) - Hệ thống feed tin tức

## Mức độ khó: ⭐⭐⭐⭐ (Khó)

## Giới thiệu
Hệ thống News Feed là core của social media platforms. Phải hiển thị relevant posts từ friends/follows với freshness và ranking algorithms. Scale tới billions của posts và hundreds của millions concurrent users.

## Yêu cầu Chức năng (Functional Requirements)
- Fetch news feed: show posts từ following users
- Post creation: publish new posts (text, images, videos)
- Like, comment, share: interactions với posts
- Follow/unfollow: manage relationships
- Newsfeed ranking: show most relevant posts first
- Real-time updates: new posts appear immediately
- Media support: images, videos, links

## Yêu cầu Phi chức năng (Non-Functional Requirements)
- Low latency: < 100ms để load feed
- High throughput: billions requests/day
- Availability: 99.95% uptime
- Scalability: handle exponential growth
- Freshness: recent posts prioritized
- Relevance: personalized ranking

## Các khái niệm chính
- **Fan-out**: Push posts to followers' feeds (cache invalidation challenge)
- **Feed Ranking**: Relevance scoring (engagement, recency, relationships)
- **Denormalization**: Store pre-computed data để faster retrieval
- **Cache Strategy**: Redis/Memcached để store user feeds
- **Timeline vs Feed**: Timeline = chronological, Feed = ranked
- **Hybrid approach**: Push for active users, pull for inactive

## Ước lượng
- Daily Active Users: 300 million
- Posts per day: 10 billion
- Requests per second: 1 million
- Concurrent users: 50 million
- Feed size per user: 100-500 posts
- Storage per user feed: ~100MB (cached)

## Kiến trúc cấp cao
```
User Feed Request
    ↓
API Gateway
    ↓
Feed Service
    ├─ Check Cache (Redis)
    ├─ If Miss: Query Database
    ├─ Apply Ranking Algorithm
    └─ Return Top N Posts
    ↓
Response with Posts
```

## Các trade-off chính
- **Push vs Pull**: Push precomputes feeds (fast reads, expensive writes), Pull computes on-demand (slow reads, cheap writes)
- **Freshness vs Performance**: Real-time updates slower, batch updates faster
- **Relevance vs Diversity**: Personalization increases engagement but may create filter bubbles
- **Storage vs Computation**: Pre-rank feeds faster but uses more storage
- **Consistency vs Availability**: Strong consistency slower, eventual consistency faster

## Các bài toán phân nhánh
- Hashtag feeds
- Location-based feeds
- Trending topics integration
- Video feeds optimization
- Personalization algorithms
- Spam/abuse detection in feeds
