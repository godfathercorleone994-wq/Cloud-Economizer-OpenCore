# Installation Guide

## Requirements

- Python 3.8 or higher
- pip package manager
- Cloud provider credentials (AWS, Azure, and/or GCP)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/godfathercorleone994-wq/Cloud-Economizer-OpenCore.git
cd Cloud-Economizer-OpenCore
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Cloud Economizer

```bash
pip install -e .
```

### 5. Verify Installation

```bash
cloud-economizer --version
```

## Cloud Provider Setup

### AWS

1. Install AWS CLI: https://aws.amazon.com/cli/
2. Configure credentials:
   ```bash
   aws configure
   ```

### Azure

1. Install Azure CLI: https://docs.microsoft.com/cli/azure/install-azure-cli
2. Login:
   ```bash
   az login
   ```

### GCP

1. Install gcloud CLI: https://cloud.google.com/sdk/docs/install
2. Authenticate:
   ```bash
   gcloud auth application-default login
   ```

## Configuration

Create your configuration file:

```bash
cp config/config.example.yaml config/config.yaml
```

Edit `config/config.yaml` with your settings.

## Troubleshooting

### Import Errors

If you see import errors, ensure you've activated your virtual environment and installed all dependencies.

### Permission Errors

Ensure your cloud credentials have the necessary permissions to read resource information. Cloud Economizer only needs read-only access.

### Module Not Found

If you see "module not found" errors, try reinstalling:

```bash
pip install -e . --force-reinstall
```

## Next Steps

- See [examples/analyze_aws.md](../examples/analyze_aws.md) for usage examples
- Read the [Configuration Guide](configuration.md) for detailed settings
