"""
Core analysis engine for cloud cost optimization
"""
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional


class CloudAnalyzer:
    """Main analyzer that orchestrates cloud cost analysis"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.results = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'categories': {},
            'recommendations': [],
            'total_savings': 0
        }
    
    def analyze(self, provider: str, aws_profile: Optional[str] = None,
                azure_subscription_id: Optional[str] = None,
                gcp_project_id: Optional[str] = None) -> Dict:
        """
        Run analysis on specified cloud provider(s)
        
        Args:
            provider: Cloud provider to analyze ('aws', 'azure', 'gcp', 'all')
            aws_profile: AWS profile name
            azure_subscription_id: Azure subscription ID
            gcp_project_id: GCP project ID
            
        Returns:
            Dictionary containing analysis results
        """
        providers_to_analyze = []
        
        if provider == 'all':
            if self.config.get('aws', {}).get('enabled', True):
                providers_to_analyze.append('aws')
            if self.config.get('azure', {}).get('enabled', False):
                providers_to_analyze.append('azure')
            if self.config.get('gcp', {}).get('enabled', False):
                providers_to_analyze.append('gcp')
        else:
            providers_to_analyze.append(provider)
        
        for prov in providers_to_analyze:
            if prov == 'aws':
                self._analyze_aws(aws_profile)
            elif prov == 'azure':
                self._analyze_azure(azure_subscription_id)
            elif prov == 'gcp':
                self._analyze_gcp(gcp_project_id)
        
        # Apply AI analysis if enabled
        if self.config.get('ai', {}).get('enabled', False):
            self._apply_ai_insights()
        
        # Save results
        self._save_results()
        
        return self.results
    
    def _analyze_aws(self, profile: Optional[str] = None):
        """Analyze AWS infrastructure"""
        from cloud_economizer.providers.aws_analyzer import AWSAnalyzer
        
        analyzer = AWSAnalyzer(self.config.get('aws', {}), profile)
        aws_results = analyzer.analyze()
        
        # Merge results
        for category, data in aws_results.items():
            if category not in self.results['categories']:
                self.results['categories'][category] = {'count': 0, 'savings': 0, 'items': []}
            
            self.results['categories'][category]['count'] += data.get('count', 0)
            self.results['categories'][category]['savings'] += data.get('savings', 0)
            self.results['categories'][category]['items'].extend(data.get('items', []))
            self.results['total_savings'] += data.get('savings', 0)
    
    def _analyze_azure(self, subscription_id: Optional[str] = None):
        """Analyze Azure infrastructure"""
        from cloud_economizer.providers.azure_analyzer import AzureAnalyzer
        
        config = self.config.get('azure', {})
        if subscription_id:
            config['subscription_id'] = subscription_id
        
        analyzer = AzureAnalyzer(config)
        azure_results = analyzer.analyze()
        
        # Merge results
        for category, data in azure_results.items():
            if category not in self.results['categories']:
                self.results['categories'][category] = {'count': 0, 'savings': 0, 'items': []}
            
            self.results['categories'][category]['count'] += data.get('count', 0)
            self.results['categories'][category]['savings'] += data.get('savings', 0)
            self.results['categories'][category]['items'].extend(data.get('items', []))
            self.results['total_savings'] += data.get('savings', 0)
    
    def _analyze_gcp(self, project_id: Optional[str] = None):
        """Analyze GCP infrastructure"""
        from cloud_economizer.providers.gcp_analyzer import GCPAnalyzer
        
        config = self.config.get('gcp', {})
        if project_id:
            config['project_id'] = project_id
        
        analyzer = GCPAnalyzer(config)
        gcp_results = analyzer.analyze()
        
        # Merge results
        for category, data in gcp_results.items():
            if category not in self.results['categories']:
                self.results['categories'][category] = {'count': 0, 'savings': 0, 'items': []}
            
            self.results['categories'][category]['count'] += data.get('count', 0)
            self.results['categories'][category]['savings'] += data.get('savings', 0)
            self.results['categories'][category]['items'].extend(data.get('items', []))
            self.results['total_savings'] += data.get('savings', 0)
    
    def _apply_ai_insights(self):
        """Apply AI-powered insights to recommendations"""
        from cloud_economizer.ai.insight_engine import InsightEngine
        
        engine = InsightEngine(self.config.get('ai', {}))
        enhanced_recommendations = engine.enhance_recommendations(
            self.results['categories']
        )
        
        self.results['recommendations'] = enhanced_recommendations
    
    def _save_results(self):
        """Save analysis results to file"""
        output_dir = Path('output')
        output_dir.mkdir(exist_ok=True)
        
        output_file = output_dir / 'analysis_results.json'
        with open(output_file, 'w') as f:
            json.dump(self.results, f, indent=2)
