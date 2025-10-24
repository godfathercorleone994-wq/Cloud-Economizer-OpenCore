# ☁️ Cloud Economizer - Open Core Edition

> **Reduce cloud costs by up to 70% with AI-powered optimization**

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## 🎯 What is This?

An intelligent engine that scans your cloud infrastructure and identifies cost-saving opportunities.

**Features:**
- 🔍 Deep infrastructure analysis (AWS, Azure, GCP)
- 🤖 AI-powered waste detection
- 📝 Generates ready-to-use Terraform/scripts
- 💰 Save $50K-500K+ annually

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/godfathercorleone994-wq/Cloud-Economizer-OpenCore.git
cd Cloud-Economizer-OpenCore

# Install dependencies
pip install -r requirements.txt

# Configure your cloud credentials
cp config/config.example.yaml config/config.yaml
# Edit config.yaml with your cloud credentials
```

### Basic Usage

```bash
# Analyze AWS infrastructure
python -m cloud_economizer analyze --provider aws --profile default

# Analyze Azure infrastructure
python -m cloud_economizer analyze --provider azure --subscription-id YOUR_SUB_ID

# Analyze GCP infrastructure
python -m cloud_economizer analyze --provider gcp --project-id YOUR_PROJECT_ID

# Generate optimization report
python -m cloud_economizer report --format html --output report.html

# Generate Terraform scripts for optimizations
python -m cloud_economizer generate --type terraform --output optimizations/
```

## 🔧 Configuration

Create a `config/config.yaml` file:

```yaml
# Cloud Provider Settings
aws:
  enabled: true
  regions:
    - us-east-1
    - us-west-2
  profile: default

azure:
  enabled: false
  subscription_id: ""
  tenant_id: ""

gcp:
  enabled: false
  project_id: ""
  credentials_file: ""

# Analysis Settings
analysis:
  lookback_days: 30
  min_savings_threshold: 100  # Minimum monthly savings to report (USD)
  
# AI Settings
ai:
  enabled: true
  model: gpt-4
  confidence_threshold: 0.7

# Output Settings
output:
  format: json
  include_scripts: true
  terraform_version: "1.5.0"
```

## 📊 What Gets Analyzed?

### AWS
- ✅ EC2 instances (idle, oversized, old generation)
- ✅ EBS volumes (unattached, oversized, snapshot optimization)
- ✅ RDS databases (idle, oversized)
- ✅ S3 buckets (lifecycle policies, storage class optimization)
- ✅ Load balancers (unused, consolidation opportunities)
- ✅ Elastic IPs (unattached)
- ✅ NAT Gateways (underutilized)
- ✅ Lambda functions (memory optimization)

### Azure
- ✅ Virtual Machines (idle, oversized)
- ✅ Managed Disks (unattached, optimization)
- ✅ SQL Databases (sizing, reserved instances)
- ✅ Storage Accounts (tier optimization)
- ✅ App Service Plans (consolidation)
- ✅ Virtual Networks (unused resources)

### GCP
- ✅ Compute Engine instances (idle, rightsizing)
- ✅ Persistent Disks (unattached, optimization)
- ✅ Cloud SQL (sizing optimization)
- ✅ Cloud Storage (lifecycle management)
- ✅ Load Balancers (utilization)

## 🤖 AI-Powered Insights

The AI engine analyzes:
- Historical usage patterns
- Industry best practices
- Workload characteristics
- Cost optimization opportunities
- Risk assessment for changes

## 📈 Sample Output

```
╔════════════════════════════════════════════════════════════╗
║           CLOUD ECONOMIZER ANALYSIS REPORT                 ║
╚════════════════════════════════════════════════════════════╝

Total Potential Monthly Savings: $47,832.00

TOP RECOMMENDATIONS:
─────────────────────────────────────────────────────────────

1. 🔴 EC2 Instance Rightsizing (High Priority)
   • 23 instances can be downsized
   • Monthly Savings: $18,450
   • Confidence: 94%
   • Terraform script: generated

2. 🟡 Unused EBS Volumes (Medium Priority)
   • 156 unattached volumes detected
   • Monthly Savings: $12,340
   • Confidence: 99%
   • Cleanup script: generated

3. 🟢 S3 Lifecycle Optimization (Low Risk)
   • 45 buckets without lifecycle policies
   • Monthly Savings: $8,920
   • Confidence: 88%
   • Terraform script: generated

[... 15 more recommendations ...]
```

## 🛠️ Generated Outputs

The tool generates:
- 📊 **HTML/PDF Reports** - Visual dashboards with charts
- 🔧 **Terraform Modules** - Ready-to-apply infrastructure changes
- 📜 **Shell Scripts** - Automation scripts for immediate actions
- 📋 **CSV Exports** - Detailed data for spreadsheet analysis
- 🔔 **Slack/Email Notifications** - Automated alerts

## 🔐 Security & Privacy

- All analysis runs locally or in your environment
- No data sent to external services (unless AI features enabled)
- Cloud credentials never stored, only used for API calls
- Open source - audit the code yourself
- Supports AWS IAM roles, Azure MSI, GCP service accounts

## 🧪 Testing

```bash
# Run unit tests
python -m pytest tests/

# Run integration tests (requires cloud credentials)
python -m pytest tests/integration/

# Run with coverage
python -m pytest --cov=cloud_economizer tests/
```

## 📚 Documentation

- [Installation Guide](docs/installation.md)
- [Configuration Reference](docs/configuration.md)
- [Cloud Provider Setup](docs/cloud-setup.md)
- [Architecture Overview](docs/architecture.md)
- [API Reference](docs/api.md)
- [Contributing Guide](CONTRIBUTING.md)

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details.

## 📄 License

Apache License 2.0 - see [LICENSE](LICENSE) file for details.

## 🌟 Roadmap

- [ ] Multi-account/subscription support
- [ ] Custom rule engine
- [ ] Kubernetes cost optimization
- [ ] Real-time monitoring integration
- [ ] Cost allocation and showback
- [ ] Automated remediation workflows
- [ ] Integration with FinOps platforms

## 💬 Support

- 📖 [Documentation](docs/)
- 🐛 [Issue Tracker](https://github.com/godfathercorleone994-wq/Cloud-Economizer-OpenCore/issues)
- 💬 [Discussions](https://github.com/godfathercorleone994-wq/Cloud-Economizer-OpenCore/discussions)

## ⭐ Star History

If you find this project useful, please consider giving it a star!

---

**Made with ❤️ by the Cloud Economizer community**
