"""
Simple calculator tool
"""
from .base import tool


@tool(name="calculator", description="Safely evaluate basic arithmetic expressions")
def calculate(expression: str) -> float:
    # Very limited safe eval for arithmetic
    allowed = set("0123456789+-*/(). %")
    if not set(expression) <= allowed:
        raise ValueError("Invalid characters in expression")
    return float(eval(expression, {"__builtins__": {}}, {}))


