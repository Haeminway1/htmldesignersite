# ai_api_module/core/exceptions.py
"""
Custom exceptions for AI API Module
"""
from typing import Optional

class AIError(Exception):
    """Base exception for AI API Module"""
    pass


class ProviderError(AIError):
    """Provider-specific error"""
    def __init__(self, message: str, provider: str, original_error: Exception = None):
        super().__init__(message)
        self.provider = provider
        self.original_error = original_error


class RateLimitError(AIError):
    """Rate limit exceeded"""
    def __init__(self, message: str, retry_after: Optional[int] = None):
        super().__init__(message)
        self.retry_after = retry_after


class BudgetExceededError(AIError):
    """Budget limit exceeded"""
    def __init__(self, message: str, current_cost: float, budget_limit: float):
        super().__init__(message)
        self.current_cost = current_cost
        self.budget_limit = budget_limit


class ModelNotAvailableError(AIError):
    """Requested model not available"""
    def __init__(self, message: str, model: str, fallback_model: Optional[str] = None):
        super().__init__(message)
        self.model = model
        self.fallback_model = fallback_model


class AuthenticationError(AIError):
    """API authentication failed"""
    pass


class ValidationError(AIError):
    """Request validation failed"""
    pass


class ContentFilterError(AIError):
    """Content was filtered for safety"""
    pass


class ContextLengthError(AIError):
    """Context length exceeded"""
    pass