# ai_api_module/providers/anthropic_provider.py
"""
Anthropic Claude provider implementation
"""
import base64
import asyncio
from typing import Dict, Any, List, Optional, AsyncGenerator
from pathlib import Path

from .base import BaseProvider
from ..core.response import AIResponse, Usage, Image, ToolCall
from ..core.exceptions import ProviderError, AuthenticationError, RateLimitError

# Optional module import for patching in tests
try:
    import anthropic  # type: ignore  # noqa: F401
except Exception:  # pragma: no cover
    anthropic = None  # type: ignore

class AnthropicProvider(BaseProvider):
    """Anthropic Claude provider implementation"""
    
    def __init__(self, api_key: str, config: Dict[str, Any]):
        super().__init__(api_key, config)
        self._client = None
        self._async_client = None
    
    @property
    def client(self):
        """Lazy load Anthropic client"""
        if self._client is None:
            try:
                if anthropic is None:
                    raise ImportError("anthropic client unavailable")
                self._client = anthropic.Anthropic(api_key=self.api_key)
            except ImportError:
                raise ProviderError(
                    "Anthropic package not installed. Run: pip install anthropic",
                    provider="anthropic"
                )
        return self._client
    
    @property 
    def async_client(self):
        """Lazy load async Anthropic client"""
        if self._async_client is None:
            try:
                if anthropic is None:
                    raise ImportError("anthropic async client unavailable")
                self._async_client = anthropic.AsyncAnthropic(api_key=self.api_key)
            except ImportError:
                raise ProviderError(
                    "Anthropic package not installed. Run: pip install anthropic",
                    provider="anthropic"
                )
        return self._async_client
    
    def chat(self, request_data: Dict[str, Any]) -> AIResponse:
        """Execute Anthropic chat completion"""
        try:
            # Build messages and system prompt
            messages = self._build_messages(request_data)
            system = request_data.get("system", "")
            
            # Build parameters
            params = self._build_chat_params(request_data, messages, system)
            
            # Execute request
            response = self.client.messages.create(**params)
            
            # Parse response
            return self._parse_chat_response(response, request_data)
            
        except Exception as e:
            return self._handle_error(e)
    
    async def async_chat(self, request_data: Dict[str, Any]) -> AIResponse:
        """Execute async Anthropic chat completion"""
        try:
            messages = self._build_messages(request_data)
            system = request_data.get("system", "")
            params = self._build_chat_params(request_data, messages, system)
            
            response = await self.async_client.messages.create(**params)
            return self._parse_chat_response(response, request_data)
            
        except Exception as e:
            return self._handle_error(e)
    
    async def stream_chat(self, request_data: Dict[str, Any]) -> AsyncGenerator[str, None]:
        """Stream Anthropic chat completion"""
        try:
            messages = self._build_messages(request_data)
            system = request_data.get("system", "")
            params = self._build_chat_params(request_data, messages, system)
            
            async with self.async_client.messages.stream(**params) as stream:
                async for text in stream.text_stream:
                    yield text
                    
        except Exception as e:
            yield f"Error: {str(e)}"
    
    def _build_messages(self, request_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Build Anthropic messages format"""
        messages = []
        
        # Build content array for multimodal
        content = []

        for ctx in request_data.get("context_messages") or []:
            content.append({"type": "text", "text": ctx})

        # Add documents as text fallback (Anthropic doesn't support binary upload today)
        for doc in request_data.get("documents") or []:
            content.append({
                "type": "text",
                "text": doc.get('text', '')
            })

        # Add text
        user_message = request_data["message"]
        if request_data.get("format") in {"json", "json_schema"}:
            user_message = (
                f"{user_message}\n\n위 요구사항에 대해 JSON 포맷으로만 답변해."
            )

        content.append({
            "type": "text",
            "text": user_message
        })
        
        # Add images
        if request_data.get("image"):
            image_data = self._process_image(request_data["image"])
            content.append(image_data)
        
        if request_data.get("images"):
            for image in request_data["images"]:
                image_data = self._process_image(image)
                content.append(image_data)
        
        messages.append({
            "role": "user",
            "content": content if len(content) > 1 else user_message
        })
        
        return messages
    
    def _build_chat_params(
        self, 
        request_data: Dict[str, Any], 
        messages: List[Dict[str, Any]], 
        system: str
    ) -> Dict[str, Any]:
        """Build Anthropic chat parameters"""
        model = self._normalize_model_id(request_data["model"]) 
        params = {
            "model": model,
            "messages": messages,
            # Anthropic expects max_tokens for output; map from normalized value
            "max_tokens": int(request_data.get("max_tokens", 1000)),
        }
        
        if system:
            params["system"] = system
        
        if request_data.get("temperature") is not None:
            params["temperature"] = request_data["temperature"]
        
        if request_data.get("tools"):
            params["tools"] = self._build_tools(request_data["tools"])

        if request_data.get("format") in {"json", "json_schema"}:
            self._apply_json_constraints(params, request_data)

        extra_context = self._compose_context_block(request_data)
        if extra_context:
            params.setdefault("system", "")
            params["system"] = (params["system"] + "\n" + extra_context).strip()

        return params

    def _apply_json_constraints(self, params: Dict[str, Any], request_data: Dict[str, Any]) -> None:
        """Inject instructions so Claude reliably returns JSON."""
        format_hint = request_data.get("format")
        if not format_hint:
            return

        # Anthropic SDK currently rejects 'response_format'; ensure we never send it.
        params.pop("response_format", None)

        instruction_lines: List[str] = [
            "너는 반드시 유효한 JSON 객체만으로 답변해야 해."
        ]

        schema = request_data.get("response_schema")
        if format_hint == "json_schema" and schema:
            try:
                import json

                schema_text = json.dumps(schema, ensure_ascii=False)
            except Exception:
                schema_text = None

            if schema_text:
                instruction_lines.append("다음 JSON 스키마를 충족해야 해:")
                instruction_lines.append(schema_text)
        elif format_hint == "json":
            if schema and schema.get("properties"):
                keys = ", ".join(sorted(schema["properties"].keys()))
                instruction_lines.append(f"가능하면 다음 키를 포함해: {keys}")

        json_instruction = "\n".join(instruction_lines)

        existing_system = params.get("system") or ""
        if existing_system:
            params["system"] = f"{existing_system}\n\n{json_instruction}".strip()
        else:
            params["system"] = json_instruction

    def _normalize_model_id(self, model: str) -> str:
        """Map legacy/alias Anthropic model IDs to current supported ones."""
        m = model.lower()
        # Respect explicit '-latest' aliases if SDK supports them (e.g., 3-7, 3-5)
        if "-latest" in m:
            return model
        # Common legacy → stable mappings
        mapping = {
            "claude-sonnet-4": "claude-3-7-sonnet-20250219",
            "claude-3-7-sonnet": "claude-3-7-sonnet-20250219",
            "claude-3-5-sonnet": "claude-3-5-sonnet-20241022",
            "claude-3-5-haiku": "claude-3-5-haiku-20241022",
            "claude-3-haiku": "claude-3-haiku-20240307",
            # Keep explicit 4-1 / 4-0 as-is per user guidance
            # Map ambiguous 'claude-opus-4' to a stable snapshot
            "claude-opus-4": "claude-opus-4-20250514",
        }
        for k, v in mapping.items():
            if k in m:
                return v
        return model
    
    def _build_tools(self, tools: List[str]) -> List[Dict[str, Any]]:
        """Build Anthropic tools format"""
        tool_definitions = []
        
        for tool_name in tools:
            if tool_name == "web_search":
                tool_definitions.append({
                    "name": "web_search",
                    "description": "Search the web for current information",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string"},
                            "max_results": {"type": "integer"}
                        },
                        "required": ["query"]
                    }
                })
        
        return tool_definitions
    
    def _parse_chat_response(self, response, request_data: Dict[str, Any]) -> AIResponse:
        """Parse Anthropic chat response"""
        # Extract text content
        text_content = ""
        tool_calls = []
        
        for content in response.content:
            if content.type == "text":
                text_content += content.text
            elif content.type == "tool_use":
                tool_calls.append(ToolCall(
                    name=content.name,
                    arguments=content.input
                ))
        
        # Calculate usage and cost
        usage = Usage(
            prompt_tokens=response.usage.input_tokens,
            completion_tokens=response.usage.output_tokens,
            total_tokens=response.usage.input_tokens + response.usage.output_tokens
        )
        
        cost = self._calculate_cost(request_data["model"], usage)
        structured_data = None
        if request_data.get("format") in {"json", "json_schema"}:
            try:
                import json

                structured_data = json.loads(text_content or "{}")
            except Exception:
                structured_data = None

        context_messages = request_data.get("context_messages") or []
        aggregated_text = "".join(context_messages + [text_content]) if context_messages else text_content

        text_output = text_content
        if request_data.get("format") in {"json", "json_schema"} and structured_data is not None:
            import json

            text_output = json.dumps(structured_data, ensure_ascii=False)

        return AIResponse(
            text=text_output,
            tool_calls=tool_calls,
            model=request_data["model"],
            provider="anthropic",
            usage=usage,
            cost=cost,
            structured_data=structured_data
        )

    def _compose_context_block(self, request_data: Dict[str, Any]) -> str:
        blocks = []
        for msg in request_data.get("context_messages") or []:
            blocks.append(msg)

        if request_data.get("memory_snapshot"):
            memo_lines = ["[메모리 스냅샷]"]
            for key, value in request_data["memory_snapshot"].items():
                memo_lines.append(f"- {key}: {value}")
            blocks.append("\n".join(memo_lines))

        if request_data.get("documents"):
            for doc in request_data["documents"]:
                header = doc.get("name")
                text = doc.get("text", "")
                blocks.append(f"[파일: {header}]\n{text}")

        return "\n\n".join(blocks)
    
    def _process_image(self, image_input) -> Dict[str, Any]:
        """Process image input for Anthropic format"""
        if isinstance(image_input, (str, Path)):
            image_path = Path(image_input)
            if image_path.exists():
                # Local file - convert to base64
                with open(image_path, "rb") as f:
                    image_data = base64.b64encode(f.read()).decode()
                
                # Determine media type
                suffix = image_path.suffix.lower()
                media_type = f"image/{suffix[1:]}" if suffix in ['.jpg', '.jpeg', '.png', '.gif', '.webp'] else "image/jpeg"
                
                return {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": media_type,
                        "data": image_data
                    }
                }
        
        # Assume it's a URL or base64 string
        return {
            "type": "image",
            "source": {
                "type": "url", 
                "url": str(image_input)
            }
        }
    
    def _calculate_cost(self, model: str, usage: Usage) -> float:
        """Calculate cost based on model and usage"""
        # Anthropic pricing (per 1M tokens)
        pricing = {
            "claude-opus-4-1": {"input": 15.00, "output": 75.00},
            "claude-opus-4": {"input": 15.00, "output": 75.00},
            "claude-sonnet-4": {"input": 3.00, "output": 15.00},
            "claude-3-7-sonnet": {"input": 3.00, "output": 15.00},
            "claude-3-5-sonnet": {"input": 3.00, "output": 15.00},
            "claude-3-5-haiku": {"input": 0.80, "output": 4.00},
            "claude-3-haiku": {"input": 0.25, "output": 1.25},
        }
        
        # Find closest match
        model_key = None
        for key in pricing.keys():
            if key in model:
                model_key = key
                break
        
        if not model_key:
            return 0.0
        
        input_cost = (usage.prompt_tokens / 1000000) * pricing[model_key]["input"]
        output_cost = (usage.completion_tokens / 1000000) * pricing[model_key]["output"]
        
        return input_cost + output_cost
    
    def _handle_error(self, error: Exception) -> AIResponse:
        """Handle and convert errors"""
        error_msg = str(error)
        
        if "authentication" in error_msg.lower():
            raise AuthenticationError(f"Anthropic authentication failed: {error_msg}")
        elif "rate_limit" in error_msg.lower():
            raise RateLimitError(f"Anthropic rate limit exceeded: {error_msg}")
        else:
            raise ProviderError(f"Anthropic error: {error_msg}", provider="anthropic", original_error=error)
    
    def get_available_models(self) -> List[str]:
        """Get available Anthropic models"""
        return [
            "claude-opus-4-1", "claude-opus-4", "claude-sonnet-4",
            "claude-3-7-sonnet", "claude-3-5-sonnet-latest", 
            "claude-3-5-haiku-latest", "claude-3-haiku"
        ]