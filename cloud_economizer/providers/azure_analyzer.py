"""
Azure infrastructure analyzer for cost optimization
"""
from typing import Dict, Optional
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.storage import StorageManagementClient


class AzureAnalyzer:
    """Analyzes Azure infrastructure for cost optimization opportunities"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.subscription_id = config.get('subscription_id')
        
        if not self.subscription_id:
            raise ValueError("Azure subscription_id is required")
        
        # Initialize Azure credentials
        try:
            self.credential = DefaultAzureCredential()
        except Exception as e:
            raise ValueError(f"Failed to authenticate with Azure: {e}")
    
    def analyze(self) -> Dict:
        """
        Run comprehensive Azure analysis
        
        Returns:
            Dictionary with analysis results by category
        """
        results = {}
        
        # Analyze Virtual Machines
        results['Virtual Machines'] = self._analyze_vms()
        
        # Analyze Managed Disks
        results['Managed Disks'] = self._analyze_disks()
        
        # Analyze Storage Accounts
        results['Storage Accounts'] = self._analyze_storage()
        
        return results
    
    def _analyze_vms(self) -> Dict:
        """Analyze Virtual Machines for optimization"""
        findings = []
        total_savings = 0
        
        try:
            compute_client = ComputeManagementClient(
                self.credential, 
                self.subscription_id
            )
            
            # Get all VMs
            for vm in compute_client.virtual_machines.list_all():
                vm_name = vm.name
                vm_size = vm.hardware_profile.vm_size
                
                # Check if VM is deallocated or stopped
                instance_view = compute_client.virtual_machines.instance_view(
                    vm.id.split('/')[4],  # resource group
                    vm_name
                )
                
                # Look for stopped VMs that still cost money
                statuses = [s.code for s in instance_view.statuses]
                if 'PowerState/stopped' in statuses:
                    estimated_savings = self._estimate_vm_savings(vm_size)
                    findings.append({
                        'resource_id': vm_name,
                        'resource_type': 'Virtual Machine',
                        'issue': 'VM is stopped but not deallocated',
                        'current_config': vm_size,
                        'recommendation': 'Deallocate VM to stop incurring charges',
                        'estimated_monthly_savings': estimated_savings,
                        'confidence': 1.0
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
        """Analyze Managed Disks for optimization"""
        findings = []
        total_savings = 0
        
        try:
            compute_client = ComputeManagementClient(
                self.credential,
                self.subscription_id
            )
            
            # Get all disks
            for disk in compute_client.disks.list():
                disk_name = disk.name
                disk_size = disk.disk_size_gb
                
                # Check if disk is unattached
                if not disk.managed_by:
                    estimated_savings = self._estimate_disk_savings(disk_size)
                    findings.append({
                        'resource_id': disk_name,
                        'resource_type': 'Managed Disk',
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
        """Analyze Storage Accounts for optimization"""
        findings = []
        total_savings = 0
        
        try:
            storage_client = StorageManagementClient(
                self.credential,
                self.subscription_id
            )
            
            # Get all storage accounts
            for account in storage_client.storage_accounts.list():
                account_name = account.name
                tier = account.access_tier
                
                # Check if account is using premium when it doesn't need to
                if tier == 'Premium':
                    estimated_savings = 30  # Conservative estimate
                    findings.append({
                        'resource_id': account_name,
                        'resource_type': 'Storage Account',
                        'issue': 'Using Premium tier',
                        'recommendation': 'Consider downgrading to Hot or Cool tier',
                        'estimated_monthly_savings': estimated_savings,
                        'confidence': 0.6
                    })
                    total_savings += estimated_savings
                    
        except Exception as e:
            pass
        
        return {
            'count': len(findings),
            'savings': total_savings,
            'items': findings
        }
    
    def _estimate_vm_savings(self, vm_size: str) -> float:
        """Estimate savings from VM optimization"""
        # Simplified Azure VM pricing
        pricing = {
            'Standard_B1s': 8,
            'Standard_B2s': 30,
            'Standard_D2s_v3': 70,
            'Standard_D4s_v3': 140,
            'Standard_D8s_v3': 280,
        }
        return pricing.get(vm_size, 100)
    
    def _estimate_disk_savings(self, size_gb: int) -> float:
        """Estimate savings from disk deletion"""
        # Azure managed disk pricing ~$0.05/GB/month for standard
        return size_gb * 0.05
