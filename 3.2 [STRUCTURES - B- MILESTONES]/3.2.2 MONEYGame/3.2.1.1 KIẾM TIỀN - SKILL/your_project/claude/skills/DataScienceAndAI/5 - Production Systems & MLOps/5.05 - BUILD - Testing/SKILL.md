# Testing Best Practices for Production Systems

> **Domain:** 5.05 | **Group:** BUILD | **Lifecycle:** Build Time
> **Last Updated:** 2026-03-13
> **Scope:** Testing Strategies, Test Pyramid, Performance & Security Testing

---

## 1. Overview

Testing is the primary defense against bugs reaching production. This domain covers the testing pyramid, testing strategies, and quality assurance practices that build confidence in production systems.

**Testing Impact on Reliability:**
```
Without tests:     "We're scared to deploy" (error rate 5-10%)
Manual testing:    "It takes 2 weeks to release" (error rate 1-2%)
Unit + Integration: "Confident daily deployments" (error rate 0.1-0.5%)
E2E + Load testing: "Can scale safely" (error rate < 0.1%)
```

**Goals:**
- Catch bugs before production (shift left)
- Enable fearless refactoring and optimization
- Document expected system behavior
- Reduce MTTR when production issues do occur
- Balance thoroughness with development speed

---

## 2. Core Principles

### 2.1 Test Pyramid: Lots of Unit, Fewer Integration, Few E2E
```
        △
       /E\
      / 2E \    Few tests (slow, brittle)
     /─────\
    /Integr.\   Medium tests (moderate speed)
   /─────────\
  / Unit Test \  Many tests (fast, reliable)
 /─────────────\
```

Cost and speed (per test):
- **Unit:** 1ms, $0.001
- **Integration:** 100ms, $0.10
- **E2E:** 5s, $5 (includes infrastructure startup, user simulation)

**Target Distribution:** 70% unit, 20% integration, 10% e2e

### 2.2 Test-Driven Development (TDD)
Write tests BEFORE implementing feature:
1. Red: Write failing test that describes desired behavior
2. Green: Write minimal code to make test pass
3. Refactor: Clean up code, maintain passing tests

Benefits: Forces design thinking, prevents over-engineering, excellent documentation.

### 2.3 Fast Feedback Loop
Tests should complete in < 5 minutes for local CI. Slow tests are skipped.

### 2.4 Meaningful Coverage Over 100%
Coverage metric: "Are critical paths tested?" not "Is every line executed?"

Target: 80%+ coverage on **critical paths** (payment, auth, data integrity). 50% on utilities is acceptable.

### 2.5 Reproducibility
Tests must pass/fail consistently. Flaky tests undermine confidence and waste time.

---

## 3. Best Practices

### 3.1 Unit Testing

**Practice: Isolated, Fast Unit Tests**

```python
# tests/payment/test_charge.py
import pytest
from unittest.mock import Mock, patch
from payment.charge import Charge

class TestChargeCalculation:
    """Test core charge calculation logic in isolation"""

    def test_calculates_total_with_tax(self):
        # Arrange
        charge = Charge(subtotal=100.00, tax_rate=0.10)

        # Act
        total = charge.calculate_total()

        # Assert
        assert total == 110.00

    def test_applies_discount_correctly(self):
        charge = Charge(subtotal=100.00, discount_percent=10)
        assert charge.calculate_total() == 90.00

    def test_rejects_negative_amounts(self):
        with pytest.raises(ValueError, match="Amount must be positive"):
            Charge(subtotal=-50.00)

    @patch('payment.charge.exchange_rate_service')
    def test_converts_currency(self, mock_exchange_rate):
        """Unit test with mocked external dependency"""
        mock_exchange_rate.get_rate.return_value = 0.92  # EUR/USD

        charge = Charge(subtotal=100.00, currency="EUR")
        charge.convert_to_usd()

        assert charge.total_usd == 92.00
        # Verify the mock was called correctly
        mock_exchange_rate.get_rate.assert_called_once_with("EUR", "USD")

class TestChargeValidation:
    """Separate test class for validation logic"""

    @pytest.mark.parametrize("invalid_amount", [-1, 0, None])
    def test_rejects_invalid_amounts(self, invalid_amount):
        with pytest.raises((ValueError, TypeError)):
            Charge(subtotal=invalid_amount)
```

- **What:** Tests for individual functions/methods with mocked dependencies
- **Why:** Fast (run in milliseconds), isolated (failures pinpoint exact issue), repeatable
- **How:** Use AAA pattern (Arrange-Act-Assert), mock external dependencies, use parameterized tests for edge cases
- **Anti-pattern:** Tests that depend on database, file system, or external APIs; too broad test scope

**Coverage Goals for Unit Tests:**
- Happy path (normal operation)
- Edge cases (empty input, boundary values)
- Error paths (invalid input, exceptions)
- Rarely: Implementation details (test behavior, not code)

### 3.2 Integration Testing

**Practice: Database Integration Tests with Testcontainers**

```python
# tests/integration/test_payment_repository.py
import pytest
from testcontainers.postgres import PostgresContainer
from payment.repository import PaymentRepository

@pytest.fixture(scope="session")
def postgres_container():
    """Spin up real Postgres for integration tests"""
    container = PostgresContainer("postgres:15-alpine")
    container.start()
    yield container
    container.stop()

@pytest.fixture
def payment_repo(postgres_container):
    """Create repository with test database"""
    connection_string = postgres_container.get_connection_url()
    repo = PaymentRepository(connection_string)
    repo.init_schema()  # Create tables
    yield repo
    repo.cleanup()  # Drop tables after test

class TestPaymentRepository:
    """Integration tests with real database"""

    def test_saves_and_retrieves_payment(self, payment_repo):
        # Arrange
        payment = Payment(
            user_id=123,
            amount=99.99,
            status="pending"
        )

        # Act
        saved_id = payment_repo.save(payment)
        retrieved = payment_repo.get(saved_id)

        # Assert
        assert retrieved.user_id == 123
        assert retrieved.amount == 99.99
        assert retrieved.status == "pending"

    def test_concurrent_payments_dont_lose_data(self, payment_repo):
        """Test database concurrency/isolation"""
        import threading

        payments = []
        def save_payment(amount):
            payment = Payment(user_id=456, amount=amount)
            payments.append(payment_repo.save(payment))

        threads = [
            threading.Thread(target=save_payment, args=(i,))
            for i in range(1, 11)  # 10 concurrent saves
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Verify all 10 payments saved
        assert len(payments) == 10
        all_payments = payment_repo.list_all()
        assert len(all_payments) == 10

    def test_handles_database_connection_loss(self, payment_repo):
        """Test resilience to temporary failures"""
        payment_repo.connection.close()

        with pytest.raises(DatabaseException):
            payment_repo.get(999)

        # Connection should be automatically re-established
        payment_repo.reconnect()
        # Now should work
        assert payment_repo.get(999) is None
```

Benefits of Testcontainers:
- Real database (catches SQL bugs, concurrency issues)
- Isolated per test (no shared state)
- Ephemeral (automatic cleanup)
- Docker-based (same DB as production)

- **What:** Tests that exercise system components together with real dependencies
- **Why:** Catch integration bugs (e.g., ORM misconfigurations, concurrency issues) that unit tests miss
- **How:** Use Testcontainers, set up isolated databases per test, clean up after
- **Anti-pattern:** Sharing test database across tests, testing too many components in one test

### 3.3 End-to-End (E2E) Testing

**Practice: User Journey E2E Tests with Playwright**

```python
# tests/e2e/test_payment_checkout.py
import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        yield browser
        browser.close()

class TestCheckoutFlow:
    """Full user journey through checkout"""

    def test_complete_payment_flow(self, browser):
        """User visits site → adds item → checks out → pays → receives confirmation"""
        page = browser.new_page()

        # Step 1: User visits product page
        page.goto("https://shop.example.com/products/laptop")
        page.click("text=Add to Cart")

        # Step 2: Navigate to cart
        page.click("text=View Cart")
        assert "1 item" in page.content()

        # Step 3: Click checkout
        page.click("button:has-text('Checkout')")

        # Step 4: Fill payment form
        page.fill("input[name='card-number']", "4242 4242 4242 4242")
        page.fill("input[name='expiry']", "12/25")
        page.fill("input[name='cvc']", "123")
        page.click("button:has-text('Pay')")

        # Step 5: Verify confirmation
        page.wait_for_url("**/confirmation/**")
        assert "Order confirmed" in page.content()
        assert "$999.99" in page.content()

        page.close()

    def test_user_can_return_to_cart_and_edit(self, browser):
        page = browser.new_page()
        page.goto("https://shop.example.com")
        # ... add item to cart

        # Navigation back should work
        page.go_back()
        assert page.url.endswith("/products/laptop")

        page.close()
```

- **What:** Automated tests simulating real user journeys through the application
- **Why:** Catches issues that only appear with full stack (UI, API, database, external services)
- **How:** Use Playwright/Cypress/Selenium, test critical user flows, run daily (too slow for every commit)
- **Anti-pattern:** Testing every button click, testing implementation details instead of behavior

**E2E Test Maintenance:**
- Keep tests focused on user value (checkout, login, search)
- Avoid testing third-party integrations (Stripe, Google Maps) — use stubs instead
- Refactor selectors into Page Object Model to reduce maintenance

### 3.4 Contract Testing (API Contracts)

**Practice: Pact Testing for Microservices**

Scenario: Order Service depends on Payment Service API

```python
# tests/contract/test_payment_service_contract.py
from pact import Consumer, Provider

pact = Consumer('OrderService').has_expectation_with(
    Provider('PaymentService'),
    upon_receiving='a request for payment processing',
    with_request='post', '/api/v1/payments',
    will_respond_with=200,
)

@pact.interaction
def test_order_service_calls_payment_service():
    """Order Service and Payment Service must agree on API contract"""

    # Expected request from Order Service
    with pact:
        pact.set_request(
            'POST',
            '/api/v1/payments',
            body={
                'user_id': 123,
                'amount': 99.99,
                'currency': 'USD'
            }
        )

        # Expected response from Payment Service
        pact.expect_status(200)
        pact.expect_body({
            'transaction_id': '12345',
            'status': 'success',
            'timestamp': mock.ANY(str)
        })

        # Call payment service client
        payment_client = PaymentServiceClient(
            base_url='http://localhost:8080'
        )
        result = payment_client.process_payment(123, 99.99, 'USD')

        assert result['status'] == 'success'
        assert result['transaction_id'] == '12345'

    # After test, pact writes contract file
    # Contract is verified by Payment Service in its CI
```

Benefits:
- **Consumer-Driven:** Consumers define what they need, providers implement to spec
- **Prevents Integration Breakage:** Catches API mismatches before production
- **Documentation:** Contracts serve as API documentation
- **Decouples Teams:** Order Service and Payment Service teams can develop independently

- **What:** API contracts defining request/response expectations between services
- **Why:** Prevents breaking changes in distributed systems, enables independent deployments
- **How:** Define contracts in tests, verify both sides (consumer and provider)
- **Anti-pattern:** Testing implementation details instead of API contracts

### 3.5 Load Testing

**Practice: Load Testing with k6**

```javascript
// tests/load/payment-api.js
import http from 'k6/http';
import { check, group, sleep } from 'k6';

// Define load stages
export let options = {
  stages: [
    { duration: '2m', target: 100 },   // Ramp up to 100 users
    { duration: '5m', target: 100 },   // Stay at 100 users
    { duration: '2m', target: 200 },   // Ramp up to 200
    { duration: '5m', target: 200 },   // Hold
    { duration: '1m', target: 0 },     // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<200', 'p(99)<500'],  // p95 < 200ms
    http_req_failed: ['rate<0.1'],                  // Error rate < 0.1%
  },
};

export default function() {
  let authToken;

  group('Authentication', function() {
    let res = http.post('https://api.example.com/login', {
      email: `user${__VU}@example.com`,  // ${__VU} = virtual user ID
      password: 'password123'
    });

    check(res, {
      'login succeeded': (r) => r.status === 200,
      'token present': (r) => r.json('token') !== null,
    });

    authToken = res.json('token');
  });

  group('Process Payment', function() {
    let res = http.post(
      'https://api.example.com/payments',
      {
        amount: 99.99,
        currency: 'USD',
        user_id: __VU,
      },
      {
        headers: {
          'Authorization': `Bearer ${authToken}`,
          'Content-Type': 'application/json',
        },
      }
    );

    check(res, {
      'payment processed': (r) => r.status === 200,
      'response time < 500ms': (r) => r.timings.duration < 500,
    });
  });

  sleep(1);  // Wait 1 second between requests (simulates real user think time)
}
```

Running the test:
```bash
k6 run tests/load/payment-api.js

# Output:
# ✓ login succeeded | ✓ token present | ✗ response time < 500ms (5% of requests violated)
# http_req_duration: avg=450ms, p95=620ms, p99=1200ms
# Error rate: 0.3% (above threshold of 0.1%)
```

- **What:** Simulating hundreds/thousands of concurrent users to measure system behavior under load
- **Why:** Production issues often only appear at scale (database connection pools, cache storms, race conditions)
- **How:** Use k6, Locust, or JMeter; define realistic user scenarios; monitor resource usage
- **Anti-pattern:** Load testing only happy path, not load testing before peak load events

**Load Testing Checklist:**
- [ ] Test at 2x expected peak load
- [ ] Measure p95 and p99 latency (not just average)
- [ ] Monitor resource usage (CPU, memory, database connections)
- [ ] Test gradual load increase (ramp-up), not spike
- [ ] Define clear SLA thresholds and fail if exceeded
- [ ] Load test before Black Friday, major events, or marketing campaigns

### 3.6 Chaos Testing

**Practice: Injecting Failures to Test Resilience**

```python
# tests/chaos/test_payment_resilience.py
import pytest
from chaos_toolkit import chaos_test

@chaos_test
def test_payment_survives_database_timeout():
    """
    Hypothesis: Payment service remains responsive even if database times out.

    Chaos action: Inject 10 second latency on all database queries.
    Expected: Payment service returns error to user (instead of hanging).
    """
    # Baseline: Normal payment flow
    payment_client = PaymentClient()
    start = time.time()
    result = payment_client.process_payment(amount=100)
    baseline_latency = time.time() - start
    assert result.success
    assert baseline_latency < 1  # Should be fast

    # Chaos: Inject database latency
    with chaos_inject_latency(target='database', latency_ms=10000):
        # Payment should timeout gracefully, not hang forever
        try:
            result = payment_client.process_payment(
                amount=100,
                timeout_ms=5000  # 5 second timeout
            )
        except TimeoutError:
            # Expected: client detects timeout and responds with error
            pass

        # Verify the service is still operational
        healthy = payment_client.health_check()
        assert healthy, "Service should recover after transient failure"


@chaos_test
def test_payment_survives_payment_processor_down():
    """
    Hypothesis: Payment system is resilient to external payment processor outages.

    Chaos action: Make external payment processor unresponsive (network chaos).
    """
    with chaos_inject_network_error(target='stripe.com', error='timeout'):
        # Should fail gracefully or retry
        payment_client = PaymentClient()
        result = payment_client.process_payment(amount=100)

        # Either succeeds (via retry/fallback) or fails cleanly
        assert result.status in ['success', 'failed_with_message']
        # But NOT: hanging, returning success when it actually failed
```

Common chaos tests:
- Database query timeout → Service should circuit break or return error, not hang
- External API down → Service should retry or fallback, not cascade failure
- Disk full → Service should alert, not silently drop data
- Memory pressure → Service should shed load, not OOM
- Network partition → Service should detect and recover, not split-brain

- **What:** Deliberately injecting failures to test system resilience
- **Why:** Production failures happen; systems should degrade gracefully instead of catastrophically
- **How:** Use chaos-toolkit, gremlin, or custom test utilities; start with small blasts, increase scope
- **Anti-pattern:** Running chaos without monitoring, not having rollback plan, testing in production without safeguards

### 3.7 Mutation Testing

**Practice: Ensure Tests Actually Catch Bugs**

```python
# Original tested code
def calculate_discount(price, discount_percent):
    return price * (1 - discount_percent / 100)

# Your tests
def test_calculates_discount():
    assert calculate_discount(100, 10) == 90.0

# Mutation testing runs:
# Mutation 1: return price * (discount_percent / 100)
#   TEST: 90.0 == 90.0? NO! Mutation caught ✓

# Mutation 2: return price * (1 + discount_percent / 100)
#   TEST: 110.0 == 90.0? NO! Mutation caught ✓

# Mutation 3: return price * (1 - discount_percent / 101)
#   TEST: 89.9 == 90.0? NO! Mutation caught ✓

# If mutation passed test, your test is weak
```

Running mutation tests (Python):
```bash
pip install mutmut
mutmut run --paths-to-mutate=payment/

# Results show mutation score:
# Mutation Score: 92% (92 of 100 mutations killed)
# Weak tests in: payment/discount.py line 45
```

- **What:** Automatically introduce bugs into code, verify tests catch them
- **Why:** High code coverage is meaningless if tests don't catch actual bugs
- **How:** Use mutmut (Python), stryker (JavaScript/Java), run in CI
- **Anti-pattern:** Chasing 100% mutation score (diminishing returns), only testing for coverage

### 3.8 Snapshot Testing

**Practice: Detect Unintended Changes**

```javascript
// tests/snapshot/invoice.test.js
describe('Invoice PDF generation', () => {
  it('generates invoice with correct layout', () => {
    const invoice = generateInvoice({
      user: 'John Doe',
      items: [{ name: 'Laptop', price: 999.99 }],
      total: 999.99
    });

    // First run: snapshot saved
    expect(invoice).toMatchSnapshot();

    // Future runs: Snapshot compared
    // If code changes, snapshot mismatch alerts developer:
    // "Review change: Is this intentional?"
  });
});

// Snapshot file (tests/snapshot/__snapshots__/invoice.test.js.snap)
/*
exports[`Invoice PDF generation generates invoice with correct layout 1`] = `
"Invoice to: John Doe
Item: Laptop - $999.99
Total: $999.99
Tax: $0.00
"`;
*/
```

Use cases:
- UI rendered output (catch accidental layout changes)
- PDF/report generation (catch format changes)
- API response structure (catch contract violations)

- **What:** Capture expected output, detect changes on future runs
- **Why:** Catches unintended behavior changes that would otherwise go unnoticed
- **How:** Use Jest, Vitest, or language-specific snapshot tools; review snapshot changes carefully
- **Anti-pattern:** Automatically updating snapshots without review, using for non-deterministic output

### 3.9 API Testing Strategies

**Practice: Comprehensive API Testing**

```python
# tests/api/test_payment_endpoints.py
import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

class TestPaymentAPI:

    def test_invalid_payload_returns_400(self):
        """Missing required fields"""
        response = client.post(
            "/api/v1/payments",
            json={"amount": 100}  # Missing user_id
        )
        assert response.status_code == 400
        assert "user_id required" in response.json()['error']

    def test_negative_amount_returns_422(self):
        """Validation error on invalid value"""
        response = client.post(
            "/api/v1/payments",
            json={"user_id": 123, "amount": -50}
        )
        assert response.status_code == 422

    def test_permission_denied_returns_403(self):
        """User cannot access others' payments"""
        # User 123 trying to refund user 456's payment
        response = client.post(
            "/api/v1/payments/999/refund",
            headers={"Authorization": "Bearer user123token"}
        )
        assert response.status_code == 403

    def test_successful_payment_returns_202(self):
        """Accepted for processing"""
        response = client.post(
            "/api/v1/payments",
            json={"user_id": 123, "amount": 99.99, "currency": "USD"}
        )
        assert response.status_code == 202
        assert 'transaction_id' in response.json()

    def test_response_includes_required_headers(self):
        """Verify security and caching headers"""
        response = client.get("/api/v1/payments/123")

        assert 'X-Request-ID' in response.headers
        assert 'Cache-Control' in response.headers
        assert response.headers['Cache-Control'] == 'no-store'
        assert 'X-XSS-Protection' in response.headers
```

API test categories:
- **Happy Path:** Valid requests return expected results
- **Input Validation:** Invalid payloads return 400/422
- **Authentication:** Unauthenticated requests return 401
- **Authorization:** Users cannot access others' resources (return 403)
- **Rate Limiting:** Excess requests return 429
- **Headers:** Required security headers present
- **Pagination:** Large result sets paginated correctly
- **Caching:** Appropriate cache headers set

### 3.10 Database Testing

**Practice: Testing Complex Queries**

```sql
-- tests/database/test_payment_queries.sql

-- Test: Find payments from last 30 days with status tracking
SELECT COUNT(*) as recent_payment_count
FROM payments
WHERE created_at > NOW() - INTERVAL '30 days'
  AND status IN ('success', 'pending');

-- Expected: Returns count, query completes < 100ms
-- (Ensures INDEX on (created_at, status) exists)

-- Test: Concurrent transaction isolation
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;
  UPDATE wallet SET balance = balance - 100 WHERE user_id = 123;
  -- Concurrent transaction also tries to debit same wallet
  -- Should fail with serialization error, not apply double debit
END;

-- Test: Cascade delete behavior
DELETE FROM users WHERE id = 456;
-- Should delete user, related payments, related refunds (if CASCADE defined)
-- Should NOT leave orphaned records
SELECT COUNT(*) FROM payments WHERE user_id = 456;
-- Expected: 0 rows (verified cascade worked)
```

Database test goals:
- **Query Performance:** Queries return in expected time with indexes
- **Data Integrity:** Foreign keys, constraints enforced
- **Transaction Isolation:** Concurrent transactions don't interfere
- **Backup Integrity:** Restored backups have consistent data

---

## 4. Decision Frameworks

### 4.1 Test Type Selection

| Test Type | Speed | Coverage | Cost | Best For |
|-----------|-------|----------|------|----------|
| Unit | <1ms | Single function | Low | Core logic, algorithms |
| Integration | 100ms | Component interaction | Med | Database, APIs, caching |
| E2E | 5s+ | Full user journey | High | Critical workflows |
| Load | Variable | System limits | High | Scalability testing |
| Contract | 100ms | API compatibility | Med | Microservices |
| Mutation | Variable | Test quality | High | Ensuring tests work |

**Decision Tree:**
```
Need to test...
├─ Pure function/logic → Unit test
├─ Component interaction (DB, cache) → Integration test
├─ Complete user journey → E2E test
├─ System under load → Load test
├─ API compatibility across services → Contract test
└─ Quality of existing tests → Mutation test
```

### 4.2 Coverage Goals by Domain

| Domain | Target | Critical Paths | Why |
|--------|--------|-----------------|-----|
| Payment processing | 95%+ | Yes (financial risk) | Missing payment logic = revenue loss |
| Authentication | 90%+ | Yes (security) | Auth bypass = data breach |
| Data persistence | 85%+ | Yes (data loss) | Query bugs = corrupted data |
| Utilities | 50%+ | No | Non-critical, low risk |
| UI rendering | 40%+ | No | Tested manually, high churn |

---

## 5. Checklist

### Before Merging Code
- [ ] All unit tests passing locally and in CI
- [ ] New code has test coverage (minimum 70%)
- [ ] Integration tests pass on staging database
- [ ] No flaky tests (run 3x locally to verify)
- [ ] Test names describe behavior, not implementation
- [ ] No hardcoded test data (use fixtures)
- [ ] Error cases tested (not just happy path)
- [ ] External API calls mocked (not real calls in tests)

### Load Testing Requirements
- [ ] Load test run against staging environment
- [ ] Test scenario reflects real user behavior
- [ ] P95 and P99 latency below SLA
- [ ] Error rate below acceptable threshold
- [ ] No memory leaks detected
- [ ] Database connection pool not exhausted
- [ ] Results documented with test parameters

### Security Testing
- [ ] SAST (static analysis) passing (ESLint, Bandit, SonarQube)
- [ ] DAST (penetration testing) run against staging
- [ ] SQL injection tests for all database queries
- [ ] XSS prevention tested (input sanitization)
- [ ] CSRF tokens validated
- [ ] No sensitive data in logs or error messages
- [ ] Authentication/authorization edge cases tested

---

## 6. Common Mistakes & Anti-Patterns

### 6.1 Testing Implementation, Not Behavior
Bad:
```python
def test_create_user():
    user = User()
    user.first_name = "John"  # Testing the assignment
    assert user.first_name == "John"
```

Good:
```python
def test_user_can_login():
    user = create_user("john@example.com", "password123")
    assert user.is_authenticated is True
    assert user.last_login is not None
```

### 6.2 Shared Test State
Bad:
```python
# Shared database across tests
@pytest.fixture(scope="session")
def db():
    return Database()  # Same DB for all tests

# Test 1 leaves data that affects Test 2
def test_create_payment(db):
    db.payments.insert(...)

def test_list_payments(db):
    payments = db.payments.list()
    # Will find payment from previous test!
```

Good:
```python
@pytest.fixture
def db():  # scope="function" (default)
    database = Database()
    database.setup()  # Create clean schema
    yield database
    database.teardown()  # Clean up after each test
```

### 6.3 Flaky Tests (Timing-Dependent)
Bad:
```python
def test_message_received():
    send_message("hello")
    time.sleep(1)  # Hope it's received by then?
    assert received_messages[-1] == "hello"  # Could have other messages
```

Good:
```python
def test_message_received():
    received = []
    def on_message(msg):
        received.append(msg)

    subscription = subscribe(on_message)
    send_message("hello")

    # Wait for specific message (with timeout)
    wait_for(lambda: "hello" in received, timeout=5)

    subscription.unsubscribe()
```

### 6.4 Testing External Services (Stripe, Google, AWS)
Bad:
```python
def test_charge_with_stripe():
    # Makes real API call to Stripe during tests!
    charge = stripe.Charge.create(amount=100, source="tok_visa")
    assert charge.status == "succeeded"
    # Cost: $1.00 per test run, slow, flaky, creates test data
```

Good:
```python
@patch('stripe.Charge.create')
def test_charge_with_stripe(mock_create):
    mock_create.return_value = Mock(status='succeeded', id='ch_123')

    charge = process_payment(100)

    assert charge.status == 'succeeded'
    mock_create.assert_called_once_with(amount=100, ...)
    # Fast, free, deterministic
```

### 6.5 Skipping Tests Instead of Fixing Them
Bad:
```python
@pytest.mark.skip("flaky on CI")
def test_concurrent_updates():
    # Test is skipped, no one fixes it
    pass
```

Good:
```python
def test_concurrent_updates():
    # Fix the actual concurrency issue
    # Use locks/transactions properly
    # Test now passes consistently
    pass
```

### 6.6 No Load Testing Before Peak Events
Thinking: "We've been fine for a year, why would Black Friday be different?"

Reality: One viral post or news mention can drive 10x normal traffic. Database connections exhaust, API timeouts spike, cascading failures.

**Solution:** Load test before major events, monitor p99 latency, be ready to scale.

### 6.7 Treating Snapshot Tests as Holy
Bad:
```python
# Any code change breaks snapshot
# Developer just does: pytest --snapshot-update
# Without actually reviewing the change
```

Good:
```python
# Review snapshot changes carefully
# Ask: Is this change intentional?
# Snapshot update should be deliberate, not automatic
```

---

## 7. Tools & References

### Testing Frameworks
- **Python:** pytest (simple, powerful), unittest (standard library)
- **JavaScript/Node:** Jest (snapshot testing), Vitest (fast), Mocha (flexible)
- **Java:** JUnit 5, TestNG
- **Go:** testing (standard), testify
- **C#/.NET:** xUnit, NUnit

### Integration & Database Testing
- **Testcontainers:** Run Docker containers for databases in tests
- **LocalStack:** Local AWS services for testing
- **Docker Compose:** Multi-service test environments

### Load & Performance Testing
- **k6:** Modern load testing, nice visualizations, scriptable
- **Locust:** Python-based, developer-friendly
- **Apache JMeter:** Java-based, powerful but steep learning curve
- **Gatling:** Scala-based, great for CI/CD integration

### API Testing
- **Postman:** UI-based API testing
- **REST Assured:** Java library for API testing
- **Requests (Python):** Simple HTTP testing

### Security Testing
- **SAST (Static):** ESLint, Bandit, SonarQube, Checkmarx
- **DAST (Dynamic):** OWASP ZAP, Burp Suite, acunetix
- **Dependency Scanning:** Dependabot, Snyk, WhiteSource

### Test Automation CI
- **GitHub Actions:** Native, generous free tier
- **CircleCI:** Great caching, performance insights
- **GitLab CI:** Built-in, excellent documentation

### References
- *Google Testing Blog* — Best practices from tech giants
- *Martin Fowler's Test Pyramid* — Testing strategy foundation
- *Accelerate* by Forsgren et al. — Data on testing ROI
- *Growing Object-Oriented Software, Guided by Tests* — TDD deep dive
- *The Phoenix Project* — Business case for quality testing

---

**Key Takeaway:** Good tests enable fast, confident deployments. Invest in test infrastructure (CI, databases, load testing platforms) early. Measure test quality (mutation score, coverage of critical paths), not just coverage percentage.

---

*For Vietnamese engineers (dành cho kỹ sư Cường):*
- **Unit test:** Kiểm tra một hàm/phương thức trong cô lập
- **Integration test:** Kiểm tra tương tác giữa các thành phần (DB, cache)
- **E2E test:** Kiểm tra toàn bộ hành trình người dùng
- **Load test:** Kiểm tra hệ thống dưới tải cao
- **Flaky test:** Test không ổn định, có khi pass có khi fail
- **Mock/Stub:** Thay thế dependency bên ngoài trong test
- **Test pyramid:** Nhiều unit test, ít E2E test (vì tốc độ)
- **Canary deployment:** Triển khai dần, theo dõi kỹ lưỡng từng bước
