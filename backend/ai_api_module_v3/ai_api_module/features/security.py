"""
Security stubs (sanitization/rate limiting placeholders)
"""
from typing import Dict, Any


def sanitize_input(text: str, max_len: int = 10000) -> str:
    text = text.strip()
    if len(text) > max_len:
        return text[:max_len]
    return text


def redact_sensitive(data: Dict[str, Any]) -> Dict[str, Any]:
    redacted = {}
    for k, v in data.items():
        if "key" in k.lower() or "token" in k.lower():
            redacted[k] = "***"
        else:
            redacted[k] = v
    return redacted


