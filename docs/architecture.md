# Architecture Overview

## System Design

Cloud Economizer follows a modular architecture for analyzing cloud infrastructure and generating cost optimization recommendations.

```
┌─────────────────────────────────────────────────────────┐
│                        CLI Layer                        │
│                   (User Interface)                      │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                   Analysis Engine                       │
│              (Orchestration & Results)                  │
└─────┬──────────────────┬──────────────────┬────────────┘
      │                  │                  │
┌─────▼─────┐   ┌────────▼────────┐  ┌─────▼──────────┐
│   AWS     │   │     Azure       │  │      GCP       │
│ Analyzer  │   │   Analyzer      │  │   Analyzer     │
└─────┬─────┘   └────────┬────────┘  └─────┬──────────┘
      │                  │                  │
      │                  │                  │
┌─────▼──────────────────▼──────────────────▼────────────┐
│                  AI Insight Engine                      │
│            (Pattern Recognition & Scoring)              │
└────────────────────────┬────────────────────────────────┘
                         │
         ┌───────────────┴───────────────┐
         │                               │
┌────────▼──────────┐         ┌─────────▼──────────┐
│  Report Generator │         │  Script Generator  │
│   (HTML/PDF/CSV)  │         │ (Terraform/Shell)  │
└───────────────────┘         └────────────────────┘
```

## Core Components

### 1. CLI Layer (`cli.py`)

- Entry point for user interactions
- Command parsing and validation
- Progress reporting
- Error handling

### 2. Analysis Engine (`analysis/analyzer.py`)

- Orchestrates analysis across cloud providers
- Aggregates results
- Manages configuration
- Coordinates with AI engine

### 3. Cloud Provider Analyzers

Each provider has its own analyzer:

- **AWS Analyzer** (`providers/aws_analyzer.py`)
  - EC2, EBS, RDS, S3, Elastic IP analysis
  - CloudWatch metrics integration
  - Cost estimation

- **Azure Analyzer** (`providers/azure_analyzer.py`)
  - VM, Disk, Storage account analysis
  - Azure Monitor integration
  - Resource utilization checks

- **GCP Analyzer** (`providers/gcp_analyzer.py`)
  - Compute, Disk, Storage analysis
  - Stackdriver metrics
  - Cost calculations

### 4. AI Insight Engine (`ai/insight_engine.py`)

- Recommendation prioritization
- Risk assessment
- Confidence scoring
- Pattern recognition (when AI is enabled)

### 5. Generators

- **Report Generator** (`generators/report_generator.py`)
  - HTML, PDF, JSON, CSV outputs
  - Visual dashboards
  - Summary statistics

- **Script Generator** (`generators/script_generator.py`)
  - Terraform modules
  - Shell scripts
  - Documentation generation

## Data Flow

1. **Input**: User runs CLI command with cloud provider selection
2. **Configuration**: System loads config.yaml settings
3. **Authentication**: Connect to cloud provider APIs
4. **Discovery**: Enumerate resources (instances, disks, etc.)
5. **Metrics Collection**: Gather usage metrics (CPU, I/O, etc.)
6. **Analysis**: Apply optimization rules and heuristics
7. **AI Enhancement**: Optionally enhance with AI insights
8. **Output Generation**: Create reports and scripts
9. **Results**: Present findings to user

## Extension Points

### Adding a New Cloud Provider

1. Create analyzer in `cloud_economizer/providers/`
2. Implement `analyze()` method
3. Return standardized result format
4. Register in `analysis/analyzer.py`

### Adding New Analysis Rules

1. Add detection logic in provider analyzer
2. Calculate estimated savings
3. Provide recommendation text
4. Set confidence level

### Custom Report Formats

1. Add generator method in `report_generator.py`
2. Create template
3. Register format in CLI

## Security Considerations

- Read-only access to cloud resources
- Credentials never stored
- Local execution by default
- No data sent externally (unless AI enabled)
- Open source for auditing

## Performance

- Parallel region scanning
- Efficient API usage
- Result caching
- Minimal resource footprint
