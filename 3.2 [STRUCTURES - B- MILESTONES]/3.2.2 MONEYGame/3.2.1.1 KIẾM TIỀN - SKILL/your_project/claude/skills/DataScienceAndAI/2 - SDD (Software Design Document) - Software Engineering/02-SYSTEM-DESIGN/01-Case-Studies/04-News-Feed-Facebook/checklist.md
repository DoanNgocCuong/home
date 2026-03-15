# Checklist - News Feed (Facebook)

## Mức độ cơ bản (Basic)
- [ ] News feed là gì? Khác gì timeline?
- [ ] Fan-out là gì? Tại sao important?
- [ ] Push model vs Pull model: ưu nhược điểm?
- [ ] Ranking algorithm: cần track metrics nào?
- [ ] Follow/Follower relationship: lưu thế nào?
- [ ] Post storage: database schema nên là sao?
- [ ] Caching strategy: cache gì để improve performance?

## Mức độ trung bình (Intermediate)
- [ ] Hybrid push-pull approach: khi nào dùng push, khi nào pull?
- [ ] Hot vs Cold users: handle inactive users thế nào?
- [ ] Feed consistency: eventual vs strong consistency?
- [ ] Denormalization: lợi ích và risks?
- [ ] Redis feed cache: structure (sorted set, list)?
- [ ] Feed generation latency: acceptable window?
- [ ] Ranking signals: engagement, recency, social distance?
- [ ] Multi-feed support: home feed, explore, trending?
- [ ] Real-time feed updates: WebSocket hay polling?

## Mức độ nâng cao (Advanced)
- [ ] Personalization at scale: ML models cho ranking?
- [ ] A/B testing: test ranking algorithm changes?
- [ ] Cascade filters: handle millions posts efficiently?
- [ ] Fan-out optimization: batch writes, asynchronous?
- [ ] Cache coherence: invalidation strategy khi posts updated?
- [ ] Geographic distribution: serve different regions?
- [ ] Trending topics integration: real-time trends?
- [ ] Content moderation: abuse detection in feeds?
- [ ] Graph representation: efficient friend network queries?
- [ ] System monitoring: track feed staleness, ranking quality?

## Thực hành
- [ ] Design user, post, relationship schemas
- [ ] Implement basic feed generation (pull model)
- [ ] Add caching layer (Redis) cho feeds
- [ ] Implement push model cho selected users
- [ ] Design ranking algorithm
- [ ] Optimize query performance
- [ ] Write tests cho feed consistency
