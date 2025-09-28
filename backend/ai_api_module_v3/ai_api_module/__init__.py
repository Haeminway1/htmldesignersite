"""AI API Module - Unified interface for multiple AI providers."""

# Ensure relative imports work even when the package is executed from a
# cloned repository without installation.
from .bootstrap import ensure_path as _ensure_path  # noqa: F401

from .core.ai import AI
from .core.response import AIResponse
from .core.conversation import Conversation
from .core.exceptions import *  # noqa: F401,F403
from .tools.base import tool

__version__ = "0.1.0"
__all__ = [
    "AI",
    "AIResponse", 
    "Conversation",
    "tool",
    # Exceptions
    "AIError",
    "ProviderError",
    "RateLimitError",
    "BudgetExceededError",
    "ModelNotAvailableError",
]