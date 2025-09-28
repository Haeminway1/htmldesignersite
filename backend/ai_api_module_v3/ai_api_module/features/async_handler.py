# ai_api_module/features/async_handler.py
"""
Async operations handler
"""
import asyncio
from typing import List, Dict, Any, Optional
from asyncio import Semaphore

from ..core.response import AIResponse
from ..core.exceptions import AIError


class AsyncHandler:
    """Handles async operations and batch processing"""
    
    def __init__(self, provider_router, ai_instance):
        self.provider_router = provider_router
        self.default_semaphore = Semaphore(5)  # Default concurrency limit
        self.ai = ai_instance
    
    async def chat(self, message: str, **kwargs) -> AIResponse:
        """Single async chat request"""
        try:
            request_data = self._build_request_data(message, **kwargs)
            provider = self.provider_router._select_provider(request_data)
            response = await provider.async_chat(request_data)
            return response
        except Exception as e:
            raise AIError(f"Async chat failed: {str(e)}")
    
    async def batch_chat(
        self, 
        messages: List[str], 
        max_concurrent: int = 5,
        **kwargs
    ) -> List[AIResponse]:
        """Process multiple messages concurrently"""
        semaphore = Semaphore(max_concurrent)
        
        async def process_message(msg: str) -> AIResponse:
            async with semaphore:
                return await self.chat(msg, **kwargs)
        
        tasks = [process_message(msg) for msg in messages]
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Convert exceptions to error responses
        result = []
        for i, response in enumerate(responses):
            if isinstance(response, Exception):
                result.append(AIResponse(
                    text=f"Error processing message {i}: {str(response)}",
                    cost=0.0
                ))
            else:
                result.append(response)
        
        return result
    
    async def parallel_providers(
        self,
        message: str,
        providers: List[str],
        **kwargs
    ) -> Dict[str, AIResponse]:
        """Send same message to multiple providers in parallel"""
        
        async def query_provider(provider: str) -> AIResponse:
            try:
                return await self.chat(message, provider=provider, **kwargs)
            except Exception as e:
                return AIResponse(
                    text=f"Error from {provider}: {str(e)}",
                    provider=provider,
                    cost=0.0
                )
        
        tasks = {
            provider: query_provider(provider) 
            for provider in providers
        }
        
        results = await asyncio.gather(*tasks.values())
        
        return dict(zip(tasks.keys(), results))
    
    def _build_request_data(self, message: str, **kwargs) -> Dict[str, Any]:
        """Build request data structure"""
        model = kwargs.get("model")
        provider = kwargs.get("provider")
        system = kwargs.get("system")
        temperature = kwargs.get("temperature")
        max_tokens = kwargs.get("max_tokens")

        final_model = model or self.ai.config.default_model
        resolved_model, resolved_provider = self.ai.model_registry.resolve(final_model, provider)

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
                system=system,
                temperature=temperature,
                max_tokens=self.ai._normalize_max_tokens(max_tokens, resolved_model),
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

        return request_data
