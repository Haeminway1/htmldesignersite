# ai_api_module/core/config.py
"""
Configuration management
"""
import os
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field


@dataclass
class Config:
    """Configuration class for AI API Module"""
    
    # Provider settings
    default_provider: Optional[str] = None
    default_model: str = "smart"
    
    # API Keys
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    google_api_key: Optional[str] = None
    xai_api_key: Optional[str] = None
    
    # Default parameters
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    
    # Budget and limits
    daily_budget_limit: Optional[float] = None
    monthly_budget_limit: Optional[float] = None
    
    # Features
    enable_cache: bool = True
    enable_web_search: bool = True
    debug: bool = False
    
    # Cost optimization
    cost_optimization: Dict[str, bool] = field(default_factory=lambda: {
        "prefer_cheaper_models": False,
        "aggressive_caching": False,
        "token_budgets": False,
        "smart_routing": True
    })
    
    def __post_init__(self):
        """Initialize config from environment variables"""
        # Load API keys from environment
        self.openai_api_key = self.openai_api_key or os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key = self.anthropic_api_key or os.getenv("ANTHROPIC_API_KEY")
        self.google_api_key = self.google_api_key or os.getenv("GOOGLE_API_KEY")
        self.xai_api_key = self.xai_api_key or os.getenv("XAI_API_KEY")
        
        # Load other settings
        self.default_provider = self.default_provider or os.getenv("AI_DEFAULT_PROVIDER")
        self.default_model = os.getenv("AI_DEFAULT_MODEL", self.default_model)
        
        # Budget limits
        if os.getenv("AI_DAILY_BUDGET_LIMIT"):
            self.daily_budget_limit = float(os.getenv("AI_DAILY_BUDGET_LIMIT"))
        if os.getenv("AI_MONTHLY_BUDGET_LIMIT"):
            self.monthly_budget_limit = float(os.getenv("AI_MONTHLY_BUDGET_LIMIT"))
        
        # Debug mode
        if os.getenv("AI_DEBUG"):
            self.debug = os.getenv("AI_DEBUG").lower() in ["true", "1", "yes"]
        
        # Auto-detect provider if not specified
        if not self.default_provider:
            self.default_provider = self._detect_default_provider()
    
    def _detect_default_provider(self) -> Optional[str]:
        """Auto-detect best available provider"""
        if self.openai_api_key:
            return "openai"
        elif self.anthropic_api_key:
            return "anthropic"
        elif self.google_api_key:
            return "google"
        elif self.xai_api_key:
            return "xai"
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary"""
        return {
            "default_provider": self.default_provider,
            "default_model": self.default_model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "daily_budget_limit": self.daily_budget_limit,
            "monthly_budget_limit": self.monthly_budget_limit,
            "enable_cache": self.enable_cache,
            "enable_web_search": self.enable_web_search,
            "debug": self.debug,
            "cost_optimization": self.cost_optimization
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Config":
        """Create config from dictionary"""
        return cls(**data)
    
    def validate(self) -> List[str]:
        """Validate configuration and return list of issues"""
        issues = []
        
        # Check if at least one API key is provided
        if not any([
            self.openai_api_key,
            self.anthropic_api_key, 
            self.google_api_key,
            self.xai_api_key
        ]):
            issues.append("No API keys provided. Please set at least one provider API key.")
        
        # Validate temperature
        if not 0 <= self.temperature <= 2:
            issues.append("Temperature must be between 0 and 2")
        
        # Validate budget limits
        if self.daily_budget_limit and self.daily_budget_limit <= 0:
            issues.append("Daily budget limit must be positive")
        
        if self.monthly_budget_limit and self.monthly_budget_limit <= 0:
            issues.append("Monthly budget limit must be positive")
        
        return issues
