# Configuration & Secrets Management — Production Best Practices

> **Domain:** 5.12 | **Group:** CROSS | **Lifecycle:** Cross-Cutting
> **Last Updated:** 2026-03-13

## 1. Overview

Configuration management is the art of externalizing application behavior from code. Proper configuration enables deployments across environments (dev/staging/prod) without code changes, supports secret rotation without downtime, and prevents configuration drift. This domain covers configuration hierarchy, secret management strategies, and infrastructure-as-code principles.

**Vietnamese:** Cấu hình đúng đắn cho phép deploy cùng codebase trên nhiều environment. Secrets phải tách biệt hoàn toàn khỏi code.

## 2. Core Principles

- **12-Factor App Configuration:** Store config in environment, not in code
- **Separation of Concerns:** App logic ≠ configuration ≠ secrets
- **Never Version Secrets:** Git contains only configuration templates
- **Immutable Infrastructure:** Configuration baked into containers, not changed after deployment
- **Single Source of Truth:** Vault/Secrets Manager as authoritative secret store
- **Configuration Validation:** Fail fast if required config is missing or invalid

## 3. Best Practices

### 3.1 12-Factor App Configuration

**Practice: Environment Variables as Primary Config**
- **What:** Use environment variables for all environment-specific configuration
- **Why:** Standard across containerized deployments, works with orchestrators (K8s, ECS), no file management overhead
- **How:**
  ```javascript
  // app.js - Always with sensible defaults
  const config = {
    port: process.env.PORT || 3000,
    nodeEnv: process.env.NODE_ENV || 'development',
    dbHost: process.env.DB_HOST || 'localhost',
    dbPort: parseInt(process.env.DB_PORT || '5432'),
    apiTimeout: parseInt(process.env.API_TIMEOUT || '30000'),
    logLevel: process.env.LOG_LEVEL || 'info'
  };

  // Validate on startup
  if (!process.env.DB_HOST && process.env.NODE_ENV === 'production') {
    throw new Error('DB_HOST environment variable required in production');
  }
  ```
  - Defaults only for development; production requires explicit vars
  - Strict parsing with error messages (parseInt can silently fail)
- **Anti-pattern:** Different config files per environment checked into git, hardcoded values, no defaults with production warnings

**Practice: Configuration Hierarchy**
- **What:** Resolution order: defaults → environment variables → runtime overrides → CLI flags
- **Why:** Allows flexibility without configuration explosion
- **How:**
  ```yaml
  # 1. defaults.json (hardcoded in codebase)
  {
    "cache_ttl": 3600,
    "max_retries": 3,
    "log_level": "info"
  }

  # 2. environment variables override defaults
  export LOG_LEVEL=debug
  export CACHE_TTL=7200

  # 3. config file in /etc/myapp/config.json overrides both
  # Used in containerized environments for ConfigMaps/Secrets

  # 4. CLI flags have highest priority
  ./app --log-level=trace --cache-ttl=1800
  ```
  - Clear precedence prevents confusion
  - Document hierarchy in README
- **Anti-pattern:** Unclear precedence, multiple config sources without clear rules, silent overrides

### 3.2 Secret Management Patterns

**Practice: .env Files Only for Development**
- **What:** .env files contain secrets for local development only
- **Why:** Prevents accidental commits, matches production reality (use Vault/Secrets Manager)
- **How:**
  ```bash
  # .env (NEVER committed)
  DB_PASSWORD=dev_password_only
  API_KEY=dev_key_only
  JWT_SECRET=dev_secret_only

  # .env.example (committed, no actual secrets)
  DB_PASSWORD=CHANGE_ME_IN_PRODUCTION
  API_KEY=CHANGE_ME_IN_PRODUCTION
  JWT_SECRET=CHANGE_ME_IN_PRODUCTION

  # Load in app
  require('dotenv').config();
  const dbPassword = process.env.DB_PASSWORD;
  ```
  - .gitignore: `*.env*` and `!.env.example`
  - Git pre-commit hook: refuse commit if .env included
  - Tools: `git-secret`, `blackbox`, `git-crypt` for encrypted secrets in git
- **Anti-pattern:** Committing .env files, "temp" or "test" credentials that aren't actually temporary, .env with 200+ vars (break into modules)

**Practice: HashiCorp Vault for Secret Rotation**
- **What:** Centralized secret storage with automatic rotation policies
- **Why:** Single source of truth, audit logs, key rotation without app restart, immediate revocation
- **How:**
  ```bash
  # Store database credentials
  vault kv put secret/myapp/database \
    username=admin \
    password=generated_password

  # Application reads at runtime
  # Kubernetes: Vault Agent injects secrets into pod
  vault agent -config=/etc/vault/agent.hcl

  # Or direct API call
  curl -H "X-Vault-Token: $VAULT_TOKEN" \
    http://vault:8200/v1/secret/data/myapp/database

  # Automatic rotation (example: database password every 30 days)
  vault write database/static-roles/myapp \
    db_name=postgres \
    username=vault_user \
    rotation_statements="ALTER ROLE vault_user WITH PASSWORD '{{password}}';" \
    rotation_period=30d
  ```
  - Vault authentication: Kubernetes auth, AWS IAM, OIDC (no hardcoded tokens)
  - Secret consumption: init containers, sidecars, direct API
- **Anti-pattern:** Storing Vault token in plaintext, same secret for all environments, no rotation policy, long-lived root tokens

**Practice: AWS Secrets Manager & SSM Parameter Store**
- **What:** AWS native secret management with encryption, audit, and access control
- **Why:** Integrated with IAM, auto-rotated, KMS encryption included, Lambda native support
- **How:**
  ```python
  # Python application
  import boto3
  client = boto3.client('secretsmanager', region_name='us-east-1')

  secret = client.get_secret_value(SecretId='myapp/db/password')
  db_password = secret['SecretString']

  # Or from SSM Parameter Store (for non-secret config)
  ssm = boto3.client('ssm')
  param = ssm.get_parameter(Name='/myapp/api-timeout', WithDecryption=True)
  timeout = param['Parameter']['Value']

  # Automatic rotation: Lambda function triggered on schedule
  # AWS rotates secret → calls Lambda → Lambda updates app
  ```
  - Secrets Manager: for sensitive data (passwords, API keys)
  - Parameter Store: for configuration (flags, URLs, non-sensitive values)
  - IAM policies: restrict read access to specific applications/roles
- **Anti-pattern:** Using Parameter Store for passwords, overly broad IAM permissions, not using KMS for encryption, manual rotation

**Practice: Kubernetes ConfigMaps & Secrets**
- **What:** Native K8s resources for configuration (ConfigMaps) and sensitive data (Secrets)
- **Why:** Works with pod lifecycle, supports dynamic updates, mounted as files or env vars
- **How:**
  ```yaml
  # ConfigMap: non-sensitive config
  apiVersion: v1
  kind: ConfigMap
  metadata:
    name: myapp-config
  data:
    app.properties: |
      log.level=info
      cache.ttl=3600
    api.endpoint: https://api.example.com

  # Secret: sensitive data (base64 encoded by K8s)
  apiVersion: v1
  kind: Secret
  metadata:
    name: myapp-secrets
  type: Opaque
  data:
    db.password: cGFzc3dvcmQxMjM=  # base64 encoded
    api.key: YWJjZGVmZ2hpamts  # base64 encoded

  # Pod consumes both
  apiVersion: v1
  kind: Pod
  metadata:
    name: myapp
  spec:
    containers:
    - name: app
      image: myapp:latest
      envFrom:
      - configMapRef:
          name: myapp-config
      - secretRef:
          name: myapp-secrets
      volumeMounts:
      - name: config-vol
        mountPath: /etc/config
    volumes:
    - name: config-vol
      configMap:
        name: myapp-config
  ```
  - Encrypt secrets at rest in etcd: `--encryption-provider-config` in kube-apiserver
  - Use external secret operator (ESO) to sync from Vault/AWS Secrets Manager
  - Never store secrets in image layers
- **Anti-pattern:** Checking secrets into ConfigMaps (should use Secrets resource), base64 !== encrypted, storing credentials in image builds

### 3.3 Configuration Validation & Hot Reload

**Practice: Configuration Validation on Startup**
- **What:** Verify all required config exists and is valid before application starts
- **Why:** Catch configuration errors early, prevent runtime failures, fail fast
- **How:**
  ```javascript
  // config.js with validation
  const Joi = require('joi');

  const schema = Joi.object().keys({
    port: Joi.number().integer().min(1024).max(65535).required(),
    nodeEnv: Joi.string().valid('development', 'staging', 'production').required(),
    dbHost: Joi.string().hostname().required(),
    dbPort: Joi.number().integer().min(1).max(65535).required(),
    dbName: Joi.string().required(),
    dbUser: Joi.string().required(),
    dbPassword: Joi.string().required(),
    jwtSecret: Joi.string().min(32).required(),
    logLevel: Joi.string().valid('debug', 'info', 'warn', 'error').default('info')
  });

  const { error, value } = schema.validate(process.env);
  if (error) {
    console.error('Configuration validation failed:', error.details);
    process.exit(1);
  }

  module.exports = value;
  ```
  - Run validation in application entry point before starting server
  - Provide clear error messages (which vars are missing, what are expected values)
  - Different validation for development vs production
- **Anti-pattern:** Logging secrets with validation errors, no production validation, silent defaults that hide issues

**Practice: Feature Flags as Configuration**
- **What:** Use runtime toggles to control feature availability
- **Why:** Deploy without releasing features, A/B testing, gradual rollout, quick disable if issues found
- **How:**
  ```javascript
  // Feature flags from environment or service
  const features = {
    newPaymentFlow: process.env.FEATURE_NEW_PAYMENT === 'true',
    aiRecommendations: process.env.FEATURE_AI === 'true',
    advancedAnalytics: process.env.FEATURE_ANALYTICS === 'true'
  };

  // In application
  if (features.newPaymentFlow) {
    router.post('/payment', newPaymentHandler); // v2
  } else {
    router.post('/payment', legacyPaymentHandler); // v1
  }

  // Or use feature flag service (LaunchDarkly, Unleash)
  const featureManager = new LaunchDarkly.LDClient(SDK_KEY);
  const isEnabled = featureManager.variation('new-payment-flow', {key: userId}, false);
  ```
  - Start with simple env vars, migrate to dedicated service for complex rules
  - Always include fallback for disabled features
  - Remove/archive old feature flags when old code path deleted
- **Anti-pattern:** Hardcoded flags, flags that never get removed, no way to disable at runtime without redeployment

### 3.4 Secret Rotation Strategy

**Practice: Rolling Secret Rotation Without Downtime**
- **What:** Update secrets on schedule without service interruption
- **Why:** Reduces blast radius if secret is compromised, compliance requirement
- **How:**
  ```bash
  # Database password rotation scenario
  # 1. New secret generated in Vault
  vault write -f database/rotate-root/mydb

  # 2. Vault updates database password
  # (configured with database engine)

  # 3. Vault delivers new password to applications
  # (via polling or event notification)

  # 4. Applications reconnect with new password
  # (connection pool refreshes, no active queries killed)

  # 5. Old password revoked after grace period
  vault lease revoke database/static-roles/old-cred

  # Application-level: connection pool with dynamic credentials
  # Each connection requests fresh creds from Vault, not cached
  class DatabasePool {
    async getConnection() {
      const creds = await vault.getCredentials('db');
      return mysql.createConnection({
        host: creds.host,
        user: creds.username,
        password: creds.password,
        ...
      });
    }
  }
  ```
  - Grace period: keep old secret valid during transition
  - Monitoring: alert if rotation fails
  - Testing: practice rotation in staging regularly
- **Anti-pattern:** Zero grace period (breaks active connections), synchronous rotation (blocking), no alert on failure, secrets hardcoded in app forcing manual update

## 4. Decision Frameworks

**Config vs Secret vs Feature Flag:**
| Item | Type | Storage | Sensitive |
|------|------|---------|-----------|
| Database host | Config | Env var/ConfigMap | No |
| Database password | Secret | Vault/Secrets Manager | Yes |
| New feature toggle | Feature flag | LaunchDarkly/Unleash | No |
| API rate limit | Config | ConfigMap | No |
| API key | Secret | Vault/Secrets Manager | Yes |

**When to use which secret storage:**
- **Development:** .env file (local only)
- **Staging/Production on VMs:** HashiCorp Vault
- **AWS environment:** AWS Secrets Manager + IAM
- **Kubernetes:** External Secrets Operator + Vault or AWS Secrets Manager
- **Quick prototyping:** Base64-encoded K8s Secrets (NOT for production)

## 5. Checklist

- [ ] No secrets in version control (Git history scanned for leaks)
- [ ] .env.example committed, actual .env ignored
- [ ] All environment variables documented with expected values
- [ ] Configuration validation on application startup
- [ ] Required vs optional configuration clearly marked
- [ ] Secrets loaded from external vault, not environment at build time
- [ ] Secret rotation policy defined and tested
- [ ] All secrets encrypted at rest and in transit
- [ ] Feature flags implemented for new features
- [ ] Configuration hierarchy documented (defaults → env → override)
- [ ] Development config differs from production (different secrets, log levels, timeouts)
- [ ] ConfigMap and Secret resources encrypted in Kubernetes
- [ ] Access to secrets restricted by IAM/RBAC
- [ ] Secrets audit logs enabled and monitored
- [ ] Grace period for secret rotation (no immediate revocation)

## 6. Common Mistakes & Anti-Patterns

1. **Committing .env files** → Use `git-secret` if absolutely necessary, otherwise local-only
2. **No validation, hardcoded defaults for production values** → Fail loudly if production config missing
3. **Same secret across all environments** → Different secrets per env, rotated independently
4. **Database password in application logs** → Sanitize logs, never log credentials
5. **Tokens stored in plaintext in containers** → Use init containers or admission webhooks to inject
6. **Manual secret rotation** → Automate with Vault, Secrets Manager, or operator
7. **Super long secret validity** → Rotate every 30-90 days, more frequently for high-risk secrets
8. **No audit trail for secret access** → Enable audit logging in Vault/Secrets Manager, monitor
9. **Mixing feature flags with configuration** → Different systems, flags runtime, config deployment-time
10. **Configuration drift** → No manual edits after deployment, detect with compliance scanning

## 7. Tools & References

**Secret Management:**
- HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, Google Secret Manager
- Sealed Secrets, External Secrets Operator (Kubernetes)

**Configuration Management:**
- Terraform (infrastructure), Ansible (configuration), cfn-lint, Pulumi

**Feature Flags:**
- LaunchDarkly, Unleash, Harness Feature Flags, CloudBees Feature Management

**Secret Scanning:**
- GitGuardian, git-secrets, detect-secrets, TruffleHog

**Standards:**
- 12-Factor App (https://12factor.net)
- NIST Configuration Management guidelines

---

**Vietnamese Note:** Cấu hình là bridge giữa code và infrastructure. Phải tách biệt hoàn toàn khỏi application code. (Configuration is the bridge between code and infrastructure; must be completely separated from application code.)
