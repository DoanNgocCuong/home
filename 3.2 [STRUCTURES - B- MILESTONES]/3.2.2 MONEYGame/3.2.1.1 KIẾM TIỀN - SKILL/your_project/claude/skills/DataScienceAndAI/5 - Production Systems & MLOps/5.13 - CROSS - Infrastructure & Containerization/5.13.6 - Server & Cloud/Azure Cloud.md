

![](https://user-gen-media-assets.s3.amazonaws.com/seedream_images/2afcdea9-a830-46a4-af83-a4ce695137c1.png)



<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Azure container registry

Tuyệt vời! Bây giờ tôi sẽ tạo báo cáo tóm tắt trong một định dạng dễ đọc.

## 📋 **DEEP RESEARCH: Azure Container Registry (ACR)** - Báo Cáo Toàn Diện

Tôi đã hoàn thành một **báo cáo nghiên cứu sâu (1,330 dòng)** về Azure Container Registry với các nội dung chính:

***

## 📚 **Nội Dung Chính Của Báo Cáo:**

### **1. Giới Thiệu \& Kiến Trúc**

- Khái niệm ACR và khi nào nên dùng
- So sánh ACR vs Docker Hub
- Kiến trúc chi tiết với data flow (push/pull operations)


### **2. SKU Comparison \& Pricing**

| Tier | Daily Price | Storage | Use Case |
| :-- | :-- | :-- | :-- |
| **Basic** | \$0.167 | 10 GB | Dev/Test |
| **Standard** | \$0.667 | 100 GB | Production |
| **Premium** | \$1.34 | 500 GB | Enterprise |

- Geo-replication, private endpoints, content trust (Premium only)
- Cost optimization strategies tiết kiệm 10-70%


### **3. ACR Tasks - Automation** ⭐

- **Trigger types:** Manual, Code commit, Base image update, Schedule
- **Multi-step builds:** Build → Test → Scan → Push
- **YAML configuration examples**
- **Cost:** ~\$0.01 per build minute


### **4. Authentication \& Authorization** 🔐

- 4 phương pháp: Entra ID, Service Principal, Managed Identity, Admin account
- RBAC roles: AcrPull, AcrPush, AcrDelete, AcrImageSigner
- Repository-scoped tokens for fine-grained control


### **5. Networking \& Security**

- **Private Endpoints** + Azure Private Link (Premium)
- **Image Signing** với Docker Content Trust
- **Vulnerability Scanning** tích hợp Defender for Cloud
- **Encryption:** At-rest \& in-transit (HTTPS/TLS)


### **6. Image Lifecycle Management**

- **Retention policies:** Auto-delete untagged images
- **Soft delete:** Recover deleted images trong 7 ngày
- **Image locking:** Prevent accidental deletion


### **7. Deployment Patterns**

- **Kubernetes (AKS)** - Managed Identity authentication
- **Azure Container Instances (ACI)**
- **App Service** - Continuous deployment
- **GitHub Actions \& Azure DevOps** - Complete CI/CD examples


### **8. Best Practices**

- Dockerfile optimization (multi-stage builds)
- Naming \& tagging strategy
- Performance tuning (layer caching, artifact streaming)
- Monitoring \& alerting setup


### **9. Troubleshooting \& Performance**

- Common issues \& solutions (401, 403, timeout, throttling)
- Expected latencies: 50-300ms
- Debugging commands


### **10. Competitor Comparison**

- **Docker Hub:** Cheaper, less features, rate limited
- **Quay.io:** Multi-cloud, flat-rate pricing
- **Harbor:** Self-hosted, full customization

***

## 🎯 **Key Insights:**

1. **Premium SKU recommended** cho enterprise (geo-replication, private endpoints, content trust)
2. **ACR Tasks vs Local Docker:**
    - ACR Tasks: Serverless, no infrastructure, auto-trigger, \$0.01/min
    - Docker: Full control, local testing, higher operational cost
3. **Authentication Priority:**
    - ✅ Managed Identity (best - no secrets)
    - ✅ Service Principal (good - for CI/CD)
    - ⚠️ Admin account (avoid - shared credential)
    - ✅ Entra ID (best for humans)
4. **Security Checklist:**
    - [ ] Enable private endpoints (Premium)
    - [ ] Configure image scanning
    - [ ] Enable content trust (if needed)
    - [ ] Use Managed Identity
    - [ ] Implement least-privilege RBAC
    - [ ] Enable audit logging
5. **Cost Optimization:**
    - Delete old images = 10-30% savings
    - Use Alpine base = 50-70% smaller
    - Multi-stage builds = 40-60% smaller

***

## 📊 **Quick Reference:**

```bash
# Create registry
az acr create --resource-group myrg --name myregistry --sku Premium

# Build and push
az acr build --registry myregistry --image myapp:v1.0.0 .

# Setup CI/CD trigger
az acr task create \
  --registry myregistry \
  --name buildOnPush \
  --image myapp:{{.SourceTriggerID}} \
  --context https://github.com/user/repo.git \
  --file Dockerfile

# Create managed identity authentication
az aks update --resource-group myrg --name myaks --attach-acr myregistry

# Enable vulnerability scanning
az support ticket create --issue-type "service-and-subscription-limits"
```


***

## 📌 **When to Use ACR:**

✅ **Ideal for:**

- Azure-first organizations (AKS, App Service)
- Native integration with Azure DevOps/GitHub
- Enterprise security + compliance
- High availability + geo-distribution
- .NET/Windows container workloads

❌ **Consider alternatives:**

- Multi-cloud strategy → Quay.io, Harbor
- Budget constraint → Docker Hub
- On-premises deployment → Harbor
- Customization requirements → Self-hosted

***

## 📁 **Deliverable:**

Báo cáo được lưu tại: **`Azure_Container_Registry_Deep_Research.md`**

Nội dung bao gồm:

- ✅ 1,330 dòng chi tiết
- ✅ 50+ code examples (Bash, YAML, PowerShell)
- ✅ 15+ tables \& comparisons
- ✅ Architecture diagrams (ASCII)
- ✅ Troubleshooting guides
- ✅ Quick reference commands
- ✅ Enterprise best practices

***

**Có gì bạn muốn tìm hiểu thêm về ACR hoặc các Azure services khác?** 🚀
<span style="display:none">[^1][^10][^11][^12][^13][^14][^15][^16][^17][^18][^19][^2][^20][^21][^22][^23][^24][^25][^26][^27][^28][^29][^3][^30][^31][^32][^33][^34][^35][^36][^37][^38][^39][^4][^40][^41][^42][^43][^44][^45][^46][^47][^48][^49][^5][^50][^51][^52][^53][^54][^55][^56][^57][^58][^6][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: https://azure.microsoft.com/en-us/pricing/details/container-registry/

[^2]: https://learn.microsoft.com/en-us/azure/container-registry/container-registry-skus

[^3]: https://azure.microsoft.com/en-us/pricing

[^4]: https://docs.azure.cn/en-us/container-registry/container-registry-storage

[^5]: https://azure.microsoft.com/en-us/pricing/details/container-apps/

[^6]: https://hasangural.com/automated-docker-image-updates-part-1

[^7]: https://circleci.com/docs/guides/deploy/deploy-to-azure-container-registry/

[^8]: https://www.linkedin.com/pulse/azure-acr-cost-optimization-practices-best-strategies-reduce-i4muc

[^9]: https://www.geeksforgeeks.org/devops/azure-container-registry-for-docker-container-management/

[^10]: https://learn.microsoft.com/en-us/azure/container-instances/container-instances-using-azure-container-registry

[^11]: https://shipyard.build/blog/container-registries/

[^12]: https://www.youtube.com/watch?v=vaDIWadpquA

[^13]: https://www.jorgebernhardt.com/terraform-azure-container-registry/

[^14]: https://www.theknowledgeacademy.com/blog/azure-container-registry/

[^15]: https://notes.kodekloud.com/docs/AZ-204-Developing-Solutions-for-Microsoft-Azure/Managing-Container-Images-in-Azure-Container-Registry/Building-and-Managing-Containers-With-ACR-Tasks

[^16]: https://www.youtube.com/watch?v=cvKwvGNrRJo

[^17]: https://azure.microsoft.com/en-us/blog/azure-container-registry-now-generally-available/

[^18]: https://parveensingh.com/how-to-build-and-publish-a-docker-image-to-azure-container-registry/

[^19]: https://learn.microsoft.com/en-us/azure/container-registry/

[^20]: https://bluelight.co/blog/how-to-choose-a-container-registry

[^21]: https://learn.microsoft.com/en-us/azure/container-registry/container-registry-tutorial-quick-task

[^22]: https://azure.github.io/acr/tasks/container-registry-tasks-overview.html

[^23]: https://learn.microsoft.com/en-us/azure/container-registry/container-registry-tutorial-build-task

[^24]: https://docs.azure.cn/en-us/container-registry/container-registry-tutorial-build-task

[^25]: https://learn.microsoft.com/en-us/azure/container-registry/container-registry-auth-service-principal

[^26]: https://docs.aws.amazon.com/AmazonECR/latest/userguide/LifecyclePolicies.html

[^27]: https://azure.github.io/AppService/2021/11/01/how-to-setup-continuous-deployment-using-acr-tasks-with-windows-containers.html

[^28]: https://learn.microsoft.com/en-us/azure/container-registry/container-registry-auth-service-principal?WT.mc_id=stackoverflow-stackoverflow-nepeters

[^29]: https://distr.sh/glossary/oci-container-artifact-registry/

[^30]: https://www.youtube.com/watch?v=oCPFomcij3w

[^31]: https://learn.microsoft.com/en-us/azure/container-registry/container-registry-authentication-managed-identity

[^32]: https://stackoverflow.com/questions/70360107/azure-container-registry-retention-policy

[^33]: https://docs.azure.cn/en-us/container-registry/container-registry-tutorial-base-image-update

[^34]: https://docs.azure.cn/en-us/container-registry/container-registry-tasks-authentication-managed-identity

[^35]: https://github.com/Azure-Samples/acr-tasks

[^36]: https://external-secrets.io/v0.9.10/api/generator/acr/

[^37]: https://platformengineering.org/tools/azure-container-registry

[^38]: https://www.reddit.com/r/AZURE/comments/sforfm/is_there_any_reason_to_use_acr_tasks_over_azure/

[^39]: https://learn.microsoft.com/en-us/azure/container-registry/container-registry-private-link

[^40]: https://github.com/andriktr/private-azure-acr/blob/main/README.md

[^41]: https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-overview

[^42]: https://docs.azure.cn/en-us/container-registry/container-registry-dedicated-data-endpoints

[^43]: https://cloud.redhat.com/experts/aro/aro-acr/

[^44]: https://www.aquasec.com/blog/image-vulnerability-scanning-in-azure-container-registry/

[^45]: https://learn.microsoft.com/en-us/azure/container-registry/container-registry-content-trust

[^46]: https://www.youtube.com/watch?v=0OzMJyyvgWs

[^47]: https://docs.azure.cn/en-us/defender-for-cloud/agentless-vulnerability-assessment-azure

[^48]: https://avd.aquasec.com/misconfig/azure/container-registry/acr-content-trust-enabled/

[^49]: https://learn.microsoft.com/en-us/cli/azure/acr/private-endpoint-connection?view=azure-cli-latest

[^50]: https://www.wiz.io/academy/container-security/azure-container-security-scanning

[^51]: https://github.com/azure/acr/issues/837

[^52]: https://foggykitchen.com/2025/12/19/aks-acr-private-endpoint-terraform/

[^53]: https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-scanning.html

[^54]: https://docs.azure.cn/en-us/container-registry/container-registry-content-trust-deprecation

[^55]: https://trendmicro.com/cloudoneconformity/knowledge-base/azure/ContainerRegistry/use-private-endpoints.html

[^56]: https://learn.microsoft.com/en-us/troubleshoot/azure/azure-container-registry/image-vulnerability-assessment

[^57]: https://stackoverflow.com/questions/56835649/sign-docker-images-with-internal-companys-ca

[^58]: https://github.com/Azure/Microsoft-Defender-for-Cloud/blob/master/Container Image Scan Vulnerability Assessment/Image Scan Automation Enrichment Security Gate/ImageScanSummaryAssessmentGate.ps1

