"""
Unit tests for Cloud Economizer
"""
import pytest
from cloud_economizer.analysis.analyzer import CloudAnalyzer


def test_analyzer_initialization():
    """Test analyzer can be initialized"""
    config = {
        'aws': {'enabled': True, 'regions': ['us-east-1']},
        'azure': {'enabled': False},
        'gcp': {'enabled': False}
    }
    
    analyzer = CloudAnalyzer(config)
    assert analyzer is not None
    assert analyzer.config == config


def test_analyzer_results_structure():
    """Test analyzer initializes results correctly"""
    config = {}
    analyzer = CloudAnalyzer(config)
    
    assert 'timestamp' in analyzer.results
    assert 'categories' in analyzer.results
    assert 'recommendations' in analyzer.results
    assert 'total_savings' in analyzer.results
    assert analyzer.results['total_savings'] == 0
