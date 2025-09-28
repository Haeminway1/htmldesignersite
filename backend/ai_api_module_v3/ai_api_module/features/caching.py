# ai_api_module/features/caching.py
"""
Response caching system
"""
import hashlib
import json
import time
from pathlib import Path
from typing import Dict, Any, Optional, Union

from ..core.response import AIResponse


class CacheManager:
    """Manages response caching"""
    
    def __init__(
        self, 
        duration: int = 3600,  # 1 hour default
        max_size: int = 1000,
        cache_dir: Optional[Path] = None
    ):
        self.duration = duration
        self.max_size = max_size
        self.cache_dir = cache_dir or Path.home() / ".ai_api_module" / "cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # In-memory cache for quick access
        self._memory_cache: Dict[str, Dict[str, Any]] = {}
        self._access_times: Dict[str, float] = {}
    
    def _generate_key(self, request_data: Dict[str, Any]) -> str:
        """Generate cache key from request data"""
        # Create a normalized version for consistent hashing
        normalized = {
            "message": request_data.get("message", ""),
            "model": request_data.get("model", ""),
            "provider": request_data.get("provider", ""),
            "system": request_data.get("system", ""),
            "temperature": request_data.get("temperature"),
            "max_tokens": request_data.get("max_tokens"),
            "tools": request_data.get("tools"),
            "format": request_data.get("format"),
            "conversation_id": request_data.get("conversation_id"),
            "files": self._normalize_files(request_data.get("files")),
            "native_files": self._normalize_files(request_data.get("native_files")),
            "images": self._normalize_files(request_data.get("images")),
        }
        
        # Remove None values
        normalized = {k: v for k, v in normalized.items() if v is not None}
        
        # Create hash
        content = json.dumps(normalized, sort_keys=True)
        return hashlib.md5(content.encode()).hexdigest()

    def _normalize_files(self, files: Optional[Union[str, Path, list]]):
        if not files:
            return None
        if isinstance(files, (str, Path)):
            return [str(Path(files).resolve())]
        normalized = []
        for f in files:
            try:
                normalized.append(str(Path(f).resolve()))
            except Exception:
                normalized.append(str(f))
        return normalized
    
    def get(self, request_data: Dict[str, Any]) -> Optional[AIResponse]:
        """Get cached response"""
        key = self._generate_key(request_data)
        
        # Check memory cache first
        if key in self._memory_cache:
            cache_entry = self._memory_cache[key]
            
            # Check if still valid
            if time.time() - cache_entry["timestamp"] < self.duration:
                self._access_times[key] = time.time()
                return self._deserialize_response(cache_entry["data"])
            else:
                # Expired, remove from cache
                del self._memory_cache[key]
                if key in self._access_times:
                    del self._access_times[key]
        
        # Check disk cache
        cache_file = self.cache_dir / f"{key}.json"
        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    cache_entry = json.load(f)
                
                if time.time() - cache_entry["timestamp"] < self.duration:
                    # Load into memory cache
                    self._memory_cache[key] = cache_entry
                    self._access_times[key] = time.time()
                    return self._deserialize_response(cache_entry["data"])
                else:
                    # Expired, remove file
                    cache_file.unlink()
            except:
                # Corrupted cache file, remove it
                cache_file.unlink()
        
        return None
    
    def set(self, request_data: Dict[str, Any], response: AIResponse):
        """Cache response"""
        key = self._generate_key(request_data)
        
        cache_entry = {
            "timestamp": time.time(),
            "data": self._serialize_response(response)
        }
        
        # Add to memory cache
        self._memory_cache[key] = cache_entry
        self._access_times[key] = time.time()
        
        # Clean up if over size limit
        self._cleanup_memory_cache()
        
        # Save to disk
        cache_file = self.cache_dir / f"{key}.json"
        try:
            with open(cache_file, 'w') as f:
                json.dump(cache_entry, f)
        except:
            pass  # Fail silently if can't write to disk
    
    def _serialize_response(self, response: AIResponse) -> Dict[str, Any]:
        """Serialize response for caching"""
        return {
            "text": response.text,
            "model": response.model,
            "provider": response.provider,
            "cost": response.cost,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            },
            "timestamp": response.timestamp.isoformat(),
            "cached": True
        }
    
    def _deserialize_response(self, data: Dict[str, Any]) -> AIResponse:
        """Deserialize cached response"""
        from datetime import datetime
        from ..core.response import Usage
        
        return AIResponse(
            text=data["text"],
            model=data["model"],
            provider=data["provider"],
            cost=data["cost"],
            usage=Usage(
                prompt_tokens=data["usage"]["prompt_tokens"],
                completion_tokens=data["usage"]["completion_tokens"],
                total_tokens=data["usage"]["total_tokens"]
            ),
            timestamp=datetime.fromisoformat(data["timestamp"])
        )
    
    def _cleanup_memory_cache(self):
        """Remove old entries if cache is too large"""
        if len(self._memory_cache) <= self.max_size:
            return
        
        # Sort by access time and remove oldest
        sorted_keys = sorted(
            self._access_times.keys(),
            key=lambda k: self._access_times[k]
        )
        
        to_remove = len(self._memory_cache) - self.max_size + 10  # Remove a few extra
        
        for key in sorted_keys[:to_remove]:
            if key in self._memory_cache:
                del self._memory_cache[key]
            if key in self._access_times:
                del self._access_times[key]
    
    def clear(self):
        """Clear all caches"""
        self._memory_cache.clear()
        self._access_times.clear()
        
        # Remove cache files
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                cache_file.unlink()
            except:
                pass
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return {
            "memory_entries": len(self._memory_cache),
            "disk_entries": len(list(self.cache_dir.glob("*.json"))),
            "max_size": self.max_size,
            "duration": self.duration,
            "cache_dir": str(self.cache_dir)
        }