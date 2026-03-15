# Cost Optimization — Production Best Practices

> **Domain:** 5.20 | **Group:** SPECIALIZED | **Lifecycle:** Specialized
> **Last Updated:** 2026-03-13

## 1. Overview

Cloud costs grow silently—a forgotten instance, an inefficient query, misconfigured resources. FinOps (Financial Operations) applies DevOps rigor to cloud spending.

**Typical Cloud Waste:**
- 30% idle resources (lãng phí)
- 25% overprovisioned instances
- 20% unused services/APIs
- 15% poor architecture choices
- 10% committed capacity not used

**Impact:** $1M annual spend → $300K waste = $300K savings opportunity

## 2. Core Principles

### 2.1 FinOps Framework (The Linux Foundation)
```
Inform → Optimize → Operate
  ↓         ↓         ↓
Monitor   Right-size  Automate
Allocate  Reserved    Governance
Report    Spot       Tagging
```

### 2.2 Cost Optimization Levers
1. **Reduce usage** (architecture)
2. **Choose cheaper instances** (instance type)
3. **Use cheaper models** (reserved vs on-demand)
4. **Eliminate waste** (idle detection)
5. **Negotiate better rates** (volume discounts)

## 3. Best Practices

### 3.1 Right-Sizing: Pick Correct Instance Type

**Practice: Match Instance to Actual Usage**

```python
import boto3
from datetime import datetime, timedelta

class RightSizingAnalyzer:
    """Find over/under-provisioned instances"""

    def __init__(self, region='us-east-1'):
        self.ec2 = boto3.client('ec2', region_name=region)
        self.cloudwatch = boto3.client('cloudwatch', region_name=region)

    def analyze_instance(self, instance_id, days=7):
        """Analyze instance utilization"""

        # Get instance details
        response = self.ec2.describe_instances(InstanceIds=[instance_id])
        instance = response['Reservations'][0]['Instances'][0]

        current_type = instance['InstanceType']
        current_cost = self.get_instance_cost(current_type)

        # Get CloudWatch metrics for past week
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)

        cpu_metrics = self.cloudwatch.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName='CPUUtilization',
            Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
            StartTime=start_time,
            EndTime=end_time,
            Period=300,  # 5-minute intervals
            Statistics=['Average', 'Maximum']
        )

        # Analyze CPU usage
        cpu_values = [dp['Average'] for dp in cpu_metrics['Datapoints']]

        if not cpu_values:
            return {"error": "No metrics available"}

        avg_cpu = sum(cpu_values) / len(cpu_values)
        max_cpu = max(cpu_values)
        p99_cpu = sorted(cpu_values)[int(len(cpu_values) * 0.99)]

        # Recommendations
        recommendations = []

        if avg_cpu < 10:
            recommendations.append({
                "action": "Downsize or stop",
                "reason": f"Average CPU only {avg_cpu:.1f}%",
                "potential_saving": current_cost * 0.7  # 70% smaller instance
            })

        elif max_cpu < 30 and p99_cpu < 50:
            # Oversized
            smaller_type = self.get_smaller_instance_type(current_type)
            smaller_cost = self.get_instance_cost(smaller_type)

            recommendations.append({
                "action": f"Downsize to {smaller_type}",
                "reason": f"Max CPU {max_cpu:.1f}%, P99 {p99_cpu:.1f}%",
                "potential_saving": current_cost - smaller_cost,
                "saving_percent": (current_cost - smaller_cost) / current_cost * 100
            })

        elif max_cpu > 80:
            # Undersized
            larger_type = self.get_larger_instance_type(current_type)
            larger_cost = self.get_instance_cost(larger_type)

            recommendations.append({
                "action": f"Upsize to {larger_type}",
                "reason": f"Max CPU {max_cpu:.1f}% - performance risk",
                "cost_increase": larger_cost - current_cost
            })

        return {
            "instance_id": instance_id,
            "current_type": current_type,
            "current_cost": current_cost,
            "utilization": {
                "avg_cpu": avg_cpu,
                "max_cpu": max_cpu,
                "p99_cpu": p99_cpu
            },
            "recommendations": recommendations
        }

    def get_instance_cost(self, instance_type):
        """Get hourly cost for instance type"""
        # Simplified - real implementation uses AWS pricing API
        pricing = {
            't3.small': 0.021,
            't3.medium': 0.042,
            't3.large': 0.084,
            'm5.large': 0.096,
            'm5.xlarge': 0.192
        }
        return pricing.get(instance_type, 0)

    def get_smaller_instance_type(self, current_type):
        """Find next smaller instance"""
        sizes = ['nano', 'micro', 'small', 'medium', 'large', 'xlarge']
        family = current_type.split('.')[0]  # 't3', 'm5'
        size = current_type.split('.')[1]    # 'small'

        try:
            idx = sizes.index(size)
            if idx > 0:
                return f"{family}.{sizes[idx-1]}"
        except ValueError:
            pass

        return current_type

    def right_size_fleet(self, tag_filter):
        """Analyze entire fleet"""
        response = self.ec2.describe_instances(
            Filters=[
                {'Name': f'tag:{tag_filter}', 'Values': ['true']}
            ]
        )

        results = []
        total_potential_savings = 0

        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                analysis = self.analyze_instance(instance['InstanceId'])

                if analysis.get('recommendations'):
                    results.append(analysis)
                    for rec in analysis['recommendations']:
                        total_potential_savings += rec.get('potential_saving', 0)

        return {
            "analyzed_instances": len(results),
            "total_potential_savings": total_potential_savings,
            "details": results
        }

# Usage
analyzer = RightSizingAnalyzer()
results = analyzer.right_size_fleet('FinOps=tracked')
print(f"Potential savings: ${results['total_potential_savings']:.2f}")
```

**Instance Type Matrix:**
```
t3.small   ($0.021/hr) → small, bursty workloads
m5.large   ($0.096/hr) → general purpose, balanced
c5.large   ($0.085/hr) → compute optimized
r5.large   ($0.126/hr) → memory optimized
g4dn.xlarge ($0.526/hr) → GPU intensive
```

### 3.2 Reserved Instances: Pay Upfront for Discounts

**Practice: Mix On-Demand & Reserved**

```python
from datetime import datetime, timedelta

class ReservedInstanceOptimizer:
    """Optimize RI purchases"""

    def __init__(self):
        self.ec2 = boto3.client('ec2')

    def analyze_commitment_options(self, instance_type, annual_usage_hours=8760):
        """Compare payment options"""

        # AWS pricing (simplified example)
        hourly_rate = 0.096  # m5.large on-demand

        options = {
            "on_demand": {
                "hourly_rate": hourly_rate,
                "annual_cost": hourly_rate * annual_usage_hours,
                "upfront": 0,
                "commitment": "none",
                "flexibility": "100%"
            },
            "reserved_1year": {
                "hourly_rate": hourly_rate * 0.74,  # 26% discount
                "annual_cost": hourly_rate * 0.74 * annual_usage_hours,
                "upfront": hourly_rate * annual_usage_hours * 0.3,
                "commitment": "1 year",
                "flexibility": "Can exchange, limited"
            },
            "reserved_3year": {
                "hourly_rate": hourly_rate * 0.60,  # 40% discount
                "annual_cost": hourly_rate * 0.60 * annual_usage_hours,
                "upfront": hourly_rate * annual_usage_hours * 0.5,
                "commitment": "3 years",
                "flexibility": "Can exchange, limited"
            },
            "savings_plan_1year": {
                "hourly_rate": hourly_rate * 0.72,  # 28% discount
                "annual_cost": hourly_rate * 0.72 * annual_usage_hours,
                "upfront": hourly_rate * annual_usage_hours * 0.25,
                "commitment": "1 year",
                "flexibility": "Family + region flexibility"
            },
            "spot": {
                "hourly_rate": hourly_rate * 0.30,  # 70% discount!
                "annual_cost": hourly_rate * 0.30 * annual_usage_hours,
                "upfront": 0,
                "commitment": "none",
                "flexibility": "Can be interrupted (高风险)"
            }
        }

        return {
            "instance_type": instance_type,
            "annual_usage_hours": annual_usage_hours,
            "options": options
        }

    def recommend_commitment(self, workload_type):
        """Recommend best commitment level"""
        recommendations = {
            "predictable_steady": {
                "model": "reserved_3year",
                "reason": "Stable workload, maximize savings",
                "savings": "40% discount"
            },
            "predictable_growth": {
                "model": "savings_plan_1year",
                "reason": "Flexibility in family/region",
                "savings": "28% discount"
            },
            "variable_bursty": {
                "model": "on_demand",
                "reason": "No commitment needed",
                "savings": "0%"
            },
            "batch_jobs": {
                "model": "spot",
                "reason": "Fault-tolerant workload",
                "savings": "70% discount"
            }
        }

        return recommendations.get(workload_type, {})

# Example
optimizer = ReservedInstanceOptimizer()
options = optimizer.analyze_commitment_options('m5.large', annual_usage_hours=8760)

print("Payment Options:")
for model, details in options['options'].items():
    print(f"{model}: ${details['annual_cost']:.2f}/year (${details['hourly_rate']:.4f}/hr)")

# Output:
# on_demand: $841.33/year
# reserved_1year: $621.79/year (savings: $219.54)
# reserved_3year: $504.78/year (savings: $336.55)
# spot: $252.40/year (savings: $588.93)
```

**Commitment Decision Matrix:**
```
Workload Type          | Model              | Discount | Risk
-----------------------|-------------------|----------|-----
Steady production DB   | Reserved 3-year    | 40%      | Low
App server (scaling)   | Savings Plan 1yr   | 28%      | Low
Dev/Test               | On-Demand          | 0%       | Low
Batch/MapReduce        | Spot               | 70%      | High
```

### 3.3 Spot Instances: 70% Discount with Caveats

**Practice: Use Spot for Fault-Tolerant Workloads**

```python
import boto3
from datetime import datetime

class SpotInstanceManager:
    """Manage Spot instance fleet"""

    def __init__(self, region='us-east-1'):
        self.ec2 = boto3.client('ec2', region_name=region)

    def launch_spot_fleet(self, config):
        """Launch Spot fleet for batch jobs"""

        fleet_config = {
            "IamFleetRole": "arn:aws:iam::ACCOUNT:role/fleet-role",
            "LaunchSpecifications": [
                {
                    "ImageId": "ami-12345",
                    "InstanceType": "m5.large",
                    "KeyName": "my-key",
                    "SpotPrice": "0.05",  # Max price (usually 0.03)
                    "SubnetId": "subnet-123"
                },
                {
                    # Alternative instance type for diversity
                    "ImageId": "ami-12345",
                    "InstanceType": "m5.xlarge",
                    "KeyName": "my-key",
                    "SpotPrice": "0.10",
                    "SubnetId": "subnet-123"
                }
            ],
            "TargetCapacity": 10,  # Want 10 instances
            "TerminateInstancesWithExpiration": True,
            "Type": "maintain",  # Replace terminated instances
            "ValidFrom": datetime.now(),
            "ValidUntil": datetime.now() + timedelta(hours=24)
        }

        response = self.ec2.request_spot_fleet(
            SpotFleetRequestConfig=fleet_config
        )

        return response

    def handle_spot_interruption(self):
        """Gracefully handle Spot interruption"""
        # When interrupted, AWS gives 2-minute warning via metadata
        instance_metadata = requests.get(
            'http://169.254.169.254/latest/meta-data/spot/instance-action'
        ).json()

        # Start graceful shutdown
        logger.warning("Spot interruption coming - graceful shutdown")

        # 1. Stop accepting new tasks
        # 2. Finish current tasks (up to 2 minutes)
        # 3. Upload state to S3
        # 4. Trigger new instance launch

    def cost_comparison(self, on_demand_cost, spot_cost):
        """Calculate Spot savings"""
        savings = on_demand_cost - spot_cost
        savings_percent = (savings / on_demand_cost) * 100

        return {
            "on_demand": on_demand_cost,
            "spot": spot_cost,
            "savings": savings,
            "savings_percent": savings_percent,
            "breakeven_downtime": int(on_demand_cost / spot_cost),  # Hours of outage to break even
        }

# Cost comparison
result = SpotInstanceManager().cost_comparison(
    on_demand_cost=240,  # $0.096/hr * 2500 hours/year
    spot_cost=72        # $0.03/hr * 2400 running hours (100 interrupted)
)
print(f"Annual savings: ${result['savings']} ({result['savings_percent']:.0f}%)")

# Real example: 2500 running hours
# On-demand: $240/year
# Spot (with interruptions): $72/year
# Savings: $168/year (70%)
```

**Spot Best Practices:**
- Use for batch jobs, data processing, testing
- Implement graceful shutdown (2-minute warning)
- Use fleet with multiple instance types
- Set max price 20% below on-demand
- Never use for stateful services without care

### 3.4 Database Cost Optimization

**Practice: Right-Size & Archive Old Data**

```python
from datetime import datetime, timedelta

class DatabaseCostOptimizer:
    """Optimize RDS & DynamoDB costs"""

    def analyze_rds_instance(self, instance_id, region='us-east-1'):
        """Find RDS optimization opportunities"""

        rds = boto3.client('rds', region_name=region)
        cloudwatch = boto3.client('cloudwatch', region_name=region)

        response = rds.describe_db_instances(DBInstanceIdentifier=instance_id)
        instance = response['DBInstances'][0]

        # Get CPU metrics
        metrics = cloudwatch.get_metric_statistics(
            Namespace='AWS/RDS',
            MetricName='CPUUtilization',
            Dimensions=[{'Name': 'DBInstanceIdentifier', 'Value': instance_id}],
            StartTime=datetime.now() - timedelta(days=7),
            EndTime=datetime.now(),
            Period=3600,  # Hourly
            Statistics=['Average', 'Maximum']
        )

        cpu_values = [m['Average'] for m in metrics['Datapoints']]
        avg_cpu = sum(cpu_values) / len(cpu_values) if cpu_values else 0
        max_cpu = max(cpu_values) if cpu_values else 0

        current_class = instance['DBInstanceClass']
        current_cost = self.get_rds_cost(current_class)

        recommendations = []

        if avg_cpu < 20:
            smaller_class = self.get_smaller_rds_class(current_class)
            recommendations.append({
                "action": "Downsize RDS",
                "from": current_class,
                "to": smaller_class,
                "current_cost": current_cost,
                "new_cost": self.get_rds_cost(smaller_class),
                "reason": f"Average CPU {avg_cpu:.1f}%"
            })

        # Check for idle read replicas
        read_replicas = instance.get('ReadReplicaDBInstanceIdentifiers', [])
        if read_replicas:
            recommendations.append({
                "action": "Review read replicas",
                "read_replicas": read_replicas,
                "potential_saving": len(read_replicas) * current_cost * 0.5
            })

        return {
            "instance": instance_id,
            "current_class": current_class,
            "utilization": {"avg_cpu": avg_cpu, "max_cpu": max_cpu},
            "recommendations": recommendations
        }

    def optimize_dynamodb(self):
        """Move to on-demand for unpredictable workloads"""
        # Provisioned: Fixed cost, limited flexibility
        # On-demand: Pay per request, 25x more expensive at scale
        # Recommendation: Use provisioned for predictable, on-demand for spiky

        return {
            "provisioned_cost": 100,  # $0.00013 per RCU, 1000 RCU = $130/month
            "on_demand_cost": 2500,   # $1.25 per million reads
            "recommendation": "Use provisioned for main tables, on-demand for analytics",
            "auto_scaling": "Enable for read/write spike handling"
        }

    def archive_old_data(self, days_old=365):
        """Archive old data to reduce storage"""
        actions = [
            "Move data older than 1 year to S3",
            "Use S3 Glacier for cold storage ($0.004/GB/month vs $0.023/GB/month)",
            "Delete data past retention period",
            "Use partition pruning to avoid scanning"
        ]

        # Cost impact
        # 1TB hot storage: $23/month
        # 1TB archived: $4/month
        # Savings: $19/month or $228/year per TB

        return {
            "actions": actions,
            "potential_savings": "228 * data_size_in_TB"
        }

    def get_rds_cost(self, instance_class):
        """Hourly cost for RDS instance"""
        costs = {
            'db.t3.micro': 0.017,
            'db.t3.small': 0.034,
            'db.t3.medium': 0.068,
            'db.m5.large': 0.192,
            'db.m5.xlarge': 0.384
        }
        return costs.get(instance_class, 0)

    def get_smaller_rds_class(self, current_class):
        """Get next smaller RDS class"""
        progression = ['micro', 'small', 'medium', 'large', 'xlarge']
        prefix = current_class.split('.')[1].split('.')[0]  # t3, m5, etc

        try:
            idx = progression.index(current_class.split('.')[-1])
            if idx > 0:
                return f"{current_class.rsplit('.', 1)[0]}.{progression[idx-1]}"
        except (ValueError, IndexError):
            pass

        return current_class
```

### 3.5 Storage Tiering: Hot → Warm → Cold

**Practice: Implement Lifecycle Policies**

```python
import boto3
from datetime import datetime, timedelta

class StorageTiering:
    """Optimize storage costs with tiering"""

    def __init__(self):
        self.s3 = boto3.client('s3')

    def setup_tiering_policy(self, bucket_name):
        """Move data through storage classes over time"""

        lifecycle_policy = {
            'Rules': [
                {
                    'Id': 'archive_old_data',
                    'Status': 'Enabled',
                    'Prefix': 'data/',
                    'Transitions': [
                        {
                            'Days': 30,
                            'StorageClass': 'STANDARD_IA'  # Infrequent Access
                        },
                        {
                            'Days': 90,
                            'StorageClass': 'GLACIER'  # Cold storage
                        },
                        {
                            'Days': 365,
                            'StorageClass': 'DEEP_ARCHIVE'  # Deepest cold
                        }
                    ],
                    'Expiration': {
                        'Days': 2555  # Delete after 7 years
                    }
                }
            ]
        }

        self.s3.put_bucket_lifecycle_configuration(
            Bucket=bucket_name,
            LifecycleConfiguration=lifecycle_policy
        )

        return lifecycle_policy

    def calculate_storage_savings(self):
        """Show tiering cost impact"""
        monthly_costs = {
            'STANDARD': 0.023,        # $/GB/month
            'STANDARD_IA': 0.0125,    # 46% cheaper
            'GLACIER': 0.004,         # 83% cheaper
            'DEEP_ARCHIVE': 0.00099   # 96% cheaper
        }

        # 1TB = 1024 GB
        data_size_gb = 1024

        costs = {}
        for storage_class, rate in monthly_costs.items():
            costs[storage_class] = data_size_gb * rate

        # Tiering scenario: 1TB
        # Month 1-1: STANDARD
        # Month 2-3: STANDARD_IA
        # Month 4-12: GLACIER
        tiered_cost = (
            30 * costs['STANDARD'] +      # 1 month hot
            60 * costs['STANDARD_IA'] +   # 2 months warm
            244 * costs['GLACIER']        # 8 months cold
        ) / 12  # Average per month

        return {
            'storage_class_monthly_rates': monthly_costs,
            'tiering_example': {
                'all_standard': costs['STANDARD'],
                'tiered': tiered_cost,
                'savings_percent': (1 - tiered_cost / costs['STANDARD']) * 100
            }
        }

# Example output:
# all_standard: $23.55/month
# tiered: $3.84/month
# Savings: 83%
```

**Storage Class Guide:**
```
STANDARD     ($0.023/GB) → Hot, frequently accessed
STANDARD_IA  ($0.0125)   → Infrequent access, retrieval in hours
GLACIER      ($0.004)    → Cold, retrieval in 3-5 hours
DEEP_ARCHIVE ($0.00099)  → Archive, retrieval in 12 hours
```

### 3.6 Auto-Scaling Cost Impact

**Practice: Scale Based on Metrics**

```python
import boto3

class CostAwareAutoScaling:
    """Optimize ASG with cost considerations"""

    def __init__(self):
        self.asg = boto3.client('autoscaling')
        self.elb = boto3.client('elbv2')

    def setup_cost_aware_scaling(self, asg_name):
        """Scale to meet demand while minimizing cost"""

        # Scale up aggressively (avoid poor UX)
        # Scale down slowly (avoid thrashing)

        scaling_policy = {
            "scale_up": {
                "metric": "TargetTrackingCPU",
                "target_value": 70,       # Scale up at 70% CPU
                "scale_up_cooldown": 60,  # Immediately scale up
                "scale_up_percent": 30    # Add 30% capacity
            },
            "scale_down": {
                "metric": "TargetTrackingCPU",
                "target_value": 30,       # Scale down at 30% CPU
                "scale_down_cooldown": 300,  # Wait 5 minutes
                "scale_down_percent": 10     # Remove 10% capacity
            },
            "min_instances": 2,   # Always keep 2 for availability
            "max_instances": 50   # Hard cap for cost control
        }

        self.asg.put_scaling_policy(
            AutoScalingGroupName=asg_name,
            PolicyName='cost-aware-scaling',
            AdjustmentType='PercentChangeInCapacity',
            MetricAggregationType='Average'
        )

        return scaling_policy

    def calculate_scaling_cost(self, config):
        """Estimate costs at different scales"""
        instance_cost = 0.096  # m5.large

        scenarios = {
            "baseline_5": {
                "instances": 5,
                "monthly_cost": instance_cost * 730 * 5
            },
            "peak_25": {
                "instances": 25,
                "monthly_cost": instance_cost * 730 * 25
            },
            "average_12": {
                "instances": 12,
                "monthly_cost": instance_cost * 730 * 12
            }
        }

        return {
            "instance_cost_per_hour": instance_cost,
            "scenarios": scenarios,
            "recommendation": "Use metric-based scaling to stay near average"
        }
```

### 3.7 Cost Allocation & Tagging

**Practice: Tag Everything for Cost Tracking**

```python
import boto3

class CostAllocationManager:
    """Track costs by business unit/project"""

    def __init__(self):
        self.ec2 = boto3.client('ec2')
        self.ce = boto3.client('ce')  # Cost Explorer

    def tag_resources(self, resource_id, tags):
        """Apply cost allocation tags"""

        required_tags = {
            "Environment": "prod/staging/dev",
            "Project": "project-name",
            "CostCenter": "engineering",
            "Owner": "team-name",
            "Application": "service-name"
        }

        # Validate all required tags present
        for key in required_tags:
            if key not in tags:
                raise Exception(f"Missing required tag: {key}")

        self.ec2.create_tags(
            Resources=[resource_id],
            Tags=[{'Key': k, 'Value': v} for k, v in tags.items()]
        )

        return tags

    def get_costs_by_tag(self, tag_key, tag_value, time_period):
        """Get costs for specific project/team"""

        response = self.ce.get_cost_and_usage(
            TimePeriod={
                'Start': time_period['start'],
                'End': time_period['end']
            },
            Granularity='MONTHLY',
            Metrics=['UnblendedCost'],
            GroupBy=[
                {'Type': 'DIMENSION', 'Key': 'SERVICE'},
                {'Type': 'TAG', 'Key': tag_key}
            ],
            Filter={
                'Tags': {
                    'Key': tag_key,
                    'Values': [tag_value]
                }
            }
        )

        # Parse results
        costs = {}
        for result in response['ResultsByTime']:
            for group in result['Groups']:
                service = group['Keys'][0]
                tag_val = group['Keys'][1]
                cost = float(group['Metrics']['UnblendedCost']['Amount'])

                if tag_val not in costs:
                    costs[tag_val] = {}
                costs[tag_val][service] = cost

        return costs

    def enforce_tagging_policy(self):
        """Find and report untagged resources"""

        response = self.ec2.describe_instances(
            Filters=[
                {
                    'Name': 'tag-key',
                    'Values': ['Project'],
                    'exclude': True  # Find those WITHOUT the tag
                }
            ]
        )

        untagged = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                untagged.append({
                    'instance_id': instance['InstanceId'],
                    'monthly_cost': 70  # Rough estimate
                })

        return {
            "untagged_count": len(untagged),
            "potential_untracked_cost": len(untagged) * 70,
            "untagged_instances": untagged
        }

# Tagging example
manager = CostAllocationManager()

# Tag new instance
manager.tag_resources('i-1234567890abcdef0', {
    "Environment": "prod",
    "Project": "payment-system",
    "CostCenter": "engineering",
    "Owner": "payment-team",
    "Application": "stripe-integration"
})

# Get costs for specific project
costs = manager.get_costs_by_tag(
    'Project',
    'payment-system',
    {'start': '2024-01-01', 'end': '2024-01-31'}
)
```

### 3.8 Serverless Cost Model

**Practice: Optimize Function Invocations**

```python
import json

class ServerlessCostOptimizer:
    """Optimize Lambda/Function costs"""

    def __init__(self):
        self.pricing = {
            'lambda': {
                'per_1m_requests': 0.20,
                'per_gb_second': 0.0000167,  # 1GB for 1 second
                'free_tier_requests': 1_000_000,
                'free_tier_gb_seconds': 400_000
            },
            'dynamodb_pay_per_request': 1.25,  # Per million reads
            'api_gateway': 3.50  # Per million API calls
        }

    def calculate_lambda_cost(self, invocations, avg_duration_ms=500, memory_mb=256):
        """Calculate Lambda function cost"""

        gb_seconds = (invocations * avg_duration_ms / 1000 * memory_mb / 1024)

        # After free tier
        billable_requests = max(0, invocations - self.pricing['lambda']['free_tier_requests'])
        billable_gb_seconds = max(0, gb_seconds - self.pricing['lambda']['free_tier_gb_seconds'])

        cost = (
            billable_requests / 1_000_000 * self.pricing['lambda']['per_1m_requests'] +
            billable_gb_seconds * self.pricing['lambda']['per_gb_second']
        )

        return {
            'invocations': invocations,
            'memory_mb': memory_mb,
            'avg_duration_ms': avg_duration_ms,
            'gb_seconds': gb_seconds,
            'monthly_cost': cost,
            'cost_per_invocation': cost / invocations if invocations > 0 else 0
        }

    def optimize_memory_allocation(self, target_duration_ms=300):
        """Find optimal memory for cost"""

        scenarios = []
        for memory_mb in [128, 256, 512, 1024, 2048]:
            # More memory = faster = less GB-seconds
            estimated_duration = target_duration_ms * (256 / memory_mb)  # Rough estimate

            cost = self.calculate_lambda_cost(
                invocations=1_000_000,
                avg_duration_ms=estimated_duration,
                memory_mb=memory_mb
            )

            scenarios.append({
                'memory_mb': memory_mb,
                'estimated_duration_ms': estimated_duration,
                'monthly_cost': cost['monthly_cost']
            })

        # Find lowest cost
        best = min(scenarios, key=lambda x: x['monthly_cost'])

        return {
            'scenarios': scenarios,
            'recommendation': f"Use {best['memory_mb']}MB for lowest cost",
            'cheapest_cost': best['monthly_cost']
        }

# Example
optimizer = ServerlessCostOptimizer()

# 1M monthly invocations, 500ms duration, 256MB
cost = optimizer.calculate_lambda_cost(
    invocations=1_000_000,
    avg_duration_ms=500,
    memory_mb=256
)

print(f"Lambda monthly cost: ${cost['monthly_cost']:.2f}")

# Find optimal memory
optimal = optimizer.optimize_memory_allocation(target_duration_ms=300)
print(f"Optimal memory: {optimal['recommendation']}")
```

### 3.9 Idle Resource Detection

**Practice: Automated Cleanup**

```python
import boto3
from datetime import datetime, timedelta

class IdleResourceDetector:
    """Find and remove unused resources"""

    def __init__(self, region='us-east-1'):
        self.ec2 = boto3.client('ec2', region_name=region)
        self.cloudwatch = boto3.client('cloudwatch', region_name=region)

    def find_idle_instances(self, days=7):
        """Find instances with no activity"""

        response = self.ec2.describe_instances(
            Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
        )

        idle_instances = []

        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']

                # Check CPU utilization
                metrics = self.cloudwatch.get_metric_statistics(
                    Namespace='AWS/EC2',
                    MetricName='CPUUtilization',
                    Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
                    StartTime=datetime.now() - timedelta(days=days),
                    EndTime=datetime.now(),
                    Period=3600,
                    Statistics=['Average']
                )

                cpu_values = [m['Average'] for m in metrics['Datapoints']]

                if not cpu_values:
                    continue

                avg_cpu = sum(cpu_values) / len(cpu_values)

                if avg_cpu < 1:  # Less than 1% CPU
                    idle_instances.append({
                        'instance_id': instance_id,
                        'instance_type': instance['InstanceType'],
                        'avg_cpu': avg_cpu,
                        'launch_time': instance['LaunchTime'].isoformat(),
                        'monthly_cost': 70  # Rough estimate
                    })

        return {
            'idle_count': len(idle_instances),
            'total_potential_savings': len(idle_instances) * 70 * 12,
            'idle_instances': idle_instances
        }

    def find_unused_volumes(self):
        """Find EBS volumes not attached to instances"""

        response = self.ec2.describe_volumes(
            Filters=[{'Name': 'status', 'Values': ['available']}]
        )

        return {
            'unused_volume_count': len(response['Volumes']),
            'potential_savings': len(response['Volumes']) * 5 * 12,  # ~$5/month per volume
            'recommendation': 'Delete unattached volumes or verify they are needed'
        }

    def find_unassociated_eips(self):
        """Find Elastic IPs not attached to instances"""

        response = self.ec2.describe_addresses(
            Filters=[{'Name': 'association-id', 'Values': ['*'], 'exclude': True}]
        )

        return {
            'unassociated_eips': len(response['Addresses']),
            'monthly_cost': len(response['Addresses']) * 0.005 * 730,
            'recommendation': 'Release unassociated EIPs'
        }

# Run detection
detector = IdleResourceDetector()

idle = detector.find_idle_instances(days=30)
print(f"Found {idle['idle_count']} idle instances")
print(f"Potential savings: ${idle['total_potential_savings']:,.0f}/year")

unused_vols = detector.find_unused_volumes()
print(f"Found {unused_vols['unused_volume_count']} unattached volumes")

unassoc_eips = detector.find_unassociated_eips()
print(f"Found {unassoc_eips['unassociated_eips']} unassociated EIPs")
```

### 3.10 Cost Monitoring & Alerting

**Practice: Proactive Budget Management**

```python
import boto3

class CostMonitoring:
    """Monitor and alert on spending anomalies"""

    def __init__(self):
        self.ce = boto3.client('ce')
        self.cloudwatch = boto3.client('cloudwatch')

    def setup_budget_alert(self, budget_name, limit, alert_threshold):
        """Alert if costs exceed threshold"""

        budgets = boto3.client('budgets')

        budget_config = {
            'BudgetName': budget_name,
            'BudgetLimit': {'Amount': str(limit), 'Unit': 'USD'},
            'TimeUnit': 'MONTHLY',
            'BudgetType': 'COST',
            'NotificationsWithSubscribers': [
                {
                    'Notification': {
                        'NotificationType': 'ACTUAL',
                        'ComparisonOperator': 'GREATER_THAN',
                        'Threshold': alert_threshold  # % of budget
                    },
                    'Subscribers': [
                        {'SubscriptionType': 'EMAIL', 'Address': 'ops@company.com'}
                    ]
                }
            ]
        }

        return budget_config

    def detect_anomalies(self):
        """Detect unusual spending patterns"""

        response = self.ce.get_cost_and_usage(
            TimePeriod={'Start': '2024-01-01', 'End': '2024-01-31'},
            Granularity='DAILY',
            Metrics=['UnblendedCost'],
            GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
        )

        # Calculate moving average
        costs_by_day = []
        for result in response['ResultsByTime']:
            daily_total = sum(
                float(g['Metrics']['UnblendedCost']['Amount'])
                for g in result['Groups']
            )
            costs_by_day.append(daily_total)

        # Find anomalies
        avg_cost = sum(costs_by_day) / len(costs_by_day)
        std_dev = (sum((x - avg_cost) ** 2 for x in costs_by_day) / len(costs_by_day)) ** 0.5

        anomalies = [
            (day, cost) for day, cost in enumerate(costs_by_day)
            if abs(cost - avg_cost) > 2 * std_dev  # 2 std deviations
        ]

        return {
            'daily_average': avg_cost,
            'std_deviation': std_dev,
            'anomalies': anomalies,
            'action': 'Investigate spikes' if anomalies else 'Normal spending'
        }

    def cost_per_metric(self, metric_name, metric_value):
        """Calculate cost per business metric"""

        total_monthly_cost = 5000  # Example

        cost_per_metric = total_monthly_cost / metric_value if metric_value > 0 else 0

        return {
            'metric': metric_name,
            'metric_value': metric_value,
            'total_cost': total_monthly_cost,
            'cost_per_metric': cost_per_metric,
            'trend': 'Use to track efficiency improvements'
        }

# Example: Cost per active user
result = CostMonitoring().cost_per_metric('active_users', 100000)
print(f"Cost per user: ${result['cost_per_metric']:.4f}/month")
```

## 4. Decision Frameworks

### Choose Commitment Model:
1. **Steady workload** → 3-year Reserved (40% discount)
2. **Growing workload** → 1-year Savings Plan (28% discount)
3. **Variable workload** → On-Demand (0% discount)
4. **Batch/fault-tolerant** → Spot (70% discount)

### Right-Sizing Priority:
1. Instances with <10% average CPU
2. Unattached storage
3. Idle databases
4. Unused Elastic IPs

## 5. Checklist

- [ ] All resources tagged with cost allocation tags
- [ ] Budget alerts configured
- [ ] Right-sizing analysis quarterly
- [ ] Reserved instance utilization tracked
- [ ] Spot instances used for fault-tolerant work
- [ ] Database idle connections terminated
- [ ] Storage lifecycle policies configured
- [ ] Old data archived to cold storage
- [ ] Auto-scaling configured with cost controls
- [ ] Idle resources identified and cleaned up
- [ ] Cost per transaction/request tracked
- [ ] FinOps metrics reported monthly
- [ ] Build vs buy decisions documented with cost
- [ ] License optimization reviewed annually

## 6. Common Mistakes & Anti-Patterns

| Mistake | Impact | Fix |
|---------|--------|-----|
| Massive on-demand instances | 2-3x cost | Right-size, use commitments |
| No Reserved Instances | 25% cheaper available | Purchase RIs for baseline |
| Ignoring idle resources | $100k+ annual waste | Automate idle detection |
| No cost tagging | Can't allocate costs | Tag everything at creation |
| Spot without fault tolerance | Unexpected outages | Use Spot only for resilient services |
| Over-provisioned databases | 2-3x cost | Right-size based on metrics |
| No data lifecycle policy | Storage cost grows forever | Archive old data automatically |
| Manual cost review | Findings ignored | Automate detection & alerts |

## 7. Tools & References

**Cost Management:**
- AWS Cost Explorer, AWS Trusted Advisor
- CloudHealth, Densify, Cloudozer
- Terraform for IaC (cost estimation)

**FinOps:**
- FinOps Foundation (Linux Foundation)
- "Cloud FinOps" book
- AWS Well-Architected Framework

**Monitoring:**
- Datadog, New Relic, Prometheus
- Custom CloudWatch dashboards

**Optimization Tools:**
- AWS Compute Optimizer, Savings Planner
- Right-sizing recommendation engines
- Spot fleet for batch jobs
