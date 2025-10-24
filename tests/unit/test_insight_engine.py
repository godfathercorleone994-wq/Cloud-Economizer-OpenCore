"""
Unit tests for AI insight engine
"""
import pytest
from cloud_economizer.ai.insight_engine import InsightEngine


def test_insight_engine_initialization():
    """Test insight engine can be initialized"""
    config = {
        'enabled': False,
        'model': 'gpt-4',
        'confidence_threshold': 0.7
    }
    
    engine = InsightEngine(config)
    assert engine is not None
    assert engine.model == 'gpt-4'
    assert engine.confidence_threshold == 0.7


def test_basic_recommendations():
    """Test basic recommendations generation"""
    config = {'enabled': False}
    engine = InsightEngine(config)
    
    categories = {
        'EC2 Instances': {
            'count': 5,
            'savings': 1000,
            'items': []
        },
        'EBS Volumes': {
            'count': 10,
            'savings': 500,
            'items': []
        }
    }
    
    recommendations = engine.enhance_recommendations(categories)
    
    assert len(recommendations) == 2
    assert recommendations[0]['total_savings'] >= recommendations[1]['total_savings']


def test_priority_calculation():
    """Test priority calculation"""
    config = {'enabled': False}
    engine = InsightEngine(config)
    
    # High priority
    assert engine._calculate_priority(15000, 60) == "High"
    
    # Medium priority
    assert engine._calculate_priority(5000, 20) == "Medium"
    
    # Low priority
    assert engine._calculate_priority(500, 5) == "Low"


def test_risk_assessment():
    """Test risk assessment"""
    config = {'enabled': False}
    engine = InsightEngine(config)
    
    assert engine._assess_risk('EC2 Instances') == "Medium"
    assert engine._assess_risk('EBS Volumes') == "Low"
    assert engine._assess_risk('Elastic IPs') == "Very Low"
