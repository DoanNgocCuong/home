# E-Commerce (Amazon) - Hệ thống thương mại điện tử

## Mức độ khó: ⭐⭐⭐⭐ (Khó)

## Giới thiệu
Amazon-scale e-commerce system cần handle millions products, billions transactions, distributed inventory, payment processing, order fulfillment. Challenges include inventory consistency, shopping cart operations, search, recommendations at massive scale.

## Yêu cầu Chức năng (Functional Requirements)
- Product listing: browse and search products
- Shopping cart: add/remove items
- Checkout: order placement dengan payment
- Inventory management: track stock levels
- Order fulfillment: manage shipment tracking
- User accounts: manage profiles, addresses, payment methods
- Reviews and ratings: product feedback
- Recommendations: personalized suggestions
- Returns and refunds: handle return process

## Yêu cầu Phi chức năng (Non-Functional Requirements)
- Low latency: < 200ms page load, < 1s checkout
- High availability: 99.99% uptime
- Strong consistency: inventory accuracy
- Scalability: billions requests/day
- Security: PCI compliance, fraud detection
- Reliability: transaction ACID properties
- Cost-effective: minimize operational costs

## Các khái niệm chính
- **Distributed Transactions**: ACID guarantees across services
- **Inventory Sharding**: Partition inventory by region/product
- **Denormalization**: Pre-compute aggregates (ratings, counts)
- **Payment Processing**: Secure payment gateway integration
- **Caching Strategy**: Cache popular products, cart data
- **Search Engine**: Elasticsearch for product search
- **Order Management**: Track order lifecycle
- **Recommendation Engine**: Collaborative filtering, content-based

## Ước lượng
- Daily active users: 100 million
- Concurrent users: 5 million
- Products: 1 billion SKUs
- Daily orders: 10 million
- Transactions per second: 100k+
- Cart operations: 10M per second
- Search queries: 1M per second
- Average order value: $50

## Kiến trúc cấp cao
```
User Request (Browse/Search/Buy)
    ↓
API Gateway (Load Balance)
    ↓
├─ Product Service (Search, Cache)
├─ Cart Service (Redis, Stateful)
├─ Inventory Service (Strong consistency)
├─ Order Service
├─ Payment Service
└─ Recommendation Service
    ↓
Databases (Multiple stores)
└─ External Services (Payment gateway, Shipping)
```

## Các trade-off chính
- **Consistency vs Availability**: Strict inventory consistency may reduce availability
- **Strong vs Eventual**: Strong guarantees slower, eventual faster
- **Cache vs Accuracy**: Stale cache may show wrong stock
- **Monolith vs Microservices**: Monolith simpler but less scalable
- **Synchronous vs Asynchronous**: Sync faster response, async better throughput
- **Single vs Multiple payment gateways**: Multiple adds reliability but complexity

## Các bài toán phân nhánh
- Flash sales with inventory limits
- Dynamic pricing and promotions
- Multi-seller marketplace
- Fraud detection and prevention
- Supply chain optimization
- Regional inventory optimization
- Prime membership benefits
