# tests/test_core.py
"""
Core functionality tests
"""
import pytest
from unittest.mock import Mock, patch
from ai_api_module.core.ai import AI
from ai_api_module.core.response import AIResponse, Usage
from ai_api_module.core.config import Config
from ai_api_module.core.conversation import Conversation
from ai_api_module.core.exceptions import BudgetExceededError, ModelNotAvailableError


class TestAI:
    """Test AI class functionality"""
    
    def test_ai_initialization(self, test_config):
        """Test AI initialization"""
        ai = AI()
        assert ai.config is not None
        assert ai.model_registry is not None
        assert ai.provider_router is not None
    
    def test_ai_with_custom_config(self):
        """Test AI with custom configuration"""
        ai = AI(
            provider="anthropic",
            temperature=0.5,
            budget_limit=5.0
        )
        assert ai.config.default_provider == "anthropic"
        assert ai.config.temperature == 0.5
        assert ai.config.daily_budget_limit == 5.0
    
    @patch('ai_api_module.providers.openai_provider.OpenAIProvider')
    def test_chat_basic(self, mock_provider_class, mock_ai_instance, sample_response):
        """Test basic chat functionality"""
        # Setup mock
        mock_provider = Mock()
        mock_provider.chat.return_value = sample_response
        mock_provider_class.return_value = mock_provider
        
        # Mock provider router
        mock_ai_instance.provider_router.execute = Mock(return_value=sample_response)
        
        # Test chat
        response = mock_ai_instance.chat("Hello world")
        
        assert isinstance(response, AIResponse)
        assert response.text == "This is a test response"
        assert response.cost == 0.001

    def test_chat_with_files_and_context(self, mock_ai_instance, sample_response, tmp_path):
        """Ensure chat handles file attachments and context injection."""
        doc_path = tmp_path / "doc.txt"
        doc_path.write_text("Important document content", encoding="utf-8")

        mock_ai_instance.provider_router.execute = Mock(return_value=sample_response)

        response = mock_ai_instance.chat(
            "Summarize",
            files=[doc_path],
            history=[{"role": "user", "content": "Earlier question"}],
            use_memory=True,
        )

        assert isinstance(response, AIResponse)
        assert mock_ai_instance.provider_router.execute.called
        executed_request = mock_ai_instance.provider_router.execute.call_args[0][0]
        assert "documents" in executed_request
        assert executed_request["documents"][0]["name"] == doc_path.name
        assert executed_request.get("history") is not None

    def test_prepare_attachments_native_support(self, tmp_path, mock_ai_instance):
        text_file = tmp_path / "sample.txt"
        text_file.write_text("Gemini native text", encoding="utf-8")

        mock_ai_instance._pending_model_name = "gemini-2.5-pro"
        attachments = mock_ai_instance._prepare_attachments(None, None, [text_file])
        assert attachments["native_files"] == [str(text_file.resolve())]
        assert attachments["documents"] == []

    def test_prepare_attachments_non_native(self, tmp_path, mock_ai_instance):
        text_file = tmp_path / "notes.txt"
        text_file.write_text("OpenAI fallback text", encoding="utf-8")

        mock_ai_instance._pending_model_name = "gpt-5"
        attachments = mock_ai_instance._prepare_attachments(None, None, [text_file])
        assert attachments["native_files"] == []
        assert len(attachments["documents"]) == 1
        assert "OpenAI fallback text" in attachments["documents"][0].text
    
    def test_budget_enforcement(self, mock_ai_instance):
        """Test budget limit enforcement"""
        mock_ai_instance.config.daily_budget_limit = 0.001
        mock_ai_instance._get_daily_cost = Mock(return_value=0.0005)
        
        # Mock high cost estimation
        mock_ai_instance.model_registry.estimate_request_cost = Mock(return_value=0.002)
        
        with pytest.raises(BudgetExceededError):
            mock_ai_instance.chat("Expensive request")
    
    def test_model_resolution(self, mock_ai_instance):
        """Test model alias resolution"""
        # Test smart routing
        model, provider = mock_ai_instance.model_registry.resolve("smart", None)
        assert model is not None
        assert provider is not None
        
        # Test provider shortcuts
        model, provider = mock_ai_instance.model_registry.resolve("gpt", "openai")
        assert provider == "openai"


class TestConversation:
    """Test conversation management"""
    
    def test_conversation_creation(self, mock_ai_instance):
        """Test conversation creation"""
        conv = Conversation(
            ai_instance=mock_ai_instance,
            name="Test Chat",
            system="You are helpful"
        )
        
        assert conv.name == "Test Chat"
        assert conv.system == "You are helpful"
        assert len(conv.messages) == 1  # System message
        assert conv.messages[0].role == "system"
    
    def test_add_messages(self, mock_ai_instance):
        """Test adding messages to conversation"""
        conv = Conversation(ai_instance=mock_ai_instance)
        
        conv.add_user_message("Hello")
        conv.add_assistant_message("Hi there!")
        
        assert len(conv.messages) == 2
        assert conv.messages[0].role == "user"
        assert conv.messages[1].role == "assistant"
    
    def test_conversation_send(self, mock_ai_instance, sample_response):
        """Test sending messages in conversation"""
        mock_ai_instance.chat = Mock(return_value=sample_response)
        
        conv = Conversation(ai_instance=mock_ai_instance)
        conv.add_user_message("Test message")
        
        response = conv.send()
        
        assert isinstance(response, AIResponse)
        assert len(conv.responses) == 1
        mock_ai_instance.chat.assert_called_once()
    
    def test_model_switching(self, mock_ai_instance):
        """Test switching models mid-conversation"""
        conv = Conversation(ai_instance=mock_ai_instance)
        
        conv.switch_model("claude", "anthropic")
        
        assert conv.current_model == "claude"
        assert conv.current_provider == "anthropic"


class TestConfig:
    """Test configuration management"""
    
    def test_config_creation(self):
        """Test config creation"""
        config = Config(
            default_provider="openai",
            temperature=0.7
        )
        
        assert config.default_provider == "openai"
        assert config.temperature == 0.7
    
    def test_config_validation(self):
        """Test config validation"""
        config = Config(temperature=3.0)  # Invalid temperature
        
        issues = config.validate()
        assert len(issues) > 0
        assert any("temperature" in issue.lower() for issue in issues)
    
    def test_config_from_env(self, mock_api_keys):
        """Test config loading from environment"""
        config = Config()
        
        assert config.openai_api_key == mock_api_keys["OPENAI_API_KEY"]
        assert config.anthropic_api_key == mock_api_keys["ANTHROPIC_API_KEY"]
