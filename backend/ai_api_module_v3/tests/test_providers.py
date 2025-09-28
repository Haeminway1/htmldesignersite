# tests/test_providers.py
"""
Provider tests
"""
import pytest
from unittest.mock import Mock, patch
from ai_api_module.providers.openai_provider import OpenAIProvider
from ai_api_module.providers.anthropic_provider import AnthropicProvider
from ai_api_module.core.response import AIResponse
from ai_api_module.providers.google_provider import GoogleProvider


class TestOpenAIProvider:
    """Test OpenAI provider"""
    
    @patch('ai_api_module.providers.openai_provider.OpenAI')
    def test_openai_provider_init(self, mock_openai_class):
        """Test OpenAI provider initialization"""
        provider = OpenAIProvider("test-key", {})
        
        assert provider.api_key == "test-key"
        assert provider.provider_name == "openai"
    
    @patch('ai_api_module.providers.openai_provider.OpenAI')
    def test_openai_chat(self, mock_openai_class, mock_openai_client):
        """Test OpenAI chat functionality"""
        mock_openai_class.return_value = mock_openai_client
        
        provider = OpenAIProvider("test-key", {})
        
        request_data = {
            "message": "Hello",
            "model": "gpt-4",
            "temperature": 0.7,
            "format": "json"
        }
        
        response = provider.chat(request_data)
        
        assert isinstance(response, AIResponse)
        mock_openai_client.chat.completions.create.assert_called_once()
    
    def test_openai_cost_calculation(self):
        """Test OpenAI cost calculation"""
        provider = OpenAIProvider("test-key", {})
        
        from ai_api_module.core.response import Usage
        usage = Usage(prompt_tokens=1000, completion_tokens=500)
        
        cost = provider._calculate_cost("gpt-4o", usage)
        assert cost > 0


class TestAnthropicProvider:
    """Test Anthropic provider"""
    
    @patch('ai_api_module.providers.anthropic_provider.anthropic')
    def test_anthropic_provider_init(self, mock_anthropic):
        """Test Anthropic provider initialization"""
        provider = AnthropicProvider("test-key", {})
        
        assert provider.api_key == "test-key"
        assert provider.provider_name == "anthropic"
    
    @patch('ai_api_module.providers.anthropic_provider.anthropic')
    def test_anthropic_chat(self, mock_anthropic, mock_anthropic_client):
        """Test Anthropic chat functionality"""
        mock_anthropic.Anthropic.return_value = mock_anthropic_client
        
        provider = AnthropicProvider("test-key", {})
        
        request_data = {
            "message": "Hello",
            "model": "claude-3-sonnet",
            "system": "You are helpful"
        }
        
        response = provider.chat(request_data)
        
        assert isinstance(response, AIResponse)
        mock_anthropic_client.messages.create.assert_called_once()


@patch('ai_api_module.providers.google_provider.genai', create=True)
@patch('ai_api_module.providers.google_provider.GoogleProvider._guess_mime_type')
def test_google_chat_native_files(mock_guess, mock_genai, tmp_path):
    part = Mock()
    mock_genai.Client.return_value = Mock()
    mock_guess.return_value = 'application/pdf'
    provider = GoogleProvider('test-key', {})

    file_path = tmp_path / 'sample.pdf'
    file_path.write_bytes(b'%PDF-1.4 native upload test')

    request_data = {
        'message': 'Summarise',
        'model': 'gemini-2.5-pro',
        'documents': [],
        'native_files': [str(file_path)],
    }

    provider.chat(request_data)

    provider.client.models.generate_content.assert_called_once()
    args, kwargs = provider.client.models.generate_content.call_args
    contents = kwargs['contents']
    assert len(contents) >= 2
    assert request_data['documents'] == []