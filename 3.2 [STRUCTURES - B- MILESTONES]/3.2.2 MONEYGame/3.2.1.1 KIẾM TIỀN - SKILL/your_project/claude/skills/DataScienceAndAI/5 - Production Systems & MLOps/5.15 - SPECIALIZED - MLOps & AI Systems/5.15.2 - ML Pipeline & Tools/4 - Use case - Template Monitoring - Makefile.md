
```Makefile
# Docker Compose Management for Split Architecture
# Infrastructure: Milvus (etcd, minio, standalone, attu)
# Models: Embedding services (jina-vllm, infinity-proxy)
# App: Mem0 application
# All services use shared network: mem0_network

.PHONY: start-infrastructure stop-infrastructure restart-infrastructure logs-infrastructure
.PHONY: start-models stop-models restart-models logs-models
.PHONY: start-app stop-app restart-app logs-app
.PHONY: start-all stop-all restart-all logs-all
.PHONY: down-all ps status wait-infinity-proxy
.PHONY: monitor monitor-quick monitor-all monitor-all-snapshot monitor-summary analyze monitor-stress analyze-csv monitor-install monitor-clean
.PHONY: setup-scripts

# Infrastructure (Milvus) - Creates shared network
start-infrastructure:
	docker compose -f docker-compose-infrastructure.yml up -d

stop-infrastructure:
	docker compose -f docker-compose-infrastructure.yml down

restart-infrastructure:
	docker compose -f docker-compose-infrastructure.yml restart

logs-infrastructure:
	docker compose -f docker-compose-infrastructure.yml logs -f

# Models (Embedding) - Uses shared network
start-models:
	docker compose -f docker-compose-models.yml up -d

stop-models:
	docker compose -f docker-compose-models.yml down

restart-models:
	docker compose -f docker-compose-models.yml restart

logs-models:
	docker compose -f docker-compose-models.yml logs -f

# Wait for infinity-proxy to be healthy
wait-infinity-proxy:
	@echo "⏳ Waiting for infinity-proxy to be healthy..."
	@for i in $$(seq 1 90); do \
		status=$$(docker inspect infinity-proxy --format='{{.State.Health.Status}}' 2>/dev/null || echo "not-found"); \
		if [ "$$status" = "healthy" ]; then \
			echo "✅ infinity-proxy is healthy"; \
			exit 0; \
		fi; \
		[ $$((i % 10)) -eq 0 ] && echo "  Still waiting... ($$i/90) - Status: $$status"; \
		sleep 2; \
	done; \
	echo "❌ Timeout waiting for infinity-proxy"; \
	exit 1

# App (Mem0) - Uses shared network, waits for infinity-proxy
start-app: wait-infinity-proxy
	docker compose -f docker-compose-app.yml up -d

stop-app:
	docker compose -f docker-compose-app.yml down

restart-app:
	docker compose -f docker-compose-app.yml restart

logs-app:
	docker compose -f docker-compose-app.yml logs -f

# All services - Auto-setup scripts before starting
start-all: setup-scripts start-infrastructure start-models start-app
	@echo "✅ All services started. Checking status..."
	@sleep 2
	@docker compose -f docker-compose-infrastructure.yml ps
	@docker compose -f docker-compose-models.yml ps
	@docker compose -f docker-compose-app.yml ps
	@echo ""
	@echo "💡 Monitoring tools ready! Use:"
	@echo "   make monitor-all              # Monitor all project containers"
	@echo "   make monitor c=mem0-server    # Monitor single container (default: 5 min)"
	@echo "   make monitor-quick            # Quick stats snapshot"
	@echo "   make analyze                  # Worker recommendations"

stop-all: stop-app stop-models stop-infrastructure

restart-all: restart-infrastructure restart-models restart-app

logs-all:
	@echo "=== Infrastructure Logs ==="
	@docker compose -f docker-compose-infrastructure.yml logs --tail=50
	@echo "\n=== Models Logs ==="
	@docker compose -f docker-compose-models.yml logs --tail=50
	@echo "\n=== App Logs ==="
	@docker compose -f docker-compose-app.yml logs --tail=50

# Utility commands
down-all: stop-all

ps:
	@echo "=== Infrastructure Services ==="
	@docker compose -f docker-compose-infrastructure.yml ps
	@echo "\n=== Models Services ==="
	@docker compose -f docker-compose-models.yml ps
	@echo "\n=== App Services ==="
	@docker compose -f docker-compose-app.yml ps

status: ps

# ============================================================================
# Setup - Ensure scripts are executable (auto-run before start-all)
# ============================================================================
setup-scripts:
	@chmod +x scripts/*.sh 2>/dev/null || true
	@mkdir -p monitoring_results
	@echo "✅ Scripts ready"

# ============================================================================
# Resource Monitoring - All-in-one container monitoring
# ============================================================================

## Monitor container với CSV export (Usage: make monitor [c=container] [d=duration] [i=interval])
monitor: setup-scripts
	@bash scripts/monitor-container.sh ${c:-mem0-server} ${d:-300} ${i:-1}

## Quick stats snapshot (no CSV)
monitor-quick:
	@echo "📊 Quick stats for ${c:-mem0-server}:"
	@docker stats ${c:-mem0-server} --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}\t{{.NetIO}}\t{{.PIDs}}"

## Monitor all project containers (REAL-TIME - runs continuously, Ctrl+C to stop)
monitor-all:
	@echo "📊 Real-time stats for project containers (Ctrl+C to stop):"
	@CONTAINERS=$$(docker compose -f docker-compose-infrastructure.yml ps -q 2>/dev/null && \
		docker compose -f docker-compose-models.yml ps -q 2>/dev/null && \
		docker compose -f docker-compose-app.yml ps -q 2>/dev/null); \
	if [ -n "$$CONTAINERS" ]; then \
		docker stats --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}\t{{.NetIO}}" $$CONTAINERS; \
	else \
		echo "⚠️  No project containers running. Start services with: make start-all"; \
	fi

## Monitor all project containers (SNAPSHOT - one-time check)
monitor-all-snapshot:
	@echo "📊 Snapshot stats for project containers:"
	@CONTAINERS=$$(docker compose -f docker-compose-infrastructure.yml ps -q 2>/dev/null && \
		docker compose -f docker-compose-models.yml ps -q 2>/dev/null && \
		docker compose -f docker-compose-app.yml ps -q 2>/dev/null); \
	if [ -n "$$CONTAINERS" ]; then \
		docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}\t{{.NetIO}}" $$CONTAINERS; \
	else \
		echo "⚠️  No project containers running. Start services with: make start-all"; \
	fi

## Monitor with summary and recommendations
monitor-summary: monitor-all
	@echo ""
	@echo "📈 Resource Usage Summary:"
	@CONTAINERS=$$(docker compose -f docker-compose-infrastructure.yml ps -q 2>/dev/null && \
		docker compose -f docker-compose-models.yml ps -q 2>/dev/null && \
		docker compose -f docker-compose-app.yml ps -q 2>/dev/null); \
	if [ -n "$$CONTAINERS" ]; then \
		docker stats --no-stream --format "{{.Name}}|{{.CPUPerc}}|{{.MemPerc}}" $$CONTAINERS | \
		awk -F'|' '{ \
			cpu=$$2; gsub(/%/, "", cpu); \
			mem=$$3; gsub(/%/, "", mem); \
			if (cpu > 80) print "⚠️  " $$1 ": High CPU (" cpu "%)"; \
			if (mem > 80) print "⚠️  " $$1 ": High Memory (" mem "%)"; \
			cpu_total+=cpu; mem_total+=mem; count++ \
		} END { \
			if (count > 0) { \
				print ""; \
				print "📊 Average Usage:"; \
				printf "   CPU: %.1f%%\n", cpu_total/count; \
				printf "   Memory: %.1f%%\n", mem_total/count; \
				print ""; \
				print "💡 Recommendations:"; \
				avg_cpu=cpu_total/count; avg_mem=mem_total/count; \
				if (avg_cpu > 80) print "   - High CPU usage. Consider increasing CPU limits or reducing load"; \
				if (avg_cpu < 50) print "   - Low CPU usage. System can handle more load"; \
				if (avg_mem > 80) print "   - High Memory usage. Consider increasing memory limits"; \
				if (avg_mem < 50) print "   - Memory usage is healthy"; \
			} \
		}'; \
	fi

## Stress test: monitor trong background + recommendations
# Usage: make stress-test [c=container] [d=duration]
stress-test: monitor
	@echo ""
	@echo "💡 Next steps:"
	@echo "   - Run your stress test now (e.g., locust, k6, curl loop)"
	@echo "   - Results will be saved to monitoring_results/"
	@echo "   - Run 'make analyze-csv CSV_FILE=monitoring_results/stress_test_*.csv' to analyze"

## Install monitor script globally for system-wide use
monitor-install: setup-scripts
	@echo "📦 Installing monitor script globally..."
	@sudo install -m 755 scripts/monitor-container.sh /usr/local/bin/monitor-container 2>/dev/null || \
		install -m 755 scripts/monitor-container.sh /usr/local/bin/monitor-container
	@echo "✅ Installed to /usr/local/bin/monitor-container"
	@echo "💡 Usage: monitor-container <container_name> [duration] [interval]"

## Clean monitoring results
monitor-clean:
	@echo "🧹 Cleaning monitoring results..."
	@rm -rf monitoring_results/*
	@echo "✅ Cleaned"

## Detailed resource analysis and worker recommendations
analyze: setup-scripts
	@./scripts/worker_calculator.sh

## Legacy: Old monitor-stress command (redirects to new monitor)
monitor-stress: monitor

## Analyze CSV from stress test (Usage: make analyze-csv CSV_FILE=monitoring_results/stress_test_*.csv)
analyze-csv:
	@if [ -z "${CSV_FILE}" ]; then \
		echo "❌ Error: CSV_FILE required. Usage: make analyze-csv CSV_FILE=path/to/file.csv"; \
		exit 1; \
	fi
	@python3 scripts/analyze_csv.py ${CSV_FILE} --plot

# Legacy commands (for backward compatibility)
# build:
# 	docker build -t mem0-api-server .

# run_local:
# 	docker run -p 8000:8000 -v $(shell pwd):/app mem0-api-server --env-file .env


```

# 1. Makefile for monitor

## 1.1 monitor-container.sh


```bash
#!/bin/bash
# monitor-container.sh - All-in-one Docker container monitoring script
# Usage: ./scripts/monitor-container.sh <container_name> [duration] [interval]
# Or via Makefile: make monitor c=<container>

set -euo pipefail

# ============================================================================
# Configuration (có thể override từ Makefile qua env vars)
# ============================================================================
CONTAINER_NAME="${1:-${MONITOR_CONTAINER:-}}"
DURATION="${2:-${MONITOR_DURATION:-300}}"
INTERVAL="${3:-${MONITOR_INTERVAL:-1}}"
OUTPUT_DIR="${MONITOR_OUTPUT_DIR:-./monitoring_results}"

if [ -z "$CONTAINER_NAME" ]; then
    echo "❌ Error: Container name required"
    echo "Usage: $0 <container_name> [duration] [interval]"
    echo "   Or: MONITOR_CONTAINER=name $0"
    exit 1
fi

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_FILE="${OUTPUT_DIR}/stress_test_${CONTAINER_NAME}_${TIMESTAMP}.csv"
METADATA_FILE="${OUTPUT_DIR}/metadata_${CONTAINER_NAME}_${TIMESTAMP}.json"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# ============================================================================
# Helper Functions
# ============================================================================
log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1" >&2; }
log_warning() { echo -e "${YELLOW}[WARN]${NC} $1"; }

cleanup() {
    if [ -f "$OUTPUT_FILE" ] && [ -s "$OUTPUT_FILE" ]; then
        generate_summary
    fi
    exit 0
}

trap cleanup SIGINT SIGTERM EXIT

# ============================================================================
# Validation
# ============================================================================
validate_environment() {
    if ! docker info > /dev/null 2>&1; then
        log_error "Docker is not running or not accessible"
        exit 1
    fi
    
    if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
        log_error "Container '${CONTAINER_NAME}' is not running"
        log_info "Available containers:"
        docker ps --format "  - {{.Names}}"
        exit 1
    fi
    
    mkdir -p "$OUTPUT_DIR"
}

# ============================================================================
# Unit Conversion
# ============================================================================
convert_to_mb() {
    local value=$1
    local unit=$2
    
    case $unit in
        B|"")      awk "BEGIN {printf \"%.2f\", $value / 1024 / 1024}" ;;
        KiB)       awk "BEGIN {printf \"%.2f\", $value / 1024}" ;;
        MiB)       echo "$value" ;;
        GiB)       awk "BEGIN {printf \"%.2f\", $value * 1024}" ;;
        *)         echo "0" ;;
    esac
}

# ============================================================================
# Save Metadata
# ============================================================================
save_metadata() {
    cat > "$METADATA_FILE" <<EOF
{
  "test_config": {
    "container_name": "$CONTAINER_NAME",
    "duration_seconds": $DURATION,
    "interval_seconds": $INTERVAL,
    "start_time": "$(date -Iseconds)",
    "host": "$(hostname)"
  },
  "container_info": {
    "image": "$(docker inspect "$CONTAINER_NAME" --format '{{.Config.Image}}' 2>/dev/null || echo 'unknown')",
    "status": "$(docker inspect "$CONTAINER_NAME" --format '{{.State.Status}}' 2>/dev/null || echo 'unknown')"
  }
}
EOF
}

# ============================================================================
# Main Monitoring
# ============================================================================
monitor_container() {
    log_info "Starting monitoring: $CONTAINER_NAME"
    log_info "Duration: ${DURATION}s | Interval: ${INTERVAL}s"
    log_info "Output: $OUTPUT_FILE"
    echo ""
    
    # CSV Header
    echo "timestamp,unix_timestamp,cpu_percent,memory_usage_mb,memory_limit_mb,memory_percent,pids" > "$OUTPUT_FILE"
    
    local count=0
    local max_iterations=$((DURATION / INTERVAL))
    
    while [ $count -lt $max_iterations ]; do
        if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
            log_error "Container stopped at iteration $count"
            break
        fi
        
        local stats=$(docker stats --no-stream --format "{{.Container}},{{.CPUPerc}},{{.MemUsage}},{{.MemPerc}},{{.PIDs}}" "$CONTAINER_NAME" 2>/dev/null)
        
        if [ -z "$stats" ]; then
            sleep "$INTERVAL"
            ((count++))
            continue
        fi
        
        IFS=',' read -r container cpu_raw mem_raw mem_perc pids <<< "$stats"
        
        # Parse CPU
        cpu_percent=$(echo "$cpu_raw" | sed 's/%//')
        
        # Parse Memory (handles MiB, GiB, etc.)
        mem_usage_str=$(echo "$mem_raw" | awk '{print $1}')
        mem_limit_str=$(echo "$mem_raw" | awk -F'/' '{print $2}' | awk '{print $1}')
        
        mem_usage_num=$(echo "$mem_usage_str" | sed 's/[^0-9.]//g')
        mem_unit_usage=$(echo "$mem_usage_str" | sed 's/[0-9.]//g' | sed 's/iB//' | sed 's/B//')
        mem_limit_num=$(echo "$mem_limit_str" | sed 's/[^0-9.]//g')
        mem_unit_limit=$(echo "$mem_limit_str" | sed 's/[0-9.]//g' | sed 's/iB//' | sed 's/B//')
        
        mem_usage_mb=$(convert_to_mb "$mem_usage_num" "$mem_unit_usage")
        mem_limit_mb=$(convert_to_mb "$mem_limit_num" "$mem_unit_limit")
        mem_percent_clean=$(echo "$mem_perc" | sed 's/%//')
        
        # Write to CSV
        echo "$(date '+%Y-%m-%d %H:%M:%S'),$(date +%s),$cpu_percent,$mem_usage_mb,$mem_limit_mb,$mem_percent_clean,$pids" >> "$OUTPUT_FILE"
        
        # Progress bar
        ((count++))
        local progress=$((count * 100 / max_iterations))
        local bar_len=$((progress / 2))
        local bar=$(printf '#%.0s' $(seq 1 $bar_len))
        printf "\r⏳ Progress: [%-50s] %d%% (%d/%d) | CPU: %s%% | MEM: %s%%" \
            "$bar" "$progress" "$count" "$max_iterations" "$cpu_percent" "$mem_percent_clean"
        
        sleep "$INTERVAL"
    done
    
    echo ""
    log_info "Monitoring completed ✓"
}

# ============================================================================
# Generate Summary
# ============================================================================
generate_summary() {
    if [ ! -f "$OUTPUT_FILE" ] || [ ! -s "$OUTPUT_FILE" ]; then
        return
    fi
    
    local summary_file="${OUTPUT_DIR}/summary_${CONTAINER_NAME}_${TIMESTAMP}.txt"
    
    local avg_cpu=$(awk -F',' 'NR>1 && $3!="" {sum+=$3; count++} END {if(count>0) printf "%.2f", sum/count; else print "0"}' "$OUTPUT_FILE")
    local max_cpu=$(awk -F',' 'NR>1 && $3!="" {if($3>max || NR==2) max=$3} END {printf "%.2f", max}' "$OUTPUT_FILE")
    local min_cpu=$(awk -F',' 'NR>1 && $3!="" {if($3<min || NR==2) min=$3} END {printf "%.2f", min}' "$OUTPUT_FILE")
    
    local avg_mem=$(awk -F',' 'NR>1 && $4!="" {sum+=$4; count++} END {if(count>0) printf "%.2f", sum/count; else print "0"}' "$OUTPUT_FILE")
    local max_mem=$(awk -F',' 'NR>1 && $4!="" {if($4>max || NR==2) max=$4} END {printf "%.2f", max}' "$OUTPUT_FILE")
    local min_mem=$(awk -F',' 'NR>1 && $4!="" {if($4<min || NR==2) min=$4} END {printf "%.2f", min}' "$OUTPUT_FILE")
    
    local mem_limit=$(awk -F',' 'NR==2 && $5!="" {printf "%.2f", $5}' "$OUTPUT_FILE")
    
    cat > "$summary_file" <<EOF
================================================================================
Stress Test Summary Report
================================================================================
Container: $CONTAINER_NAME
Test Duration: ${DURATION}s
Timestamp: $(date)
Host: $(hostname)

--- CPU Statistics ---
Average CPU:  ${avg_cpu}%
Max CPU:      ${max_cpu}%
Min CPU:      ${min_cpu}%

--- Memory Statistics ---
Average Memory: ${avg_mem} MB
Max Memory:     ${max_mem} MB
Min Memory:     ${min_mem} MB
Memory Limit:   ${mem_limit} MB

--- Files ---
Raw Data:  $OUTPUT_FILE
Metadata:  $METADATA_FILE
================================================================================
EOF
    
    cat "$summary_file"
    log_info "Summary saved: $summary_file"
}

# ============================================================================
# Main Execution
# ============================================================================
main() {
    validate_environment
    save_metadata
    monitor_container
}

main "$@"


```


---
`
## 1.2 worker_calculator.sh

```bash
#!/bin/bash
# Worker Calculator - Helps determine optimal number of workers
# Based on CPU cores and expected workload

echo "🧮 Worker Calculator for Uvicorn/FastAPI"
echo "========================================"
echo ""

# Get CPU cores available - try CpuQuota first, then NanoCpus
CPU_QUOTA=$(docker inspect mem0-server --format='{{.HostConfig.CpuQuota}}' 2>/dev/null)
CPU_PERIOD=$(docker inspect mem0-server --format='{{.HostConfig.CpuPeriod}}' 2>/dev/null)
NANO_CPUS=$(docker inspect mem0-server --format='{{.HostConfig.NanoCpus}}' 2>/dev/null)

if [ -n "$NANO_CPUS" ] && [ "$NANO_CPUS" != "0" ] && [ "$NANO_CPUS" != "<no value>" ]; then
    CPU_CORES=$(awk "BEGIN {printf \"%.1f\", $NANO_CPUS / 1000000000}")
    echo "✅ CPU Limit: $CPU_CORES cores (from NanoCpus)"
elif [ -n "$CPU_QUOTA" ] && [ "$CPU_QUOTA" != "0" ] && [ "$CPU_QUOTA" != "<no value>" ] && [ -n "$CPU_PERIOD" ]; then
    CPU_CORES=$(awk "BEGIN {printf \"%.1f\", $CPU_QUOTA / $CPU_PERIOD}")
    echo "✅ CPU Limit: $CPU_CORES cores (from CpuQuota/CpuPeriod)"
else
    echo "⚠️  CPU limit not set in Docker. Getting host CPU count..."
    CPU_CORES=$(docker exec mem0-server nproc 2>/dev/null || echo "2")
    echo "   Using host CPU cores: $CPU_CORES (but recommend setting CPU limit in docker-compose.yml)"
fi

# Get current memory limit
MEM_GB=$(docker inspect mem0-server --format='{{.HostConfig.Memory}}' 2>/dev/null | awk '{if($1) printf "%.2f", $1/1024/1024/1024; else print "unlimited"}')
echo "✅ Memory Limit: ${MEM_GB} GB"
echo ""

# Get current worker count - check actual uvicorn processes
CURRENT_WORKERS=$(docker exec mem0-server sh -c 'ps aux | grep "[u]vicorn.*worker" | wc -l' 2>/dev/null | tr -d ' \n')
if [ -z "$CURRENT_WORKERS" ] || [ "$CURRENT_WORKERS" = "0" ]; then
    # Try to get from command line in docker-compose or inspect
    CMD_ARGS=$(docker inspect mem0-server --format='{{range .Config.Cmd}}{{.}} {{end}}' 2>/dev/null)
    # Extract --workers N using awk (more portable than grep -oE)
    CURRENT_WORKERS=$(echo "$CMD_ARGS" | awk '{
        for(i=1; i<=NF; i++) {
            if($i == "--workers" && i+1 <= NF) {
                print $(i+1);
                exit
            }
        }
    }' || echo "unknown")
fi
echo "👷 Current Workers: $CURRENT_WORKERS"
echo ""

echo "📐 Recommended Worker Calculation:"
echo "-----------------------------------"

# Formula: Workers = (2 × CPU cores) + 1
# This is a common rule of thumb for I/O-bound applications like FastAPI
if [[ "$CPU_CORES" =~ ^[0-9]+\.?[0-9]*$ ]]; then
    RECOMMENDED=$(awk "BEGIN {printf \"%.0f\", $CPU_CORES * 2 + 1}")
    
    # Conservative estimate (1 worker per core)
    CONSERVATIVE=$(awk "BEGIN {printf \"%.0f\", $CPU_CORES}")
    
    # Aggressive estimate (4 workers per core, max 16)
    AGGRESSIVE=$(awk "BEGIN {result=$CPU_CORES * 4; if(result>16) print 16; else printf \"%.0f\", result}")
    
    echo "   Conservative (1x CPU):    $CONSERVATIVE workers"
    echo "   Recommended (2x+1):       $RECOMMENDED workers  ⭐"
    echo "   Aggressive (4x CPU):      $AGGRESSIVE workers"
    echo ""
    
    echo "💡 Explanation:"
    echo "   - For I/O-bound apps (API, database calls): Use 2-4x CPU cores"
    echo "   - For CPU-bound apps: Use 1x CPU cores"
    echo "   - FastAPI is typically I/O-bound, so 2x+1 is recommended"
    echo ""
    
    if [[ "$CURRENT_WORKERS" =~ ^[0-9]+$ ]] && [ "$CURRENT_WORKERS" -ne "$RECOMMENDED" ]; then
        echo "⚠️  Current workers ($CURRENT_WORKERS) differs from recommended ($RECOMMENDED)"
        echo ""
        echo "To change workers, edit docker-compose-app.yml line 21:"
        echo "   command: uvicorn main:app --host 0.0.0.0 --port 8000 --workers $RECOMMENDED --loop uvloop --http httptools"
        echo ""
        echo "Then restart:"
        echo "   make restart-app"
    else
        echo "✅ Worker count matches recommendation!"
    fi
    
    # Memory check
    if [[ "$MEM_GB" != "unlimited" ]] && [[ "$MEM_GB" =~ ^[0-9]+\.?[0-9]*$ ]]; then
        MEM_PER_WORKER=$(awk "BEGIN {printf \"%.2f\", $MEM_GB / $RECOMMENDED}")
        echo ""
        echo "📊 Memory per worker (estimated): ${MEM_PER_WORKER} GB"
        
        LOW_MEM_CHECK=$(awk "BEGIN {if ($MEM_PER_WORKER < 0.25) print 1; else print 0}")
        HIGH_MEM_CHECK=$(awk "BEGIN {if ($MEM_PER_WORKER > 1) print 1; else print 0}")
        
        if [ "$LOW_MEM_CHECK" -eq 1 ]; then
            echo "   ⚠️  Low memory per worker! Consider increasing memory limit"
        elif [ "$HIGH_MEM_CHECK" -eq 1 ]; then
            echo "   ✅ Sufficient memory per worker"
        fi
    fi
else
    echo "⚠️  Cannot determine CPU cores. Using default recommendation:"
    echo "   Recommended: 4-8 workers"
fi

echo ""
echo "🔍 To monitor actual usage:"
echo "   make monitor        # Monitor for 60 seconds"
echo "   make monitor-quick  # Quick stats snapshot"


```