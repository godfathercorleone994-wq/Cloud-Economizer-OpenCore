"""
GCP infrastructure analyzer for cost optimization
"""
from typing import Dict, Optional
from google.cloud import compute_v1
from google.cloud import storage


class GCPAnalyzer:
    """Analyzes GCP infrastructure for cost optimization opportunities"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.project_id = config.get('project_id')
        
        if not self.project_id:
            raise ValueError("GCP project_id is required")
    
    def analyze(self) -> Dict:
        """
        Run comprehensive GCP analysis
        
        Returns:
            Dictionary with analysis results by category
        """
        results = {}
        
        # Analyze Compute Engine instances
        results['Compute Instances'] = self._analyze_compute_instances()
        
        # Analyze Persistent Disks
        results['Persistent Disks'] = self._analyze_disks()
        
        # Analyze Cloud Storage
        results['Cloud Storage'] = self._analyze_storage()
        
        return results
    
    def _analyze_compute_instances(self) -> Dict:
        """Analyze Compute Engine instances for optimization"""
        findings = []
        total_savings = 0
        
        try:
            instances_client = compute_v1.InstancesClient()
            
            # Get all instances across all zones
            aggregated_list = instances_client.aggregated_list(
                project=self.project_id
            )
            
            for zone, response in aggregated_list:
                if response.instances:
                    for instance in response.instances:
                        instance_name = instance.name
                        machine_type = instance.machine_type.split('/')[-1]
                        status = instance.status
                        
                        # Check if instance is stopped
                        if status == 'TERMINATED':
                            estimated_savings = self._estimate_instance_savings(machine_type)
                            findings.append({
                                'resource_id': instance_name,
                                'resource_type': 'Compute Instance',
                                'issue': 'Stopped instance still incurring disk charges',
                                'current_config': machine_type,
                                'recommendation': 'Delete if not needed',
                                'estimated_monthly_savings': estimated_savings,
                                'confidence': 0.9
                            })
                            total_savings += estimated_savings
                            
        except Exception as e:
            # Skip if we don't have permissions
            pass
        
        return {
            'count': len(findings),
            'savings': total_savings,
            'items': findings
        }
    
    def _analyze_disks(self) -> Dict:
        """Analyze Persistent Disks for optimization"""
        findings = []
        total_savings = 0
        
        try:
            disks_client = compute_v1.DisksClient()
            
            # Get all disks
            aggregated_list = disks_client.aggregated_list(
                project=self.project_id
            )
            
            for zone, response in aggregated_list:
                if response.disks:
                    for disk in response.disks:
                        disk_name = disk.name
                        disk_size = disk.size_gb
                        
                        # Check if disk is unattached
                        if not disk.users:
                            estimated_savings = self._estimate_disk_savings(disk_size)
                            findings.append({
                                'resource_id': disk_name,
                                'resource_type': 'Persistent Disk',
                                'issue': 'Unattached disk',
                                'current_config': f'{disk_size}GB',
                                'recommendation': 'Delete if not needed or create snapshot',
                                'estimated_monthly_savings': estimated_savings,
                                'confidence': 0.95
                            })
                            total_savings += estimated_savings
                            
        except Exception as e:
            pass
        
        return {
            'count': len(findings),
            'savings': total_savings,
            'items': findings
        }
    
    def _analyze_storage(self) -> Dict:
        """Analyze Cloud Storage buckets for optimization"""
        findings = []
        total_savings = 0
        
        try:
            storage_client = storage.Client(project=self.project_id)
            
            # Get all buckets
            for bucket in storage_client.list_buckets():
                bucket_name = bucket.name
                
                # Check if lifecycle management is configured
                if not bucket.lifecycle_rules:
                    estimated_savings = 40  # Conservative estimate
                    findings.append({
                        'resource_id': bucket_name,
                        'resource_type': 'Cloud Storage Bucket',
                        'issue': 'No lifecycle management',
                        'recommendation': 'Configure lifecycle rules to move old data to cheaper storage classes',
                        'estimated_monthly_savings': estimated_savings,
                        'confidence': 0.65
                    })
                    total_savings += estimated_savings
                    
        except Exception as e:
            pass
        
        return {
            'count': len(findings),
            'savings': total_savings,
            'items': findings
        }
    
    def _estimate_instance_savings(self, machine_type: str) -> float:
        """Estimate savings from instance optimization"""
        # Simplified GCP pricing
        pricing = {
            'e2-micro': 6,
            'e2-small': 12,
            'e2-medium': 24,
            'n1-standard-1': 25,
            'n1-standard-2': 50,
            'n1-standard-4': 100,
        }
        return pricing.get(machine_type, 80)
    
    def _estimate_disk_savings(self, size_gb: int) -> float:
        """Estimate savings from disk deletion"""
        # GCP persistent disk pricing ~$0.04/GB/month for standard
        return size_gb * 0.04
