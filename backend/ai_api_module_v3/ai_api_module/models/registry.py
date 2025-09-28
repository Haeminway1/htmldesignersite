# ai_api_module/models/registry.py
"""
Model registry and alias management
"""
import yaml
from typing import Dict, Any, Tuple, Optional, List
from pathlib import Path
from ..core.exceptions import ModelNotAvailableError


class ModelRegistry:
    """Manages model aliases and routing"""
    
    def __init__(self):
        self.aliases = self._load_aliases()
        self.pricing = self._load_pricing()
        self.capabilities = self._load_capabilities()
        self.native_file_support = self._load_native_file_support()
    
    def _load_aliases(self) -> Dict[str, str]:
        """Load model aliases from catalog"""
        catalog_path = Path(__file__).parent / "catalog.yaml"
        
        if catalog_path.exists():
            with open(catalog_path, 'r') as f:
                data = yaml.safe_load(f)
                return data.get("aliases", {})
        
        # Default aliases if catalog doesn't exist
        return {
            # Smart routing
            "smart": "gpt-5",
            "fast": "gpt-5-mini", 
            "cheap": "gpt-4.1-nano",
            "creative": "claude-sonnet-4",
            
            # Provider shortcuts
            "gpt": "gpt-5",
            "claude": "claude-sonnet-4",
            "gemini": "gemini-2.5-flash",
            "grok": "grok-4",
            
            # Task-specific
            "coding": "grok-code-fast-1",
            "analysis": "claude-opus-4",
            "research": "o3-deep-research",
            
            # Image models
            "image": "dall-e-3",
            "gpt-image": "dall-e-3",
            "claude-image": "dall-e-3",  # Claude doesn't generate images
            "gemini-image": "gemini-2.5-flash-image-preview",
            "grok-image": "grok-2-image-1212",
        }
    
    def _load_pricing(self) -> Dict[str, Dict[str, float]]:
        """Load pricing information"""
        return {
            # OpenAI
            "gpt-5": {"input": 1.25, "output": 10.00},
            "gpt-5-mini": {"input": 0.25, "output": 2.00},
            "gpt-5-nano": {"input": 0.05, "output": 0.40},
            "gpt-4.1": {"input": 2.00, "output": 8.00},
            "gpt-4.1-mini": {"input": 0.40, "output": 1.60},
            "gpt-4.1-nano": {"input": 0.10, "output": 0.40},
            "gpt-4o": {"input": 5.00, "output": 15.00},
            "gpt-4o-mini": {"input": 0.15, "output": 0.60},
            "gpt-image-1": {"image": 0.042},
            "dall-e-3": {"image": 0.04},
            "dall-e-2": {"image": 0.02},
            
            # Anthropic
            "claude-opus-4-1": {"input": 15.00, "output": 75.00},
            "claude-opus-4": {"input": 15.00, "output": 75.00},
            "claude-sonnet-4": {"input": 3.00, "output": 15.00},
            "claude-3-5-sonnet": {"input": 3.00, "output": 15.00},
            "claude-3-5-haiku": {"input": 0.80, "output": 4.00},
            
            # Google
            "gemini-2.5-pro": {"input": 1.25, "output": 10.00},
            "gemini-2.5-flash": {"input": 0.10, "output": 0.40},
            "gemini-1.5-pro": {"input": 1.25, "output": 5.00},
            "gemini-1.5-flash": {"input": 0.075, "output": 0.30},
            
            # xAI
            "grok-4": {"input": 3.00, "output": 15.00},
            "grok-3": {"input": 3.00, "output": 15.00},
            "grok-3-mini": {"input": 0.30, "output": 0.50},
            "grok-code-fast-1": {"input": 0.20, "output": 1.50},
            "grok-2-image-1212": {"image": 0.07},
        }
    
    def _load_capabilities(self) -> Dict[str, List[str]]:
        """Load model capabilities"""
        return {
            # Text generation
            "gpt-5": ["text", "reasoning", "code", "tools"],
            "gpt-5-mini": ["text", "code", "tools"],
            "claude-opus-4": ["text", "reasoning", "analysis", "vision"],
            "claude-sonnet-4": ["text", "reasoning", "vision", "tools"],
            "gemini-2.5-pro": ["text", "vision", "audio", "tools", "web_search"],
            "gemini-2.5-flash": ["text", "vision", "tools", "web_search"],
            "grok-4": ["text", "reasoning", "vision", "web_search"],
            "grok-3": ["text", "reasoning"],
            
            # Image generation
            "dall-e-3": ["image_generation"],
            "dall-e-2": ["image_generation"],
            "gemini-2.5-flash-image-preview": ["image_generation"],
            "grok-2-image-1212": ["image_generation"],
            
            # Audio
            "whisper-1": ["audio_transcription"],
            "tts-1": ["text_to_speech"],
        }

    def _load_native_file_support(self) -> Dict[str, List[str]]:
        """Models that can ingest binary files directly."""
        pdf = "application/pdf"
        docx = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        doc = "application/msword"
        txt = "text/plain"
        md = "text/markdown"

        return {
            "gemini-2.5-pro": [pdf, docx, doc, txt, md],
            "gemini-2.5-flash": [pdf, docx, doc, txt, md],
            "gemini-2.5-flash-lite": [pdf, docx, doc, txt, md],
            "gemini-1.5-pro": [pdf, docx, doc, txt, md],
            "gemini-1.5-flash": [pdf, docx, doc, txt, md],
            "gemini-1.0-pro": [pdf, docx, doc, txt, md],
        }
    
    def resolve(self, model: str, provider: Optional[str] = None) -> Tuple[str, str]:
        """Resolve model alias to concrete model and provider"""
        
        # Resolve alias
        resolved_model = self.aliases.get(model, model)
        
        # Determine provider
        if provider:
            resolved_provider = provider
        else:
            resolved_provider = self._detect_provider(resolved_model)
        
        # Validate combination
        if not self._is_valid_combination(resolved_model, resolved_provider):
            # Try to find alternative
            alternative = self._find_alternative(model, provider)
            if alternative:
                return alternative
            else:
                raise ModelNotAvailableError(
                    f"Model {resolved_model} not available on provider {resolved_provider}",
                    model=resolved_model
                )
        
        return resolved_model, resolved_provider
    
    def resolve_image_model(self, model: Optional[str], provider: Optional[str]) -> Tuple[str, str]:
        """Resolve image generation model"""
        if model and "image" in model:
            return self.resolve(model, provider)
        
        # Default image models by provider
        if provider == "openai":
            return "gpt-image-1", "openai"
        elif provider == "google":
            return "gemini-2.5-flash-image-preview", "google"
        elif provider == "xai":
            return "grok-2-image-1212", "xai"
        else:
            # Default to OpenAI
            return "gpt-image-1", "openai"
    
    def _detect_provider(self, model: str) -> str:
        """Detect provider from model name"""
        if any(x in model.lower() for x in ["gpt", "dall-e", "whisper", "tts"]):
            return "openai"
        elif any(x in model.lower() for x in ["claude"]):
            return "anthropic"
        elif any(x in model.lower() for x in ["gemini"]):
            return "google"
        elif any(x in model.lower() for x in ["grok"]):
            return "xai"
        else:
            # Default to openai for unknown models
            return "openai"
    
    def _is_valid_combination(self, model: str, provider: str) -> bool:
        """Check if model/provider combination is valid"""
        provider_models = {
            "openai": ["gpt", "dall-e", "whisper", "tts", "o3"],
            "anthropic": ["claude"],
            "google": ["gemini"],
            "xai": ["grok"]
        }
        
        if provider not in provider_models:
            return False
        
        return any(prefix in model.lower() for prefix in provider_models[provider])
    
    def _find_alternative(self, original_model: str, provider: Optional[str]) -> Optional[Tuple[str, str]]:
        """Find alternative model/provider combination"""
        # Try same capability different provider
        if original_model in ["smart", "gpt"]:
            alternatives = [
                ("claude-sonnet-4", "anthropic"),
                ("gemini-2.5-flash", "google"),
                ("grok-4", "xai")
            ]
        elif original_model in ["fast", "cheap"]:
            alternatives = [
                ("gpt-4.1-mini", "openai"),
                ("claude-3-5-haiku", "anthropic"),
                ("gemini-2.5-flash", "google"),
                ("grok-3-mini", "xai")
            ]
        else:
            return None
        
        for alt_model, alt_provider in alternatives:
            if self._is_valid_combination(alt_model, alt_provider):
                return alt_model, alt_provider
        
        return None
    
    def estimate_cost(self, text: str, model: str, **kwargs) -> float:
        """Estimate cost for a request"""
        # Rough token estimation (4 chars = 1 token)
        estimated_tokens = len(text) // 4
        # Ensure max_tokens has a sane default when None or invalid
        max_tokens_arg = kwargs.get("max_tokens")
        try:
            max_tokens = int(max_tokens_arg) if max_tokens_arg is not None else 1000
        except Exception:
            max_tokens = 1000
        
        resolved_model, _ = self.resolve(model)
        
        if resolved_model not in self.pricing:
            return 0.0
        
        pricing = self.pricing[resolved_model]
        
        if "image" in pricing:
            return pricing["image"]
        
        input_cost = (estimated_tokens / 1000000) * pricing.get("input", 0)
        output_cost = (max_tokens / 1000000) * pricing.get("output", 0)
        
        return input_cost + output_cost
    
    def estimate_request_cost(self, request_data: Dict[str, Any]) -> float:
        """Estimate cost for a full request"""
        message = request_data.get("message", "")
        model = request_data.get("model", "gpt-4.1-mini")
        # Avoid passing duplicate keys (model/message) to estimate_cost
        extra_kwargs = {
            k: v for k, v in request_data.items() if k not in ("message", "model")
        }
        return self.estimate_cost(message, model, **extra_kwargs)

    def get_native_file_types(self, model: str) -> List[str]:
        """Return native file MIME types supported by the resolved model."""
        if model in self.native_file_support:
            return self.native_file_support[model]

        # Fallback: match by prefix for dated model IDs (e.g., gemini-2.5-pro-latest)
        for key, types in self.native_file_support.items():
            if key in model:
                return types
        return []
    
    def get_cheapest_model(self, capability: str = "text") -> str:
        """Get cheapest model with specified capability"""
        cheap_models = {
            "text": "gpt-4.1-nano",
            "image": "dall-e-2",
            "reasoning": "grok-3-mini",
            "vision": "claude-3-5-haiku"
        }
        
        return cheap_models.get(capability, "gpt-4.1-nano")
    
    def get_fastest_model(self, capability: str = "text") -> str:
        """Get fastest model with specified capability"""
        fast_models = {
            "text": "gpt-5-nano",
            "image": "dall-e-2", 
            "reasoning": "grok-code-fast-1",
            "vision": "gemini-2.5-flash"
        }
        
        return fast_models.get(capability, "gpt-5-nano")
    
    def get_best_model(self, capability: str = "text") -> str:
        """Get best quality model with specified capability"""
        best_models = {
            "text": "gpt-5",
            "reasoning": "o3-deep-research",
            "image": "dall-e-3",
            "vision": "claude-opus-4",
            "code": "grok-code-fast-1",
            "analysis": "claude-opus-4"
        }
        
        return best_models.get(capability, "gpt-5")
