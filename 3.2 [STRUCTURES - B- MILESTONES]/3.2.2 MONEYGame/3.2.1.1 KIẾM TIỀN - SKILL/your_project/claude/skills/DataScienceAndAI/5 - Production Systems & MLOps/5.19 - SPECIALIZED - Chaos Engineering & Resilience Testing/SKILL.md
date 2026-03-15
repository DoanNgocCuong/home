# Chaos Engineering & Resilience Testing — Production Best Practices

> **Domain:** 5.19 | **Group:** SPECIALIZED | **Lifecycle:** Specialized
> **Last Updated:** 2026-03-13

## 1. Overview

Chaos Engineering is the practice of intentionally breaking systems to find weaknesses before users do. It answers:
- Can we survive a database failure?
- What happens when we lose 30% network connectivity?
- How does the system degrade under extreme load?

**Core Principle:** Better to learn from controlled failure than catastrophic surprise.

**Netflix Chaos Monkey** (2010): Randomly terminates production servers. Result: Netflix became resilient infrastructure leader.

## 2. Core Principles

### 2.1 Steady-State Hypothesis
Define normal behavior, then intentionally break things while monitoring metrics:

```
Normal (steady-state):
- API latency: 50ms (p99)
- Error rate: 0.1%
- Requests/sec: 1000

Experiment:
- Kill 2 out of 3 database replicas
- Measure impact

Expected:
- Latency increases, but stays <500ms
- Error rate increases but <5%
- Requests/sec drops to 800

If it doesn't: We've discovered a weakness!
```

### 2.2 Blast Radius Control
- **Small blasts first**: Test with 1% of traffic
- **Escalate gradually**: 1% → 5% → 10% → 25% → 100%
- **Kill switches**: Always ready to revert
- **Rollback plan**: Know how to restore within minutes

### 2.3 Game Days
Regular exercises where team practices response:
- Simulate outage scenario
- Team works through incident response
- Debrief: What went well? What failed?
- Document learnings & improvements

## 3. Best Practices

### 3.1 Chaos Monkey: Random Infrastructure Failure

**Practice: Randomly Terminate Instances**

```python
import random
import boto3
from datetime import datetime
import logging

class ChaosMoneky:
    """Netflix-style chaos injection"""

    def __init__(self, aws_region='us-east-1'):
        self.ec2 = boto3.client('ec2', region_name=aws_region)
        self.asg = boto3.client('autoscaling', region_name=aws_region)
        self.cloudwatch = boto3.client('cloudwatch', region_name=aws_region)

    def terminate_random_instance(self, asg_name):
        """Randomly kill instance in ASG (kết thúc)"""

        # Get instances in ASG
        response = self.asg.describe_auto_scaling_groups(
            AutoScalingGroupNames=[asg_name]
        )

        instances = response['AutoScalingGroups'][0]['Instances']

        if not instances:
            logging.warning(f"No instances in {asg_name}")
            return None

        # Select random instance
        target = random.choice(instances)
        instance_id = target['InstanceId']

        logging.info(f"Chaos: Terminating {instance_id}")

        # Terminate (AWS Auto-Scaling will launch replacement)
        self.ec2.terminate_instances(InstanceIds=[instance_id])

        # Record metric
        self.cloudwatch.put_metric_data(
            Namespace='ChaosEngineering',
            MetricData=[{
                'MetricName': 'InstanceTerminated',
                'Value': 1,
                'Unit': 'Count',
                'Dimensions': [{'Name': 'ASG', 'Value': asg_name}]
            }]
        )

        return instance_id

    def should_inject_failure(self, probability=0.001):
        """Decide whether to inject failure this second"""
        # Probability of 0.001 = ~2.5 times per 46 hours
        return random.random() < probability

    def run_continuous(self, asg_name):
        """Run chaos continuously in background"""
        while True:
            if self.should_inject_failure():
                self.terminate_random_instance(asg_name)
            time.sleep(1)

# Run chaos
# chaos = ChaosMonkey()
# chaos.run_continuous('web-server-asg')
```

### 3.2 Litmus Chaos: Kubernetes Failure Injection

**Practice: Chaos Experiments on K8s**

```yaml
# chaos-experiment.yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: app-resilience-test
spec:
  appinfo:
    appns: production
    applabel: "app=payment-service"  # Target pods
    appkind: deployment

  engineState: "active"

  chaosServiceAccount: chaos-user

  experiments:
    - name: pod-delete
      spec:
        components:
          env:
            - name: TOTAL_CHAOS_DURATION
              value: "60"  # Chaos for 60 seconds
            - name: CHAOS_INTERVAL
              value: "10"  # Kill pod every 10 seconds

    - name: container-kill
      spec:
        components:
          env:
            - name: TARGET_CONTAINER_NAME
              value: "payment-app"
            - name: CHAOS_DURATION
              value: "60"

    - name: network-chaos
      spec:
        components:
          env:
            - name: NETWORK_DELAY
              value: "250"  # Add 250ms latency
            - name: PACKET_LOSS_PERCENTAGE
              value: "5"    # Lose 5% packets
            - name: CHAOS_DURATION
              value: "60"

  resultName: chaos-test-result
```

### 3.3 Gremlin: Commercial Chaos Platform

**Practice: Systematic Failure Injection**

```python
from gremlin_python_sdk import GremlinAPIClient

class GremlinChaosRunner:
    """Run Gremlin experiments for chaos engineering"""

    def __init__(self, api_key):
        self.client = GremlinAPIClient(api_key)

    def test_cpu_stress(self, target_label, duration=120):
        """Stress CPU to 100%"""
        experiment = {
            "name": "CPU Stress Test",
            "description": "Stress CPU to saturation",
            "target": {"labels": target_label},
            "action": {
                "type": "cpu",
                "config": {
                    "cores": -1,  # All cores
                    "duration": duration,
                    "percent": 100  # 100% CPU
                }
            }
        }

        result = self.client.run_experiment(experiment)
        return result

    def test_disk_full(self, target_label, duration=120):
        """Simulate disk full condition"""
        experiment = {
            "name": "Disk Full Test",
            "description": "Fill disk to capacity",
            "target": {"labels": target_label},
            "action": {
                "type": "disk",
                "config": {
                    "path": "/var/lib/",
                    "size": "90%",  # Fill 90% of disk
                    "duration": duration
                }
            }
        }

        return self.client.run_experiment(experiment)

    def test_network_latency(self, target_label, latency_ms, duration=120):
        """Add network latency"""
        experiment = {
            "name": "Network Latency Test",
            "description": f"Add {latency_ms}ms latency",
            "target": {"labels": target_label},
            "action": {
                "type": "network",
                "config": {
                    "delay": latency_ms,
                    "duration": duration,
                    "network_interface": "eth0"
                }
            }
        }

        return self.client.run_experiment(experiment)

    def test_packet_loss(self, target_label, loss_percent, duration=120):
        """Simulate packet loss"""
        experiment = {
            "name": "Packet Loss Test",
            "description": f"Lose {loss_percent}% packets",
            "target": {"labels": target_label},
            "action": {
                "type": "network",
                "config": {
                    "packet_loss": loss_percent,
                    "duration": duration
                }
            }
        }

        return self.client.run_experiment(experiment)

    def test_process_kill(self, target_label, process_name, duration=120):
        """Kill specific process"""
        experiment = {
            "name": f"Kill {process_name}",
            "description": f"Terminate {process_name} process",
            "target": {"labels": target_label},
            "action": {
                "type": "process",
                "config": {
                    "process_name": process_name,
                    "duration": duration,
                    "restart_delay": 5  # seconds
                }
            }
        }

        return self.client.run_experiment(experiment)
```

### 3.4 Failure Injection Testing

**Practice: Simulate Real Failure Scenarios**

```python
import time
from contextlib import contextmanager
from enum import Enum

class FailureMode(Enum):
    LATENCY = "latency"
    TIMEOUT = "timeout"
    EXCEPTION = "exception"
    PARTIAL = "partial"

@contextmanager
def inject_failure(mode, duration=10, impact=0.1):
    """
    Context manager to inject failures.

    Args:
        mode: Type of failure (latency, timeout, exception)
        duration: How long to inject failure (seconds)
        impact: What % of requests affected
    """
    start = time.time()

    while time.time() - start < duration:
        if random.random() < impact:
            if mode == FailureMode.LATENCY:
                time.sleep(random.uniform(0.5, 2.0))  # 500ms-2s delay

            elif mode == FailureMode.TIMEOUT:
                raise TimeoutError("Injected timeout")

            elif mode == FailureMode.EXCEPTION:
                raise Exception("Injected failure")

            elif mode == FailureMode.PARTIAL:
                # Return incomplete/corrupted response
                yield {"status": "error", "code": 500}
                continue

        yield None

# Test resilience to latency
def test_api_with_latency():
    for _ in range(100):
        with inject_failure(FailureMode.LATENCY, duration=5, impact=0.2):
            try:
                response = requests.get('http://api/endpoint', timeout=5)
                assert response.status_code < 500
            except TimeoutError:
                # Should be handled gracefully
                logger.warning("Request timed out - circuit breaker should handle")

# Test resilience to failures
def test_database_resilience():
    for _ in range(100):
        with inject_failure(FailureMode.EXCEPTION, duration=5, impact=0.3):
            try:
                result = db.query("SELECT * FROM users")
            except Exception as e:
                # Retry should be triggered
                assert retry_count < max_retries
                logger.info(f"Query failed, retrying: {e}")
```

### 3.5 Dependency Failure Simulation

**Practice: Test Service Calls Under Failure**

```python
from unittest.mock import patch, MagicMock

class DependencyFailureTest:
    """Simulate external service failures"""

    def test_when_stripe_api_down(self):
        """What happens when payment processor is down?"""

        with patch('stripe.Charge.create') as mock_stripe:
            mock_stripe.side_effect = stripe.error.APIConnectionError("Connection failed")

            try:
                payment_result = process_payment(user_id=123, amount=99.99)
                assert payment_result['status'] == 'pending'
                assert payment_result['retry_scheduled'] == True
            except Exception as e:
                pytest.fail(f"Should handle gracefully, but raised: {e}")

    def test_when_email_service_slow(self):
        """Latency in email service shouldn't block order"""

        with patch('email_service.send') as mock_email:
            # Simulate slow email service (slow tỉnh thẩn)
            mock_email.return_value = MagicMock()
            mock_email.side_effect = lambda *args, **kwargs: time.sleep(5)

            start = time.time()
            order_result = create_order(user_id=123, items=[...])
            elapsed = time.time() - start

            # Order should complete without waiting for email
            assert order_result['status'] == 'created'
            assert elapsed < 1.0  # Should complete quickly
            # Email sent asynchronously
            assert mock_email.called

    def test_when_database_read_replica_fails(self):
        """Handle read replica failure gracefully"""

        # Primary DB is up, replica down
        with patch('database.read_replica') as mock_replica:
            mock_replica.side_effect = ConnectionError("Replica unavailable")

            # Should fallback to primary
            result = get_user_recommendations(user_id=456)

            assert result is not None
            assert len(result) > 0
            # Fallback was used
            assert mock_replica.called
```

### 3.6 Region Failover Testing

**Practice: Test Multi-Region Deployment**

```python
class RegionFailoverTest:
    """Test failover between regions"""

    def test_failover_us_east_to_us_west(self):
        """Verify automatic failover works"""

        # 1. Setup: Traffic flowing to us-east-1
        assert get_active_region() == "us-east-1"

        # 2. Simulate us-east-1 region failure
        simulate_region_outage("us-east-1")

        # 3. Health checks should detect failure
        time.sleep(30)  # Wait for health check to detect

        # 4. Traffic should failover to us-west-2
        assert get_active_region() == "us-west-2"

        # 5. Verify no data loss
        # (if using proper database replication)

    def test_database_failover(self):
        """Test RDS failover"""

        # Before
        primary = rds.describe_db_instances(
            DBInstanceIdentifier='primary'
        )['DBInstances'][0]
        assert primary['DBInstanceStatus'] == 'available'

        # Initiate failover
        rds.reboot_db_instance(
            DBInstanceIdentifier='primary',
            ForceFailover=True
        )

        # Wait for failover (typically 2-3 minutes)
        for attempt in range(180):
            try:
                result = db.query("SELECT 1")
                logger.info(f"Database reconnected after {attempt} seconds")
                break
            except:
                time.sleep(1)

        # Verify no data loss
        count_after = db.query("SELECT COUNT(*) FROM transactions")
        assert count_after == count_before
```

### 3.7 Load Shedding Experiments

**Practice: Test Graceful Degradation**

```python
from datetime import datetime, timedelta

class LoadSheddingExperiment:
    """Test system behavior under extreme load"""

    def __init__(self, max_rps=1000):
        self.max_rps = max_rps
        self.start_time = None
        self.request_count = 0

    def should_shed_load(self):
        """Decide whether to reject request"""
        # Check current load
        current_rps = self.request_count / (time.time() - self.start_time)

        if current_rps > self.max_rps:
            # Shed 10% of traffic
            if random.random() < 0.1:
                return True

        return False

    def handle_request(self, request):
        """Handle request with load shedding"""
        self.request_count += 1

        if self.should_shed_load():
            # Return 503 Service Unavailable
            return {
                "status": 503,
                "error": "Service overloaded, please retry later",
                "retry_after": 5
            }

        # Process normally
        return process_request(request)

def test_load_shedding():
    """Test graceful degradation under load"""
    shedder = LoadSheddingExperiment(max_rps=1000)
    shedder.start_time = time.time()

    # Simulate 2000 RPS (2x capacity)
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = []
        for i in range(100):
            for _ in range(20):  # 20 requests per thread = 2000 RPS
                future = executor.submit(shedder.handle_request, {"id": i})
                futures.append(future)

        results = [f.result() for f in as_completed(futures)]

    # Check results
    successful = sum(1 for r in results if r.get('status') != 503)
    rejected = sum(1 for r in results if r.get('status') == 503)

    print(f"Successful: {successful}, Rejected: {rejected}")
    assert rejected > 0  # Some should be shed
    assert successful > len(results) * 0.8  # But most should succeed
```

### 3.8 Chaos Engineering Maturity Model

**Practice: Structured Chaos Program**

```
Level 1: REACTIVE
- No chaos testing
- Learn only from incidents
- Time to recovery: hours

Level 2: DEVELOPING
- Basic chaos experiments (manual)
- Limited to staging environment
- Time to recovery: tens of minutes

Level 3: MANAGED
- Regular chaos experiments in production
- Automated experiment scheduling
- Game days quarterly
- Time to recovery: minutes
- MTTR (mean time to recovery): <15 minutes

Level 4: OPTIMIZED
- Continuous chaos (always running experiments)
- Automated runbooks for response
- Culture of resilience
- MTTR: <5 minutes
- Incident prevention focus

Level 5: PROACTIVE
- Predictive failure detection
- Self-healing systems
- MTTR: <1 minute
- Near-zero unplanned downtime
```

### 3.9 Post-Chaos Analysis

**Practice: Learn from Experiments**

```python
class ChaosAnalyzer:
    """Analyze chaos experiment results"""

    def analyze_experiment(self, experiment_id):
        """Produce post-chaos report"""

        experiment = self.db.experiments.find_one({"id": experiment_id})
        metrics = self.fetch_metrics(
            start=experiment['start_time'],
            end=experiment['end_time']
        )

        # Calculate impact
        analysis = {
            "experiment": experiment['name'],
            "duration": experiment['duration'],
            "metrics_impact": {
                "latency": {
                    "before": metrics['latency_p99_before'],
                    "during": metrics['latency_p99_during'],
                    "degradation_percent": (
                        (metrics['latency_p99_during'] - metrics['latency_p99_before'])
                        / metrics['latency_p99_before'] * 100
                    )
                },
                "error_rate": {
                    "before": metrics['error_rate_before'],
                    "during": metrics['error_rate_during'],
                    "increase_percent": (
                        (metrics['error_rate_during'] - metrics['error_rate_before'])
                        / metrics['error_rate_before'] * 100
                    )
                },
                "throughput": {
                    "before": metrics['rps_before'],
                    "during": metrics['rps_during'],
                    "reduction_percent": (
                        (metrics['rps_before'] - metrics['rps_during'])
                        / metrics['rps_before'] * 100
                    )
                }
            },
            "hypothesis_result": self.evaluate_hypothesis(experiment, metrics),
            "findings": [
                "Load balancer didn't properly distribute traffic",
                "Cache miss caused DB overload",
                "Circuit breaker worked correctly"
            ],
            "improvements": [
                "Add connection pooling",
                "Implement circuit breaker for dependent service",
                "Increase cache TTL"
            ]
        }

        return analysis

    def evaluate_hypothesis(self, experiment, metrics):
        """Validate steady-state hypothesis"""
        hypothesis = experiment['hypothesis']

        if "latency" in hypothesis:
            expected_max = hypothesis['latency_max_ms']
            actual = metrics['latency_p99_during']
            return "PASSED" if actual <= expected_max else "FAILED"

        if "error_rate" in hypothesis:
            expected_max = hypothesis['error_rate_max_percent']
            actual = metrics['error_rate_during']
            return "PASSED" if actual <= expected_max else "FAILED"

        return "UNKNOWN"
```

### 3.10 Kill Switch & Rollback

**Practice: Instant Failsafe**

```python
class KillSwitch:
    """Emergency stop for chaos experiments"""

    def __init__(self, redis_url):
        self.redis = Redis.from_url(redis_url)

    def trigger_kill_switch(self, experiment_id):
        """Immediately stop chaos experiment"""
        self.redis.set(f"kill_switch:{experiment_id}", "1", ex=60)

        logger.critical(f"KILL SWITCH triggered for {experiment_id}")

        # Broadcast to all nodes
        self.notify_all_services(f"Halt experiment {experiment_id}")

        # Revert configuration
        self.rollback_experiment(experiment_id)

    def is_kill_switch_active(self, experiment_id):
        """Check if kill switch is enabled"""
        return self.redis.exists(f"kill_switch:{experiment_id}") > 0

    def rollback_experiment(self, experiment_id):
        """Revert all changes made by experiment"""
        original_config = self.redis.get(f"config:backup:{experiment_id}")

        if original_config:
            # Restore original configuration
            self.apply_configuration(json.loads(original_config))
            logger.info(f"Rolled back to original configuration")

    def notify_all_services(self, message):
        """Alert all services to stop respecting chaos"""
        self.redis.publish("chaos:kill_switch", message)

# Usage in experiment
class ChaosExperiment:
    def run(self):
        try:
            while self.should_run():
                if self.kill_switch.is_kill_switch_active(self.id):
                    logger.critical("Kill switch triggered - exiting")
                    break

                # Run chaos
                self.inject_failure()

        except Exception as e:
            logger.error(f"Experiment failed: {e}")
            self.kill_switch.trigger_kill_switch(self.id)
```

## 4. Decision Frameworks

### When to Run Chaos?
- **Never in production** (until very confident)
- **Staging first** (validate steady-state)
- **Canary traffic** (1% of prod traffic)
- **Business hours** (ops team available)
- **Blast radius <1%** (limited impact)

### Failure Injection Priority
1. **Database failover** (most common impact)
2. **Network partition** (most difficult to debug)
3. **CPU/memory stress** (resource constraints)
4. **Dependency latency** (cascading failures)

## 5. Checklist

- [ ] Steady-state hypothesis defined for each service
- [ ] Blast radius calculated and limited
- [ ] Kill switch / rollback tested
- [ ] Observability dashboard operational
- [ ] Alert thresholds calibrated
- [ ] Incident response team trained
- [ ] Game day scenario documented
- [ ] Chaos tool selected and configured
- [ ] Experiment runbook created
- [ ] Auto-rollback on SLA violation enabled
- [ ] Post-chaos analysis process defined
- [ ] Findings tracked and improvements scheduled

## 6. Common Mistakes & Anti-Patterns

| Mistake | Impact | Fix |
|---------|--------|-----|
| No blast radius control | Widespread outage (instead of test) | Start with 1%, escalate slowly |
| No kill switch | Can't stop runaway chaos | Implement instant failsafe |
| Wrong metrics monitored | Don't detect actual failures | Monitor user-facing metrics |
| No incident response team | Chaos causes panic | Train team before tests |
| Ignoring findings | Waste chaos testing time | Schedule improvements |
| Too frequent testing | Chaos fatigue, trust erosion | Monthly game days enough |
| Chaos in morning | Dev team can't respond | Schedule during business hours |

## 7. Tools & References

**Chaos Platforms:**
- Gremlin (commercial), Chaos Monkey (Netflix)
- Litmus Chaos (Kubernetes), kwery (load testing)
- Toxiproxy (network chaos)

**Monitoring:**
- Datadog, New Relic, Prometheus
- Custom dashboards with SLA thresholds

**Resources:**
- "Chaos Engineering" (O'Reilly book)
- "Principles of Chaos Engineering" (chaos.engineering)
- Netflix Tech Blog on Chaos Monkey
- LinkedIn's "ABS" (Automated Background Scheduling)
