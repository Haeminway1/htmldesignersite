"""유틸 스텁"""
from typing import Any

def ensure_text(value: Any) -> str:
    return value if isinstance(value, str) else str(value)
