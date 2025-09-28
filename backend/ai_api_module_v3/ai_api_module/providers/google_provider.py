# ai_api_module/providers/google_provider.py
"""
Google Gemini provider implementation
"""
import base64
import asyncio
from typing import Dict, Any, List, Optional, AsyncGenerator
from pathlib import Path

from .base import BaseProvider
from ..core.response import AIResponse, Usage, Image, ToolCall
from ..core.exceptions import ProviderError, AuthenticationError, RateLimitError


class GoogleProvider(BaseProvider):
    """Google Gemini provider implementation"""
    
    def __init__(self, api_key: str, config: Dict[str, Any]):
        super().__init__(api_key, config)
        self._client = None
    
    @property
    def client(self):
        """Lazy load Google client"""
        if self._client is None:
            try:
                from google import genai
                self._client = genai.Client(api_key=self.api_key)
            except ImportError:
                raise ProviderError(
                    "Google GenAI package not installed. Run: pip install google-genai",
                    provider="google"
                )
        return self._client
    
    def chat(self, request_data: Dict[str, Any]) -> AIResponse:
        """Execute Google Gemini chat completion"""
        try:
            from google.genai import types

            contents = self._build_contents(request_data)
            config = self._build_config(request_data)

            native_files = request_data.get("native_files") or []
            request_kwargs = {
                "model": request_data["model"],
                "contents": contents,
                "config": config,
            }
            uploaded_any = False
            if native_files:
                blobs = []
                for path in native_files:
                    with open(path, "rb") as fh:
                        data = fh.read()
                    mime_type = self._guess_mime_type(path)
                    blobs.append(types.Part.from_bytes(data=data, mime_type=mime_type))
                if blobs:
                    request_kwargs["contents"].append(types.Content(role="user", parts=blobs))
                    uploaded_any = True

            response = self.client.models.generate_content(**request_kwargs)

            if uploaded_any:
                request_data["documents"] = []

            return self._parse_chat_response(response, request_data)

        except Exception as e:
            return self._handle_error(e)
    
    async def async_chat(self, request_data: Dict[str, Any]) -> AIResponse:
        """Execute async Google chat completion"""
        # Google GenAI doesn't have native async, so we'll run in executor
        return await asyncio.get_event_loop().run_in_executor(
            None, self.chat, request_data
        )
    
    async def stream_chat(self, request_data: Dict[str, Any]) -> AsyncGenerator[str, None]:
        """Stream Google chat completion"""
        try:
            from google.genai import types
            
            contents = self._build_contents(request_data)
            config = self._build_config(request_data)
            
            stream = self.client.models.generate_content_stream(
                model=request_data["model"],
                contents=contents,
                config=config
            )
            
            for chunk in stream:
                if hasattr(chunk, 'text') and chunk.text:
                    yield chunk.text
                    
        except Exception as e:
            yield f"Error: {str(e)}"
    
    def generate_image(self, request_data: Dict[str, Any]) -> AIResponse:
        """Generate image using Google Imagen"""
        try:
            # Map to Google image model
            model = request_data.get("model") or "gemini-2.5-flash-image-preview"

            response = self.client.models.generate_content(
                model=model,
                contents=[request_data["prompt"]]
            )

            # Extract images from candidates → content.parts[*].inline_data
            extracted_images: List[Image] = []

            def _append_image(blob, mime_type: str):
                fmt = "png"
                if mime_type and "/" in mime_type:
                    fmt = mime_type.split("/")[-1]
                # blob.data may be bytes or base64-encoded string
                data_attr = getattr(blob, "data", None)
                if isinstance(data_attr, (bytes, bytearray)):
                    data_bytes = bytes(data_attr)
                elif isinstance(data_attr, str):
                    import base64
                    data_bytes = base64.b64decode(data_attr)
                else:
                    # Fallback: try interpreting blob itself as bytes
                    data_bytes = bytes(data_attr or b"")
                if data_bytes:
                    extracted_images.append(Image(data=data_bytes, format=fmt))

            # Primary path
            if hasattr(response, "candidates") and response.candidates:
                for cand in response.candidates:
                    content = getattr(cand, "content", None)
                    if not content:
                        continue
                    parts = getattr(content, "parts", []) or []
                    for part in parts:
                        inline_data = getattr(part, "inline_data", None)
                        if inline_data is not None:
                            _append_image(inline_data, getattr(inline_data, "mime_type", "image/png"))

            # Fallback: some SDK versions may attach inline data on response.content.parts
            if not extracted_images and hasattr(response, "content"):
                content = getattr(response, "content", None)
                parts = getattr(content, "parts", []) or []
                for part in parts:
                    inline_data = getattr(part, "inline_data", None)
                    if inline_data is not None:
                        _append_image(inline_data, getattr(inline_data, "mime_type", "image/png"))

            return AIResponse(
                text=f"Generated image: {request_data['prompt']}",
                images=extracted_images,
                model=model,
                provider="google",
                cost=self._calculate_image_cost()
            )
            
        except Exception as e:
            return self._handle_error(e)
    
    def _build_contents(self, request_data: Dict[str, Any]) -> Any:
        """Build Google contents format"""
        from google.genai import types
        
        contents = []
        
        # Add text
        base_parts = []

        for ctx in request_data.get("context_messages") or []:
            base_parts.append(types.Part.from_text(text=ctx))

        if request_data.get("memory_snapshot"):
            memo_lines = ["[메모리 스냅샷]"]
            for key, value in request_data["memory_snapshot"].items():
                memo_lines.append(f"- {key}: {value}")
            base_parts.append(types.Part.from_text(text="\n".join(memo_lines)))

        for doc in request_data.get("documents") or []:
            base_parts.append(
                types.Part.from_text(text=f"[파일: {doc.get('name')}]\n{doc.get('text', '')}")
            )

        base_parts.append(types.Part.from_text(text=request_data["message"]))

        contents.append(
            types.Content(
                role='user',
                parts=base_parts
            )
        )
        
        # Add images
        if request_data.get("image"):
            image_part = self._process_image(request_data["image"])
            contents[-1].parts.append(image_part)
        
        if request_data.get("images"):
            for image in request_data["images"]:
                image_part = self._process_image(image)
                contents[-1].parts.append(image_part)
        
        return contents
    
    def _build_config(self, request_data: Dict[str, Any]) -> Any:
        """Build Google config"""
        from google.genai import types
        
        config_kwargs = {}

        system_instructions: List[str] = []
        if request_data.get("system"):
            system_instructions.append(request_data["system"])
        for msg in request_data.get("context_messages") or []:
            system_instructions.append(msg)
        if request_data.get("memory_snapshot"):
            memo_lines = ["[메모리 스냅샷]"]
            for key, value in request_data["memory_snapshot"].items():
                memo_lines.append(f"- {key}: {value}")
            system_instructions.append("\n".join(memo_lines))
        for doc in request_data.get("documents") or []:
            system_instructions.append(f"[파일: {doc.get('name')}]\n{doc.get('text', '')}")
        if system_instructions:
            config_kwargs["system_instruction"] = "\n\n".join(system_instructions)

        # Parameters
        if request_data.get("temperature") is not None:
            config_kwargs["temperature"] = float(request_data["temperature"])

        if request_data.get("max_tokens"):
            # Gemini uses max_output_tokens
            config_kwargs["max_output_tokens"] = int(request_data["max_tokens"])

        # Structured outputs
        if request_data.get("format") == "json":
            config_kwargs["response_mime_type"] = "application/json"
        elif request_data.get("format") == "json_schema" and request_data.get("response_schema"):
            config_kwargs["response_mime_type"] = "application/json"
            config_kwargs["response_schema"] = request_data["response_schema"]

        # Tools
        if request_data.get("tools"):
            config_kwargs["tools"] = self._build_tools(request_data["tools"])

        # Web search
        if request_data.get("web_search"):
            config_kwargs["tools"] = [types.Tool(google_search=types.GoogleSearch())]

        return types.GenerateContentConfig(**config_kwargs) if config_kwargs else None
    
    def _build_tools(self, tools: List[str]) -> List[Any]:
        """Build Google tools format"""
        from google.genai import types
        
        tool_definitions = []
        
        for tool_name in tools:
            if tool_name == "web_search":
                tool_definitions.append(types.Tool(google_search=types.GoogleSearch()))
            elif tool_name == "code_execution":
                tool_definitions.append(types.Tool(code_execution=types.ToolCodeExecution()))
        
        return tool_definitions
    
    def _process_image(self, image_input) -> Any:
        """Process image input for Google format"""
        from google.genai import types
        
        if isinstance(image_input, (str, Path)):
            image_path = Path(image_input)
            if image_path.exists():
                # Local file
                with open(image_path, "rb") as f:
                    image_data = f.read()
                
                mime_type = f"image/{image_path.suffix[1:]}"
                return types.Part.from_bytes(data=image_data, mime_type=mime_type)
            else:
                # URL
                return types.Part.from_uri(uri=str(image_input), mime_type="image/jpeg")
        
        return types.Part.from_text(text=str(image_input))

    def _guess_mime_type(self, path: str) -> str:
        suffix = Path(path).suffix.lower()
        mapping = {
            ".pdf": "application/pdf",
            ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ".doc": "application/msword",
            ".txt": "text/plain",
            ".md": "text/markdown",
        }
        return mapping.get(suffix, "application/octet-stream")
    
    def _parse_chat_response(self, response, request_data: Dict[str, Any]) -> AIResponse:
        """Parse Google chat response"""
        # Primary path
        text = getattr(response, 'text', '') or ''
        
        # Fallback: parse from candidates -> content.parts[*].text
        if not text and hasattr(response, 'candidates') and response.candidates:
            parts_text: List[str] = []
            try:
                for cand in response.candidates:
                    content = getattr(cand, 'content', None)
                    if not content:
                        continue
                    parts = getattr(content, 'parts', []) or []
                    for p in parts:
                        t = getattr(p, 'text', None)
                        if t:
                            parts_text.append(str(t))
                if parts_text:
                    text = "".join(parts_text)
            except Exception:
                pass
        
        # Extract tool calls
        tool_calls = []
        if hasattr(response, 'function_calls') and response.function_calls:
            for fc in response.function_calls:
                tool_calls.append(ToolCall(
                    name=fc.name,
                    arguments=dict(getattr(fc.function_call, 'args', {}) or {})
                ))
        
        # Usage (approximate)
        prompt_tokens = len(request_data["message"]) // 4  # Rough estimate
        completion_tokens = len(text) // 4
        usage = Usage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
        )
        
        cost = self._calculate_cost(request_data["model"], usage)
        
        structured_data = None
        if request_data.get("format") in {"json", "json_schema"}:
            try:
                import json
                structured_data = json.loads(text or "{}")
            except Exception:
                structured_data = None

        context_messages = request_data.get("context_messages") or []
        aggregated_text = "".join(context_messages + [text]) if context_messages else text

        return AIResponse(
            text=aggregated_text,
            tool_calls=tool_calls,
            model=request_data["model"],
            provider="google",
            usage=usage,
            cost=cost,
            structured_data=structured_data
        )
    
    def _calculate_cost(self, model: str, usage: Usage) -> float:
        """Calculate cost based on model and usage"""
        # Google pricing (per 1M tokens)
        pricing = {
            "gemini-2.5-pro": {"input": 1.25, "output": 10.00},
            "gemini-2.5-flash": {"input": 0.10, "output": 0.40},
            "gemini-1.5-pro": {"input": 1.25, "output": 5.00},
            "gemini-1.5-flash": {"input": 0.075, "output": 0.30},
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
    
    def _calculate_image_cost(self) -> float:
        """Calculate image generation cost"""
        return 0.05  # Placeholder
    
    def _handle_error(self, error: Exception) -> AIResponse:
        """Handle and convert errors"""
        error_msg = str(error)
        
        if "authentication" in error_msg.lower() or "api_key" in error_msg.lower():
            raise AuthenticationError(f"Google authentication failed: {error_msg}")
        elif "quota" in error_msg.lower() or "rate" in error_msg.lower():
            raise RateLimitError(f"Google rate limit exceeded: {error_msg}")
        else:
            raise ProviderError(f"Google error: {error_msg}", provider="google", original_error=error)
    
    def get_available_models(self) -> List[str]:
        """Get available Google models"""
        return [
            "gemini-2.5-pro", "gemini-2.5-flash", "gemini-2.5-flash-lite",
            "gemini-1.5-pro", "gemini-1.5-flash", "gemini-1.0-pro"
        ]