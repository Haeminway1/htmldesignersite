# ai_api_module/core/response.py
"""
AIResponse class - Unified response object
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from pathlib import Path


@dataclass
class Usage:
    """Token and cost usage information"""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    reasoning_tokens: int = 0
    image_tokens: int = 0
    audio_tokens: int = 0
    total_tokens: int = 0


@dataclass
class ToolCall:
    """Function/tool call information"""
    name: str
    arguments: Dict[str, Any]
    result: Optional[Any] = None


@dataclass
class Image:
    """Image data container"""
    data: bytes
    format: str
    width: Optional[int] = None
    height: Optional[int] = None
    url: Optional[str] = None
    
    def save(self, path: Union[str, Path], quality: int = 95):
        """Save image to file"""
        from PIL import Image as PILImage
        import io
        
        data_bytes = self.data
        # If data is empty but URL is available, download
        if (not data_bytes or len(data_bytes) == 0) and self.url:
            try:
                import httpx
                r = httpx.get(self.url, timeout=30)
                r.raise_for_status()
                data_bytes = r.content
            except Exception:
                data_bytes = self.data  # keep original
        
        img = PILImage.open(io.BytesIO(data_bytes))
        img.save(str(path), quality=quality)


@dataclass
class Audio:
    """Audio data container"""
    data: bytes
    format: str
    duration: Optional[float] = None
    sample_rate: Optional[int] = None
    
    def save(self, path: Union[str, Path]):
        """Save audio to file"""
        with open(path, 'wb') as f:
            f.write(self.data)


@dataclass
class AIResponse:
    """
    Unified response object across all providers
    """
    # Core content
    text: str = ""
    images: List[Image] = field(default_factory=list)
    audio: Optional[Audio] = None
    tool_calls: List[ToolCall] = field(default_factory=list)
    
    # Metadata
    model: str = ""
    provider: str = ""
    usage: Usage = field(default_factory=Usage)
    reasoning: Optional[str] = None
    
    # Context management
    conversation_id: Optional[str] = None
    message_id: str = ""
    
    # Quality metrics
    confidence: float = 1.0
    safety_flags: List[str] = field(default_factory=list)
    
    # Cost tracking
    cost: float = 0.0
    
    # Structured data (for JSON responses)
    structured_data: Optional[Any] = None

    # Timing
    timestamp: datetime = field(default_factory=datetime.now)
    response_time: float = 0.0
    
    # Citations and sources (for web search)
    citations: List[Dict[str, Any]] = field(default_factory=list)
    sources: List[str] = field(default_factory=list)
    
    def __str__(self) -> str:
        """String representation"""
        return self.text
    
    def __bool__(self) -> bool:
        """Boolean representation"""
        return bool(self.text or self.images or self.audio)
    
    @property
    def has_images(self) -> bool:
        """Check if response contains images"""
        return len(self.images) > 0
    
    @property
    def has_audio(self) -> bool:
        """Check if response contains audio"""
        return self.audio is not None
    
    @property
    def has_tool_calls(self) -> bool:
        """Check if response contains tool calls"""
        return len(self.tool_calls) > 0
    
    def save_images(self, directory: Union[str, Path] = "images"):
        """Save all images to directory"""
        directory = Path(directory)
        directory.mkdir(exist_ok=True)
        
        for i, image in enumerate(self.images):
            filename = f"image_{i:03d}.{image.format}"
            image.save(directory / filename)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "text": self.text,
            "model": self.model,
            "provider": self.provider,
            "usage": {
                "prompt_tokens": self.usage.prompt_tokens,
                "completion_tokens": self.usage.completion_tokens,
                "total_tokens": self.usage.total_tokens,
            },
            "cost": self.cost,
            "timestamp": self.timestamp.isoformat(),
            "response_time": self.response_time,
            "has_images": self.has_images,
            "has_audio": self.has_audio,
            "has_tool_calls": self.has_tool_calls,
        }