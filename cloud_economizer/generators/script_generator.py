"""
Script generator for Terraform and shell scripts
"""
import json
from pathlib import Path
from typing import Dict, List


class ScriptGenerator:
    """Generates Terraform and shell scripts for optimizations"""
    
    def __init__(self):
        pass
    
    def generate(self, data_file: str, script_type: str, output_dir: str) -> List[str]:
        """
        Generate scripts for implementing optimizations
        
        Args:
            data_file: Path to analysis results JSON
            script_type: Type of scripts ('terraform', 'shell', 'all')
            output_dir: Output directory for scripts
            
        Returns:
            List of generated file paths
        """
        # Load analysis data
        with open(data_file, 'r') as f:
            data = json.load(f)
        
        generated_files = []
        
        if script_type in ['terraform', 'all']:
            tf_files = self._generate_terraform(data, output_dir)
            generated_files.extend(tf_files)
        
        if script_type in ['shell', 'all']:
            shell_files = self._generate_shell_scripts(data, output_dir)
            generated_files.extend(shell_files)
        
        return generated_files
    
    def _generate_terraform(self, data: Dict, output_dir: str) -> List[str]:
        """Generate Terraform scripts"""
        output_path = Path(output_dir)
        generated = []
        
        # Generate main.tf
        main_tf = output_path / 'main.tf'
        with open(main_tf, 'w') as f:
            f.write(self._get_terraform_header())
            
            # Generate resources based on findings
            for category, cat_data in data.get('categories', {}).items():
                if 'EBS' in category or 'Disk' in category:
                    f.write(self._generate_ebs_terraform(cat_data))
                elif 'S3' in category or 'Storage' in category:
                    f.write(self._generate_s3_terraform(cat_data))
        
        generated.append(str(main_tf))
        
        # Generate variables.tf
        vars_tf = output_path / 'variables.tf'
        with open(vars_tf, 'w') as f:
            f.write(self._get_terraform_variables())
        generated.append(str(vars_tf))
        
        # Generate README
        readme = output_path / 'README.md'
        with open(readme, 'w') as f:
            f.write(self._get_terraform_readme(data))
        generated.append(str(readme))
        
        return generated
    
    def _generate_shell_scripts(self, data: Dict, output_dir: str) -> List[str]:
        """Generate shell scripts"""
        output_path = Path(output_dir)
        generated = []
        
        # Generate cleanup script for AWS
        if any('EC2' in cat or 'EBS' in cat or 'Elastic' in cat 
               for cat in data.get('categories', {}).keys()):
            aws_script = output_path / 'cleanup_aws.sh'
            with open(aws_script, 'w') as f:
                f.write(self._generate_aws_cleanup_script(data))
            aws_script.chmod(0o755)
            generated.append(str(aws_script))
        
        # Generate cleanup script for Azure
        if any('Virtual' in cat or 'Managed' in cat 
               for cat in data.get('categories', {}).keys()):
            azure_script = output_path / 'cleanup_azure.sh'
            with open(azure_script, 'w') as f:
                f.write(self._generate_azure_cleanup_script(data))
            azure_script.chmod(0o755)
            generated.append(str(azure_script))
        
        # Generate cleanup script for GCP
        if any('Compute' in cat or 'Persistent' in cat 
               for cat in data.get('categories', {}).keys()):
            gcp_script = output_path / 'cleanup_gcp.sh'
            with open(gcp_script, 'w') as f:
                f.write(self._generate_gcp_cleanup_script(data))
            gcp_script.chmod(0o755)
            generated.append(str(gcp_script))
        
        return generated
    
    def _get_terraform_header(self) -> str:
        """Get Terraform configuration header"""
        return """# Cloud Economizer - Generated Optimization Scripts
# Review carefully before applying!

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

"""
    
    def _get_terraform_variables(self) -> str:
        """Get Terraform variables"""
        return """variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "dry_run" {
  description = "Perform a dry run without making changes"
  type        = bool
  default     = true
}
"""
    
    def _generate_ebs_terraform(self, data: Dict) -> str:
        """Generate Terraform for EBS optimizations"""
        tf = "\n# EBS Volume Cleanup\n"
        
        for item in data.get('items', [])[:5]:  # Limit to first 5 as example
            volume_id = item.get('resource_id', '')
            if volume_id:
                tf += f"""
# Remove unattached volume: {volume_id}
# Estimated savings: ${item.get('estimated_monthly_savings', 0):.2f}/month
# resource "aws_ebs_volume" "{volume_id.replace('-', '_')}" {{
#   # This volume should be deleted
#   # Uncomment and run terraform destroy to remove
# }}
"""
        return tf
    
    def _generate_s3_terraform(self, data: Dict) -> str:
        """Generate Terraform for S3 optimizations"""
        tf = "\n# S3 Lifecycle Policies\n"
        
        for item in data.get('items', [])[:3]:
            bucket_name = item.get('resource_id', '')
            if bucket_name:
                tf += f"""
resource "aws_s3_bucket_lifecycle_configuration" "{bucket_name.replace('-', '_').replace('.', '_')}" {{
  bucket = "{bucket_name}"

  rule {{
    id     = "transition-old-data"
    status = "Enabled"

    transition {{
      days          = 30
      storage_class = "STANDARD_IA"
    }}

    transition {{
      days          = 90
      storage_class = "GLACIER"
    }}

    expiration {{
      days = 365
    }}
  }}
}}
"""
        return tf
    
    def _get_terraform_readme(self, data: Dict) -> str:
        """Generate README for Terraform scripts"""
        total_savings = data.get('total_savings', 0)
        return f"""# Cloud Economizer - Terraform Scripts

## Overview
These Terraform scripts implement cost optimizations identified by Cloud Economizer.

**Potential Monthly Savings:** ${total_savings:.2f}

## Usage

1. Review the generated scripts carefully
2. Initialize Terraform:
   ```bash
   terraform init
   ```

3. Preview changes:
   ```bash
   terraform plan
   ```

4. Apply changes (when ready):
   ```bash
   terraform apply
   ```

## Safety Notes

- Always run `terraform plan` first
- Test in non-production environments
- Have backups before deleting resources
- Review each change individually

## Generated Files

- `main.tf` - Main configuration
- `variables.tf` - Configuration variables

---
Generated by Cloud Economizer - Open Core Edition
"""
    
    def _generate_aws_cleanup_script(self, data: Dict) -> str:
        """Generate AWS cleanup shell script"""
        script = """#!/bin/bash
# Cloud Economizer - AWS Cleanup Script
# Review and modify before running!

set -e

echo "Cloud Economizer - AWS Cleanup Script"
echo "======================================"
echo ""
echo "WARNING: This script will delete resources. Review carefully!"
echo ""
read -p "Continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Aborted."
    exit 0
fi

# Set your AWS region
AWS_REGION="${AWS_REGION:-us-east-1}"

echo "Using region: $AWS_REGION"
echo ""

"""
        
        # Add cleanup commands for unattached EBS volumes
        ebs_data = data.get('categories', {}).get('EBS Volumes', {})
        if ebs_data.get('items'):
            script += "# Cleanup unattached EBS volumes\n"
            script += "echo 'Cleaning up unattached EBS volumes...'\n"
            for item in ebs_data.get('items', [])[:10]:
                volume_id = item.get('resource_id', '')
                if volume_id:
                    script += f"# aws ec2 delete-volume --volume-id {volume_id} --region $AWS_REGION\n"
            script += "\n"
        
        # Add cleanup for unattached Elastic IPs
        eip_data = data.get('categories', {}).get('Elastic IPs', {})
        if eip_data.get('items'):
            script += "# Release unattached Elastic IPs\n"
            script += "echo 'Releasing unattached Elastic IPs...'\n"
            for item in eip_data.get('items', [])[:10]:
                allocation_id = item.get('resource_id', '')
                if allocation_id:
                    script += f"# aws ec2 release-address --allocation-id {allocation_id} --region $AWS_REGION\n"
            script += "\n"
        
        script += """
echo ""
echo "Cleanup complete!"
echo "Note: Commands are commented out by default. Review and uncomment to execute."
"""
        return script
    
    def _generate_azure_cleanup_script(self, data: Dict) -> str:
        """Generate Azure cleanup shell script"""
        return """#!/bin/bash
# Cloud Economizer - Azure Cleanup Script
# Review and modify before running!

set -e

echo "Cloud Economizer - Azure Cleanup Script"
echo "========================================"
echo ""
echo "WARNING: This script will delete resources. Review carefully!"
echo ""

# Add Azure cleanup commands here based on findings
# Example: az disk delete --name <disk-name> --resource-group <rg>

echo "Cleanup complete!"
"""
    
    def _generate_gcp_cleanup_script(self, data: Dict) -> str:
        """Generate GCP cleanup shell script"""
        return """#!/bin/bash
# Cloud Economizer - GCP Cleanup Script
# Review and modify before running!

set -e

echo "Cloud Economizer - GCP Cleanup Script"
echo "====================================="
echo ""
echo "WARNING: This script will delete resources. Review carefully!"
echo ""

# Add GCP cleanup commands here based on findings
# Example: gcloud compute disks delete <disk-name> --zone=<zone>

echo "Cleanup complete!"
"""
