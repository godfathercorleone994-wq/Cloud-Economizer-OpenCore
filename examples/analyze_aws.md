# Example: Analyze AWS Infrastructure

This example demonstrates how to analyze AWS infrastructure for cost optimization opportunities.

## Prerequisites

1. AWS CLI configured with credentials
2. Cloud Economizer installed

## Configuration

Create `config/config.yaml`:

```yaml
aws:
  enabled: true
  regions:
    - us-east-1
    - us-west-2
  profile: default

analysis:
  lookback_days: 30
  min_savings_threshold: 100
```

## Run Analysis

```bash
# Analyze all regions
cloud-economizer analyze --provider aws

# Analyze specific profile
cloud-economizer analyze --provider aws --profile production

# Generate HTML report
cloud-economizer report --format html --output aws-optimization-report.html

# Generate Terraform scripts
cloud-economizer generate --type terraform --output optimizations/
```

## Expected Output

```
🔍 Starting Cloud Economizer Analysis
Provider: aws
✓ Configuration loaded from config/config.yaml

Running analysis...

Analysis Summary:

Category                Findings    Est. Monthly Savings
──────────────────────────────────────────────────────────
EC2 Instances                 23             $18,450.00
EBS Volumes                  156             $12,340.00
Elastic IPs                   12                $43.20
RDS Databases                  5              $2,100.00
S3 Storage                    45              $8,920.00
──────────────────────────────────────────────────────────
TOTAL                        241             $41,853.20

✓ Analysis complete!
Run 'cloud-economizer report' to generate detailed reports
```

## Review Results

1. Open the HTML report in your browser
2. Review each finding carefully
3. Implement changes using generated scripts
4. Monitor savings over time

## Safety Tips

- Always test in non-production environments first
- Review generated scripts before executing
- Have backups before deleting resources
- Use `terraform plan` before `terraform apply`
