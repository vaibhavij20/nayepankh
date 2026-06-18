"""
Pytest configuration and fixtures.
"""

import pytest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def mock_config():
    """Mock configuration for testing."""
    import config
    original_api_key = config.Config.GEMINI_API_KEY
    config.Config.GEMINI_API_KEY = "test_api_key"
    
    yield config.Config
    
    config.Config.GEMINI_API_KEY = original_api_key
