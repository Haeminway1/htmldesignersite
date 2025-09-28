# ai_api_module/providers/openai_provider.py
"""
OpenAI provider implementation
"""
import base64
import asyncio
from typing import Dict, Any, List, Optional, AsyncGenerator
from pathlib import Path

from .base import BaseProvider
from ..core.response import AIResponse, Usage, Image, Audio, ToolCall
from ..core.exceptions import ProviderError, AuthenticationError, RateLimitError
from ..utils.file_utils import load_file, get_file_type
from ..utils.image_utils import process_image

# Optional imports for easier testing/patching (expose names for tests)
try:
    from openai import OpenAI  # noqa: F401
    from openai import AsyncOpenAI  # noqa: F401
except Exception:  # pragma: no cover - allow tests to patch symbols
    OpenAI = None  # type: ignore
    AsyncOpenAI = None  # type: ignore

class OpenAIProvider(BaseProvider):
    """OpenAI provider implementation"""
    
    def __init__(self, api_key: str, config: Dict[str, Any]):
        super().__init__(api_key, config)
        self._client = None
        self._async_client = None
        
    @property
    def client(self):
        """Lazy load OpenAI client"""
        if self._client is None:
            try:
                if OpenAI is None:
                    raise ImportError("openai client unavailable")
                self._client = OpenAI(api_key=self.api_key)
            except ImportError:
                raise ProviderError(
                    "OpenAI package not installed. Run: pip install openai",
                    provider="openai"
                )
        return self._client
    
    @property
    def async_client(self):
        """Lazy load async OpenAI client"""
        if self._async_client is None:
            try:
                if AsyncOpenAI is None:
                    raise ImportError("openai async client unavailable")
                self._async_client = AsyncOpenAI(api_key=self.api_key)
            except ImportError:
                raise ProviderError(
                    "OpenAI package not installed. Run: pip install openai",
                    provider="openai"
                )
        return self._async_client
    
    def chat(self, request_data: Dict[str, Any]) -> AIResponse:
        """Execute OpenAI chat completion"""
        try:
            # Build messages
            messages = self._build_messages(request_data)
            
            # Build parameters
            params = self._build_chat_params(request_data, messages)
            
            # Execute request
            response = self.client.chat.completions.create(**params)
            
            # Parse response
            return self._parse_chat_response(response, request_data)
            
        except Exception as e:
            return self._handle_error(e)
    
    async def async_chat(self, request_data: Dict[str, Any]) -> AIResponse:
        """Execute async OpenAI chat completion"""
        try:
            messages = self._build_messages(request_data)
            params = self._build_chat_params(request_data, messages)
            
            response = await self.async_client.chat.completions.create(**params)
            return self._parse_chat_response(response, request_data)
            
        except Exception as e:
            return self._handle_error(e)
    
    async def stream_chat(self, request_data: Dict[str, Any]) -> AsyncGenerator[str, None]:
        """Stream OpenAI chat completion"""
        try:
            messages = self._build_messages(request_data)
            params = self._build_chat_params(request_data, messages)
            params["stream"] = True
            
            stream = await self.async_client.chat.completions.create(**params)
            
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            yield f"Error: {str(e)}"
    
    def generate_image(self, request_data: Dict[str, Any]) -> AIResponse:
        """Generate image using OpenAI DALL-E"""
        try:
            # Determine model
            model = request_data.get("model", "dall-e-3")
            if "gpt-image" in model:
                model = "dall-e-3"  # Map to actual OpenAI model
            
            # Build parameters
            params = {
                "model": model,
                "prompt": request_data["prompt"],
                "size": request_data.get("size", "1024x1024"),
                "quality": request_data.get("quality", "standard"),
                "n": 1,
                "response_format": "b64_json"
            }
            
            response = self.client.images.generate(**params)
            
            # Parse response
            image_data = base64.b64decode(response.data[0].b64_json)
            image = Image(
                data=image_data,
                format="png",
                width=int(params["size"].split("x")[0]),
                height=int(params["size"].split("x")[1])
            )
            
            # Calculate cost
            cost = self._calculate_image_cost(model, params["size"], params["quality"])
            
            return AIResponse(
                text=f"Generated image: {request_data['prompt']}",
                images=[image],
                model=model,
                provider="openai",
                cost=cost
            )
            
        except Exception as e:
            return self._handle_error(e)
    
    def transcribe_audio(self, request_data: Dict[str, Any]) -> AIResponse:
        """Transcribe audio using OpenAI Whisper"""
        try:
            audio_path = request_data["audio_path"]
            
            with open(audio_path, "rb") as audio_file:
                response = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
            
            return AIResponse(
                text=response,
                model="whisper-1",
                provider="openai",
                cost=self._calculate_audio_cost(audio_path)
            )
            
        except Exception as e:
            return self._handle_error(e)
    
    def text_to_speech(self, request_data: Dict[str, Any]) -> AIResponse:
        """Convert text to speech using OpenAI TTS"""
        try:
            response = self.client.audio.speech.create(
                model="tts-1",
                voice=request_data.get("voice", "alloy"),
                input=request_data["text"],
                response_format=request_data.get("output_format", "mp3"),
                speed=request_data.get("speed", 1.0)
            )
            
            audio = Audio(
                data=response.content,
                format=request_data.get("output_format", "mp3")
            )
            
            return AIResponse(
                text=f"Generated speech for: {request_data['text'][:50]}...",
                audio=audio,
                model="tts-1",
                provider="openai",
                cost=self._calculate_tts_cost(request_data["text"])
            )
            
        except Exception as e:
            return self._handle_error(e)
    
    def _build_messages(self, request_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Build OpenAI messages format"""
        messages = []
        
        # System message
        if request_data.get("system"):
            messages.append({
                "role": "system",
                "content": request_data["system"]
            })
        
        # Main message with potential multimodal content
        content = []

        # Include context messages as separate text parts before primary message
        for ctx in request_data.get("context_messages") or []:
            content.append({"type": "text", "text": ctx})

        if request_data.get("memory_snapshot"):
            memo_lines = ["[메모리 스냅샷]"]
            for key, value in request_data["memory_snapshot"].items():
                memo_lines.append(f"- {key}: {value}")
            content.append({"type": "text", "text": "\n".join(memo_lines)})

        for doc in request_data.get("documents") or []:
            content.append({
                "type": "text",
                "text": doc.get('text', '')
            })

        # Add user text
        content.append({
            "type": "text",
            "text": request_data["message"]
        })
        
        # Add images
        if request_data.get("image"):
            image_data = self._process_image(request_data["image"])
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": image_data,
                    "detail": "auto"
                }
            })
        
        if request_data.get("images"):
            for image in request_data["images"]:
                image_data = self._process_image(image)
                content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": image_data,
                        "detail": "auto"
                    }
                })
        
        messages.append({
            "role": "user",
            "content": content if len(content) > 1 else request_data["message"]
        })
        
        return messages
    
    def _build_chat_params(self, request_data: Dict[str, Any], messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Build OpenAI chat parameters"""
        params = {
            "model": request_data["model"],
            "messages": messages,
        }
        
        # Optional parameters
        if request_data.get("temperature") is not None:
            params["temperature"] = request_data["temperature"]

        if request_data.get("max_tokens") is not None:
            # For reasoning models (e.g., gpt-5, o3-*), OpenAI expects max_completion_tokens
            if self._requires_max_completion_tokens(request_data["model"]):
                params["max_completion_tokens"] = int(request_data["max_tokens"])
            else:
                params["max_tokens"] = int(request_data["max_tokens"])

        if request_data.get("tools"):
            params["tools"] = self._build_tools(request_data["tools"])

        if request_data.get("format") == "json":
            params["response_format"] = {"type": "json_object"}
        elif request_data.get("format") == "json_schema" and request_data.get("response_schema"):
            params["response_format"] = {
                "type": "json_schema",
                "json_schema": {
                    "name": request_data.get("response_schema_name", "structured_response"),
                    "schema": request_data["response_schema"],
                },
            }
        
        return params

    def _requires_max_completion_tokens(self, model: str) -> bool:
        """Heuristic to detect reasoning models requiring max_completion_tokens."""
        m = model.lower()
        return ("gpt-5" in m) or ("o3" in m) or ("deep-research" in m)
    
    def _build_tools(self, tools: List[str]) -> List[Dict[str, Any]]:
        """Build OpenAI tools format"""
        tool_definitions = []
        
        for tool_name in tools:
            if tool_name == "web_search":
                tool_definitions.append({
                    "type": "function",
                    "function": {
                        "name": "web_search",
                        "description": "Search the web for current information",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "query": {"type": "string"},
                                "max_results": {"type": "integer"}
                            },
                            "required": ["query"]
                        }
                    }
                })
        
        return tool_definitions
    
    def _parse_chat_response(self, response, request_data: Dict[str, Any]) -> AIResponse:
        """Parse OpenAI chat response"""
        choice = response.choices[0]
        message = choice.message
        
        # Extract tool calls
        tool_calls = []
        if message.tool_calls:
            for tool_call in message.tool_calls:
                tool_calls.append(ToolCall(
                    name=tool_call.function.name,
                    arguments=eval(tool_call.function.arguments)  # Use safe eval in production
                ))
        
        # Calculate usage and cost
        usage = Usage(
            prompt_tokens=response.usage.prompt_tokens,
            completion_tokens=response.usage.completion_tokens,
            total_tokens=response.usage.total_tokens
        )
        
        cost = self._calculate_cost(request_data["model"], usage)
        structured_data = None
        if request_data.get("format") in {"json", "json_schema"}:
            try:
                import json

                structured_data = json.loads(message.content or "{}")
            except Exception:
                structured_data = None

        return AIResponse(
            text=message.content or "",
            tool_calls=tool_calls,
            model=request_data["model"],
            provider="openai",
            usage=usage,
            cost=cost,
            structured_data=structured_data
        )
    
    def _process_image(self, image_input) -> str:
        """Process image input to data URL or URL"""
        if isinstance(image_input, (str, Path)):
            image_path = Path(image_input)
            if image_path.exists():
                # Local file - convert to base64
                with open(image_path, "rb") as f:
                    image_data = base64.b64encode(f.read()).decode()
                mime_type = f"image/{image_path.suffix[1:]}"
                return f"data:{mime_type};base64,{image_data}"
            else:
                # Assume it's a URL
                return str(image_input)
        
        return str(image_input)
    
    def _calculate_cost(self, model: str, usage: Usage) -> float:
        """Calculate cost based on model and usage"""
        # OpenAI pricing (per 1M tokens)
        pricing = {
            "gpt-5": {"input": 1.25, "output": 10.00},
            "gpt-5-mini": {"input": 0.25, "output": 2.00},
            "gpt-4.1": {"input": 2.00, "output": 8.00},
            "gpt-4.1-mini": {"input": 0.40, "output": 1.60},
            "gpt-4o": {"input": 5.00, "output": 15.00},
            "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        }
        
        if model not in pricing:
            return 0.0
        
        input_cost = (usage.prompt_tokens / 1000000) * pricing[model]["input"]
        output_cost = (usage.completion_tokens / 1000000) * pricing[model]["output"]
        
        return input_cost + output_cost
    
    def _calculate_image_cost(self, model: str, size: str, quality: str) -> float:
        """Calculate image generation cost"""
        if model == "dall-e-3":
            if quality == "hd":
                return 0.08 if size == "1024x1024" else 0.12
            else:
                return 0.04
        return 0.02  # dall-e-2
    
    def _calculate_audio_cost(self, audio_path: str) -> float:
        """Calculate audio transcription cost"""
        # Whisper costs $0.006 per minute
        # Estimate duration from file size (rough approximation)
        file_size = Path(audio_path).stat().st_size
        estimated_minutes = file_size / (1024 * 1024)  # Very rough estimate
        return estimated_minutes * 0.006
    
    def _calculate_tts_cost(self, text: str) -> float:
        """Calculate TTS cost"""
        # TTS costs $15 per 1M characters
        return (len(text) / 1000000) * 15.0
    
    def _handle_error(self, error: Exception) -> AIResponse:
        """Handle and convert errors"""
        error_msg = str(error)
        
        if "authentication" in error_msg.lower():
            raise AuthenticationError(f"OpenAI authentication failed: {error_msg}")
        elif "rate_limit" in error_msg.lower():
            raise RateLimitError(f"OpenAI rate limit exceeded: {error_msg}")
        else:
            raise ProviderError(f"OpenAI error: {error_msg}", provider="openai", original_error=error)
    
    def get_available_models(self) -> List[str]:
        """Get available OpenAI models"""
        try:
            models = self.client.models.list()
            return [model.id for model in models.data]
        except:
            return [
                "gpt-5", "gpt-5-mini", "gpt-4.1", "gpt-4.1-mini",
                "gpt-4o", "gpt-4o-mini", "dall-e-3", "dall-e-2",
                "whisper-1", "tts-1"
            ]