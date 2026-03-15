# Compliance & Data Protection — Production Best Practices

> **Domain:** 5.18 | **Group:** SPECIALIZED | **Lifecycle:** Specialized
> **Last Updated:** 2026-03-13

## 1. Overview

Data protection and compliance are not optional—they're business requirements. Violations lead to:
- **Financial penalties**: GDPR up to €20M or 4% global revenue (whichever is larger)
- **Reputational damage**: User trust destroyed, market share loss
- **Legal liability**: Civil lawsuits, criminal charges
- **Operational disruption**: Service shutdowns, data seizures

**Key Principle:** Data protection by design, not by accident.

## 2. Core Principles

### 2.1 Privacy Regulations
- **GDPR** (EU): Strictest, applies globally to EU residents
- **CCPA** (California): Similar to GDPR for California residents
- **HIPAA** (US Healthcare): Patient health information
- **PCI DSS** (Payment): Credit card data
- **SOC 2** (Service providers): Operational controls

### 2.2 Data Classification
```
PUBLIC: No restrictions (product info, public posts)
INTERNAL: Employee only (salary, strategy)
CONFIDENTIAL: Restricted access (customer data, contracts)
RESTRICTED: Highly sensitive (passwords, crypto keys, health data)
```

### 2.3 Privacy Principles
- **Minimization**: Collect only needed data
- **Purpose limitation**: Use only for declared purpose
- **Storage limitation**: Delete when no longer needed
- **Integrity**: Data accurate and secure
- **Confidentiality**: Protect from unauthorized access

## 3. Best Practices

### 3.1 GDPR Compliance Checklist

**Practice: Implement All Required Elements**

```python
# 1. Lawful basis for processing
LAWFUL_BASES = {
    "consent": "User explicitly agreed",
    "contract": "Required to fulfill contract",
    "legal_obligation": "Law requires it",
    "vital_interests": "Protect human life",
    "public_task": "Government function",
    "legitimate_interests": "Balancing test required"
}

# 2. Consent mechanism
class ConsentManager:
    def __init__(self, db):
        self.db = db

    def request_consent(self, user_id, purpose, data_categories):
        """Request explicit, informed consent (xin phép)"""
        consent_record = {
            "user_id": user_id,
            "purpose": purpose,  # e.g., "marketing_emails"
            "data_categories": data_categories,  # ["email", "phone"]
            "timestamp": datetime.now(),
            "version": "2.1",  # Track consent version
            "ip_address": get_client_ip(),  # Proof of consent
            "user_agent": get_user_agent()
        }
        self.db.consent.insert_one(consent_record)
        return consent_record

    def withdraw_consent(self, user_id, purpose):
        """User can withdraw consent anytime"""
        self.db.consent.update_one(
            {"user_id": user_id, "purpose": purpose},
            {"$set": {"withdrawn_at": datetime.now()}}
        )

        # Stop processing immediately
        stop_marketing_to_user(user_id)

    def has_consent(self, user_id, purpose):
        """Check valid consent before processing"""
        consent = self.db.consent.find_one({
            "user_id": user_id,
            "purpose": purpose,
            "withdrawn_at": None
        })
        return consent is not None

# 3. Data Processing Agreement (DPA)
# Ensure all processors (vendors) have signed DPA before sharing data
class ProcessorRegistry:
    def __init__(self):
        self.processors = {}

    def register_processor(self, processor_name, contract_date, data_categories):
        """Vendors must have signed DPA"""
        if not contract_date:
            raise Exception(f"{processor_name}: Missing DPA - cannot share data")

        self.processors[processor_name] = {
            "dpa_signed": contract_date,
            "data_categories": data_categories,
            "sub_processors": []
        }

    def can_share_with(self, processor_name, data_category):
        """Check processor authorization"""
        if processor_name not in self.processors:
            return False

        processor = self.processors[processor_name]
        return data_category in processor["data_categories"]

# 4. Audit logging
class AuditLog:
    def __init__(self, db):
        self.db = db

    def log_access(self, user_id, data_accessed, timestamp=None):
        """Log who accessed what data and when"""
        log_entry = {
            "user_id": user_id,
            "data_accessed": data_accessed,
            "timestamp": timestamp or datetime.now(),
            "ip_address": get_client_ip(),
            "reason": "performance_analysis"  # Why accessed
        }
        self.db.audit_logs.insert_one(log_entry)

    def get_access_log(self, user_id, days=90):
        """User has right to see who accessed their data"""
        cutoff = datetime.now() - timedelta(days=days)
        return list(self.db.audit_logs.find({
            "user_id": user_id,
            "timestamp": {"$gte": cutoff}
        }))
```

### 3.2 Right to be Forgotten (RTBF)

**Practice: Data Deletion Pipeline**

```python
class DeletionService:
    def __init__(self, db, file_storage, backup_system):
        self.db = db
        self.file_storage = file_storage
        self.backup_system = backup_system

    async def delete_user_data(self, user_id):
        """Implement full right to be forgotten"""

        # Phase 1: Gather all user data locations
        deletion_scope = {
            "database": [],
            "object_storage": [],
            "backups": [],
            "analytics": [],
            "third_party": []
        }

        # Database records
        user_records = self.db.users.find_one({"user_id": user_id})
        if user_records:
            deletion_scope["database"].append({
                "collection": "users",
                "records": 1
            })

        # Object storage (files, documents)
        user_files = self.file_storage.list_objects(
            prefix=f"user/{user_id}"
        )
        deletion_scope["object_storage"].extend(user_files)

        # Backups (delete from latest backup)
        backups = self.backup_system.find_backups(user_id)
        deletion_scope["backups"].extend(backups)

        # Analytics (anonymize)
        self.db.analytics.update_many(
            {"user_id": user_id},
            {"$set": {"user_id": "ANONYMOUS"}}
        )

        # Third-party services (request deletion)
        third_party_services = [
            ("Stripe", delete_from_stripe),
            ("Salesforce", delete_from_salesforce),
            ("SendGrid", delete_from_sendgrid)
        ]

        for service_name, delete_fn in third_party_services:
            try:
                await delete_fn(user_id)
                deletion_scope["third_party"].append({
                    "service": service_name,
                    "status": "deleted"
                })
            except Exception as e:
                deletion_scope["third_party"].append({
                    "service": service_name,
                    "status": "failed",
                    "error": str(e)
                })

        # Phase 2: Execute deletion (in transaction when possible)
        try:
            # Delete from database
            self.db.users.delete_one({"user_id": user_id})
            self.db.user_profiles.delete_many({"user_id": user_id})
            self.db.user_activity.delete_many({"user_id": user_id})

            # Delete from object storage
            for file_path in user_files:
                self.file_storage.delete_object(file_path)

            # Create deletion certificate
            deletion_certificate = {
                "user_id": user_id,
                "deleted_at": datetime.now(),
                "scope": deletion_scope,
                "verified_by": "compliance_team"
            }

            self.db.deletion_certificates.insert_one(deletion_certificate)

            return deletion_certificate

        except Exception as e:
            logger.critical(f"Deletion failed for {user_id}: {e}")
            raise

    def verify_complete_deletion(self, user_id):
        """Prove to user all data is deleted"""
        # Query all systems
        checks = {
            "database": len(list(self.db.users.find({"user_id": user_id}))),
            "backups": self.backup_system.user_exists(user_id),
            "analytics": len(list(self.db.analytics.find({"user_id": user_id}))),
        }

        if all(count == 0 for count in checks.values()):
            return {"status": "complete_deletion_verified"}
        else:
            return {"status": "deletion_incomplete", "details": checks}
```

### 3.3 Data Encryption

**Practice: Encryption at Rest and in Transit**

```python
from cryptography.fernet import Fernet
import ssl

# Encryption at rest (in database)
class EncryptedField:
    def __init__(self, encryption_key):
        self.cipher = Fernet(encryption_key)

    def encrypt(self, plaintext):
        """Encrypt sensitive field"""
        return self.cipher.encrypt(plaintext.encode())

    def decrypt(self, ciphertext):
        """Decrypt sensitive field"""
        return self.cipher.decrypt(ciphertext).decode()

# Usage in database
class UserModel:
    def __init__(self, name, ssn, encryption_key):
        self.name = name
        self.ssn_encrypted = EncryptedField(encryption_key).encrypt(ssn)

# Encryption in transit (TLS)
import requests

# Good: HTTPS with certificate verification
response = requests.get(
    'https://api.example.com/data',
    verify=True,  # Verify SSL certificate
    timeout=10
)

# Configuration: Enforce TLS 1.2+
ssl_context = ssl.create_default_context()
ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2
ssl_context.check_hostname = True
ssl_context.verify_mode = ssl.CERT_REQUIRED

# Database encryption
DATABASE_URL = "postgresql://user:pass@host/db?sslmode=require"
```

### 3.4 PII Handling & Anonymization

**Practice: Identify and Protect PII**

```python
import re
from typing import List

class PIIDetector:
    """Detect personally identifiable information"""

    # Patterns for common PII
    PATTERNS = {
        "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "phone": r"(\+\d{1,3})?[-.\s]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}",
        "ssn": r"\d{3}-\d{2}-\d{4}",
        "credit_card": r"\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}",
        "passport": r"[A-Z]{1,2}[0-9]{6,9}",
        "ip_address": r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
    }

    def detect_pii(self, text: str) -> dict:
        """Find all PII in text"""
        findings = {}
        for pii_type, pattern in self.PATTERNS.items():
            matches = re.findall(pattern, text)
            if matches:
                findings[pii_type] = matches
        return findings

    def redact_pii(self, text: str) -> str:
        """Replace PII with placeholders"""
        redacted = text
        for pii_type, pattern in self.PATTERNS.items():
            redacted = re.sub(pattern, f"[{pii_type.upper()}]", redacted)
        return redacted

# Anonymization techniques
class Anonymizer:
    @staticmethod
    def anonymize_email(email):
        """Replace email with hash"""
        import hashlib
        return hashlib.sha256(email.encode()).hexdigest()[:16]

    @staticmethod
    def anonymize_name(name):
        """Truncate name"""
        parts = name.split()
        return parts[0][0] + "." + parts[-1][:3] if len(parts) > 1 else "A.N."

    @staticmethod
    def anonymize_date(date_obj):
        """Generalize date to month"""
        return f"{date_obj.year}-{date_obj.month:02d}"

    @staticmethod
    def anonymize_location(latitude, longitude):
        """Round to lower precision"""
        return round(latitude, 1), round(longitude, 1)  # 11km precision

# Logging sanitization
class SanitizedLogger:
    def __init__(self):
        self.detector = PIIDetector()

    def log(self, message):
        """Log with PII redacted"""
        pii = self.detector.detect_pii(message)

        if pii:
            message = self.detector.redact_pii(message)
            logger.warning(f"PII detected and redacted: {pii}")

        logger.info(message)
```

### 3.5 Data Retention Policies

**Practice: Implement Automated Deletion**

```python
from datetime import datetime, timedelta

class RetentionPolicy:
    """Define how long to keep different data types"""

    POLICIES = {
        "user_activity": 90,      # 90 days
        "login_logs": 180,        # 6 months
        "error_logs": 30,         # 30 days
        "backups": 365,           # 1 year
        "deleted_user_data": 0,   # Delete immediately (no recovery)
        "financial_records": 2555 # 7 years (regulatory requirement)
    }

    @staticmethod
    def cleanup_expired_data():
        """Run daily - delete data past retention period"""
        now = datetime.now()

        for data_type, retention_days in RetentionPolicy.POLICIES.items():
            cutoff_date = now - timedelta(days=retention_days)

            if data_type == "user_activity":
                deleted = db.user_activity.delete_many({
                    "created_at": {"$lt": cutoff_date}
                })
                logger.info(f"Deleted {deleted.deleted_count} old activity records")

            elif data_type == "login_logs":
                deleted = db.login_logs.delete_many({
                    "timestamp": {"$lt": cutoff_date}
                })
                logger.info(f"Deleted {deleted.deleted_count} old login logs")

            # Continue for other data types...

    @staticmethod
    def get_retention_period(data_type):
        """Check how long data can be retained"""
        return RetentionPolicy.POLICIES.get(data_type)
```

### 3.6 Cookie Consent & GDPR

**Practice: Proper Cookie Consent Mechanism**

```python
class CookieConsent:
    """Manage cookie consent as per GDPR"""

    COOKIE_CATEGORIES = {
        "essential": {
            "required": True,
            "description": "Required for site function"
        },
        "analytics": {
            "required": False,
            "description": "Google Analytics tracking"
        },
        "marketing": {
            "required": False,
            "description": "Advertising personalization"
        },
        "preferences": {
            "required": False,
            "description": "Remember user preferences"
        }
    }

    def __init__(self):
        self.consent_record = {}

    def show_consent_banner(self):
        """Display consent banner to user"""
        return {
            "message": "We use cookies to improve your experience",
            "categories": self.COOKIE_CATEGORIES,
            "options": [
                "Accept All",
                "Reject All",
                "Manage Preferences"
            ]
        }

    def record_consent(self, user_id, consents):
        """Record which cookies user accepted"""
        self.consent_record[user_id] = {
            "timestamp": datetime.now(),
            "consents": consents,
            "ip_address": get_client_ip()
        }

    def can_use_analytics(self, user_id):
        """Check if user consented to analytics"""
        consent = self.consent_record.get(user_id, {})
        return consent.get("consents", {}).get("analytics", False)

    def can_use_marketing(self, user_id):
        """Check if user consented to marketing"""
        consent = self.consent_record.get(user_id, {})
        return consent.get("consents", {}).get("marketing", False)

# Implementation
consent = CookieConsent()

# User sees banner and selects preferences
@app.route('/api/cookie-consent', methods=['POST'])
def set_cookie_consent():
    user_id = session['user_id']
    consents = request.json
    consent.record_consent(user_id, consents)

    # Only set analytics cookie if consented
    if consent.can_use_analytics(user_id):
        set_cookie('ga_consent', 'true')

    return {"status": "ok"}
```

### 3.7 Data Processing Agreements (DPA)

**Practice: Vendor Management for GDPR**

```python
class VendorComplianceManager:
    """Ensure all vendors comply with data protection"""

    def __init__(self, db):
        self.db = db

    def register_vendor(self, vendor_name, dpa_signed_date, data_categories):
        """Register vendor with signed DPA"""
        if not dpa_signed_date:
            raise Exception(f"Cannot use {vendor_name} without signed DPA")

        vendor_record = {
            "name": vendor_name,
            "dpa_signed_date": dpa_signed_date,
            "data_categories": data_categories,
            "dpia_completed": False,  # Data Protection Impact Assessment
            "last_audit": None,
            "status": "active"
        }

        self.db.vendors.insert_one(vendor_record)

    def data_protection_impact_assessment(self, vendor_name):
        """DPIA required for high-risk data sharing"""
        return {
            "vendor": vendor_name,
            "risk_level": "medium",  # low, medium, high
            "personal_data_transferred": [
                "email",
                "usage_patterns",
                "purchase_history"
            ],
            "safeguards": [
                "Encryption in transit",
                "Data minimization",
                "Sub-processor approval"
            ],
            "risk_mitigation": [
                "Annual security audit",
                "Immediate breach notification"
            ]
        }

    def can_share_with_vendor(self, vendor_name, data_category):
        """Check vendor authorization before sharing"""
        vendor = self.db.vendors.find_one({"name": vendor_name})

        if not vendor:
            raise Exception(f"{vendor_name} not registered")

        if data_category not in vendor["data_categories"]:
            raise Exception(f"{vendor_name} not authorized for {data_category}")

        return True

    def audit_vendor(self, vendor_name):
        """Audit vendor compliance"""
        vendor = self.db.vendors.find_one({"name": vendor_name})

        audit_report = {
            "vendor": vendor_name,
            "date": datetime.now(),
            "findings": [
                "Encryption enabled: PASS",
                "Access controls: PASS",
                "Breach notification: PASS",
                "Sub-processors documented: FAIL"
            ]
        }

        self.db.vendor_audits.insert_one(audit_report)
        return audit_report
```

### 3.8 Breach Notification

**Practice: Incident Response Plan**

```python
class BreachNotificationManager:
    """Handle data breach discovery & notification"""

    def __init__(self, db, email_service):
        self.db = db
        self.email_service = email_service

    def report_breach(self, breach_type, affected_users, root_cause):
        """Log breach and initiate response"""

        breach_record = {
            "id": str(uuid.uuid4()),
            "type": breach_type,  # "unauthorized_access", "malware", etc.
            "discovered_at": datetime.now(),
            "affected_user_count": len(affected_users),
            "root_cause": root_cause,
            "status": "investigating"
        }

        self.db.breaches.insert_one(breach_record)

        # GDPR requirement: Notify authority within 72 hours if personal data breached
        self.schedule_authority_notification(breach_record, affected_users)

        return breach_record

    def schedule_authority_notification(self, breach_record, affected_users):
        """Notify data protection authority"""
        # Required if affects >100 people or high-risk data
        notification = {
            "authority": "Data Protection Authority",
            "breach_id": breach_record["id"],
            "notification_deadline": datetime.now() + timedelta(hours=72),
            "affected_count": len(affected_users),
            "affected_data": ["email", "password_hash"]  # What was breached
        }

        self.db.authority_notifications.insert_one(notification)

    def notify_users(self, breach_record, affected_users):
        """Notify affected users within 72 hours"""
        for user in affected_users:
            message = f"""
            Dear {user['name']},

            We discovered a data breach affecting your account on {breach_record['discovered_at']}.

            What was breached: {', '.join(breach_record.get('affected_data', []))}

            Steps we've taken:
            1. Secured all systems
            2. Investigating the incident

            What you should do:
            1. Change your password immediately
            2. Enable two-factor authentication
            3. Monitor your accounts for suspicious activity

            Sincerely,
            Our Security Team
            """

            self.email_service.send(
                to=user['email'],
                subject="Important: Your Account Was Affected by a Data Breach",
                body=message
            )

            # Log notification
            self.db.breach_notifications.insert_one({
                "user_id": user['id'],
                "breach_id": breach_record["id"],
                "notified_at": datetime.now()
            })
```

### 3.9 Access Control Audit

**Practice: Implement Least Privilege**

```python
class AccessControlAudit:
    """Ensure principle of least privilege"""

    def __init__(self, db):
        self.db = db

    def audit_user_access(self, user_id):
        """Check what data user can access"""
        user = self.db.users.find_one({"user_id": user_id})

        access_levels = {
            "own_data": user["permissions"].get("own_data", False),
            "team_data": user["permissions"].get("team_data", False),
            "admin_console": user["permissions"].get("admin", False),
            "financial_reports": user["permissions"].get("financial", False)
        }

        # Flag excessive access
        flags = []
        if access_levels["admin"] and user["role"] != "admin":
            flags.append("Non-admin has admin access")

        if access_levels["financial"] and "finance" not in user["department"]:
            flags.append("Non-finance employee has financial access")

        return {
            "user_id": user_id,
            "access_levels": access_levels,
            "compliance_flags": flags
        }

    def revoke_excessive_access(self, user_id, reason):
        """Remove unnecessary permissions"""
        self.db.users.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "permissions": {
                        "own_data": True,
                        "team_data": False,
                        "admin": False,
                        "financial": False
                    },
                    "access_revoked_at": datetime.now(),
                    "revocation_reason": reason
                }
            }
        )

    def required_access_for_role(self, role):
        """Define minimum access needed"""
        role_access = {
            "user": ["own_data"],
            "manager": ["own_data", "team_data"],
            "finance": ["own_data", "financial_reports"],
            "admin": ["own_data", "team_data", "admin_console", "financial_reports"]
        }
        return role_access.get(role, ["own_data"])
```

## 4. Decision Frameworks

### When to Conduct DPIA?
- [ ] Processing special categories (health, race, religion)
- [ ] Large-scale processing
- [ ] Automated decision-making
- [ ] High-risk processing

### Breach Severity Assessment
- **Low**: < 100 users, non-sensitive data
- **Medium**: 100-10k users, some PII
- **High**: 10k+ users, sensitive data, legal action likely

## 5. Checklist

- [ ] Lawful basis for processing documented
- [ ] Consent mechanism implemented (if applicable)
- [ ] Data Processing Agreements signed with all vendors
- [ ] Encryption at rest implemented
- [ ] TLS enforced for all data in transit
- [ ] Data retention policies automated
- [ ] Right to be forgotten workflow implemented
- [ ] Audit logging for data access
- [ ] PII detection and redaction in logs
- [ ] Cookie consent banner with categories
- [ ] Breach response plan documented
- [ ] Authority notification procedure tested
- [ ] Access control regularly audited
- [ ] Data Protection Impact Assessments conducted
- [ ] Privacy notice updated and accessible

## 6. Common Mistakes & Anti-Patterns

| Mistake | Impact | Fix |
|---------|--------|-----|
| No consent mechanism | GDPR violation, fines | Implement explicit consent tracking |
| No DPA with vendors | Processors not authorized | Sign DPA before vendor access |
| PII in logs | Breach through logs, visibility | Auto-redact PII from all logs |
| No data retention policy | Stale data accumulates | Automate deletion by policy |
| Unencrypted PII | Easy compromise on breach | Encrypt all PII at rest & transit |
| No breach plan | Chaotic response, legal issues | Document & test breach procedure |
| Excessive user access | Insider threat risk | Implement least privilege |
| No audit trail | Can't investigate breaches | Log all data access attempts |

## 7. Tools & References

**Compliance Tools:**
- OneTrust (GDPR/CCPA management)
- BigID (data discovery & classification)
- TrustArc (compliance assessments)
- Drata (SOC 2 automation)

**Data Protection:**
- HashiCorp Vault (secrets management)
- Encryption libraries (cryptography, PyCryptodome)
- DLP tools (Forcepoint, Digital Guardian)

**Incident Response:**
- NIST Cybersecurity Framework
- OWASP Incident Response Handbook

**Regulations:**
- GDPR official guidance (EDPB)
- CCPA/CPRA (California Attorney General)
- HIPAA Security Rule (HHS)
- PCI DSS (Payment Card Industry)
