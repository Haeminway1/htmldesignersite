# tests/test_async.py
"""
Async functionality tests
"""
import pytest
import asyncio
from unittest.mock import Mock, AsyncMock
from ai_api_module.features.async_handler import AsyncHandler
from ai_api_module.core.response import AIResponse


@pytest.mark.asyncio
class TestAsyncHandler:
    """Test async functionality"""
    
    async def test_async_chat(self):
        """Test async chat"""
        mock_router = Mock()
        mock_provider = Mock()
        mock_provider.async_chat = AsyncMock(return_value=AIResponse(text="Async response"))
        mock_router._select_provider.side_effect = lambda request: mock_provider
        
        handler = AsyncHandler(mock_router)
        
        response = await handler.chat("Hello async")
        
        assert response.text == "Async response"
        mock_provider.async_chat.assert_called_once()
    
    async def test_batch_chat(self):
        """Test batch chat processing"""
        mock_router = Mock()
        mock_provider = Mock()
        
        # Mock multiple responses
        async def mock_async_chat(request_data):
            return AIResponse(
                text=f"Response to: {request_data['message']}",
                structured_data=request_data.get("structured_payload")
            )
        
        mock_provider.async_chat = mock_async_chat
        mock_router._select_provider.side_effect = lambda request: mock_provider
        
        handler = AsyncHandler(mock_router)
        
        messages = ["Message 1", "Message 2", "Message 3"]
        responses = await handler.batch_chat(messages, max_concurrent=2)
        
        assert len(responses) == 3
        for i, response in enumerate(responses):
            assert f"Message {i+1}" in response.text
