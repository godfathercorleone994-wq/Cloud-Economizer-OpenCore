"""
Test configuration and fixtures
"""
import pytest


@pytest.fixture
def sample_config():
    """Sample configuration for testing"""
    return {
        'aws': {
            'enabled': True,
            'regions': ['us-east-1'],
            'profile': 'default'
        },
        'azure': {
            'enabled': False
        },
        'gcp': {
            'enabled': False
        },
        'analysis': {
            'lookback_days': 30,
            'min_savings_threshold': 100
        },
        'ai': {
            'enabled': False,
            'model': 'gpt-4',
            'confidence_threshold': 0.7
        }
    }


@pytest.fixture
def sample_findings():
    """Sample findings for testing"""
    return {
        'categories': {
            'EC2 Instances': {
                'count': 5,
                'savings': 1000,
                'items': [
                    {
                        'resource_id': 'i-12345',
                        'resource_type': 'EC2 Instance',
                        'issue': 'Low CPU utilization',
                        'recommendation': 'Downsize instance',
                        'estimated_monthly_savings': 200,
                        'confidence': 0.9
                    }
                ]
            }
        },
        'total_savings': 1000,
        'timestamp': '2025-01-01T00:00:00'
    }
