# Ride Sharing (Uber) - Hệ thống gọi xe

## Mức độ khó: ⭐⭐⭐⭐⭐ (Rất khó)

## Giới thiệu
Uber-like system cần real-time matching giữa riders và drivers, location tracking, pricing, payment processing. Complex spatial data structures, real-time updates, high concurrency, multi-region support.

## Yêu cầu Chức năng (Functional Requirements)
- Request ride: users book rides
- Driver matching: find nearby drivers efficiently
- Ride acceptance: drivers accept/decline requests
- Location tracking: real-time location updates
- Pricing: calculate fare dynamically
- Payment: process payments securely
- Rating/Review: rate after ride completion
- Ride history: track past rides
- Pickup/Dropoff locations: handle map interactions

## Yêu cầu Phi chức năng (Non-Functional Requirements)
- Low latency: < 1s untuk match riders dan drivers
- High availability: 99.9% uptime
- Strong consistency: no double-booking
- Real-time: location updates < 5 seconds
- Scalability: millions of concurrent users
- Geographic distribution: multi-region support

## Các khái niệm chính
- **Geohashing**: Partition map into grids untuk efficient location search
- **Quadtree**: Tree structure for spatial indexing
- **Real-time WebSocket**: Location updates, ride status
- **Eventual Consistency**: Accept some latency in matching
- **Sharding**: Partition data by geography (region-based)
- **Pricing Algorithm**: Surge pricing, distance-based
- **Payment Processing**: Secure payment gateway integration

## Ước lượng
- Daily active riders: 5 million
- Daily active drivers: 500,000
- Daily rides: 1 million
- Concurrent active rides: 100,000
- Location update frequency: every 5 seconds
- Rider-driver distance: ~2-5 miles average

## Kiến trúc cấp cao
```
Rider Request
    ↓
Location Service (Geohashing)
    ├─ Find nearby drivers in grid
    ├─ Apply filters (rating, capacity)
    └─ Match algorithms (ETA, price)
    ↓
Driver Notification (WebSocket)
    ↓
Pickup → In-ride → Dropoff
    ↓
Payment & Rating
```

## Các trade-off chính
- **Accuracy vs Speed**: More accurate matching is slower
- **Consistency vs Availability**: Strong consistency reduces throughput
- **Centralized vs Distributed**: Centralized simpler but less scalable
- **Real-time accuracy vs Bandwidth**: More frequent updates = higher bandwidth
- **Surge pricing**: Maximize revenue but may reduce demand
- **Driver vs Rider incentives**: Balance both sides' satisfaction

## Các bài toán phân nhánh
- Pool/Shared rides (multiple passengers)
- Scheduled rides
- Corporate/Enterprise rides
- Insurance and liability
- Driver earning optimization
- Fraud detection
- Carbon offset tracking
