# Checklist - Ride Sharing (Uber)

## Mức độ cơ bản (Basic)
- [ ] Ride sharing system requirements?
- [ ] Geohashing là gì? Tại sao dùng?
- [ ] Nearest neighbor search: implement thế nào?
- [ ] Matching algorithm: criteria gì để match riders + drivers?
- [ ] Location tracking: update frequency, storage?
- [ ] Pricing: dynamic surge pricing logic?
- [ ] Payment flow: secure payment handling?
- [ ] Ride status: states (requested, accepted, picked, completed)?

## Mức độ trung bình (Intermediate)
- [ ] Spatial indexing: Quadtree vs R-tree vs Geohashing?
- [ ] Real-time location updates: WebSocket vs polling?
- [ ] Matching optimization: minimize wait time, maximize acceptance rate?
- [ ] Driver availability: track online/offline status?
- [ ] Pickup/Dropoff navigation: route optimization?
- [ ] Concurrent ride handling: prevent double-booking?
- [ ] Multi-region coordination: handle requests across regions?
- [ ] ETA calculation: estimate time to arrive?
- [ ] Rating/Review system: affect matching?

## Mức độ nâng cao (Advanced)
- [ ] Surge pricing strategy: maximize revenue vs demand?
- [ ] Matching algorithm ML: predict acceptance probability?
- [ ] Pool rides: group multiple riders efficiently?
- [ ] Driver supply optimization: incentivize during peak times?
- [ ] Fraud detection: detect fake rides, no-shows?
- [ ] Geographic sharding: partition data by region?
- [ ] Disaster recovery: what if region goes down?
- [ ] A/B testing: test matching algorithms?
- [ ] Ride prediction: anticipate demand before it happens?
- [ ] Scheduled rides: handle advance bookings?

## Thực hành
- [ ] Design database schema: users, drivers, rides, locations
- [ ] Implement geohashing or spatial index
- [ ] Build driver matching algorithm
- [ ] Implement location tracking service
- [ ] Design pricing calculation
- [ ] Create payment integration
- [ ] Implement rating system
- [ ] Handle concurrent ride requests
