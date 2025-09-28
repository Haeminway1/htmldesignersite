# ai_api_module/providers/xai_provider.py
"""
xAI Grok provider implementation
"""
import asyncio
import base64
import mimetypes
from typing import Dict, Any, List, Optional, AsyncGenerator
from pathlib import Path

from .base import BaseProvider
from ..core.response import AIResponse, Usage, Image
from ..core.exceptions import ProviderError, AuthenticationError, RateLimitError


class XAIProvider(BaseProvider):
    """xAI Grok provider implementation"""
    
    def __init__(self, api_key: str, config: Dict[str, Any]):
        super().__init__(api_key, config)
        self._client = None
        self._async_client = None
    
    @property
    def client(self):
        """Lazy load xAI client"""
        if self._client is None:
            try:
                from xai_sdk import Client
                self._client = Client(api_key=self.api_key)
            except ImportError:
                raise ProviderError(
                    "xAI SDK not installed. Run: pip install xai-sdk",
                    provider="xai"
                )
        return self._client
    
    @property
    def async_client(self):
        """Lazy load async xAI client"""
        if self._async_client is None:
            try:
                from xai_sdk import AsyncClient
                self._async_client = AsyncClient(api_key=self.api_key)
            except ImportError:
                raise ProviderError(
                    "xAI SDK not installed. Run: pip install xai-sdk",
                    provider="xai"
                )
        return self._async_client
    
    def chat(self, request_data: Dict[str, Any]) -> AIResponse:
        """Execute xAI chat completion"""
        try:
            from xai_sdk.chat import user, system
            
            # Create chat
            chat = self.client.chat.create(
                model=request_data["model"],
                max_tokens=int(request_data.get("max_tokens", 2000))
            )
            
            # Add system message
            if request_data.get("system"):
                chat.append(system(request_data["system"]))

            for ctx in request_data.get("context_messages") or []:
                chat.append(system(ctx))

            if request_data.get("memory_snapshot"):
                memo_lines = ["[메모리 스냅샷]"]
                for key, value in request_data["memory_snapshot"].items():
                    memo_lines.append(f"- {key}: {value}")
                chat.append(system("\n".join(memo_lines)))

            for doc in request_data.get("documents") or []:
                chat.append(system(doc.get('text', '')))

            chat.append(self._build_user_message(request_data))
            
            # Configure search if needed
            if request_data.get("web_search"):
                from xai_sdk.search import SearchParameters, web_source
                search_params = SearchParameters(
                    mode="auto",
                    sources=[web_source()],
                    max_search_results=10
                )
                chat.search_parameters = search_params
            
            # Execute
            response = chat.sample()
            
            # Parse response
            return self._parse_chat_response(response, request_data)
            
        except Exception as e:
            return self._handle_error(e)
    
    async def async_chat(self, request_data: Dict[str, Any]) -> AIResponse:
        """Execute async xAI chat completion"""
        try:
            from xai_sdk.chat import user, system
            
            chat = self.async_client.chat.create(
                model=request_data["model"],
                max_tokens=int(request_data.get("max_tokens", 2000))
            )
            
            if request_data.get("system"):
                chat.append(system(request_data["system"]))

            for ctx in request_data.get("context_messages") or []:
                chat.append(system(ctx))

            if request_data.get("memory_snapshot"):
                memo_lines = ["[메모리 스냅샷]"]
                for key, value in request_data["memory_snapshot"].items():
                    memo_lines.append(f"- {key}: {value}")
                chat.append(system("\n".join(memo_lines)))

            for doc in request_data.get("documents") or []:
                chat.append(system(doc.get('text', '')))

            chat.append(self._build_user_message(request_data))
            
            response = await chat.sample()
            return self._parse_chat_response(response, request_data)
            
        except Exception as e:
            return self._handle_error(e)
    
    async def stream_chat(self, request_data: Dict[str, Any]) -> AsyncGenerator[str, None]:
        """Stream xAI chat completion"""
        try:
            from xai_sdk.chat import user, system
            
            chat = self.async_client.chat.create(model=request_data["model"])
            
            if request_data.get("system"):
                chat.append(system(request_data["system"]))
            
            chat.append(self._build_user_message(request_data))
            
            async for chunk in chat.stream():
                if hasattr(chunk, 'content') and chunk.content:
                    yield chunk.content
                    
        except Exception as e:
            yield f"Error: {str(e)}"
    
    def generate_image(self, request_data: Dict[str, Any]) -> AIResponse:
        """Generate image using xAI"""
        try:
            # xAI image generation
            img = self.client.image.sample(
                model="grok-2-image-1212",
                prompt=request_data["prompt"],
                image_format="url"
            )
            
            # Create Image object
            data_bytes = b""
            try:
                import httpx
                r = httpx.get(img.url, timeout=60)
                r.raise_for_status()
                data_bytes = r.content
            except Exception:
                data_bytes = b""

            image = Image(
                data=data_bytes,
                format="jpg",
                url=getattr(img, "url", None)
            )
            
            return AIResponse(
                text=f"Generated image: {request_data['prompt']}",
                images=[image],
                model="grok-2-image-1212",
                provider="xai",
                cost=0.07  # xAI image cost
            )
            
        except Exception as e:
            return self._handle_error(e)
    
    def _parse_chat_response(self, response, request_data: Dict[str, Any]) -> AIResponse:
        """Parse xAI chat response"""
        text = getattr(response, 'content', '') or ''
        
        # Usage
        usage = Usage(
            prompt_tokens=getattr(response.usage, 'prompt_tokens', 0),
            completion_tokens=getattr(response.usage, 'completion_tokens', 0),
            reasoning_tokens=getattr(response.usage, 'reasoning_tokens', 0)
        )
        
        cost = self._calculate_cost(request_data["model"], usage)
        
        # Citations
        citations = []
        if hasattr(response, 'citations') and response.citations:
            citations = [{"url": c.url, "title": c.title} for c in response.citations]
        
        structured_data = None
        if request_data.get("format") in {"json", "json_schema"}:
            try:
                import json

                structured_data = json.loads(text or "{}")
            except Exception:
                structured_data = None

        return AIResponse(
            text=text,
            model=request_data["model"],
            provider="xai",
            usage=usage,
            cost=cost,
            citations=citations,
            reasoning=getattr(response, 'reasoning_content', None),
            structured_data=structured_data
        )

    def _build_user_message(self, request_data: Dict[str, Any]):
        """Create user message with optional image attachments for xAI chat."""
        from xai_sdk.chat import user, image as image_part

        message_text = request_data.get("message", "")
        image_refs = list(request_data.get("images") or [])

        single_image = request_data.get("image")
        if single_image:
            image_refs.insert(0, single_image)

        parts = []
        for img in image_refs:
            part = self._build_image_part(img, image_part)
            if part is not None:
                parts.append(part)

        if parts:
            return user(message_text, *parts)
        return user(message_text)

    def _build_image_part(self, image_ref: str, image_part_callable):
        """Convert image reference into an xAI image part."""
        if not image_ref:
            return None

        ref_str = str(image_ref)
        if ref_str.startswith(("http://", "https://", "data:")):
            if ref_str.lower().endswith(".png") and "data:image" not in ref_str:
                return image_part_callable(image_url=f"file://{ref_str}", detail="high")
            return image_part_callable(image_url=ref_str, detail="high")

        try:
            path = Path(ref_str)
            if path.exists() and path.is_file():
                mime_type, _ = mimetypes.guess_type(str(path))
                mime_type = mime_type or "image/png"
                data = path.read_bytes()
                encoded = base64.b64encode(data).decode("utf-8")
                data_url = f"data:{mime_type};base64,{encoded}"
                return image_part_callable(image_url=data_url, detail="high")
        except Exception:
            pass

        # Fallback: treat as URL without verification
        return image_part_callable(image_url=ref_str, detail="high")
    
    def _calculate_cost(self, model: str, usage: Usage) -> float:
        """Calculate cost based on model and usage"""
        # xAI pricing (per 1M tokens)
        pricing = {
            "grok-4": {"input": 3.00, "output": 15.00},
            "grok-3": {"input": 3.00, "output": 15.00},
            "grok-3-mini": {"input": 0.30, "output": 0.50},
            "grok-code-fast-1": {"input": 0.20, "output": 1.50},
        }
        
        model_key = None
        for key in pricing.keys():
            if key in model:
                model_key = key
                break
        
        if not model_key:
            return 0.0
        
        input_cost = (usage.prompt_tokens / 1000000) * pricing[model_key]["input"]
        output_cost = ((usage.completion_tokens + usage.reasoning_tokens) / 1000000) * pricing[model_key]["output"]
        
        return input_cost + output_cost
    
    def _handle_error(self, error: Exception) -> AIResponse:
        """Handle and convert errors"""
        error_msg = str(error)
        
        if "authentication" in error_msg.lower():
            raise AuthenticationError(f"xAI authentication failed: {error_msg}")
        elif "rate_limit" in error_msg.lower():
            raise RateLimitError(f"xAI rate limit exceeded: {error_msg}")
        else:
            raise ProviderError(f"xAI error: {error_msg}", provider="xai", original_error=error)
    
    def get_available_models(self) -> List[str]:
        """Get available xAI models"""
        return [
            "grok-4", "grok-3", "grok-3-mini", "grok-code-fast-1",
            "grok-2-image-1212"
        ]