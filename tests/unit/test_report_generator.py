"""
Unit tests for report generator
"""
import pytest
import json
import tempfile
from pathlib import Path
from cloud_economizer.generators.report_generator import ReportGenerator


def test_report_generator_initialization():
    """Test report generator can be initialized"""
    generator = ReportGenerator()
    assert generator is not None


def test_json_report_generation():
    """Test JSON report generation"""
    generator = ReportGenerator()
    
    # Create test data
    test_data = {
        'timestamp': '2025-01-01T00:00:00',
        'categories': {
            'EC2 Instances': {
                'count': 5,
                'savings': 1000,
                'items': [
                    {
                        'resource_id': 'i-12345',
                        'issue': 'Low utilization',
                        'estimated_monthly_savings': 200
                    }
                ]
            }
        },
        'total_savings': 1000
    }
    
    # Create temporary files
    with tempfile.TemporaryDirectory() as tmpdir:
        data_file = Path(tmpdir) / 'data.json'
        output_file = Path(tmpdir) / 'report.json'
        
        # Write test data
        with open(data_file, 'w') as f:
            json.dump(test_data, f)
        
        # Generate report
        generator.generate(str(data_file), 'json', str(output_file))
        
        # Verify output
        assert output_file.exists()
        with open(output_file, 'r') as f:
            result = json.load(f)
        
        assert result['total_savings'] == 1000
        assert 'EC2 Instances' in result['categories']


def test_html_report_generation():
    """Test HTML report generation"""
    generator = ReportGenerator()
    
    test_data = {
        'timestamp': '2025-01-01T00:00:00',
        'categories': {},
        'total_savings': 0
    }
    
    with tempfile.TemporaryDirectory() as tmpdir:
        data_file = Path(tmpdir) / 'data.json'
        output_file = Path(tmpdir) / 'report.html'
        
        with open(data_file, 'w') as f:
            json.dump(test_data, f)
        
        generator.generate(str(data_file), 'html', str(output_file))
        
        assert output_file.exists()
        content = output_file.read_text()
        assert 'Cloud Economizer' in content
        assert 'html' in content.lower()
