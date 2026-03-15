# Checklist - Chat System (WhatsApp)

## Mức độ cơ bản (Basic)
- [ ] Chat system requirements là gì? Functional vs non-functional?
- [ ] WebSocket là gì và tại sao dùng cho chat?
- [ ] Alternativea nào thay cho WebSocket (polling, long-polling)?
- [ ] Presence system là gì? Online/offline status?
- [ ] Message history cần lưu ở đâu?
- [ ] Group chat vs 1-to-1 chat có khác gì không?
- [ ] Delivery status (sent, delivered, read) cần track làm sao?

## Mức độ trung bình (Intermediate)
- [ ] Offline message handling: làm sao lưu cho users offline?
- [ ] Message ordering: guarantee FIFO delivery?
- [ ] Deduplication: tại sao important? Implement thế nào?
- [ ] Presence service: dùng Redis hay database?
- [ ] Typing indicators: implement real-time updates?
- [ ] Group chat optimization: handle large groups efficiently?
- [ ] Message search: implement full-text search?
- [ ] Scalability: multiple chat servers need coordination?
- [ ] Load balancing: sticky sessions vs stateless design?

## Mức độ nâng cao (Advanced)
- [ ] End-to-End encryption challenges: impact on search, delivery?
- [ ] Consistency model: CAP theorem trade-offs?
- [ ] Event sourcing vs snapshot approach cho message history?
- [ ] Pub/Sub pattern cho message broadcasting?
- [ ] Distributed transactions cho group messages (atomic delivery)?
- [ ] Handling network failures: retry strategy?
- [ ] Multi-region deployment: message sync across regions?
- [ ] Analytics: track message metrics without losing privacy?
- [ ] Rate limiting cho chat messages?
- [ ] Cost optimization: trade-off between latency và cost?

## Thực hành
- [ ] Design schema cho messages, users, conversations
- [ ] Implement basic WebSocket chat system
- [ ] Add offline message queue using message broker
- [ ] Implement presence tracking
- [ ] Design group chat data structure
- [ ] Handle message ordering và deduplication
- [ ] Write tests cho message delivery guarantees
