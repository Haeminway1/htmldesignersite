"""
Compatibility re-exports for exceptions.
Allows `from ai_api_module.exceptions import ...` as used in docs.
"""
from .core.exceptions import *  # noqa: F401,F403

__all__ = [
    # Explicitly mirror core.exceptions exports
    "AIError",
    "ProviderError",
    "RateLimitError",
    "BudgetExceededError",
    "ModelNotAvailableError",
    "AuthenticationError",
    "ValidationError",
    "ContentFilterError",
    "ContextLengthError",
]


