# Video Platform (YouTube) - Hệ thống chia sẻ video

## Mức độ khó: ⭐⭐⭐⭐⭐ (Rất khó)

## Giới thiệu
YouTube-like system là một trong những challenging system design problems. Cần handle massive video uploads, encoding, storage, streaming tới billions users globally. Combine requirements từ push (upload), store, and pull (streaming) model.

## Yêu cầu Chức năng (Functional Requirements)
- Upload videos: users upload large files (GB+)
- Encode videos: multiple qualities/formats (360p, 720p, 1080p, etc.)
- Storage: efficiently store video files
- Streaming: serve videos to viewers efficiently
- Search: find videos by title, tags, channel
- Recommendations: suggest relevant videos
- Comments: users can comment on videos
- Playlists: create and manage video collections
- Analytics: track views, engagement, revenue

## Yêu cầu Phi chức năng (Non-Functional Requirements)
- Scalability: billions of videos, billions of requests/day
- Availability: 99.99% uptime (multi-region)
- Low latency: < 1s to start streaming
- High bandwidth efficiency: optimize video delivery
- Reliability: no video loss or corruption
- Security: prevent unauthorized access, DRM
- Cost-effective: video storage is expensive

## Các khái niệm chính
- **Transcoding**: Convert video to multiple qualities
- **Adaptive Bitrate Streaming**: Adjust quality based on bandwidth
- **Content Delivery Network (CDN)**: Distribute content globally
- **Message Queue**: Async transcoding jobs
- **Metadata Service**: Track video information
- **Search Index**: Full-text search on videos
- **Sharding**: Distribute videos across servers

## Ước lượng
- Daily uploads: 500 hours of video
- Daily views: 1 billion
- Concurrent viewers: 50 million
- Video library: 1 billion videos
- Average video duration: 10 minutes
- Average video size: 500MB
- Total storage: ~500 petabytes

## Kiến trúc cấp cao
```
Upload Flow:
Video File → Upload Service → Video Store → Transcoding Queue
                                           ↓
                                      Workers (encode)
                                           ↓
                                      Encoded Files → CDN

Streaming Flow:
Client Request → API Gateway → Load Balancer → CDN Node → Video
```

## Các trade-off chính
- **Quality vs Speed**: Higher quality takes longer to encode
- **Cost vs Experience**: More storage/CDN nodes = better experience but higher cost
- **Transcoding async vs sync**: Async faster user experience but delayed availability
- **Single codec vs multiple**: Multiple codecs better compatibility but more storage
- **Streaming protocol**: HLS (more compatible) vs DASH (better adaptation)

## Các bài toán phân nhánh
- Live streaming support
- Video editing features
- Monetization (ads, subscriptions)
- Copyright detection
- Community guidelines enforcement
- Video analytics at scale
