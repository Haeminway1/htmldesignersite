# tests/test_integration.py
"""
Integration tests (require API keys)
"""
import pytest
import os
from ai_api_module import AI


@pytest.mark.integration
class TestIntegration:
    """Integration tests with real APIs"""
    
    def test_real_openai_chat(self):
        """Test real OpenAI chat (requires API key)"""
        if not os.getenv("OPENAI_API_KEY"):
            pytest.skip("OpenAI API key not available")
        
        ai = AI(provider="openai")
        
        response = ai.chat(
            "Say 'test' and nothing else",
            model="gpt-4o-mini",
            max_tokens=10
        )
        
        assert isinstance(response.text, str)
        assert len(response.text) > 0
        assert response.cost > 0
    
    def test_real_anthropic_chat(self):
        """Test real Anthropic chat (requires API key)"""
        if not os.getenv("ANTHROPIC_API_KEY"):
            pytest.skip("Anthropic API key not available")
        
        ai = AI(provider="anthropic")
        
        response = ai.chat(
            "Say 'test' and nothing else",
            model="claude-3-haiku-20240307",
            max_tokens=10
        )
        
        assert isinstance(response.text, str)
        assert len(response.text) > 0
        assert response.cost > 0
    
    def test_conversation_flow(self):
        """Test conversation flow"""
        if not any(os.getenv(key) for key in ["OPENAI_API_KEY", "ANTHROPIC_API_KEY"]):
            pytest.skip("No API keys available")
        
        ai = AI()
        
        conversation = ai.start_conversation(
            name="Test Conversation",
            system="Be very brief in responses"
        )
        
        # First message
        conversation.add_user_message("Say hello")
        response1 = conversation.send()
        
        assert len(response1.text) > 0
        
        # Second message
        conversation.add_user_message("Say goodbye")
        response2 = conversation.send()
        
        assert len(response2.text) > 0
        assert conversation.total_cost > 0
