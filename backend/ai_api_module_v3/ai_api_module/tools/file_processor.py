"""
File processing tool (basic)
"""
from typing import Union
from pathlib import Path
from .base import tool


@tool(name="read_text_file", description="Read a small text file and return its contents")
def read_text_file(path: str) -> str:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(str(path))
    return p.read_text(encoding="utf-8")


