"""
Web search tool (stub) used by providers/tools interface
"""
from typing import List, Dict, Any
from .base import tool


@tool(name="web_search", description="Search the web for current information (stub)")
def web_search(query: str, max_results: int = 5) -> Dict[str, Any]:
    # Stub implementation to satisfy tooling interface
    # In production, integrate a real web search API.
    return {
        "query": query,
        "results": [
            {"title": f"Result {i+1} for {query}", "url": f"https://example.com/{i+1}"}
            for i in range(max_results)
        ],
    }


