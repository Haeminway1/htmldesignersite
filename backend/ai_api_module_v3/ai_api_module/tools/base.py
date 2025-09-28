# ai_api_module/tools/base.py
"""
Base tool system
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Callable, List
import inspect


class Tool(ABC):
    """Base class for AI tools"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    def execute(self, **kwargs) -> Any:
        """Execute the tool"""
        pass
    
    def get_schema(self) -> Dict[str, Any]:
        """Get JSON schema for the tool"""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self._generate_schema()
        }
    
    def _generate_schema(self) -> Dict[str, Any]:
        """Generate JSON schema from function signature"""
        # For FunctionTool, use the original function signature
        if hasattr(self, 'func'):
            sig = inspect.signature(self.func)
        else:
            sig = inspect.signature(self.execute)
            
        properties = {}
        required = []
        
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
                
            param_schema = {"type": "string"}  # Default type
            
            # Try to infer type from annotation
            if param.annotation != inspect.Parameter.empty:
                if param.annotation == int:
                    param_schema["type"] = "integer"
                elif param.annotation == float:
                    param_schema["type"] = "number"
                elif param.annotation == bool:
                    param_schema["type"] = "boolean"
                elif param.annotation == list:
                    param_schema["type"] = "array"
                elif param.annotation == dict:
                    param_schema["type"] = "object"
            
            properties[param_name] = param_schema
            
            # Check if parameter is required
            if param.default == inspect.Parameter.empty:
                required.append(param_name)
        
        return {
            "type": "object",
            "properties": properties,
            "required": required
        }


def tool(name: str = None, description: str = None):
    """Decorator to create tools from functions"""
    def decorator(func: Callable) -> Tool:
        tool_name = name or func.__name__
        tool_description = description or func.__doc__ or f"Tool: {tool_name}"
        
        class FunctionTool(Tool):
            def __init__(self):
                super().__init__(tool_name, tool_description)
                self.func = func
            
            def execute(self, **kwargs) -> Any:
                return self.func(**kwargs)
        
        return FunctionTool()
    
    return decorator