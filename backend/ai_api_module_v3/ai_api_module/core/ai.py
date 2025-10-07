# ai_api_module/core/ai.py
"""
Main AI class - Unified interface for all providers
"""
import asyncio
import mimetypes
import os
from pathlib import Path
from typing import List, Optional, Union, Dict, Any, AsyncGenerator, Callable

from .config import Config
from .response import AIResponse
from .conversation import Conversation
from .memory import Memory
from .exceptions import *
from ..providers.router import ProviderRouter
from ..models.registry import ModelRegistry
from ..tools.base import Tool
from ..features.async_handler import AsyncHandler
from ..features.streaming import StreamingHandler
from ..features.caching import CacheManager
from ..utils.logging import setup_logging
from ..utils.document_utils import extract_document, ExtractedDocument


class AI:
    """
    Main AI interface supporting multiple providers (OpenAI, Anthropic, Google, xAI)
    
    Usage:
        ai = AI()
        response = ai.chat("Hello world")
        
        # With specific provider
        ai = AI(provider="openai")
        
        # With custom config
        ai = AI(
            provider="anthropic",
            budget_limit=10.0,
            temperature=0.7
        )
    """
    
    def __init__(
        self,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        budget_limit: Optional[float] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        debug: bool = False,
        **kwargs
    ):
        """Initialize AI instance with configuration"""
        
        # Load configuration (map to Config's actual fields)
        config_kwargs: Dict[str, Any] = {
            "default_provider": provider,
            "default_model": model or "smart",
            "temperature": temperature,
            "max_tokens": max_tokens,
            "debug": debug,
        }
        if budget_limit is not None:
            # Treat budget_limit as daily budget for convenience
            config_kwargs["daily_budget_limit"] = budget_limit

        # If explicit api_key provided with provider, set the right field
        if api_key and provider:
            provider_key_map = {
                "openai": "openai_api_key",
                "anthropic": "anthropic_api_key",
                "google": "google_api_key",
                "xai": "xai_api_key",
            }
            key_field = provider_key_map.get(provider)
            if key_field:
                config_kwargs[key_field] = api_key

        # Allow additional overrides
        config_kwargs.update(kwargs)

        self.config = Config(**config_kwargs)
        
        # Setup logging
        setup_logging(level="DEBUG" if debug else "INFO")
        
        # Initialize components
        self.model_registry = ModelRegistry()
        self.provider_router = ProviderRouter(self.config)
        self.memory = Memory()
        self.cache = CacheManager() if self.config.enable_cache else None
        
        # Feature handlers
        self.async_handler = AsyncHandler(self.provider_router, self)
        self.streaming_handler = StreamingHandler(self.provider_router, self)
        
        # Usage tracking
        self.total_cost = 0.0
        self.request_count = 0
        
        # Available tools
        self._tools: Dict[str, Tool] = {}

        # Internal tracking for attachment preparation
        self._pending_model_name: Optional[str] = None
        
    def chat(
        self,
        message: str,
        *,
        model: Optional[str] = None,
        provider: Optional[str] = None,
        system: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        reasoning_effort: Optional[str] = None,
        tools: Optional[List[Union[str, Tool, Callable]]] = None,
        image: Optional[Union[str, Path]] = None,
        images: Optional[List[Union[str, Path]]] = None,
        files: Optional[List[Union[str, Path]]] = None,
        history: Optional[List[Dict[str, Any]]] = None,
        web_search: bool = False,
        stream: bool = False,
        format: Optional[str] = None,
        conversation_id: Optional[str] = None,
        use_memory: bool = False,
        **kwargs
    ) -> Union[AIResponse, AsyncGenerator[str, None]]:
        """
        Send a chat message and get AI response
        
        Args:
            message: The message to send
            model: Model to use (e.g., "gpt", "claude", "smart", "fast")
            provider: Force specific provider ("openai", "anthropic", "google", "xai")
            system: System prompt
            temperature: Randomness (0-2)
            max_tokens: Maximum output tokens
            reasoning_effort: "minimal", "low", "medium", "high"
            tools: List of tool names to enable
            image: Single image path/URL
            images: Multiple image paths/URLs
            files: List of file paths for analysis
            web_search: Enable web search
            stream: Stream response
            format: Output format ("json", "markdown", etc.)
            conversation_id: Continue existing conversation
            use_memory: Use long-term memory
            
        Returns:
            AIResponse object or streaming generator
        """
        
        # Resolve model and provider
        final_model = model or self.config.default_model
        # If provider not explicitly given, allow auto-detection by passing None
        final_provider = provider
        
        resolved_model, resolved_provider = self.model_registry.resolve(
            final_model, final_provider
        )
        
        memory_snapshot = self._build_memory_snapshot() if use_memory else None

        if format in {"json", "json_schema"} and not system:
            system = "Please respond in valid JSON format."

        self._pending_model_name = resolved_model
        try:
            request_data = self._build_request(
                message=message,
                model=resolved_model,
                provider=resolved_provider,
                system=system,
                temperature=temperature,
                max_tokens=self._normalize_max_tokens(max_tokens, resolved_model),
                reasoning_effort=reasoning_effort,
                tools=self._normalize_tools(tools),
                image=image,
                images=images,
                files=files,
                history=history,
                web_search=web_search,
                format=format,
                conversation_id=conversation_id,
                use_memory=use_memory,
                memory_snapshot=memory_snapshot,
                **kwargs
            )
        finally:
            self._pending_model_name = None
        
        # Check cache
        if self.cache and not stream:
            cached_response = self.cache.get(request_data)
            if cached_response:
                return cached_response
                
        # Check budget
        self._check_budget(request_data)
        
        # Execute request
        if stream:
            return self.streaming_handler.stream(request_data)
        else:
            response = self.provider_router.execute(request_data)

            # Cache response
            if self.cache:
                self.cache.set(request_data, response)

            # Update usage tracking
            self._update_usage(response)

            return response
    
    async def async_chat(self, message: str, **kwargs) -> AIResponse:
        """Async version of chat()"""
        return await self.async_handler.chat(message, **kwargs)
    
    async def batch_chat(
        self, 
        messages: List[str], 
        max_concurrent: int = 5,
        **kwargs
    ) -> List[AIResponse]:
        """Process multiple messages concurrently"""
        return await self.async_handler.batch_chat(
            messages, max_concurrent, **kwargs
        )
    
    async def stream_chat(
        self, 
        message: str, 
        on_chunk=None, 
        on_complete=None,
        **kwargs
    ) -> AsyncGenerator[str, None]:
        """Stream chat response with callbacks (async)."""
        async for chunk in self.streaming_handler.stream_with_callbacks(
            message, on_chunk, on_complete, **kwargs
        ):
            yield chunk
    
    # Image capabilities
    def generate_image(
        self,
        prompt: str,
        *,
        model: Optional[str] = None,
        provider: Optional[str] = None,
        style: str = "natural",
        size: str = "1024x1024",
        quality: str = "standard",
        **kwargs
    ) -> AIResponse:
        """Generate image from text prompt"""
        
        # Route to image generation provider
        image_model, image_provider = self.model_registry.resolve_image_model(
            model, provider
        )
        
        request_data = {
            "type": "image_generation",
            "prompt": prompt,
            "model": image_model,
            "provider": image_provider,
            "style": style,
            "size": size,
            "quality": quality,
            **kwargs
        }
        
        return self.provider_router.execute(request_data)
    
    def analyze_image(
        self,
        image: Union[str, Path],
        prompt: str,
        **kwargs
    ) -> AIResponse:
        """Analyze image with AI"""
        return self.chat(
            message=prompt,
            image=image,
            **kwargs
        )
    
    def analyze_images(
        self,
        images: List[Union[str, Path]],
        prompt: str,
        **kwargs
    ) -> AIResponse:
        """Analyze multiple images"""
        return self.chat(
            message=prompt,
            images=images,
            **kwargs
        )
    
    # Document processing
    def analyze_document(
        self,
        file_path: Union[str, Path],
        prompt: str,
        **kwargs
    ) -> AIResponse:
        """Analyze document (PDF, DOCX, TXT, etc.)"""
        return self.chat(
            message=prompt,
            files=[file_path],
            **kwargs
        )
    
    def analyze_documents(
        self,
        file_paths: List[Union[str, Path]],
        prompt: str,
        **kwargs
    ) -> AIResponse:
        """Analyze multiple documents"""
        return self.chat(
            message=prompt,
            files=file_paths,
            **kwargs
        )
    
    # Audio capabilities
    def transcribe_audio(
        self,
        audio_path: Union[str, Path],
        **kwargs
    ) -> str:
        """Convert speech to text"""
        request_data = {
            "type": "audio_transcription",
            "audio_path": audio_path,
            **kwargs
        }
        
        response = self.provider_router.execute(request_data)
        return response.text
    
    def generate_speech(
        self,
        text: str,
        voice: str = "natural",
        speed: float = 1.0,
        output_format: str = "mp3",
        **kwargs
    ) -> AIResponse:
        """Convert text to speech"""
        request_data = {
            "type": "text_to_speech",
            "text": text,
            "voice": voice,
            "speed": speed,
            "output_format": output_format,
            **kwargs
        }
        
        return self.provider_router.execute(request_data)
    
    # Web search
    def web_search(
        self,
        query: str,
        sources: List[str] = ["general"],
        max_results: int = 10,
        date_range: Optional[str] = None,
        **kwargs
    ) -> AIResponse:
        """Perform web search"""
        return self.chat(
            message=f"Search: {query}",
            web_search=True,
            tools=["web_search"],
            search_config={
                "sources": sources,
                "max_results": max_results,
                "date_range": date_range,
                **kwargs
            }
        )
    
    # Conversation management
    def start_conversation(
        self,
        name: Optional[str] = None,
        system: Optional[str] = None,
        **kwargs
    ) -> Conversation:
        """Start a new conversation"""
        return Conversation(
            ai_instance=self,
            name=name,
            system=system,
            **kwargs
        )
    
    def load_conversation(self, file_path: Union[str, Path]) -> Conversation:
        """Load conversation from file"""
        return Conversation.load(file_path, ai_instance=self)
    
    # Tool management
    def add_tool(self, tool: Tool):
        """Add a custom tool"""
        self._tools[tool.name] = tool
    
    def remove_tool(self, tool_name: str):
        """Remove a tool"""
        if tool_name in self._tools:
            del self._tools[tool_name]

    def tool(self, name: Optional[str] = None, description: Optional[str] = None):
        """Decorator to register a function as a tool on this AI instance.

        Usage:
            @ai.tool()
            def my_func(...):
                ...
        """
        from ..tools.base import tool as base_tool_decorator

        def decorator(func: Callable):
            t = base_tool_decorator(name=name, description=description)(func)
            self.add_tool(t)
            return t

        return decorator
    
    # Cost and usage management
    def estimate_cost(
        self,
        message: str,
        model: Optional[str] = None,
        **kwargs
    ) -> float:
        """Estimate cost before execution"""
        return self.model_registry.estimate_cost(message, model, **kwargs)
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get usage statistics"""
        return {
            "total_cost": self.total_cost,
            "request_count": self.request_count,
            "daily_cost": self._get_daily_cost(),
            "monthly_cost": self._get_monthly_cost(),
            "most_used_model": self._get_most_used_model(),
            "budget_remaining": self._get_budget_remaining()
        }

    # Logging configuration wrapper for docs/README examples
    def setup_logging(
        self,
        level: str = "INFO",
        log_to_file: bool = False,
        log_file: Optional[str] = None,
        log_costs: bool = False,
        log_responses: bool = False
    ):
        """Configure logging consistent with documentation examples."""
        from pathlib import Path
        log_path = Path(log_file) if (log_to_file and log_file) else None
        setup_logging(level=level, log_file=log_path)
        # Note: log_costs/log_responses are placeholders for future enhancements
    
    def set_budget_limit(
        self,
        daily: Optional[float] = None,
        monthly: Optional[float] = None
    ):
        """Set budget limits"""
        if daily:
            self.config.daily_budget_limit = daily
        if monthly:
            self.config.monthly_budget_limit = monthly
    
    # Configuration methods
    def enable_cache(self, cache_duration: int = 3600, cache_size: int = 1000):
        """Enable response caching"""
        self.cache = CacheManager(
            duration=cache_duration,
            max_size=cache_size
        )
    
    def enable_cost_optimization(
        self,
        prefer_cheaper_models: bool = True,
        aggressive_caching: bool = True,
        token_budgets: bool = True,
        smart_routing: bool = True
    ):
        """Enable automatic cost optimization"""
        self.config.cost_optimization = {
            "prefer_cheaper_models": prefer_cheaper_models,
            "aggressive_caching": aggressive_caching,
            "token_budgets": token_budgets,
            "smart_routing": smart_routing
        }
    
    # Private methods
    def _build_request(self, **kwargs) -> Dict[str, Any]:
        """Build request data structure"""
        try:
            loop = asyncio.get_event_loop()
            base_timestamp = loop.time()
        except RuntimeError:
            base_timestamp = 0.0

        attachments = self._prepare_attachments(
            kwargs.pop("image", None),
            kwargs.pop("images", None),
            kwargs.get("files")
        )

        documents: List[ExtractedDocument] = attachments["documents"]
        normalized_images = attachments["images"]
        normalized_files = attachments["files"]

        memory_snapshot = kwargs.pop("memory_snapshot", None)
        if kwargs.get("use_memory") and memory_snapshot is None:
            memory_snapshot = self._build_memory_snapshot()

        context_messages = self._build_context_messages(
            documents,
            memory_snapshot
        )

        normalized_history = self._normalize_history(kwargs.pop("history", None))

        request_payload = {
            "timestamp": base_timestamp,
            "config": self.config.to_dict(),
            "images": normalized_images,
            "documents": [doc.__dict__ for doc in documents],
            "native_files": attachments["native_files"],
            "context_messages": context_messages,
            "history": normalized_history,
            "memory_snapshot": memory_snapshot,
            **kwargs
        }

        # Normalized file list retained for providers that can ingest raw files
        if normalized_files:
            request_payload["files"] = normalized_files

        return request_payload

    def _build_memory_snapshot(self) -> Dict[str, str]:
        return self.memory.get_all_facts()

    def _prepare_attachments(
        self,
        image: Optional[Union[str, Path]],
        images: Optional[List[Union[str, Path]]],
        files: Optional[List[Union[str, Path]]]
    ) -> Dict[str, Any]:
        """Normalize attachments considering native provider support."""

        normalized_images: List[str] = []
        if image:
            normalized_images.append(self._normalize_path_or_url(image))
        if images:
            for img in images:
                normalized_images.append(self._normalize_path_or_url(img))

        document_objects: List[ExtractedDocument] = []
        normalized_files: List[str] = []
        native_file_paths: List[str] = []

        target_model = getattr(self, "_pending_model_name", None)
        native_types = self.model_registry.get_native_file_types(target_model) if target_model else []

        if files:
            for file_entry in files:
                normalized_path = self._normalize_path_or_url(file_entry)
                normalized_files.append(normalized_path)
                path = Path(normalized_path)
                if not path.exists():
                    continue

                mime_type, _ = mimetypes.guess_type(str(path))
                mime_type = mime_type or "application/octet-stream"

                # Auto-detect image files and add to images array
                if mime_type.startswith("image/"):
                    normalized_images.append(normalized_path)
                    continue

                if mime_type in native_types:
                    native_file_paths.append(str(path))
                    # Skip text extraction to let provider handle the binary file
                    continue

                extracted = extract_document(path)
                if extracted:
                    document_objects.append(extracted)

        return {
            "images": normalized_images,
            "documents": document_objects,
            "files": normalized_files,
            "native_files": native_file_paths,
        }

    def _normalize_path_or_url(self, value: Union[str, Path]) -> str:
        if isinstance(value, Path):
            return str(value.resolve())
        try:
            path = Path(value)
            if path.exists():
                return str(path.resolve())
        except Exception:
            pass
        return str(value)

    def _build_context_messages(
        self,
        documents: List[ExtractedDocument],
        memory_snapshot: Optional[Dict[str, str]]
    ) -> List[str]:
        messages: List[str] = []

        if memory_snapshot:
            memo_block = ["[메모리 스냅샷]"]
            for key, value in memory_snapshot.items():
                memo_block.append(f"- {key}: {value}")
            messages.append("\n".join(memo_block))

        for doc in documents:
            messages.append(doc.as_prompt_block())

        return messages

    def _normalize_history(
        self,
        history: Optional[List[Dict[str, Any]]]
    ) -> Optional[List[Dict[str, Any]]]:
        if not history:
            return None

        normalized: List[Dict[str, Any]] = []
        for item in history:
            role = item.get("role")
            content = item.get("content")
            if not role or content is None:
                continue
            normalized.append({"role": role, "content": content})
        return normalized if normalized else None

    def _normalize_tools(self, tools: Optional[List[Union[str, Tool, Callable]]]) -> Optional[List[str]]:
        """Normalize tools into a list of tool names and register if needed."""
        if not tools:
            return None
        normalized: List[str] = []
        from ..tools.base import tool as base_tool_decorator, Tool as ToolClass
        for item in tools:
            if isinstance(item, str):
                normalized.append(item)
            elif isinstance(item, ToolClass):
                # Already a Tool instance
                self._tools[item.name] = item
                normalized.append(item.name)
            elif callable(item):
                # Convert callable to Tool and register
                t = base_tool_decorator()(item)
                self.add_tool(t)
                normalized.append(t.name)
        return normalized

    def _normalize_max_tokens(self, user_max_tokens: Optional[int], model_name: str) -> int:
        """Apply default max token policy by model capability.

        - Reasoning/Deep models: default 20000 (maps later to provider-specific fields)
        - Non-reasoning models: default 2000
        If user provided a value, respect it.
        """
        if user_max_tokens is not None:
            return int(user_max_tokens)

        # Heuristic: names indicating reasoning models
        reasoning_keywords = ["gpt-5", "o3", "opus", "sonnet", "grok-4", "deep-research", "code-fast-1"]
        is_reasoning = any(kw in model_name.lower() for kw in reasoning_keywords)
        return 20000 if is_reasoning else 2000
    
    def _check_budget(self, request_data: Dict[str, Any]):
        """Check if request would exceed budget"""
        estimated_cost = self.model_registry.estimate_request_cost(request_data)
        
        if self.config.daily_budget_limit:
            daily_cost = self._get_daily_cost()
            if daily_cost + estimated_cost > self.config.daily_budget_limit:
                raise BudgetExceededError(
                    (
                        f"Daily budget would be exceeded: "
                        f"{daily_cost + estimated_cost:.4f} > {self.config.daily_budget_limit:.4f}"
                    ),
                    current_cost=daily_cost + estimated_cost,
                    budget_limit=self.config.daily_budget_limit,
                )
        if self.config.monthly_budget_limit:
            monthly_cost = self._get_monthly_cost()
            if monthly_cost + estimated_cost > self.config.monthly_budget_limit:
                raise BudgetExceededError(
                    (
                        f"Monthly budget would be exceeded: "
                        f"{monthly_cost + estimated_cost:.4f} > {self.config.monthly_budget_limit:.4f}"
                    ),
                    current_cost=monthly_cost + estimated_cost,
                    budget_limit=self.config.monthly_budget_limit,
                )
    
    def _update_usage(self, response: AIResponse):
        """Update usage statistics"""
        self.total_cost += response.cost
        self.request_count += 1
        
        # Store usage data for analytics
        self.memory.add_usage_record({
            "timestamp": response.timestamp,
            "model": response.model,
            "provider": response.provider,
            "cost": response.cost,
            "tokens": response.usage.total_tokens
        })
    
    def _get_daily_cost(self) -> float:
        """Get today's total cost"""
        return self.memory.get_daily_cost()
    
    def _get_monthly_cost(self) -> float:
        """Get this month's total cost"""
        return self.memory.get_monthly_cost()
    
    def _get_most_used_model(self) -> str:
        """Get most frequently used model"""
        return self.memory.get_most_used_model()
    
    def _get_budget_remaining(self) -> Dict[str, float]:
        """Get remaining budget"""
        daily_remaining = None
        monthly_remaining = None
        
        if self.config.daily_budget_limit:
            daily_remaining = self.config.daily_budget_limit - self._get_daily_cost()
            
        if self.config.monthly_budget_limit:
            monthly_remaining = self.config.monthly_budget_limit - self._get_monthly_cost()
            
        return {
            "daily": daily_remaining,
            "monthly": monthly_remaining
        }