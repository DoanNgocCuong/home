# Cloud Storage (Dropbox) - Hệ thống lưu trữ đám mây

## Mức độ khó: ⭐⭐⭐⭐ (Khó)

## Giới thiệu
Dropbox-like system cần handle petabytes of user data across global data centers. Challenges include file synchronization, version history, sharing, access control, efficient storage, and dealing with large file uploads/downloads.

## Yêu cầu Chức năng (Functional Requirements)
- File upload/download: support large files
- File synchronization: sync across devices
- File versioning: maintain version history
- File sharing: share with other users/teams
- Access control: manage permissions
- Search: find files by name, content
- Trash/Restore: recover deleted files
- Notifications: notify on file changes
- Collaboration: concurrent editing support

## Yêu cầu Phi chức năng (Non-Functional Requirements)
- Reliability: no data loss
- Durability: persist data reliably
- Availability: 99.95% uptime
- Scalability: petabytes of data
- Performance: fast upload/download
- Security: encryption, access control
- Cost-effective: minimize storage costs
- Consistency: same data across regions

## Các khái niệm chính
- **Block Storage**: Store files as blocks for deduplication
- **Chunking**: Split large files into smaller chunks
- **Deduplication**: Identify identical blocks, store once
- **Delta Sync**: Only sync changed portions
- **Metadata Service**: Track file metadata separately
- **Conflict Resolution**: Handle concurrent edits
- **Replication**: Replicate data across regions
- **Rate Limiting**: Control bandwidth usage

## Ước lượng
- Total users: 500 million
- Active users: 100 million
- Total storage: 100 exabytes
- Average file size: 1 MB
- Upload/download speed: 10 Mbps average
- QPS: 100,000 requests per second
- File operations/day: 1 billion

## Kiến trúc cấp cao
```
Client Upload/Download
    ↓
API Gateway
    ↓
├─ File Service (chunking, upload)
├─ Metadata Service (file info)
├─ Storage Service (persist blocks)
├─ Notification Service
└─ Sync Service (device sync)
    ↓
Object Storage (S3-like)
└─ Metadata DB
```

## Các trade-off chính
- **Consistency vs Availability**: Strong consistency slower, eventual consistency faster
- **Deduplication vs Speed**: Deduplication saves space but slower
- **Replication vs Cost**: More replicas safer but costlier
- **Real-time sync vs Bandwidth**: More frequent sync uses more bandwidth
- **Local cache vs Freshness**: Cache faster but may be stale
- **Encryption vs Performance**: Encryption adds overhead

## Các bài toán phân nhánh
- Delta sync optimization
- Bandwidth throttling
- Selective sync (sync only certain folders)
- Offline-first support
- Collaborative editing with conflict resolution
- Search with content indexing
- Backup and disaster recovery
- Mobile optimization (limited bandwidth)
