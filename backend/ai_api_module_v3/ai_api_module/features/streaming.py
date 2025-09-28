# ai_api_module/features/streaming.py
"""
Streaming response handler
"""
import asyncio
from typing import AsyncGenerator, Callable, Optional, Dict, Any

from ..core.response import AIResponse


class StreamingHandler:
    """Handles streaming responses"""

    def __init__(self, provider_router, ai_instance):
        self.provider_router = provider_router
        self.ai = ai_instance

    async def stream(self, request_data: Dict[str, Any]) -> AsyncGenerator[str, None]:
        """Stream chat response"""
        try:
            provider = self.provider_router._select_provider(request_data)

            async for chunk in provider.stream_chat(request_data):
                yield chunk

        except Exception as e:
            yield f"Error: {str(e)}"

    async def stream_with_callbacks(
        self,
        message: str,
        on_chunk: Optional[Callable[[str], None]] = None,
        on_complete: Optional[Callable[[AIResponse], None]] = None,
        **kwargs
    ) -> AsyncGenerator[str, None]:
        """Stream with callback functions"""

        final_model = kwargs.get("model") or self.ai.config.default_model
        resolved_model, resolved_provider = self.ai.model_registry.resolve(final_model, kwargs.get("provider"))

        memory_snapshot = self.ai._build_memory_snapshot() if kwargs.get("use_memory") else None
        extras = {
            k: v for k, v in kwargs.items() if k not in {
                "model", "provider", "system", "temperature", "max_tokens",
                "tools", "image", "images", "files", "history", "web_search",
                "format", "conversation_id", "use_memory", "reasoning_effort"
            }
        }

        self.ai._pending_model_name = resolved_model
        try:
            request_data = self.ai._build_request(
                message=message,
                model=resolved_model,
                provider=resolved_provider,
                system=kwargs.get("system"),
                temperature=kwargs.get("temperature"),
                max_tokens=self.ai._normalize_max_tokens(kwargs.get("max_tokens"), resolved_model),
                reasoning_effort=kwargs.get("reasoning_effort"),
                tools=self.ai._normalize_tools(kwargs.get("tools")),
                image=kwargs.get("image"),
                images=kwargs.get("images"),
                files=kwargs.get("files"),
                history=kwargs.get("history"),
                web_search=kwargs.get("web_search", False),
                format=kwargs.get("format"),
                conversation_id=kwargs.get("conversation_id"),
                use_memory=kwargs.get("use_memory", False),
                memory_snapshot=memory_snapshot,
                **extras
            )
        finally:
            self.ai._pending_model_name = None

        request_data["stream"] = True

        full_response = ""

        try:
            async for chunk in self.stream(request_data):
                full_response += chunk

                if on_chunk:
                    on_chunk(chunk)

                yield chunk

            if on_complete:
                final_response = AIResponse(
                    text=full_response,
                    model=request_data.get("model", ""),
                    provider=request_data.get("provider", ""),
                    cost=0.0
                )
                on_complete(final_response)

        except Exception as e:
            error_chunk = f"Error: {str(e)}"
            if on_chunk:
                on_chunk(error_chunk)
            yield error_chunk