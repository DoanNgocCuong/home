# Checklist - Cloud Storage (Dropbox)

## Mức độ cơ bản (Basic)
- [ ] Cloud storage system requirements?
- [ ] File upload/download: protocols, chunking?
- [ ] File versioning: store multiple versions?
- [ ] Metadata service: what information track?
- [ ] File sharing: permission model?
- [ ] Synchronization: how to sync across devices?
- [ ] Conflict resolution: what if file modified on two devices?
- [ ] Trash: soft delete, restore capability?

## Mức độ trung bình (Intermediate)
- [ ] Block storage: why split files into blocks?
- [ ] Deduplication: identify identical blocks?
- [ ] Delta sync: only sync changed portions?
- [ ] Chunking strategy: optimal block size?
- [ ] Replication: how many copies, where?
- [ ] Consistency model: strong vs eventual?
- [ ] Access control: permissions, sharing links?
- [ ] Search functionality: file search implementation?
- [ ] Notifications: notify users on changes?

## Mức độ nâng cao (Advanced)
- [ ] Bandwidth optimization: limit upload/download speed?
- [ ] Incremental backup: only backup changed blocks?
- [ ] Garbage collection: remove unreferenced blocks?
- [ ] Encryption: at-rest and in-transit?
- [ ] Multi-region replication: sync across data centers?
- [ ] Selective sync: sync only certain folders?
- [ ] Offline-first: work offline, sync later?
- [ ] Collaborative editing: real-time editing?
- [ ] Conflict resolution algorithms: three-way merge?
- [ ] Cost optimization: storage class, lifecycle policies?

## Thực hành
- [ ] Design metadata schema
- [ ] Implement file chunking algorithm
- [ ] Build deduplication system
- [ ] Implement file synchronization logic
- [ ] Design conflict resolution strategy
- [ ] Build access control system
- [ ] Implement trash/restore functionality
- [ ] Add notification system
