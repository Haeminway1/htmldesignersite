# tests/conftest.py
"""
Pytest configuration and fixtures
"""
import pytest
import os
from unittest.mock import Mock, MagicMock
from ai_api_module import AI
from ai_api_module.core.config import Config
from ai_api_module.core.response import AIResponse, Usage


@pytest.fixture
def mock_api_keys():
    """Mock API keys for testing"""
    return {
        "OPENAI_API_KEY": "sk-test-openai-key",
        "ANTHROPIC_API_KEY": "sk-ant-test-anthropic-key", 
        "GOOGLE_API_KEY": "test-google-key",
        "XAI_API_KEY": "xai-test-key"
    }


@pytest.fixture(autouse=True)
def setup_env(mock_api_keys):
    """Setup test environment variables"""
    original_env = {}
    
    # Store original values
    for key in mock_api_keys:
        original_env[key] = os.environ.get(key)
        os.environ[key] = mock_api_keys[key]
    
    yield
    
    # Restore original values
    for key, value in original_env.items():
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = value


@pytest.fixture
def test_config(mock_api_keys):
    """Test configuration"""
    return Config(
        default_provider="openai",
        default_model="test-model",
        debug=True,
        enable_cache=False  # Disable cache for tests
    )


@pytest.fixture
def mock_ai_instance(test_config):
    """Mock AI instance for testing"""
    ai = AI()
    ai.config = test_config
    return ai


@pytest.fixture
def sample_response():
    """Sample AI response for testing"""
    return AIResponse(
        text="This is a test response",
        model="test-model",
        provider="test-provider",
        usage=Usage(
            prompt_tokens=10,
            completion_tokens=20,
            total_tokens=30
        ),
        cost=0.001
    )


@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client"""
    client = Mock()
    
    # Mock chat completion
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = "Test response"
    mock_response.choices[0].message.tool_calls = None
    mock_response.usage.prompt_tokens = 10
    mock_response.usage.completion_tokens = 20
    mock_response.usage.total_tokens = 30
    
    client.chat.completions.create.return_value = mock_response
    
    return client


@pytest.fixture
def mock_anthropic_client():
    """Mock Anthropic client"""
    client = Mock()
    
    # Mock message response
    mock_response = Mock()
    mock_response.content = [Mock()]
    mock_response.content[0].type = "text"
    mock_response.content[0].text = "Test response"
    mock_response.usage.input_tokens = 10
    mock_response.usage.output_tokens = 20
    
    client.messages.create.return_value = mock_response
    
    return client