# ai_api_module/providers/base.py
"""
Base provider interface
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, AsyncGenerator
from ..core.response import AIResponse


class BaseProvider(ABC):
    """Base interface for AI providers"""
    
    def __init__(self, api_key: str, config: Dict[str, Any]):
        self.api_key = api_key
        self.config = config
        self.provider_name = self.__class__.__name__.lower().replace('provider', '')
    
    @abstractmethod
    def chat(self, request_data: Dict[str, Any]) -> AIResponse:
        """Execute chat completion"""
        pass
    
    @abstractmethod
    async def async_chat(self, request_data: Dict[str, Any]) -> AIResponse:
        """Execute async chat completion"""
        pass
    
    @abstractmethod
    def stream_chat(self, request_data: Dict[str, Any]) -> AsyncGenerator[str, None]:
        """Stream chat completion"""
        pass
    
    def generate_image(self, request_data: Dict[str, Any]) -> AIResponse:
        """Generate image (override if supported)"""
        raise NotImplementedError(f"Image generation not supported by {self.provider_name}")
    
    def transcribe_audio(self, request_data: Dict[str, Any]) -> AIResponse:
        """Transcribe audio (override if supported)"""
        raise NotImplementedError(f"Audio transcription not supported by {self.provider_name}")
    
    def text_to_speech(self, request_data: Dict[str, Any]) -> AIResponse:
        """Text to speech (override if supported)"""
        raise NotImplementedError(f"Text to speech not supported by {self.provider_name}")
    
    def get_available_models(self) -> List[str]:
        """Get list of available models"""
        return []
    
    def estimate_cost(self, request_data: Dict[str, Any]) -> float:
        """Estimate request cost"""
        return 0.0