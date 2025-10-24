#!/usr/bin/env python
"""
Demo script to showcase Cloud Economizer capabilities
This creates mock data and demonstrates the analysis flow
"""
import json
from pathlib import Path
from cloud_economizer.analysis.analyzer import CloudAnalyzer
from cloud_economizer.ai.insight_engine import InsightEngine
from cloud_economizer.generators.report_generator import ReportGenerator
from cloud_economizer.generators.script_generator import ScriptGenerator

def create_demo_data():
    """Create demo analysis data"""
    return {
        'timestamp': '2025-10-24T00:00:00',
        'categories': {
            'EC2 Instances': {
                'count': 23,
                'savings': 18450.00,
                'items': [
                    {
                        'resource_id': 'i-1234567890abcdef0',
                        'resource_type': 'EC2 Instance',
                        'region': 'us-east-1',
                        'issue': 'Low CPU utilization (8%)',
                        'current_config': 'm5.xlarge',
                        'recommendation': 'Downsize to m5.large',
                        'cpu_utilization': 8.0,
                        'estimated_monthly_savings': 800.00,
                        'confidence': 0.94
                    },
                    {
                        'resource_id': 'i-0987654321fedcba0',
                        'resource_type': 'EC2 Instance',
                        'region': 'us-west-2',
                        'issue': 'Low CPU utilization (5%)',
                        'current_config': 'm5.2xlarge',
                        'recommendation': 'Downsize to m5.xlarge',
                        'cpu_utilization': 5.0,
                        'estimated_monthly_savings': 1400.00,
                        'confidence': 0.96
                    }
                ]
            },
            'EBS Volumes': {
                'count': 156,
                'savings': 12340.00,
                'items': [
                    {
                        'resource_id': 'vol-1234567890abcdef0',
                        'resource_type': 'EBS Volume',
                        'region': 'us-east-1',
                        'issue': 'Unattached volume',
                        'current_config': '100GB gp2',
                        'recommendation': 'Delete if not needed or create snapshot',
                        'estimated_monthly_savings': 10.00,
                        'confidence': 0.99
                    }
                ]
            },
            'Elastic IPs': {
                'count': 12,
                'savings': 43.20,
                'items': [
                    {
                        'resource_id': 'eipalloc-1234567890abcdef0',
                        'resource_type': 'Elastic IP',
                        'region': 'us-east-1',
                        'issue': 'Unattached Elastic IP',
                        'recommendation': 'Release if not needed',
                        'estimated_monthly_savings': 3.60,
                        'confidence': 1.0
                    }
                ]
            },
            'RDS Databases': {
                'count': 5,
                'savings': 2100.00,
                'items': [
                    {
                        'resource_id': 'mydb-instance',
                        'resource_type': 'RDS Instance',
                        'region': 'us-east-1',
                        'issue': 'Low CPU utilization (15%)',
                        'current_config': 'db.m5.xlarge',
                        'recommendation': 'Consider downsizing to db.m5.large',
                        'cpu_utilization': 15.0,
                        'estimated_monthly_savings': 420.00,
                        'confidence': 0.85
                    }
                ]
            },
            'S3 Storage': {
                'count': 45,
                'savings': 8920.00,
                'items': [
                    {
                        'resource_id': 'my-data-bucket',
                        'resource_type': 'S3 Bucket',
                        'issue': 'No lifecycle policy',
                        'recommendation': 'Implement lifecycle policy to move old data to cheaper storage',
                        'estimated_monthly_savings': 198.22,
                        'confidence': 0.7
                    }
                ]
            }
        },
        'total_savings': 41853.20,
        'recommendations': []
    }

def main():
    print("=" * 70)
    print("  Cloud Economizer - Demo")
    print("=" * 70)
    print()
    
    # Create demo data
    print("📊 Generating demo analysis data...")
    demo_data = create_demo_data()
    
    # Create output directory
    output_dir = Path('demo_output')
    output_dir.mkdir(exist_ok=True)
    
    # Save demo data
    data_file = output_dir / 'analysis_results.json'
    with open(data_file, 'w') as f:
        json.dump(demo_data, f, indent=2)
    print(f"✓ Demo data saved to {data_file}")
    print()
    
    # Generate AI insights
    print("🤖 Generating AI-powered insights...")
    engine = InsightEngine({'enabled': False})
    recommendations = engine.enhance_recommendations(demo_data['categories'])
    demo_data['recommendations'] = recommendations
    
    # Save updated data
    with open(data_file, 'w') as f:
        json.dump(demo_data, f, indent=2)
    print(f"✓ Generated {len(recommendations)} prioritized recommendations")
    print()
    
    # Display summary
    print("💰 Cost Optimization Summary:")
    print("-" * 70)
    print(f"   Total Potential Monthly Savings: ${demo_data['total_savings']:,.2f}")
    print(f"   Total Optimization Opportunities: {sum(cat['count'] for cat in demo_data['categories'].values())}")
    print()
    
    print("📋 Top Recommendations:")
    for i, rec in enumerate(recommendations[:5], 1):
        print(f"   {i}. {rec['category']}")
        print(f"      • {rec['finding_count']} findings")
        print(f"      • ${rec['total_savings']:,.2f}/month savings")
        print(f"      • Priority: {rec['priority']}")
        print()
    
    # Generate HTML report
    print("📄 Generating reports...")
    report_gen = ReportGenerator()
    
    html_file = output_dir / 'report.html'
    report_gen.generate(str(data_file), 'html', str(html_file))
    print(f"✓ HTML report: {html_file}")
    
    json_file = output_dir / 'report.json'
    report_gen.generate(str(data_file), 'json', str(json_file))
    print(f"✓ JSON report: {json_file}")
    
    csv_file = output_dir / 'report.csv'
    report_gen.generate(str(data_file), 'csv', str(csv_file))
    print(f"✓ CSV report: {csv_file}")
    print()
    
    # Generate scripts
    print("🔧 Generating optimization scripts...")
    script_gen = ScriptGenerator()
    scripts_dir = output_dir / 'scripts'
    scripts_dir.mkdir(exist_ok=True)
    
    generated = script_gen.generate(str(data_file), 'all', str(scripts_dir))
    for script in generated:
        print(f"✓ {script}")
    print()
    
    print("=" * 70)
    print("✨ Demo Complete!")
    print("=" * 70)
    print()
    print(f"📁 All outputs saved to: {output_dir.absolute()}")
    print()
    print("Next steps:")
    print(f"  1. Open {html_file} in your browser to view the report")
    print(f"  2. Review scripts in {scripts_dir}")
    print(f"  3. Run 'cloud-economizer --help' for real analysis")
    print()

if __name__ == '__main__':
    main()
