# Infrastructure & Containerization — Production Best Practices

> **Domain:** 5.13 | **Group:** CROSS | **Lifecycle:** Cross-Cutting
> **Last Updated:** 2026-03-13

## 1. Overview

Infrastructure is the foundation enabling application reliability, scalability, and resilience. This domain covers containerization with Docker, orchestration with Kubernetes, Infrastructure-as-Code principles, and cloud platform selection. Modern production systems are built on immutable infrastructure, declarative configuration, and automated scaling—not manual server management.

**Vietnamese:** Infrastructure production phải là immutable, declarative, và auto-scale. Không bao giờ SSH vào server để fix issues thủ công.

## 2. Core Principles

- **Immutable Infrastructure:** Containers are never modified after deployment; redeploy instead
- **Infrastructure as Code:** All infrastructure defined in version-controlled configuration, no manual changes
- **Declarative Configuration:** Describe desired state, let orchestrator handle transition
- **Cattle not Pets:** Servers/containers are disposable; don't name and cherish them individually
- **Containerization:** Isolated, reproducible, portable application environments
- **Horizontal Scaling:** Scale by adding more instances, not bigger instances
- **Automated Deployment:** CI/CD pipelines push code from repo to production with zero downtime

## 3. Best Practices

### 3.1 Docker Best Practices

**Practice: Multi-Stage Builds for Smaller Images**
- **What:** Use multiple FROM statements to separate build from runtime
- **Why:** Reduces image size (no build tools, source code, or test files in final image), faster pulls, less attack surface
- **How:**
  ```dockerfile
  # Stage 1: Build
  FROM node:18-alpine as builder
  WORKDIR /app
  COPY package*.json ./
  RUN npm ci --only=production && npm run build

  # Stage 2: Runtime (only runtime dependencies)
  FROM node:18-alpine
  WORKDIR /app
  RUN addgroup -g 1000 appuser && adduser -D -u 1000 -G appuser appuser
  COPY --from=builder /app/node_modules ./node_modules
  COPY --from=builder /app/dist ./dist
  COPY package*.json ./
  USER appuser
  EXPOSE 3000
  CMD ["node", "dist/index.js"]
  ```
  - Stage 1 (builder): ~800MB with build tools, npm scripts, dev dependencies
  - Stage 2 (runtime): ~200MB with only production runtime
  - Final image uses only Stage 2 (600MB reduction)
- **Anti-pattern:** Single stage with all dependencies included, 'latest' base image without version pinning, running as root

**Practice: .dockerignore & Layer Optimization**
- **What:** Exclude files from Docker build context and minimize layer counts
- **Why:** Faster builds, smaller context transfer, fewer unnecessary cache invalidations
- **How:**
  ```dockerfile
  # .dockerignore (similar to .gitignore)
  node_modules/
  npm-debug.log
  dist/
  .git
  .env
  .DS_Store
  coverage/
  __pycache__/
  *.pyc

  # Dockerfile with optimized layers
  FROM node:18-alpine
  WORKDIR /app

  # Dependencies (separate layer, cached)
  COPY package*.json ./
  RUN npm ci --only=production

  # Source code (changes frequently)
  COPY src ./src
  RUN npm run build

  # Runtime config (changes at deployment)
  COPY .env.production ./
  CMD ["node", "dist/index.js"]
  ```
  - Layer order: dependencies first (rarely change) → source code (frequent) → config (deployment-time)
  - Each RUN creates new layer; combine when possible: `RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*`
  - Use BuildKit: `DOCKER_BUILDKIT=1 docker build` for parallel layers and better caching
- **Anti-pattern:** Large build context (MB of files), layers that could be combined, committing node_modules to git, no layer caching strategy

**Practice: Non-Root User & Security Context**
- **What:** Run application as unprivileged user, use read-only filesystem where possible
- **Why:** Limits container escape impact, prevents privilege escalation, follows principle of least privilege
- **How:**
  ```dockerfile
  # Create non-root user
  RUN addgroup -g 1000 appuser && adduser -D -u 1000 -G appuser appuser

  # Copy with ownership
  COPY --chown=appuser:appuser . /app

  # Set working directory and switch user
  WORKDIR /app
  USER appuser

  EXPOSE 3000
  CMD ["node", "index.js"]
  ```
  - Kubernetes security context:
  ```yaml
  apiVersion: v1
  kind: Pod
  spec:
    securityContext:
      runAsNonRoot: true
      runAsUser: 1000
      fsGroup: 1000
    containers:
    - name: app
      image: myapp:latest
      securityContext:
        readOnlyRootFilesystem: true
        allowPrivilegeEscalation: false
        capabilities:
          drop:
            - ALL
      volumeMounts:
      - name: tmp
        mountPath: /tmp
    volumes:
    - name: tmp
      emptyDir: {}
  ```
  - Read-only filesystem prevents malicious processes from modifying application code
  - Temporary directories (emptyDir) needed for logs, caches
- **Anti-pattern:** Running as root, no security context, not testing under non-root conditions

### 3.2 Container Orchestration

**Practice: Kubernetes Declarative Deployments**
- **What:** Define desired state in YAML, Kubernetes maintains it automatically
- **Why:** Self-healing (restarts failed pods), rolling updates, service discovery, persistent storage
- **How:**
  ```yaml
  # Deployment: replicated application
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: myapp
  spec:
    replicas: 3
    strategy:
      type: RollingUpdate
      rollingUpdate:
        maxSurge: 1
        maxUnavailable: 0
    selector:
      matchLabels:
        app: myapp
    template:
      metadata:
        labels:
          app: myapp
      spec:
        containers:
        - name: app
          image: myapp:1.2.3
          ports:
          - containerPort: 3000
          env:
          - name: NODE_ENV
            value: production
          resources:
            requests:
              memory: 256Mi
              cpu: 100m
            limits:
              memory: 512Mi
              cpu: 500m
          livenessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 5

  # Service: load balancing and DNS
  apiVersion: v1
  kind: Service
  metadata:
    name: myapp-service
  spec:
    type: ClusterIP
    selector:
      app: myapp
    ports:
    - port: 80
      targetPort: 3000
  ```
  - Replicas: horizontal scaling handled by Kubernetes
  - RollingUpdate: new pods start before old ones terminate (zero downtime)
  - Probes: liveness (is container alive?), readiness (is container ready to serve?)
  - Resources: request (min guaranteed), limit (max allowed)
- **Anti-pattern:** Manual pod creation, no health checks, not using Services, resource limits allowing noisy neighbors

**Practice: Horizontal Pod Autoscaling (HPA)**
- **What:** Automatically scale number of replicas based on metrics
- **Why:** Cost optimization (scale down during low traffic), automatic handling of traffic spikes
- **How:**
  ```yaml
  apiVersion: autoscaling/v2
  kind: HorizontalPodAutoscaler
  metadata:
    name: myapp-hpa
  spec:
    scaleTargetRef:
      apiVersion: apps/v1
      kind: Deployment
      name: myapp
    minReplicas: 2
    maxReplicas: 10
    metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
  ```
  - Scales between 2 (always on) and 10 (peak load) replicas
  - Increases replicas when CPU or memory exceeds threshold
  - Decreases gradually (avoids flapping)
- **Anti-pattern:** No autoscaling (expensive), scaling only on CPU (ignores memory), min/max replicas not adjusted for actual load

### 3.3 Infrastructure as Code

**Practice: Terraform for Cloud Infrastructure**
- **What:** Define infrastructure (compute, storage, networking) in HCL code
- **Why:** Version control, auditability, reproducibility, drift detection, automation
- **How:**
  ```hcl
  # main.tf - AWS infrastructure
  terraform {
    required_version = ">= 1.0"
    required_providers {
      aws = {
        source  = "hashicorp/aws"
        version = "~> 5.0"
      }
    }
    backend "s3" {
      bucket         = "my-terraform-state"
      key            = "prod/terraform.tfstate"
      region         = "us-east-1"
      encrypt        = true
      dynamodb_table = "terraform-lock"
    }
  }

  provider "aws" {
    region = var.aws_region
  }

  # VPC
  resource "aws_vpc" "main" {
    cidr_block           = "10.0.0.0/16"
    enable_dns_hostnames = true
    enable_dns_support   = true

    tags = {
      Name = "myapp-vpc"
    }
  }

  # EC2 instance
  resource "aws_instance" "app" {
    ami           = "ami-0c55b159cbfafe1f0"  # Amazon Linux 2
    instance_type = "t3.medium"
    vpc_security_group_ids = [aws_security_group.app.id]

    user_data = base64encode(file("${path.module}/scripts/init.sh"))

    tags = {
      Name = "myapp-instance"
    }
  }

  output "instance_ip" {
    value = aws_instance.app.private_ip
  }
  ```
  - State file: stores real infrastructure state (commit to git with encryption or remote backend)
  - Remote backend: S3 with encryption for team collaboration
  - Apply: `terraform plan` (preview) → review → `terraform apply` (deploy)
- **Anti-pattern:** No state file tracking, manual infrastructure changes, hardcoded credentials, no remote backend

**Practice: Container Image Scanning & Artifact Management**
- **What:** Scan images for vulnerabilities before deployment, manage image versions
- **Why:** Prevents deploying images with known CVEs, ensures reproducibility
- **How:**
  ```bash
  # Build and scan with Trivy
  docker build -t myapp:1.2.3 .
  trivy image myapp:1.2.3
  # Output: HIGH severity vulnerabilities in base image

  # Use distroless images (minimal, less CVEs)
  FROM node:18-alpine as builder
  ...
  FROM gcr.io/distroless/nodejs18-debian11
  COPY --from=builder /app /app
  CMD ["app.js"]

  # Push to registry with tag (never 'latest' in production)
  docker tag myapp:1.2.3 registry.example.com/myapp:1.2.3
  docker push registry.example.com/myapp:1.2.3

  # Reference exact digest for immutability
  kubectl set image deployment/myapp \
    app=registry.example.com/myapp@sha256:abc123...
  ```
  - Trivy scans for OS package vulnerabilities
  - Grype scans for application dependency vulnerabilities
  - Pin image version (not 'latest'), use digests for immutability
  - Rebuild images to pick up base OS patches monthly
- **Anti-pattern:** Using 'latest' tag in production, no vulnerability scanning, ignoring CVEs, not updating base images

### 3.4 Cloud Platforms & Network Architecture

**Practice: Load Balancing & Service Mesh**
- **What:** Distribute traffic across instances, manage service-to-service communication
- **Why:** No single point of failure, automatic failover, traffic routing rules
- **How:**
  ```yaml
  # Kubernetes Ingress: API gateway
  apiVersion: networking.k8s.io/v1
  kind: Ingress
  metadata:
    name: myapp-ingress
  spec:
    ingressClassName: nginx
    rules:
    - host: api.example.com
      http:
        paths:
        - path: /
          pathType: Prefix
          backend:
            service:
              name: myapp-service
              port:
                number: 80
    tls:
    - hosts:
      - api.example.com
      secretName: tls-cert

  # Service Mesh (Istio): advanced traffic management
  apiVersion: networking.istio.io/v1beta1
  kind: VirtualService
  metadata:
    name: myapp
  spec:
    hosts:
    - myapp
    http:
    - match:
      - uri:
          prefix: /api/v2
      route:
      - destination:
          host: myapp
          subset: v2
        weight: 100
      timeout: 10s
      retries:
        attempts: 3
        perTryTimeout: 2s
    - route:
      - destination:
          host: myapp
          subset: v1
        weight: 100
  ```
  - Ingress: Layer 7 (HTTP) load balancing, TLS termination, routing rules
  - Service Mesh: circuit breaking, retry logic, distributed tracing, mutual TLS
- **Anti-pattern:** No load balancing (single instance failure = outage), no circuit breakers (cascading failures), no health checks

**Practice: Auto-Scaling & Cost Optimization**
- **What:** Scale infrastructure based on demand, rightsize instances
- **Why:** Reduces cost during off-peak, ensures capacity for spikes
- **How:**
  ```bash
  # AWS Auto Scaling Group
  aws autoscaling create-auto-scaling-group \
    --auto-scaling-group-name myapp-asg \
    --launch-template LaunchTemplateName=myapp-lt,Version=1 \
    --min-size 2 \
    --desired-capacity 3 \
    --max-size 10 \
    --vpc-zone-identifier "subnet-1,subnet-2,subnet-3"

  # Scaling policy based on CPU
  aws autoscaling put-scaling-policy \
    --auto-scaling-group-name myapp-asg \
    --policy-name scale-up \
    --policy-type TargetTrackingScaling \
    --target-tracking-configuration file://target-tracking-config.json

  # Scheduled scaling (e.g., business hours scale up)
  aws autoscaling put-scheduled-action \
    --auto-scaling-group-name myapp-asg \
    --scheduled-action-name morning-scale-up \
    --recurrence "0 8 * * MON-FRI" \
    --desired-capacity 10
  ```
  - Target tracking: maintain 70% CPU utilization
  - Scheduled scaling: known traffic patterns (e.g., 9am spike)
  - Spot instances: 70% discount, but can be interrupted (use mix of on-demand + spot)
- **Anti-pattern:** Fixed provisioning (expensive), no cost allocation tags, no reserved instance optimization

### 3.5 Disaster Recovery

**Practice: Backup & Restore Strategy**
- **What:** Regular automated backups with tested restore procedures
- **Why:** Recovery from data corruption, ransomware, accidental deletion
- **How:**
  ```bash
  # Database backups with retention
  # Daily automated backups, 30-day retention
  AWS RDS Automated Backups: enabled with 30-day backup retention period

  # Manual snapshot for long-term archival
  aws rds create-db-snapshot \
    --db-instance-identifier myapp-db \
    --db-snapshot-identifier myapp-db-backup-2024-03-13

  # Test restore in non-prod environment monthly
  aws rds restore-db-instance-from-db-snapshot \
    --db-instance-identifier myapp-db-test \
    --db-snapshot-identifier myapp-db-backup-2024-03-13

  # Application-level backups
  # Postgres: pg_dump with encryption
  pg_dump -U postgres -d myapp -F custom > /backup/myapp.dump
  gpg --symmetric /backup/myapp.dump  # Encrypt

  # Restore
  gpg --decrypt /backup/myapp.dump.gpg | pg_restore -d myapp -
  ```
  - RTO (Recovery Time Objective): How fast must service be restored? (target: <1 hour for critical)
  - RPO (Recovery Point Objective): How much data loss acceptable? (target: <15 minutes)
  - Test restores quarterly; backup without restore plan is worthless
- **Anti-pattern:** No backups, untested restore procedures, too-long retention policies (expensive), no encryption of backups

## 4. Decision Frameworks

**Container Orchestration Choice:**
| Criteria | Docker Swarm | Kubernetes | Serverless |
|----------|--------------|-----------|-----------|
| Complexity | Low | High | Medium |
| Scalability | Medium | High | Very High |
| Cost | Low | Medium | High (pay per execution) |
| Best for | Small teams, simple apps | Production, enterprise | Event-driven, variable load |

**Cloud Provider Selection (AWS vs GCP vs Azure):**
- **AWS:** Largest service portfolio, mature tools (Terraform support), most jobs market
- **GCP:** Cheaper compute, excellent Kubernetes (GKE), best for data analytics
- **Azure:** Best for enterprises with Microsoft stack (Active Directory, Exchange), strong .NET support

## 5. Checklist

- [ ] Docker images use multi-stage builds and are < 500MB
- [ ] Non-root user configured in Dockerfile
- [ ] Health checks (liveness + readiness) configured in Kubernetes
- [ ] Resource requests and limits set for all containers
- [ ] Horizontal Pod Autoscaler configured for production workloads
- [ ] All infrastructure defined in Terraform/IaC (no manual changes)
- [ ] Container images scanned for vulnerabilities before deployment
- [ ] Immutable tags used (image digests, not 'latest')
- [ ] Load balancing configured with health checks
- [ ] Auto-scaling policies tested under load
- [ ] Backup and restore procedures tested monthly
- [ ] Network policies restrict traffic to necessary ports only
- [ ] TLS enforced for all service-to-service communication
- [ ] Disaster recovery runbook documented with RTO/RPO targets
- [ ] Cost allocation tags applied to all resources
- [ ] Log aggregation configured (ELK, CloudWatch, Splunk)

## 6. Common Mistakes & Anti-Patterns

1. **Running as root in containers** → Always add non-root user
2. **Using 'latest' image tag** → Pin versions, use digests for immutability
3. **No resource limits** → Other workloads can starve your app (noisy neighbor)
4. **Manual infrastructure changes** → Everything via Terraform/IaC, delete manual resources
5. **Not testing failover** → Test disaster recovery scenarios quarterly
6. **Single database without replication** → One bad query = entire outage
7. **No autoscaling, fixed provisioning** → Too expensive or not resilient enough
8. **Overly complex Kubernetes setup** → Start simple, add complexity when needed
9. **No network policies** → Pods can talk to everything (lateral movement risk)
10. **Backup without restore tests** → Backup system that can't restore is useless

## 7. Tools & References

**Containerization:**
- Docker, Podman (OCI-compliant alternatives)

**Orchestration:**
- Kubernetes (K8s), Docker Swarm, HashiCorp Nomad

**Infrastructure as Code:**
- Terraform, Pulumi, AWS CloudFormation, Ansible

**Scanning & Security:**
- Trivy, Grype, Snyk, Clair (image scanning)

**Cloud Platforms:**
- AWS (EC2, ECS, EKS), Google Cloud (Compute Engine, GKE), Azure (VMs, AKS)

**Monitoring & Logging:**
- Prometheus, Grafana, ELK Stack, Datadog, New Relic

---

**Vietnamese Note:** Infrastructure là code, không phải sự kiện thủ công. Tất cả phải định nghĩa trong IaC, tracked trong git, deployed qua CI/CD. (Infrastructure is code, not manual events. Everything must be defined in IaC, tracked in git, deployed via CI/CD.)
