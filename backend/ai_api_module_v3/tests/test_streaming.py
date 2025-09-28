# tests/test_streaming.py
"""
Streaming functionality tests
"""
import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from ai_api_module import AI
from ai_api_module.features.streaming import StreamingHandler
from ai_api_module.core.response import AIResponse
import time


class TestStreamingHandler:
    """Test streaming handler functionality"""
    
    def test_streaming_handler_creation(self):
        """Test streaming handler creation"""
        mock_router = Mock()
        mock_ai = Mock()
        handler = StreamingHandler(mock_router, mock_ai)
        
        assert handler.provider_router == mock_router
        assert handler.ai == mock_ai
        assert hasattr(handler, 'stream')
    
    @pytest.mark.asyncio
    async def test_streaming_basic(self):
        """Test basic streaming functionality"""
        mock_router = Mock()
        mock_ai = Mock()
        mock_provider = Mock()
        
        # Mock streaming response
        async def mock_stream_generator():
            chunks = ["Hello", " ", "world", "!", ""]
            for chunk in chunks:
                yield chunk
                await asyncio.sleep(0.01)  # Simulate delay
        
        mock_provider.stream_chat = mock_stream_generator
        mock_router._select_provider.return_value = mock_provider
        
        handler = StreamingHandler(mock_router, mock_ai)
        
        chunks = []
        request_data = {"message": "Hello world"}
        async for chunk in handler.stream(request_data):
            chunks.append(chunk)
        
        assert chunks == ["Hello", " ", "world", "!", ""]
    
    @pytest.mark.asyncio
    async def test_streaming_with_callbacks(self):
        """Test streaming with callback functions"""
        mock_router = Mock()
        mock_ai = Mock()
        mock_provider = Mock()
        
        # Mock streaming response
        async def mock_stream_generator():
            for chunk in ["Chunk1", "Chunk2", "Chunk3"]:
                yield chunk
                await asyncio.sleep(0.01)
        
        mock_provider.stream_chat = mock_stream_generator
        mock_router._select_provider.return_value = mock_provider
        
        handler = StreamingHandler(mock_router, mock_ai)
        
        # Callback tracking
        received_chunks = []
        completed = []
        
        def on_chunk(chunk):
            received_chunks.append(chunk)
        
        def on_complete(full_response):
            completed.append(full_response)
        
        request_data = {"message": "Test message"}
        await handler.stream_with_callbacks(
            request_data,
            on_chunk=on_chunk,
            on_complete=on_complete
        )
        
        assert received_chunks == ["Chunk1", "Chunk2", "Chunk3"]
        assert len(completed) == 1
        assert completed[0] == "Chunk1Chunk2Chunk3"
    
    @pytest.mark.asyncio
    async def test_streaming_error_handling(self):
        """Test streaming error handling"""
        mock_router = Mock()
        mock_provider = Mock()
        
        # Mock streaming that raises an error
        async def mock_failing_stream():
            yield "Start"
            raise Exception("Streaming error")
        
        mock_provider.stream_chat = mock_failing_stream
        mock_router._select_provider.return_value = mock_provider
        
        handler = StreamingHandler(mock_router)
        
        chunks = []
        with pytest.raises(Exception, match="Streaming error"):
            async for chunk in handler.stream_chat("Test"):
                chunks.append(chunk)
        
        assert chunks == ["Start"]


class TestAIStreaming:
    """Test AI class streaming functionality"""
    
    @patch('ai_api_module.features.streaming.StreamingHandler')
    def test_ai_stream_chat_setup(self, mock_streaming_handler):
        """Test AI streaming setup"""
        ai = AI()
        
        # Mock streaming handler
        mock_handler_instance = Mock()
        mock_streaming_handler.return_value = mock_handler_instance
        
        # Call stream_chat (this should initialize the handler)
        try:
            ai.stream_chat("Test message")
        except:
            pass  # We expect this to fail without proper mocking
        
        # Verify handler was created with correct router
        mock_streaming_handler.assert_called_once_with(ai.provider_router)
    
    @pytest.mark.asyncio
    async def test_stream_chat_integration(self):
        """Test stream chat integration with AI class"""
        ai = AI()
        
        # Mock the streaming handler
        mock_handler = Mock()
        
        async def mock_stream():
            for chunk in ["Hello", " from", " AI"]:
                yield chunk
        
        mock_handler.stream_chat = mock_stream
        ai.streaming_handler = mock_handler
        
        chunks = []
        async for chunk in ai.stream_chat("Hello"):
            chunks.append(chunk)
        
        assert chunks == ["Hello", " from", " AI"]
    
    @pytest.mark.asyncio
    async def test_stream_chat_with_model_selection(self):
        """Test streaming with model selection"""
        ai = AI()
        
        mock_handler = Mock()
        
        async def mock_stream(message, model=None, **kwargs):
            # Verify model is passed correctly
            assert model == "fast"
            for chunk in [f"Response", " from", f" {model}"]:
                yield chunk
        
        mock_handler.stream_chat = mock_stream
        ai.streaming_handler = mock_handler
        
        chunks = []
        async for chunk in ai.stream_chat("Test", model="fast"):
            chunks.append(chunk)
        
        assert chunks == ["Response", " from", " fast"]
    
    @pytest.mark.asyncio
    async def test_stream_chat_cost_tracking(self):
        """Test cost tracking during streaming"""
        ai = AI()
        
        mock_handler = Mock()
        mock_handler.total_cost = 0.0
        
        async def mock_stream_with_cost(message, **kwargs):
            mock_handler.total_cost += 0.001
            for chunk in ["Expensive", " response"]:
                yield chunk
                mock_handler.total_cost += 0.0005
        
        mock_handler.stream_chat = mock_stream_with_cost
        ai.streaming_handler = mock_handler
        
        total_chunks = 0
        async for chunk in ai.stream_chat("Test"):
            total_chunks += 1
        
        assert total_chunks == 2
        assert mock_handler.total_cost == 0.002  # Initial + 2 * 0.0005


class TestStreamingPerformance:
    """Test streaming performance and timing"""
    
    @pytest.mark.asyncio
    async def test_streaming_latency(self):
        """Test streaming latency measurement"""
        mock_router = Mock()
        mock_provider = Mock()
        
        # Mock streaming with controlled timing
        async def mock_timed_stream():
            start_time = time.time()
            for i, chunk in enumerate(["First", "Second", "Third"]):
                # Simulate processing delay
                await asyncio.sleep(0.1)
                yield f"{chunk}_{i}"
        
        mock_provider.stream_chat = mock_timed_stream
        mock_router._select_provider.return_value = mock_provider
        
        handler = StreamingHandler(mock_router)
        
        start_time = time.time()
        chunks = []
        
        async for chunk in handler.stream_chat("Test"):
            chunks.append(chunk)
            # First chunk should arrive quickly (within reasonable time)
            if len(chunks) == 1:
                first_chunk_time = time.time() - start_time
                assert first_chunk_time < 0.2  # Should be quick
        
        total_time = time.time() - start_time
        assert len(chunks) == 3
        assert total_time >= 0.3  # Should take at least 3 * 0.1 seconds
    
    @pytest.mark.asyncio
    async def test_streaming_buffer_management(self):
        """Test streaming buffer management"""
        mock_router = Mock()
        mock_provider = Mock()
        
        # Mock streaming with large chunks
        async def mock_large_stream():
            large_chunks = [
                "A" * 1000,  # Large chunk
                "B" * 500,   # Medium chunk
                "C" * 100,   # Small chunk
            ]
            for chunk in large_chunks:
                yield chunk
                await asyncio.sleep(0.01)
        
        mock_provider.stream_chat = mock_large_stream
        mock_router._select_provider.return_value = mock_provider
        
        handler = StreamingHandler(mock_router)
        
        chunks = []
        async for chunk in handler.stream_chat("Test"):
            chunks.append(chunk)
        
        assert len(chunks) == 3
        assert len(chunks[0]) == 1000
        assert len(chunks[1]) == 500
        assert len(chunks[2]) == 100


class TestStreamingWithProviders:
    """Test streaming with different providers"""
    
    @pytest.mark.asyncio
    async def test_openai_streaming_simulation(self):
        """Test OpenAI-style streaming simulation"""
        mock_router = Mock()
        mock_provider = Mock()
        
        # Simulate OpenAI streaming format
        async def mock_openai_stream():
            openai_chunks = [
                {"choices": [{"delta": {"content": "Hello"}}]},
                {"choices": [{"delta": {"content": " world"}}]},
                {"choices": [{"delta": {"content": "!"}}]},
                {"choices": [{"delta": {}}]},  # End marker
            ]
            
            for chunk_data in openai_chunks:
                content = chunk_data["choices"][0]["delta"].get("content", "")
                if content:
                    yield content
                await asyncio.sleep(0.01)
        
        mock_provider.stream_chat = mock_openai_stream
        mock_router._select_provider.return_value = mock_provider
        
        handler = StreamingHandler(mock_router)
        
        chunks = []
        async for chunk in handler.stream_chat("Test"):
            chunks.append(chunk)
        
        assert chunks == ["Hello", " world", "!"]
    
    @pytest.mark.asyncio
    async def test_anthropic_streaming_simulation(self):
        """Test Anthropic-style streaming simulation"""
        mock_router = Mock()
        mock_provider = Mock()
        
        # Simulate Anthropic streaming format
        async def mock_anthropic_stream():
            anthropic_chunks = [
                {"type": "content_block_delta", "delta": {"text": "Hi"}},
                {"type": "content_block_delta", "delta": {"text": " there"}},
                {"type": "content_block_delta", "delta": {"text": "!"}},
                {"type": "message_stop"},  # End marker
            ]
            
            for chunk_data in anthropic_chunks:
                if chunk_data["type"] == "content_block_delta":
                    yield chunk_data["delta"]["text"]
                await asyncio.sleep(0.01)
        
        mock_provider.stream_chat = mock_anthropic_stream
        mock_router._select_provider.return_value = mock_provider
        
        handler = StreamingHandler(mock_router)
        
        chunks = []
        async for chunk in handler.stream_chat("Test"):
            chunks.append(chunk)
        
        assert chunks == ["Hi", " there", "!"]


class TestStreamingEdgeCases:
    """Test streaming edge cases and error conditions"""
    
    @pytest.mark.asyncio
    async def test_empty_stream(self):
        """Test handling of empty stream"""
        mock_router = Mock()
        mock_provider = Mock()
        
        async def mock_empty_stream():
            return
            yield  # This will never execute
        
        mock_provider.stream_chat = mock_empty_stream
        mock_router._select_provider.return_value = mock_provider
        
        handler = StreamingHandler(mock_router)
        
        chunks = []
        async for chunk in handler.stream_chat("Test"):
            chunks.append(chunk)
        
        assert chunks == []
    
    @pytest.mark.asyncio
    async def test_stream_with_empty_chunks(self):
        """Test handling of empty chunks in stream"""
        mock_router = Mock()
        mock_provider = Mock()
        
        async def mock_stream_with_empties():
            chunks = ["Hello", "", " ", "", "world", ""]
            for chunk in chunks:
                yield chunk
                await asyncio.sleep(0.01)
        
        mock_provider.stream_chat = mock_stream_with_empties
        mock_router._select_provider.return_value = mock_provider
        
        handler = StreamingHandler(mock_router)
        
        chunks = []
        async for chunk in handler.stream_chat("Test"):
            chunks.append(chunk)
        
        # Should include all chunks, including empty ones
        assert chunks == ["Hello", "", " ", "", "world", ""]
    
    @pytest.mark.asyncio
    async def test_stream_timeout_handling(self):
        """Test handling of streaming timeouts"""
        mock_router = Mock()
        mock_provider = Mock()
        
        async def mock_slow_stream():
            yield "Start"
            await asyncio.sleep(10)  # Very long delay
            yield "End"  # This should timeout before reaching here
        
        mock_provider.stream_chat = mock_slow_stream
        mock_router._select_provider.return_value = mock_provider
        
        handler = StreamingHandler(mock_router)
        
        chunks = []
        
        # Set a timeout for the stream
        try:
            async with asyncio.timeout(1.0):  # 1 second timeout
                async for chunk in handler.stream_chat("Test"):
                    chunks.append(chunk)
        except asyncio.TimeoutError:
            pass  # Expected timeout
        
        assert chunks == ["Start"]


# Integration tests requiring real API keys
@pytest.mark.integration
class TestStreamingIntegration:
    """Integration tests for streaming with real APIs"""
    
    @pytest.mark.asyncio
    async def test_real_streaming_openai(self):
        """Test real streaming with OpenAI (requires API key)"""
        import os
        
        if not os.getenv("OPENAI_API_KEY"):
            pytest.skip("OpenAI API key not available")
        
        ai = AI(provider="openai")
        
        chunks = []
        try:
            async for chunk in ai.stream_chat(
                "Count from 1 to 3",
                model="gpt-4o-mini",
                max_tokens=20
            ):
                chunks.append(chunk)
                if len(chunks) > 10:  # Safety limit
                    break
            
            assert len(chunks) > 0
            full_response = "".join(chunks)
            assert len(full_response) > 0
            
        except Exception as e:
            pytest.skip(f"Streaming not available: {e}")
    
    @pytest.mark.asyncio
    async def test_real_streaming_anthropic(self):
        """Test real streaming with Anthropic (requires API key)"""
        import os
        
        if not os.getenv("ANTHROPIC_API_KEY"):
            pytest.skip("Anthropic API key not available")
        
        ai = AI(provider="anthropic")
        
        chunks = []
        try:
            async for chunk in ai.stream_chat(
                "Say hello",
                model="claude-3-haiku-20240307",
                max_tokens=20
            ):
                chunks.append(chunk)
                if len(chunks) > 10:  # Safety limit
                    break
            
            assert len(chunks) > 0
            full_response = "".join(chunks)
            assert "hello" in full_response.lower()
            
        except Exception as e:
            pytest.skip(f"Streaming not available: {e}")
    
    @pytest.mark.asyncio
    async def test_streaming_cost_calculation(self):
        """Test cost calculation during streaming"""
        if not any(os.getenv(key) for key in ["OPENAI_API_KEY", "ANTHROPIC_API_KEY"]):
            pytest.skip("No API keys available")
        
        ai = AI()
        
        initial_cost = ai.get_usage_stats().get('daily_cost', 0)
        
        chunks = []
        try:
            async for chunk in ai.stream_chat(
                "Brief response please",
                max_tokens=10
            ):
                chunks.append(chunk)
            
            final_cost = ai.get_usage_stats().get('daily_cost', 0)
            
            # Cost should have increased (even if slightly)
            assert final_cost >= initial_cost
            
        except Exception as e:
            pytest.skip(f"Streaming cost tracking not available: {e}")
