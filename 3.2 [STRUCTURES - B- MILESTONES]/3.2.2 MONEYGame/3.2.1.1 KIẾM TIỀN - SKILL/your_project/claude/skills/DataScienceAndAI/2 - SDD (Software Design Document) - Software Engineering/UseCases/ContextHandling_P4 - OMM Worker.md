
Link: D:\GIT\context-handling-bigmodule_PikaRobot_25112025\docs\6_OMM_worker\docs1.1_OMM_worker.md

fix(worker): Add comprehensive OOM protection and memory monitoring

## Overview
Implement comprehensive fixes for worker OOM (Out of Memory) issues based on MECE analysis.
All critical (P0) and high priority (P1) fixes have been completed.

## P0 - Critical Fixes

### 1. Memory Limits in Docker Compose
File: src/docker-compose.worker.yml
- Add memory limit: 2GB (deploy.resources.limits.memory)
- Add CPU limit: 2.0 cores
- Add memory reservation: 512MB (guaranteed)
- Add CPU reservation: 0.5 cores
- Rationale: Protect worker from OOM kill, enforce resource boundaries

### 2. Message Size Validation
File: src/app/background/rabbitmq_consumer.py
- Add MAX_MESSAGE_SIZE_BYTES constant: 2MB
- Validate message body size in callback() before JSON parsing
- Reject messages > 2MB with error log and ACK (no requeue)
- Prevent memory spike from parsing oversized messages
- Rationale: Avoid OOM from poison messages with large payloads

### 3. DB Session Cleanup Improvement
File: src/app/background/rabbitmq_consumer.py
- Improve error handling in finally block for db.close()
- Check session state (is_active) before closing
- Add rollback fallback if close fails
- Better logging for session cleanup errors
- Rationale: Prevent connection leaks causing pool exhaustion

### 4. Conversation Log Size Validation
File: src/app/background/rabbitmq_consumer.py
- Add MAX_CONVERSATION_LOG_SIZE_BYTES: 1.5MB
- Add WARN_CONVERSATION_LOG_SIZE_BYTES: 500KB
- Validate conversation_log size after parsing
- Warning log if > 500KB
- Reject if > 1.5MB (with buffer from 2MB message limit)
- Rationale: Prevent memory bloat from large conversation logs

## P1 - High Priority Improvements

### 5. Memory Monitoring System
File: src/app/utils/memory_monitor.py (NEW)
- New utility module for memory monitoring
- Read memory limit from Docker cgroup or DOCKER_MEMORY_LIMIT env var
- Get current RSS (Resident Set Size) using psutil
- Alert threshold: 80% of limit (1.6GB if limit = 2GB)
- Warning threshold: 70% of limit
- Send alerts via existing alert system
- Functions:
  - get_memory_limit_bytes(): Read limit from cgroup/env
  - get_memory_usage(): Get current memory stats
  - check_memory_and_alert(): Check and send alert if needed
  - log_memory_stats(): Log memory metrics

Integration in rabbitmq_consumer.py:
- Periodic memory check every 30 messages
- Log memory stats periodically
- Automatic alerts when threshold exceeded

### 6. HTTP Client Cleanup Review
File: src/app/services/utils/llm_analysis_utils.py
- Verified: Already using async with context manager
- httpx.AsyncClient properly closed after use
- No changes needed (already correct)

### 7. Configuration Validation
File: src/app/core/config_settings.py
- Add _validate_config() function
- Validate WORKER_CONCURRENCY_PER_WORKER (warn if > 20)
- Validate total DB connections (warn if > 200)
- Validate DB_POOL_SIZE vs WORKER_CONCURRENCY_PER_WORKER
- Log warnings at startup if misconfiguration detected
- Rationale: Prevent OOM from misconfiguration

### 8. Thread Pool Monitoring
File: src/app/background/rabbitmq_consumer.py
- Monitor thread pool queue size in callback()
- Alert if queue backlog > 50 messages
- Log thread pool metrics periodically:
  - Active threads count
  - Pending tasks in queue
  - Max workers configured
- Early detection of processing bottlenecks
- Rationale: Detect issues before memory pressure builds

## Technical Details

### Memory Flow Protection
1. Message received → Size validation (< 2MB)
2. Parse JSON → conversation_log size validation (< 1.5MB)
3. Process message → Memory check every 30 messages
4. DB operations → Proper session cleanup
5. Thread pool → Queue monitoring
6. Alert system → Notify on high memory usage

### Constants Added
- MAX_MESSAGE_SIZE_BYTES: 2 * 1024 * 1024 (2MB)
- MAX_CONVERSATION_LOG_SIZE_BYTES: 1.5 * 1024 * 1024 (1.5MB)
- WARN_CONVERSATION_LOG_SIZE_BYTES: 500 * 1024 (500KB)
- MEMORY_ALERT_THRESHOLD_PERCENT: 80%
- MEMORY_WARNING_THRESHOLD_PERCENT: 70%
- DEFAULT_MEMORY_LIMIT_BYTES: 2GB

## Files Modified
- src/docker-compose.worker.yml: Resource limits
- src/app/background/rabbitmq_consumer.py: Validation, cleanup, monitoring
- src/app/core/config_settings.py: Configuration validation
- src/app/utils/memory_monitor.py: New memory monitoring utility

## Testing Recommendations
1. Test with large messages (> 2MB) - should be rejected
2. Test with large conversation_log (> 1.5MB) - should be rejected
3. Monitor memory usage under load
4. Verify alerts are sent when memory > 80%
5. Test thread pool monitoring with high concurrency
6. Verify DB session cleanup (no leaks)

## Impact
- Worker protected from OOM kill with 2GB limit
- Early detection of memory issues via monitoring
- Prevention of memory spikes from oversized messages
- Better resource cleanup and leak prevention
- Configuration validation prevents misconfiguration

Closes: Worker OOM issues identified in MECE analysis"