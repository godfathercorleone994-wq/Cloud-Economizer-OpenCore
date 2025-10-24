"""
AI-powered insight engine for enhanced recommendations
"""
from typing import Dict, List
import os


class InsightEngine:
    """Enhances cost optimization recommendations with AI insights"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.model = config.get('model', 'gpt-4')
        self.confidence_threshold = config.get('confidence_threshold', 0.7)
        self.enabled = config.get('enabled', False)
        
        # Check if OpenAI API key is available
        self.api_key = os.environ.get('OPENAI_API_KEY')
        if self.enabled and not self.api_key:
            print("Warning: AI features enabled but OPENAI_API_KEY not set")
            self.enabled = False
    
    def enhance_recommendations(self, categories: Dict) -> List[Dict]:
        """
        Enhance recommendations with AI-powered insights
        
        Args:
            categories: Analysis results by category
            
        Returns:
            List of enhanced recommendations sorted by priority
        """
        if not self.enabled:
            return self._generate_basic_recommendations(categories)
        
        try:
            return self._generate_ai_recommendations(categories)
        except Exception as e:
            print(f"Warning: AI enhancement failed, using basic recommendations: {e}")
            return self._generate_basic_recommendations(categories)
    
    def _generate_basic_recommendations(self, categories: Dict) -> List[Dict]:
        """Generate basic recommendations without AI"""
        recommendations = []
        
        for category, data in categories.items():
            if data.get('count', 0) > 0:
                avg_savings = data.get('savings', 0) / data.get('count', 1)
                
                # Determine priority based on savings and confidence
                priority = self._calculate_priority(
                    data.get('savings', 0),
                    data.get('count', 0)
                )
                
                recommendations.append({
                    'category': category,
                    'priority': priority,
                    'finding_count': data.get('count', 0),
                    'total_savings': data.get('savings', 0),
                    'average_savings_per_item': avg_savings,
                    'recommendation': self._get_category_recommendation(category),
                    'risk_level': self._assess_risk(category),
                    'effort': self._assess_effort(category)
                })
        
        # Sort by total savings
        recommendations.sort(key=lambda x: x['total_savings'], reverse=True)
        
        return recommendations
    
    def _generate_ai_recommendations(self, categories: Dict) -> List[Dict]:
        """Generate AI-enhanced recommendations"""
        # This would integrate with OpenAI API for more sophisticated analysis
        # For now, use enhanced basic recommendations
        return self._generate_basic_recommendations(categories)
    
    def _calculate_priority(self, savings: float, count: int) -> str:
        """Calculate priority level based on impact"""
        if savings > 10000 or count > 50:
            return "High"
        elif savings > 1000 or count > 10:
            return "Medium"
        else:
            return "Low"
    
    def _get_category_recommendation(self, category: str) -> str:
        """Get specific recommendation for category"""
        recommendations = {
            'EC2 Instances': 'Review and rightsize or terminate idle instances',
            'EBS Volumes': 'Delete unattached volumes or create snapshots',
            'Elastic IPs': 'Release unattached Elastic IPs',
            'RDS Databases': 'Downsize or use reserved instances for better pricing',
            'S3 Storage': 'Implement lifecycle policies to optimize storage costs',
            'Virtual Machines': 'Deallocate stopped VMs or resize active ones',
            'Managed Disks': 'Clean up unattached disks',
            'Storage Accounts': 'Optimize storage tier based on access patterns',
            'Compute Instances': 'Review instance utilization and rightsizing',
            'Persistent Disks': 'Remove unattached disks',
            'Cloud Storage': 'Configure lifecycle management for automatic optimization'
        }
        return recommendations.get(category, 'Review and optimize resources')
    
    def _assess_risk(self, category: str) -> str:
        """Assess risk level for implementing changes"""
        high_risk = ['EC2 Instances', 'RDS Databases', 'Virtual Machines', 'Compute Instances']
        medium_risk = ['EBS Volumes', 'Managed Disks', 'Persistent Disks']
        
        if category in high_risk:
            return "Medium"
        elif category in medium_risk:
            return "Low"
        else:
            return "Very Low"
    
    def _assess_effort(self, category: str) -> str:
        """Assess implementation effort"""
        low_effort = ['Elastic IPs', 'EBS Volumes', 'Managed Disks', 'Persistent Disks']
        
        if category in low_effort:
            return "Low"
        else:
            return "Medium"
