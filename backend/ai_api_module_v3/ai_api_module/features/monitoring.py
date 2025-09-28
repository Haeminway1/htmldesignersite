"""
Monitoring stubs (extensible hooks for metrics/logging)
"""
from typing import Optional, Callable, Any, Dict


class Monitor:
    """Simple monitoring hook system."""

    def __init__(self):
        self._on_request: Optional[Callable[[Dict[str, Any]], None]] = None
        self._on_response: Optional[Callable[[Dict[str, Any]], None]] = None

    def on_request(self, handler: Callable[[Dict[str, Any]], None]):
        self._on_request = handler
        return handler

    def on_response(self, handler: Callable[[Dict[str, Any]], None]):
        self._on_response = handler
        return handler

    def emit_request(self, payload: Dict[str, Any]):
        if self._on_request:
            self._on_request(payload)

    def emit_response(self, payload: Dict[str, Any]):
        if self._on_response:
            self._on_response(payload)


