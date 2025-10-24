"""
AWS infrastructure analyzer for cost optimization
"""
import boto3
from typing import Dict, Optional, List
from datetime import datetime, timedelta


class AWSAnalyzer:
    """Analyzes AWS infrastructure for cost optimization opportunities"""
    
    def __init__(self, config: Dict, profile: Optional[str] = None):
        self.config = config
        self.profile = profile or config.get('profile', 'default')
        self.regions = config.get('regions', ['us-east-1'])
        self.lookback_days = config.get('lookback_days', 30)
        
        # Initialize AWS session
        try:
            self.session = boto3.Session(profile_name=self.profile)
        except Exception as e:
            # Fallback to default credentials
            self.session = boto3.Session()
    
    def analyze(self) -> Dict:
        """
        Run comprehensive AWS analysis
        
        Returns:
            Dictionary with analysis results by category
        """
        results = {}
        
        # Analyze EC2 instances
        results['EC2 Instances'] = self._analyze_ec2_instances()
        
        # Analyze EBS volumes
        results['EBS Volumes'] = self._analyze_ebs_volumes()
        
        # Analyze Elastic IPs
        results['Elastic IPs'] = self._analyze_elastic_ips()
        
        # Analyze RDS instances
        results['RDS Databases'] = self._analyze_rds_instances()
        
        # Analyze S3 buckets
        results['S3 Storage'] = self._analyze_s3_buckets()
        
        return results
    
    def _analyze_ec2_instances(self) -> Dict:
        """Analyze EC2 instances for optimization opportunities"""
        findings = []
        total_savings = 0
        
        for region in self.regions:
            try:
                ec2 = self.session.client('ec2', region_name=region)
                cloudwatch = self.session.client('cloudwatch', region_name=region)
                
                # Get all instances
                response = ec2.describe_instances()
                
                for reservation in response.get('Reservations', []):
                    for instance in reservation.get('Instances', []):
                        instance_id = instance.get('InstanceId')
                        instance_type = instance.get('InstanceType')
                        state = instance.get('State', {}).get('Name')
                        
                        if state == 'running':
                            # Check CPU utilization
                            cpu_util = self._get_average_cpu(cloudwatch, instance_id)
                            
                            # Low CPU indicates idle or oversized instance
                            if cpu_util < 10:
                                estimated_savings = self._estimate_instance_savings(instance_type, 0.5)
                                findings.append({
                                    'resource_id': instance_id,
                                    'resource_type': 'EC2 Instance',
                                    'region': region,
                                    'issue': 'Low CPU utilization',
                                    'current_config': instance_type,
                                    'recommendation': 'Consider downsizing or stopping',
                                    'cpu_utilization': cpu_util,
                                    'estimated_monthly_savings': estimated_savings,
                                    'confidence': 0.9
                                })
                                total_savings += estimated_savings
                        
            except Exception as e:
                # Skip regions where we don't have access
                continue
        
        return {
            'count': len(findings),
            'savings': total_savings,
            'items': findings
        }
    
    def _analyze_ebs_volumes(self) -> Dict:
        """Analyze EBS volumes for cost savings"""
        findings = []
        total_savings = 0
        
        for region in self.regions:
            try:
                ec2 = self.session.client('ec2', region_name=region)
                
                # Get all volumes
                response = ec2.describe_volumes()
                
                for volume in response.get('Volumes', []):
                    volume_id = volume.get('VolumeId')
                    state = volume.get('State')
                    size = volume.get('Size', 0)
                    volume_type = volume.get('VolumeType', 'gp2')
                    
                    # Check for unattached volumes
                    if state == 'available':
                        # Unattached volume
                        estimated_savings = self._estimate_ebs_savings(size, volume_type)
                        findings.append({
                            'resource_id': volume_id,
                            'resource_type': 'EBS Volume',
                            'region': region,
                            'issue': 'Unattached volume',
                            'current_config': f'{size}GB {volume_type}',
                            'recommendation': 'Delete if not needed or create snapshot',
                            'estimated_monthly_savings': estimated_savings,
                            'confidence': 0.99
                        })
                        total_savings += estimated_savings
                        
            except Exception as e:
                continue
        
        return {
            'count': len(findings),
            'savings': total_savings,
            'items': findings
        }
    
    def _analyze_elastic_ips(self) -> Dict:
        """Analyze Elastic IPs for waste"""
        findings = []
        total_savings = 0
        
        for region in self.regions:
            try:
                ec2 = self.session.client('ec2', region_name=region)
                
                # Get all addresses
                response = ec2.describe_addresses()
                
                for address in response.get('Addresses', []):
                    allocation_id = address.get('AllocationId')
                    instance_id = address.get('InstanceId')
                    
                    # Unattached EIP costs money
                    if not instance_id:
                        estimated_savings = 3.60  # ~$0.005/hour
                        findings.append({
                            'resource_id': allocation_id,
                            'resource_type': 'Elastic IP',
                            'region': region,
                            'issue': 'Unattached Elastic IP',
                            'recommendation': 'Release if not needed',
                            'estimated_monthly_savings': estimated_savings,
                            'confidence': 1.0
                        })
                        total_savings += estimated_savings
                        
            except Exception as e:
                continue
        
        return {
            'count': len(findings),
            'savings': total_savings,
            'items': findings
        }
    
    def _analyze_rds_instances(self) -> Dict:
        """Analyze RDS instances for optimization"""
        findings = []
        total_savings = 0
        
        for region in self.regions:
            try:
                rds = self.session.client('rds', region_name=region)
                cloudwatch = self.session.client('cloudwatch', region_name=region)
                
                # Get all DB instances
                response = rds.describe_db_instances()
                
                for db in response.get('DBInstances', []):
                    db_id = db.get('DBInstanceIdentifier')
                    db_class = db.get('DBInstanceClass')
                    
                    # Check CPU utilization
                    cpu_util = self._get_average_db_cpu(cloudwatch, db_id)
                    
                    if cpu_util < 20:
                        estimated_savings = self._estimate_rds_savings(db_class, 0.3)
                        findings.append({
                            'resource_id': db_id,
                            'resource_type': 'RDS Instance',
                            'region': region,
                            'issue': 'Low CPU utilization',
                            'current_config': db_class,
                            'recommendation': 'Consider downsizing',
                            'cpu_utilization': cpu_util,
                            'estimated_monthly_savings': estimated_savings,
                            'confidence': 0.85
                        })
                        total_savings += estimated_savings
                        
            except Exception as e:
                continue
        
        return {
            'count': len(findings),
            'savings': total_savings,
            'items': findings
        }
    
    def _analyze_s3_buckets(self) -> Dict:
        """Analyze S3 buckets for optimization"""
        findings = []
        total_savings = 0
        
        try:
            s3 = self.session.client('s3')
            
            # Get all buckets
            response = s3.list_buckets()
            
            for bucket in response.get('Buckets', []):
                bucket_name = bucket.get('Name')
                
                # Check if lifecycle policy exists
                try:
                    s3.get_bucket_lifecycle_configuration(Bucket=bucket_name)
                    has_lifecycle = True
                except:
                    has_lifecycle = False
                
                if not has_lifecycle:
                    # Estimate potential savings from lifecycle policies
                    estimated_savings = 50  # Conservative estimate
                    findings.append({
                        'resource_id': bucket_name,
                        'resource_type': 'S3 Bucket',
                        'issue': 'No lifecycle policy',
                        'recommendation': 'Implement lifecycle policy to move old data to cheaper storage',
                        'estimated_monthly_savings': estimated_savings,
                        'confidence': 0.7
                    })
                    total_savings += estimated_savings
                    
        except Exception as e:
            pass
        
        return {
            'count': len(findings),
            'savings': total_savings,
            'items': findings
        }
    
    def _get_average_cpu(self, cloudwatch, instance_id: str) -> float:
        """Get average CPU utilization for an instance"""
        try:
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(days=self.lookback_days)
            
            response = cloudwatch.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='CPUUtilization',
                Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
                StartTime=start_time,
                EndTime=end_time,
                Period=86400,  # 1 day
                Statistics=['Average']
            )
            
            if response.get('Datapoints'):
                values = [dp['Average'] for dp in response['Datapoints']]
                return sum(values) / len(values)
        except:
            pass
        
        return 50.0  # Default assumption
    
    def _get_average_db_cpu(self, cloudwatch, db_id: str) -> float:
        """Get average CPU utilization for RDS instance"""
        try:
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(days=self.lookback_days)
            
            response = cloudwatch.get_metric_statistics(
                Namespace='AWS/RDS',
                MetricName='CPUUtilization',
                Dimensions=[{'Name': 'DBInstanceIdentifier', 'Value': db_id}],
                StartTime=start_time,
                EndTime=end_time,
                Period=86400,
                Statistics=['Average']
            )
            
            if response.get('Datapoints'):
                values = [dp['Average'] for dp in response['Datapoints']]
                return sum(values) / len(values)
        except:
            pass
        
        return 50.0
    
    def _estimate_instance_savings(self, instance_type: str, reduction: float) -> float:
        """Estimate savings from instance optimization"""
        # Simplified pricing model
        pricing = {
            't2.micro': 8.5,
            't2.small': 17,
            't2.medium': 34,
            't3.micro': 7.5,
            't3.small': 15,
            't3.medium': 30,
            'm5.large': 70,
            'm5.xlarge': 140,
            'm5.2xlarge': 280,
        }
        
        base_cost = pricing.get(instance_type, 100)
        return base_cost * reduction
    
    def _estimate_rds_savings(self, db_class: str, reduction: float) -> float:
        """Estimate savings from RDS optimization"""
        # Simplified RDS pricing
        pricing = {
            'db.t2.micro': 15,
            'db.t2.small': 30,
            'db.t3.micro': 14,
            'db.t3.small': 27,
            'db.m5.large': 135,
            'db.m5.xlarge': 270,
        }
        
        base_cost = pricing.get(db_class, 150)
        return base_cost * reduction
    
    def _estimate_ebs_savings(self, size_gb: int, volume_type: str) -> float:
        """Estimate savings from EBS volume deletion"""
        # Simplified EBS pricing per GB per month
        pricing = {
            'gp2': 0.10,
            'gp3': 0.08,
            'io1': 0.125,
            'io2': 0.125,
            'sc1': 0.025,
            'st1': 0.045,
        }
        
        price_per_gb = pricing.get(volume_type, 0.10)
        return size_gb * price_per_gb
