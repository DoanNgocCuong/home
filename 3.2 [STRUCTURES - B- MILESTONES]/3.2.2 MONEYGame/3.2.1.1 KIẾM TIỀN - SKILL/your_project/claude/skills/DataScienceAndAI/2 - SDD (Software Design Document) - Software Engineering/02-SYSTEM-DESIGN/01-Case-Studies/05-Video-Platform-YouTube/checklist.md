# Checklist - Video Platform (YouTube)

## Mức độ cơ bản (Basic)
- [ ] Video platform requirements: upload, storage, streaming?
- [ ] Transcoding là gì? Tại sao cần?
- [ ] Video qualities: 360p, 720p, 1080p - lưu tất cả hay compute on-demand?
- [ ] Streaming protocols: HTTP, HLS, DASH - khác gì?
- [ ] CDN là gì? Tại sao important cho video?
- [ ] Upload flow: client → server → storage?
- [ ] Video metadata: nên store ở database nào?

## Mức độ trung bình (Intermediate)
- [ ] Adaptive bitrate streaming: adjust quality based on bandwidth?
- [ ] Transcoding architecture: where to process, when?
- [ ] Message queue: why needed cho transcoding?
- [ ] Video sharding: distribute videos across servers?
- [ ] Cache strategy: what can be cached?
- [ ] Search index: full-text search on video metadata?
- [ ] Comments/interactions: separate microservice?
- [ ] Analytics: track views, watch time, engagement?
- [ ] Multi-region deployment: how to handle?

## Mức độ nâng cao (Advanced)
- [ ] Encoding optimization: codec selection, bitrate optimization?
- [ ] Live streaming: different architecture than recorded?
- [ ] P2P streaming: save bandwidth, trade-off latency?
- [ ] DRM (Digital Rights Management): protect content?
- [ ] Cost optimization: storage, bandwidth, compute trade-offs?
- [ ] Copyright detection: audio/video fingerprinting?
- [ ] Community detection: find and recommend related videos?
- [ ] Video recommendation: collaborative filtering vs content-based?
- [ ] Monetization integration: ads, subscriptions?
- [ ] Handling large uploads: resume capability?

## Thực hành
- [ ] Design database schema: videos, users, comments
- [ ] Implement upload endpoint
- [ ] Design transcoding pipeline
- [ ] Implement streaming endpoint
- [ ] Add CDN simulation (or real CDN integration)
- [ ] Design recommendation algorithm
- [ ] Implement search functionality
- [ ] Handle concurrent uploads/streams
