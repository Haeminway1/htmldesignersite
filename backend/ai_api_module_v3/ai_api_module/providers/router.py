# ai_api_module/providers/router.py
"""
Provider routing logic
"""
from typing import Dict, Any, Optional, List
from ..core.config import Config
from ..core.exceptions import ProviderError, ModelNotAvailableError
from .openai_provider import OpenAIProvider
from .anthropic_provider import AnthropicProvider
from .google_provider import GoogleProvider  
from .xai_provider import XAIProvider


class ProviderRouter:
    """Routes requests to appropriate providers"""
    
    def __init__(self, config: Config):
        self.config = config
        self.providers = {}
        self._initialize_providers()
    
    def _initialize_providers(self):
        """Initialize available providers based on API keys"""
        if self.config.openai_api_key:
            try:
                self.providers["openai"] = OpenAIProvider(
                    self.config.openai_api_key, 
                    self.config.to_dict()
                )
            except Exception as e:
                print(f"Warning: Failed to initialize OpenAI provider: {e}")
        
        if self.config.anthropic_api_key:
            try:
                self.providers["anthropic"] = AnthropicProvider(
                    self.config.anthropic_api_key,
                    self.config.to_dict()
                )
            except Exception as e:
                print(f"Warning: Failed to initialize Anthropic provider: {e}")
        
        if self.config.google_api_key:
            try:
                self.providers["google"] = GoogleProvider(
                    self.config.google_api_key,
                    self.config.to_dict()
                )
            except Exception as e:
                print(f"Warning: Failed to initialize Google provider: {e}")
        
        if self.config.xai_api_key:
            try:
                self.providers["xai"] = XAIProvider(
                    self.config.xai_api_key,
                    self.config.to_dict()
                )
            except Exception as e:
                print(f"Warning: Failed to initialize xAI provider: {e}")
        
        if not self.providers:
            raise ProviderError(
                "No providers available. Please set at least one API key.",
                provider="none"
            )
    
    def execute(self, request_data: Dict[str, Any]) -> Any:
        """Execute request with appropriate provider"""
        provider_name = request_data.get("provider")
        request_type = request_data.get("type", "chat")
        
        # Get provider
        if provider_name:
            if provider_name not in self.providers:
                raise ProviderError(
                    f"Provider {provider_name} not available",
                    provider=provider_name
                )
            provider = self.providers[provider_name]
        else:
            provider = self._select_provider(request_data)
        
        # Route to appropriate method
        if request_type == "chat":
            return provider.chat(request_data)
        elif request_type == "image_generation":
            return provider.generate_image(request_data)
        elif request_type == "audio_transcription":
            return provider.transcribe_audio(request_data)
        elif request_type == "text_to_speech":
            return provider.text_to_speech(request_data)
        else:
            raise ProviderError(
                f"Unknown request type: {request_type}",
                provider=provider.provider_name
            )
    
    def _select_provider(self, request_data: Dict[str, Any]) -> Any:
        """Select best provider for request"""
        model = request_data.get("model", "")
        
        # Model-based routing
        if any(x in model.lower() for x in ["gpt", "openai"]):
            if "openai" in self.providers:
                return self.providers["openai"]
        
        if any(x in model.lower() for x in ["claude", "anthropic"]):
            if "anthropic" in self.providers:
                return self.providers["anthropic"]
        
        if any(x in model.lower() for x in ["gemini", "google"]):
            if "google" in self.providers:
                return self.providers["google"]
        
        if any(x in model.lower() for x in ["grok", "xai"]):
            if "xai" in self.providers:
                return self.providers["xai"]
        
        # Default to first available provider
        if self.providers:
            return list(self.providers.values())[0]
        
        raise ModelNotAvailableError(
            f"No provider available for model: {model}",
            model=model
        )
    
    def get_available_providers(self) -> List[str]:
        """Get list of available providers"""
        return list(self.providers.keys())
    
    def get_provider(self, name: str) -> Optional[Any]:
        """Get specific provider instance"""
        return self.providers.get(name)