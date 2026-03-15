# Code Quality & Maintainability Best Practices

> **Domain:** 5.06 | **Group:** BUILD | **Lifecycle:** Build Time
> **Last Updated:** 2026-03-13
> **Scope:** Code Review, Quality Assurance, Technical Debt Management

---

## 1. Overview

Maintainable code is the foundation of sustainable software systems. This domain covers practices that ensure code is readable, testable, secure, and easy to evolve over time. Poor code quality creates technical debt that compounds, slowing down all future work.

**Code Quality Maturity:**
```
Level 1: "Code works" (unmaintainable, brittle, undocumented)
Level 2: Linting enabled (formatting consistent, syntax errors caught)
Level 3: Code reviews (peer feedback, design discussions)
Level 4: Static analysis (security vulnerabilities, code smells detected)
Level 5: Automated quality gates (metrics enforced, technical debt tracked)
```

**Impact on Development Speed:**
- **Poor quality:** Fast initial development, slows by 50% by month 6
- **Good quality:** Slightly slower initially, maintains speed indefinitely
- **Excellent quality:** Fast initially, accelerates due to reusable patterns

---

## 2. Core Principles

### 2.1 Readability Over Cleverness
"Code is read 10x more than it's written." Optimize for the next developer (often yourself in 6 months).

### 2.2 Explicit Over Implicit
Clear intent beats clever shortcuts. "Explicit is better than implicit" (Python Zen).

### 2.3 Small, Focused Units
Functions, classes, modules should have single responsibilities. Easier to test, reuse, and reason about.

### 2.4 Consistent Conventions
Consistency aids understanding. Conventions > discussions about which standard.

### 2.5 Zero Tolerance for Code Smells
Technical debt compounds. Fix issues when discovered, not "later" (which never comes).

### 2.6 Continuous Refactoring
Refactoring is not a project; it's ongoing practice integrated into daily work.

---

## 3. Best Practices

### 3.1 Code Review Best Practices

**Practice: Effective Pull Request Reviews**

```markdown
# Pull Request Template
## Description
What changes are made and why?

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added
- [ ] Integration tests pass
- [ ] Load test results (if applicable)

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-reviewed code before requesting review
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests added for new functionality
```

**Reviewer Checklist:**
```
Code Quality
  ✓ Code is readable and easy to understand
  ✓ Naming is clear and consistent
  ✓ Functions are reasonably short (< 50 lines)
  ✓ Classes have single responsibility
  ✓ No commented-out code left behind

Correctness
  ✓ Logic is correct for described behavior
  ✓ Edge cases handled
  ✓ Error handling appropriate
  ✓ No obvious performance issues
  ✓ Thread-safe if concurrent

Testing
  ✓ Tests are comprehensive (happy path + errors)
  ✓ Test names describe behavior
  ✓ No flaky tests
  ✓ Coverage of critical paths

Security
  ✓ No hardcoded secrets
  ✓ Input validation present
  ✓ SQL injection prevention (parameterized queries)
  ✓ XSS prevention (output encoding)
  ✓ CORS/CSRF properly handled

Maintainability
  ✓ Documentation updated
  ✓ No increase in technical debt
  ✓ Follows project conventions
  ✓ Code is DRY (Don't Repeat Yourself)
```

**Effective Review Comments:**

Bad comment (dismissive):
```
// This is inefficient
```

Good comment (specific, actionable):
```
// This O(n²) loop could be O(n) with a Set:
// Current: for each user, loop all payments to find duplicates
// Suggested: Build Set of payment IDs, check membership in O(1)
// See optimization ideas in #2345
```

- **What:** Peer review of all code before merging to main
- **Why:** Catches bugs early, improves code quality, shares knowledge, prevents regressions
- **How:** Set code review standards in CONTRIBUTING.md, enforce via branch protection, ensure reviews complete < 24h
- **Anti-pattern:** Approval without reading code, reviews after merge, single reviewer bottleneck

**Code Review Velocity:**
- Target: All PRs reviewed within 24 hours
- Large PRs (>400 lines): Break into smaller PRs
- Blocked on review: Clear blocker lane (e.g., GitHub "needs work" status)

### 3.2 Linting & Code Formatting

**Practice: Automated Linting & Formatting**

```json
// .eslintrc.json (JavaScript)
{
  "env": {
    "node": true,
    "es2021": true
  },
  "extends": ["eslint:recommended"],
  "parserOptions": {
    "ecmaVersion": "latest"
  },
  "rules": {
    "no-unused-vars": "error",
    "no-console": "warn",
    "eqeqeq": ["error", "always"],
    "no-var": "error",
    "prefer-const": "error",
    "semi": ["error", "always"],
    "quotes": ["error", "single"],
    "indent": ["error", 2],
    "max-len": ["warn", { "code": 100 }]
  }
}
```

```yaml
# .prettierrc.yaml (Code formatter)
semi: true
trailingComma: es5
singleQuote: true
printWidth: 100
tabWidth: 2
useTabs: false
```

```python
# pyproject.toml (Python)
[tool.black]
line-length = 100
target-version = ['py311']

[tool.ruff]
line-length = 100
select = ["E", "F", "W"]  # Errors, Pyflakes, Warnings

[tool.isort]
profile = "black"
line_length = 100
```

CI Pipeline enforcement:
```yaml
# .github/workflows/lint.yml
name: Lint

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run ESLint
        run: npm run lint -- --format=json --output-file=eslint.json
        continue-on-error: true

      - name: Run Prettier
        run: npm run format:check
        continue-on-error: true

      - name: Comment on PR if formatting needed
        if: failure()
        run: |
          cat << EOF > /tmp/comment.md
          ## Code formatting issues detected
          Run \`npm run format\` locally to fix.
          EOF
          gh pr comment -F /tmp/comment.md
```

- **What:** Automated tools enforcing consistent code style
- **Why:** Removes style debates, improves readability, catches potential bugs (unused variables, type errors)
- **How:** Configure linters in CI, auto-format on save (pre-commit hooks), fail PR if violations
- **Anti-pattern:** Formatting wars in code review, manual indentation fixes, no linting at all

**Pre-Commit Hooks:**
```bash
#!/bin/bash
# .git/hooks/pre-commit

# Run linter on staged files
npm run lint -- $(git diff --cached --name-only)
if [ $? -ne 0 ]; then
  echo "Linting failed. Fix errors and try again."
  exit 1
fi

# Auto-format and re-stage
npm run format
git add .
```

### 3.3 Static Analysis & Code Smells

**Practice: SonarQube / CodeClimate Configuration**

```yaml
# sonar-project.properties
sonar.projectKey=payment-service
sonar.sources=src
sonar.tests=tests
sonar.coverage.exclusions=**/node_modules/**,**/dist/**
sonar.javascript.lcov.reportPaths=coverage/lcov.info

# Quality gates (rules that must pass)
sonar.qualitygate.wait=true
sonar.qualitygate.timeout=600
```

Common code smells to catch:
- **Duplicate code:** Same code in multiple places → extract to function
- **Long methods:** Method > 50 lines → break into smaller methods
- **Long classes:** Class > 300 lines → split responsibilities
- **Too many parameters:** Function with > 5 parameters → use object/map
- **Deep nesting:** Nested if/loops > 3 levels → extract early returns
- **Magic numbers:** Unexplained constants → name them
- **Dead code:** Unreachable code, unused variables → delete
- **Comments:** Excessive comments indicate unclear code → refactor instead

Example SonarQube rule violation:
```
[CRITICAL] Cognitive Complexity 17 (max: 15)
  File: payment/process.js, Line 45-120

  Complex nested conditions and loops:
    if (user.exists)
      if (user.active)
        if (user.verified)
          if (user.balance > amount)
            for (let i = 0; i < retries; i++)
              if (processor.available)
                ...
```

Refactored:
```javascript
// Extract to guard clauses
if (!user.exists) throw new NotFoundError();
if (!user.active) throw new InactiveUserError();
if (!user.verified) throw new UnverifiedError();
if (user.balance < amount) throw new InsufficientFundsError();

// Complexity now: 1 (linear)
await retryProcessPayment(processor, amount);
```

- **What:** Automated detection of code patterns indicating bugs, maintainability issues, security vulnerabilities
- **Why:** Catches issues humans miss; prevents technical debt accumulation
- **How:** Integrate SonarQube or CodeClimate into CI, set quality gates that block merges
- **Anti-pattern:** Ignoring violations, disabling rules without understanding them

### 3.4 Cyclomatic Complexity

**Practice: Keeping Functions Simple**

Cyclomatic Complexity = number of independent paths through code

```python
# Complexity = 1 (simple, linear)
def calculate_discount(price, is_vip):
    return price * 0.9 if is_vip else price

# Complexity = 5 (too many branches)
def calculate_price(user_type, quantity, is_holiday, has_coupon, region):
    if user_type == 'vip':
        if quantity > 100:
            if is_holiday:
                if has_coupon:
                    if region == 'us':
                        return base_price * 0.5  # Path 1
                    else:
                        return base_price * 0.6  # Path 2
                else:
                    return base_price * 0.7     # Path 3
            else:
                return base_price * 0.8         # Path 4
        else:
            return base_price * 0.9             # Path 5
```

Refactored (Complexity = 1):
```python
def calculate_price(user_type, quantity, is_holiday, has_coupon, region):
    """Dispatch to strategy based on conditions"""
    multipliers = {
        ('vip', 100+, True, True, 'us'): 0.5,
        ('vip', 100+, True, True, 'intl'): 0.6,
        ('vip', 100+, True, False): 0.7,
        ('vip', 100+, False): 0.8,
        ('vip', < 100): 0.9,
    }
    key = (user_type, quantity >= 100, is_holiday, has_coupon, region)
    multiplier = multipliers.get(key, 1.0)
    return base_price * multiplier
```

**Complexity Limits:**
- Target: 1-3 (simple, easy to understand)
- Acceptable: 4-7 (moderately complex, testable)
- Needs refactoring: 8+ (hard to understand, difficult to test)

- **What:** Measure of how many different execution paths through a function
- **Why:** High complexity = harder to test, more bugs, difficult to change
- **How:** Use tools (SonarQube, Radon for Python) to measure, refactor high-complexity functions
- **Anti-pattern:** Accepting high complexity as "necessary", not measuring at all

### 3.5 Clean Code Principles (Uncle Bob)

**Practice: Meaningful Names**

Bad names:
```python
a = 0
b = []
x = user.get_data()['status']

def process(d):
    return d['amount'] * 0.9
```

Good names:
```python
transaction_count = 0
completed_orders = []
user_status = user.get_data()['status']

def calculate_discount(order):
    return order['amount'] * VIPPLAINER_DISCOUNT
```

**Principle: Single Responsibility Principle (SRP)**

Each class/function should have ONE reason to change.

Bad (multiple responsibilities):
```python
class User:
    def validate_email(self):
        """Validation logic"""
        pass

    def send_welcome_email(self):
        """Email sending logic"""
        pass

    def save_to_database(self):
        """Database logic"""
        pass

    # Change reasons: email format, email provider, database schema
```

Good (separated concerns):
```python
class User:
    """Domain object, only knows user data"""
    def validate_email(self):
        pass

class EmailService:
    """Responsible for sending emails"""
    def send_welcome(self, user):
        pass

class UserRepository:
    """Responsible for persistence"""
    def save(self, user):
        pass
```

**Principle: DRY (Don't Repeat Yourself)**

Bad (repetition):
```javascript
// In Order service
if (payment.status === 'success') {
  await notifyCustomer(payment.id);
  log.info(`Payment ${payment.id} succeeded`);
  updateMetrics('payment_success', 1);
}

// In Refund service
if (refund.status === 'success') {
  await notifyCustomer(refund.id);
  log.info(`Refund ${refund.id} succeeded`);
  updateMetrics('refund_success', 1);
}
```

Good (extracted):
```javascript
function handleFinancialTransactionSuccess(transaction) {
  await notifyCustomer(transaction.id);
  log.info(`${transaction.type} ${transaction.id} succeeded`);
  updateMetrics(`${transaction.type}_success`, 1);
}

// Used in both services
handleFinancialTransactionSuccess(payment);
handleFinancialTransactionSuccess(refund);
```

- **What:** Design principles for writing understandable, maintainable code
- **Why:** Reduces bugs, improves collaboration, makes refactoring safer
- **How:** Consistent code review focus on naming, responsibility, DRY violations
- **Anti-pattern:** Optimizing for brevity instead of clarity, ignoring duplication

### 3.6 Type Safety (TypeScript / mypy)

**Practice: Gradual Type Adoption**

```typescript
// JavaScript (no type safety)
function processPayment(user, amount) {
  return user.balance - amount;  // What if amount is string? user is null?
}

// TypeScript (type-safe)
interface User {
  id: string;
  balance: number;
  name: string;
}

interface Payment {
  user: User;
  amount: number;
  currency: string;
}

function processPayment(payment: Payment): number {
  // TypeScript catches:
  // - payment.amount as string instead of number
  // - accessing non-existent fields
  // - returning wrong type
  if (payment.amount <= 0) {
    throw new Error('Amount must be positive');
  }
  return payment.user.balance - payment.amount;
}

// Call with wrong type
processPayment({ user: { name: 'John' } });  // ❌ Type error (missing fields)
processPayment({ user, amount: '50' });      // ❌ Type error (string not number)
processPayment({ user, amount: 50 });        // ✓ OK
```

Python type hints:
```python
from typing import Optional, List, Dict

def find_user_by_email(email: str) -> Optional[User]:
    """Find user by email, return None if not found"""
    pass

def process_bulk_payments(payments: List[Dict[str, float]]) -> Dict[str, bool]:
    """Process multiple payments, return status map"""
    pass

# mypy catches type errors
user = find_user_by_email("john@example.com")
user.balance -= 100  # ❌ Error: user might be None
name: int = "John"   # ❌ Error: assigning str to int field
```

- **What:** Declaring expected types for function arguments and return values
- **Why:** Catches type-related bugs at build time instead of runtime
- **How:** Use TypeScript, mypy, or language-native type hints; enforce in CI
- **Anti-pattern:** Using `any` type, skipping type checking in CI, not typing function signatures

### 3.7 Error Handling Patterns

**Practice: Explicit Error Types**

```python
# Bad (generic exceptions)
def process_payment(payment_id):
    try:
        # ... payment logic
    except Exception as e:
        log.error(f"Error: {e}")
        return False  # Caller doesn't know what went wrong

# Good (specific exceptions)
class PaymentError(Exception):
    """Base exception for payment processing"""
    pass

class InsufficientFundsError(PaymentError):
    """User balance insufficient"""
    pass

class PaymentProcessorUnavailableError(PaymentError):
    """External payment processor not responding"""
    pass

class DuplicatePaymentError(PaymentError):
    """Payment already processed"""
    pass

def process_payment(payment_id: str) -> Payment:
    """
    Process payment, raise specific exceptions.

    Raises:
        PaymentNotFoundError: Payment ID doesn't exist
        InsufficientFundsError: User balance < amount
        PaymentProcessorUnavailableError: Processor timeout/error
        DuplicatePaymentError: Payment already processed
    """
    payment = get_payment(payment_id)
    if not payment:
        raise PaymentNotFoundError(f"Payment {payment_id} not found")

    user = get_user(payment.user_id)
    if user.balance < payment.amount:
        raise InsufficientFundsError(
            f"Insufficient balance: {user.balance} < {payment.amount}"
        )

    if payment.status != 'pending':
        raise DuplicatePaymentError(f"Payment {payment_id} already {payment.status}")

    try:
        result = processor.charge(payment.amount)
    except ProcessorTimeoutError:
        raise PaymentProcessorUnavailableError("Processor timeout after 30s") from e

    return result
```

Caller can handle specific errors:
```python
try:
    result = process_payment("pay_123")
except InsufficientFundsError:
    notify_user("Please add funds to your account")
except PaymentProcessorUnavailableError:
    notify_user("Payment processing temporarily unavailable")
except PaymentError as e:
    log.error(f"Payment failed: {e}")
```

- **What:** Create specific exception types for different error scenarios
- **Why:** Allows callers to handle different errors appropriately
- **How:** Define exception hierarchy, use `raise ... from e` to chain, document exceptions in docstrings
- **Anti-pattern:** Catching generic `Exception`, silently ignoring errors, generic error messages

### 3.8 Logging Standards

**Practice: Structured Logging**

```python
import logging
import json
from datetime import datetime

# Bad logging
log.info(f"Payment processed: {payment_id}, user: {user_id}, amount: {amount}")
# Output: "Payment processed: pay_123, user: 456, amount: 99.99"
# Hard to parse, can't filter by user or amount

# Good logging (structured)
log.info(
    "payment_processed",
    extra={
        "payment_id": payment_id,
        "user_id": user_id,
        "amount": amount,
        "currency": "USD",
        "processor": "stripe",
        "latency_ms": 245,
        "trace_id": trace_id,
    }
)
# Output (JSON):
# {"level": "INFO", "message": "payment_processed", "payment_id": "pay_123", ...}
# Easy to parse, filter, aggregate in log aggregation system
```

Log levels and usage:

```python
# DEBUG: Development troubleshooting
log.debug("Database query executed", extra={"query": sql, "rows": 1523})

# INFO: Important business events
log.info("payment_processed", extra={"payment_id": "p_123", "amount": 99.99})

# WARNING: Unexpected but recoverable
log.warning("payment_processor_slow", extra={"latency_ms": 5000, "threshold_ms": 1000})

# ERROR: Error that impacted user
log.error("payment_failed", extra={
    "error_code": "processor_error",
    "processor_response": "card_declined"
})

# CRITICAL: System-wide failure
log.critical("database_unreachable", extra={"service": "payment", "downtime": 300})
```

Avoid:
```python
# ❌ Logging sensitive data
log.info(f"Card: {card_number}")
log.info(f"SSN: {ssn}")
log.info(f"API Key: {api_key}")

# ✓ Log only necessary fields
log.info("payment_processed", extra={
    "card_last_four": card_number[-4:],
    "amount": amount,
})
```

---

### 3.9 Documentation Standards

**Practice: README Excellence**

```markdown
# Payment Service

## Overview
Brief description (1-2 sentences). What does it do? Who uses it?

## Quick Start
```bash
git clone ...
npm install
npm run dev
# Service running on port 3000
```

## Architecture
System diagram. Key components. Data flow.

## API Reference

### POST /api/v1/payments
Process a payment.

**Request:**
```json
{
  "user_id": 123,
  "amount": 99.99,
  "currency": "USD"
}
```

**Response:**
```json
{
  "transaction_id": "txn_123",
  "status": "success",
  "processed_at": "2024-03-13T14:30:00Z"
}
```

**Errors:**
- 400: Invalid request
- 402: Insufficient funds
- 500: Processor error (retryable)

## Configuration
Environment variables:
- `PAYMENT_PROCESSOR_KEY`: Stripe API key
- `DATABASE_URL`: PostgreSQL connection string
- `LOG_LEVEL`: debug/info/warning/error

## Development
### Running tests
```bash
npm test              # Unit tests
npm run test:integration  # Database tests
npm run test:load     # Load testing
```

### Code style
```bash
npm run lint          # Check linting
npm run format        # Auto-format
```

## Troubleshooting
Common issues and solutions:
- **"Database connection refused":** Ensure PostgreSQL running on port 5432
- **"Payment processor timeout":** Check network, retry enabled, timeout is 30s

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md)

## References
- [Payment API Docs](https://stripe.com/docs)
- [Architecture Decision Records](./docs/adr/)
```

**Function-Level Documentation (Docstrings):**

```python
def process_payment(payment_id: str, idempotency_key: str) -> PaymentResult:
    """
    Process a payment through the configured processor.

    This function handles the full payment lifecycle:
    1. Validates payment exists and is pending
    2. Calls external processor (Stripe)
    3. Updates database with result
    4. Publishes PaymentProcessed event
    5. Notifies customer via email

    Args:
        payment_id: Unique payment identifier (e.g., 'pay_123abc')
        idempotency_key: Prevents duplicate processing if request retried

    Returns:
        PaymentResult with transaction_id, status, and timestamp

    Raises:
        PaymentNotFoundError: If payment_id doesn't exist
        InsufficientFundsError: If user balance < amount
        PaymentProcessorError: If processor returns error (retryable)
        PaymentAlreadyProcessedError: If idempotency_key seen before

    Example:
        >>> result = process_payment('pay_123', 'idem_456')
        >>> print(result.transaction_id)
        'txn_789'

    Note:
        This function is idempotent. Multiple calls with same idempotency_key
        return same result without processing twice.

    See Also:
        refund_payment() for reversal
        verify_payment() for status checking
    """
    pass
```

- **What:** Clear, accessible documentation for users and developers
- **Why:** Reduces onboarding time, prevents misuse, serves as specification
- **How:** README, API docs, docstrings, Architecture Decision Records (ADRs)
- **Anti-pattern:** Outdated docs, documentation only in Jira, no examples

### 3.10 Dependency Management

**Practice: Keeping Dependencies Updated**

```yaml
# dependabot.yml (GitHub)
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
    allow:
      - dependency-type: "direct"
    reviewers:
      - "tech-lead"
    labels:
      - "dependencies"

  # Security updates: immediate
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "daily"
    security-updates-only: true
    pull-request-branch-name:
      separator: "/"
```

Dependency audit checklist:
```bash
# Check for known vulnerabilities
npm audit

# Check for outdated packages
npm outdated

# Check for unused packages
npm ls --all | grep "(empty)"
```

Output:
```
Package          Current  Wanted  Latest
lodash          4.17.15  4.17.21  4.17.21  ❌ SECURITY UPDATE AVAILABLE
axios            0.19.0   0.21.1   1.4.0   ⚠️ Update available
express           4.17.1   4.18.2   4.18.2  ✓ Latest

npm audit fix --force  # Updates to compatible versions only
```

Strategies:
- **Major versions:** Update quarterly after testing
- **Minor versions:** Update monthly (new features, usually safe)
- **Patch versions:** Update immediately (bug fixes, security patches)
- **Pre-release versions:** Never use in production

- **What:** Regular updates to external libraries and frameworks
- **Why:** Security vulnerabilities fixed, performance improved, bugs patched
- **How:** Automate via Dependabot/Renovate, review PRs, test before merging
- **Anti-pattern:** Never updating (stale, vulnerable code), updating without testing

### 3.11 Code Ownership (CODEOWNERS)

**Practice: Team Responsibility**

```
# .github/CODEOWNERS

# Service owners
/services/payment/         @team-payments
/services/auth/            @team-auth
/services/notifications/   @team-platform

# Critical paths (require approval from security team)
/auth/                     @team-auth @security-team
/db/migrations/            @team-database @tech-lead

# Infrastructure (require platform approval)
*.tf                       @platform-team
docker-compose.yml         @platform-team
kubernetes/                @platform-team
```

When CODEOWNERS configured:
```
PR opened changing /services/payment/process.py
  ↓
GitHub automatically requests review from @team-payments
  ↓
Merge blocked until team-payments approves
  ↓
Ensures right people review code in their domain
```

- **What:** Mapping code areas to teams/individuals responsible
- **Why:** Ensures appropriate expertise reviews changes, prevents orphaned code
- **How:** Define in CODEOWNERS file, enable branch protection rule requiring approval
- **Anti-pattern:** Random reviewers without ownership, no code ownership clarity

### 3.12 Refactoring Strategies

**Practice: Continuous Incremental Refactoring**

Bad approach:
```
"We'll do a big refactor next quarter"
  ↓
Too large, scope creeps, timeline slips
  ↓
Deprioritized, never happens
  ↓
Technical debt accumulates
```

Good approach:
```
Refactoring integrated into daily work:

Commit 1: "Extract calculateTax to function" (5 min)
Commit 2: "Move tax logic to separate module" (10 min)
Commit 3: "Add type hints to TaxCalculator" (5 min)
Commit 4: "Delete duplicate tax code in legacy service" (10 min)
  ↓
Each commit tested, reviewed, merged
  ↓
System continuously improves without disruption
```

**Refactoring Techniques:**

```python
# Technique 1: Extract Method (reduce complexity)
# Before:
def process_order(order):
    # Validation (15 lines)
    if not order.customer:
        raise ValueError()
    if order.amount <= 0:
        raise ValueError()
    # ... more validation

    # Processing (20 lines)
    charge_customer()
    update_inventory()
    send_confirmation()

# After:
def process_order(order):
    validate_order(order)
    charge_and_update(order)
    notify_customer(order)

def validate_order(order):
    if not order.customer:
        raise ValueError()
    if order.amount <= 0:
        raise ValueError()
```

```python
# Technique 2: Replace Magic Numbers with Named Constants
# Before:
def calculate_price(quantity, is_vip):
    if is_vip and quantity > 100:
        return base_price * 0.8  # What is 0.8? When does it apply?

# After:
BULK_VIP_DISCOUNT = 0.2  # 20% discount
BULK_THRESHOLD = 100

def calculate_price(quantity, is_vip):
    if is_vip and quantity >= BULK_THRESHOLD:
        return base_price * (1 - BULK_VIP_DISCOUNT)
```

```python
# Technique 3: Replace Conditional with Polymorphism
# Before:
def calculate_shipping(method, weight):
    if method == 'standard':
        return weight * 5
    elif method == 'express':
        return weight * 15
    elif method == 'overnight':
        return weight * 50

# After:
class ShippingMethod:
    def calculate(self, weight): pass

class StandardShipping(ShippingMethod):
    def calculate(self, weight):
        return weight * 5

class ExpressShipping(ShippingMethod):
    def calculate(self, weight):
        return weight * 15

# Usage:
method = get_shipping_method(user_preference)  # Returns polymorphic instance
shipping_cost = method.calculate(weight)
```

- **What:** Improving code structure without changing behavior
- **Why:** Makes future changes safer and faster, reduces bugs
- **How:** Small, incremental refactorings; automated tests ensure correctness
- **Anti-pattern:** Big refactors without tests, refactoring unrelated to feature work, "premature" optimization

---

## 4. Decision Frameworks

### 4.1 Technical Debt Classification

```
Debt Type      | Severity | Time to Fix | Block Deployment?
              |         |            |
Formatting    | Low     | 5 min      | No (fix in next PR)
Unused var    | Low     | 10 min     | No
Magic numbers | Medium  | 20 min     | No
Duplicate code| Medium  | 1 hour     | No
Deep nesting  | Medium  | 2 hours    | No (unless > 10 levels)
Weak tests    | High    | 4 hours    | Yes (block merge)
Security bug  | Critical| 15 min     | Yes (hotfix)
Performance   | Medium  | 4 hours    | No (unless regression)
```

Rule: Fix critical/high immediately. Address medium on next refactoring cycle. Accept low if system is stable.

---

## 5. Checklist

### Pre-Merge Code Quality Checklist
- [ ] All tests passing (unit, integration, e2e)
- [ ] Code coverage maintained or improved
- [ ] No obvious code smells (complex functions, duplication, unused variables)
- [ ] Linting passing (no warnings)
- [ ] Type checking passing (if using TypeScript/mypy)
- [ ] Security scan passing (no hardcoded secrets, XSS, SQL injection)
- [ ] Error handling appropriate (no silent failures)
- [ ] Logging meaningful and not excessive
- [ ] Documentation updated (README, API docs, ADRs)
- [ ] Reviewed by domain expert (CODEOWNERS)
- [ ] No increase in technical debt

### Ongoing Code Quality Management
- [ ] Dependency updates reviewed monthly
- [ ] Code coverage report reviewed in sprint retrospective
- [ ] SonarQube quality gates met
- [ ] Cyclomatic complexity < 10 for all functions
- [ ] No warnings in CI pipeline
- [ ] Documentation is current (< 3 months old)
- [ ] CODEOWNERS up-to-date with team changes
- [ ] Refactoring planned for high-debt areas
- [ ] Team trained on Clean Code principles

---

## 6. Common Mistakes & Anti-Patterns

### 6.1 "We Don't Have Time for Code Review"
Reality: Code review prevents bugs that cost 10x to fix in production.

**Time investment:**
- 30 min code review now (finding bug)
- vs. 5 hours debugging + fixing in production (missing bug)
- vs. 20 hours resolving customer impact (catastrophic bug)

**Solution:** Code review is not optional; it's quality assurance.

### 6.2 100% Code Coverage as a Metric
Bad thinking: "We have 100% coverage, so code is quality"

Reality:
```python
def process_payment(amount):
    assert amount > 0  # ✓ Test executes this line
    return True        # ✓ Test executes this line
# 100% coverage, but assertion never triggers, bugs not caught
```

Good thinking: "Are critical paths tested? Are error cases covered?"

### 6.3 "Tests Will Slow Us Down"
Short-term: Writing tests adds 20% to feature time

Long-term:
- Without tests: By month 6, every change takes 2x time (fear of breaking things)
- With tests: By month 6, still same velocity (safe refactoring)

### 6.4 Ignoring Linting Warnings
Thinking: "It's just a warning, we can ignore it"

Reality: Warnings are often bugs:
```javascript
let x = 5;
console.log(x);  // ⚠️ Unused variable
// Linter: You assigned but never used? Dead code?
```

**Solution:** Treat all warnings as errors in CI; fix or disable with comment explaining why.

### 6.5 Hardcoding Secrets
Bad:
```python
STRIPE_SECRET_KEY = "sk_live_abc123def456"  # NEVER commit this!
API_PASSWORD = "p@ssw0rd123"
```

Good:
```python
import os
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')  # Load from environment
API_PASSWORD = os.getenv('API_PASSWORD')
```

Pre-commit hook to prevent:
```bash
#!/bin/bash
# .git/hooks/pre-commit
if git diff --cached | grep -E 'password|secret|token|key'; then
  echo "ERROR: Possible hardcoded secrets detected"
  exit 1
fi
```

### 6.6 No Type Safety in Dynamic Languages
JavaScript without TypeScript:
```javascript
function calculateTotal(items, discount) {
  return items.reduce((sum, item) => sum + item.price, 0) - discount;
  // What if discount is string "50"? What if item has no price?
  // Errors only found in production
}
```

With TypeScript:
```typescript
interface Item {
  id: string;
  price: number;
}

function calculateTotal(items: Item[], discount: number): number {
  return items.reduce((sum, item) => sum + item.price, 0) - discount;
  // Errors caught at compile time
}
```

### 6.7 Refactoring Without Tests
Changing code without tests → introducing subtle bugs.

**Rule:** Tests must exist before refactoring. Refactoring should not change tests.

---

## 7. Tools & References

### Linting & Formatting
- **JavaScript:** ESLint, Prettier, StandardJS
- **Python:** Pylint, Flake8, Black, Ruff
- **Java:** Checkstyle, PMD
- **Go:** golint, gofmt
- **C#/.NET:** StyleCop, Roslyn analyzers

### Static Analysis
- **SonarQube:** Industry-standard code quality
- **CodeClimate:** SaaS alternative, GitHub integration
- **Codacy:** Automated code review
- **DeepCode:** AI-powered code reviews

### Type Checking
- **TypeScript:** JavaScript with types
- **mypy:** Python type checker
- **Pyright:** Python static type checker
- **Java/C#:** Built-in type systems

### Security Scanning
- **SonarQube Security:** Part of SonarQube
- **Snyk:** Dependency vulnerability scanning
- **WhiteSource:** Software composition analysis
- **Semgrep:** Custom security rules

### Documentation
- **Swagger/OpenAPI:** API documentation
- **MkDocs:** Markdown-based documentation
- **Sphinx:** Python documentation
- **GitHub Pages:** Host documentation

### References
- *Clean Code* by Robert C. Martin — Essential reading
- *The Pragmatic Programmer* — Best practices
- *Refactoring* by Martin Fowler — Refactoring techniques
- *Code Complete* by Steve McConnell — Comprehensive guide
- Martin Fowler's blog — Architecture, patterns, practices

---

**Key Takeaway:** Code quality is not an afterthought; it's built into every commit. Invest in tooling, processes, and team culture that prioritizes maintainability. Short-term velocity gains from cutting corners create long-term velocity losses from technical debt.

---

*For Vietnamese engineers (dành cho kỹ sư Cường):*
- **Code review:** Kiểm tra mã bởi đồng nghiệp trước khi hợp nhất
- **Linting:** Kiểm tra tự động định dạng và lỗi cú pháp
- **Static analysis:** Phân tích mã để phát hiện lỗ hổng bảo mật
- **Refactoring:** Cải thiện cấu trúc mã mà không thay đổi hành vi
- **Technical debt:** Nợ kỹ thuật từ những quyết định thiết kế xấu
- **Clean code:** Mã dễ hiểu, dễ bảo trì
- **DRY:** Don't Repeat Yourself - tránh lặp lại mã
- **CODEOWNERS:** Người chịu trách nhiệm cho từng phần mã
- **Type safety:** Kiểm tra loại dữ liệu ở thời điểm biên dịch
- **Documentation:** Tài liệu mô tả cách sử dụng và thiết kế hệ thống
