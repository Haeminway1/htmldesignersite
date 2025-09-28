# tests/test_tools.py
"""
Tool functionality tests
"""
import pytest
from unittest.mock import Mock, patch
from ai_api_module.tools.calculator import calculate
from ai_api_module.tools.web_search import web_search
from ai_api_module.tools.file_processor import read_text_file
from ai_api_module.tools.image_processor import image_info
from ai_api_module.tools.base import Tool, tool
from ai_api_module.core.response import AIResponse
import tempfile
import os


class TestBaseTool:
    """Test base tool functionality"""
    
    def test_tool_decorator(self):
        """Test tool decorator functionality"""
        @tool(name="test_tool", description="A test tool")
        def test_function(x: int, y: str = "default") -> dict:
            return {"x": x, "y": y}
        
        assert hasattr(test_function, 'name')
        assert test_function.name == "test_tool"
        assert hasattr(test_function, 'description')
        assert test_function.description == "A test tool"
    
    def test_tool_schema_generation(self):
        """Test tool schema generation"""
        @tool(name="schema_test", description="Schema test tool")
        def schema_function(required_param: str, optional_param: int = 42) -> dict:
            return {"required": required_param, "optional": optional_param}
        
        schema = schema_function.get_schema()
        
        assert schema["name"] == "schema_test"
        assert schema["description"] == "Schema test tool"
        assert "parameters" in schema
        assert "required_param" in schema["parameters"]["properties"]
        assert "optional_param" in schema["parameters"]["properties"]
        assert "required_param" in schema["parameters"]["required"]
        assert "optional_param" not in schema["parameters"]["required"]


class TestCalculator:
    """Test calculator tool"""
    
    def test_calculator_basic_operations(self):
        """Test basic calculator operations"""
        # Addition
        result = calculate.execute(expression="2 + 3")
        assert result == 5.0
        
        # Multiplication
        result = calculate.execute(expression="4 * 5")
        assert result == 20.0
        
        # Complex expression
        result = calculate.execute(expression="(10 + 5) * 2")
        assert result == 30.0
    
    def test_calculator_error_handling(self):
        """Test calculator error handling"""
        # Division by zero
        with pytest.raises(ZeroDivisionError):
            calculate.execute(expression="5 / 0")
        
        # Invalid expression
        with pytest.raises(ValueError):
            calculate.execute(expression="import os")
    
    def test_calculator_schema(self):
        """Test calculator schema"""
        schema = calculate.get_schema()
        
        assert schema["name"] == "calculator"
        assert "expression" in schema["parameters"]["properties"]


class TestWebSearch:
    """Test web search tool"""
    
    def test_web_search_basic(self):
        """Test basic web search"""
        result = web_search.execute(query="test query", max_results=3)
        
        assert isinstance(result, dict)
        assert "query" in result
        assert "results" in result
        assert result["query"] == "test query"
        assert len(result["results"]) == 3
    
    def test_web_search_schema(self):
        """Test web search schema"""
        schema = web_search.get_schema()
        
        assert schema["name"] == "web_search"
        assert "query" in schema["parameters"]["properties"]
        assert "max_results" in schema["parameters"]["properties"]


class TestFileProcessor:
    """Test file processor tool"""
    
    def test_file_processor_text_file(self, tmp_path):
        """Test processing text file"""
        # Create test file
        test_file = tmp_path / "test.txt"
        test_content = "This is a test document with important information."
        test_file.write_text(test_content, encoding='utf-8')
        
        result = read_text_file.execute(path=str(test_file))
        
        assert result == test_content
    
    def test_file_processor_nonexistent_file(self):
        """Test handling nonexistent file"""
        with pytest.raises(FileNotFoundError):
            read_text_file.execute(path="nonexistent_file.txt")
    
    def test_file_processor_schema(self):
        """Test file processor schema"""
        schema = read_text_file.get_schema()
        
        assert schema["name"] == "read_text_file"
        assert "path" in schema["parameters"]["properties"]


class TestImageProcessor:
    """Test image processor tool"""
    
    def test_image_processor_schema(self):
        """Test image processor schema"""
        schema = image_info.get_schema()
        
        assert schema["name"] == "image_info"
        assert "path" in schema["parameters"]["properties"]
    
    @patch('ai_api_module.tools.image_processor.get_image_info')
    @patch('ai_api_module.tools.image_processor.process_image')
    def test_image_processor_basic(self, mock_process, mock_get_info, tmp_path):
        """Test basic image processing"""
        # Create test image file
        test_file = tmp_path / "test.jpg"
        test_file.write_bytes(b"fake image data")
        
        # Mock return values
        mock_process.return_value = (b"processed_data", "jpeg")
        mock_get_info.return_value = {
            "width": 1024,
            "height": 768,
            "format": "JPEG",
            "mode": "RGB"
        }
        
        result = image_info.execute(path=str(test_file))
        
        assert "width" in result
        assert "height" in result
        assert "format" in result
        assert result["width"] == 1024
        assert result["height"] == 768


class TestToolIntegration:
    """Test tool integration with AI"""
    
    def test_tool_execution(self):
        """Test tool execution"""
        # Test calculator tool
        calc_result = calculate.execute(expression="2 + 2")
        assert calc_result == 4.0
        
        # Test web search tool
        search_result = web_search.execute(query="test", max_results=2)
        assert search_result["query"] == "test"
        assert len(search_result["results"]) == 2
    
    def test_tool_chaining(self, tmp_path):
        """Test chaining multiple tools"""
        # First tool: calculate something
        calc_result = calculate.execute(expression="10 * 5")
        assert calc_result == 50.0
        
        # Second tool: process a file (with temp file)
        test_file = tmp_path / "result.txt"
        test_file.write_text(f"The calculation result is {calc_result}", encoding='utf-8')
        
        file_result = read_text_file.execute(path=str(test_file))
        assert "50.0" in file_result
    
    def test_multiple_tools_list(self):
        """Test creating list of tools"""
        tools = [calculate, web_search, read_text_file, image_info]
        
        assert len(tools) == 4
        assert all(hasattr(tool, 'name') for tool in tools)
        assert all(hasattr(tool, 'get_schema') for tool in tools)
    
    def test_tool_schema_collection(self):
        """Test collecting schemas from multiple tools"""
        tools = [calculate, web_search, read_text_file]
        schemas = [tool.get_schema() for tool in tools]
        
        assert len(schemas) == 3
        
        names = [schema["name"] for schema in schemas]
        assert "calculator" in names
        assert "web_search" in names
        assert "read_text_file" in names


class TestCustomToolCreation:
    """Test creating custom tools"""
    
    def test_custom_tool_decorator(self):
        """Test creating custom tool with decorator"""
        @tool(name="custom_add", description="Add two numbers")
        def add_numbers(a: int, b: int) -> int:
            return a + b
        
        result = add_numbers.execute(a=5, b=3)
        assert result == 8
        
        schema = add_numbers.get_schema()
        assert schema["name"] == "custom_add"
        assert "a" in schema["parameters"]["properties"]
        assert "b" in schema["parameters"]["properties"]
    
    def test_tool_with_complex_types(self):
        """Test tool with complex parameter types"""
        @tool(name="complex_tool", description="Tool with complex types")
        def complex_function(
            text: str,
            number: int,
            ratio: float,
            flag: bool,
            items: list,
            config: dict
        ) -> dict:
            return {
                "text": text,
                "number": number,
                "ratio": ratio,
                "flag": flag,
                "items": items,
                "config": config
            }
        
        schema = complex_function.get_schema()
        props = schema["parameters"]["properties"]
        
        assert props["text"]["type"] == "string"
        assert props["number"]["type"] == "integer"
        assert props["ratio"]["type"] == "number"
        assert props["flag"]["type"] == "boolean"
        assert props["items"]["type"] == "array"
        assert props["config"]["type"] == "object"


# Integration tests that would require real APIs
@pytest.mark.integration
class TestToolsIntegration:
    """Integration tests for tools with real APIs"""
    
    def test_real_file_processing(self, tmp_path):
        """Test real file processing"""
        # Create a real test file
        test_file = tmp_path / "integration_test.txt"
        test_content = "This is an integration test for file processing."
        test_file.write_text(test_content, encoding='utf-8')
        
        result = read_text_file.execute(path=str(test_file))
        assert result == test_content
    
    def test_tool_with_ai_provider(self):
        """Test tools working with AI provider"""
        # This would test the full integration
        # For now, just ensure our tools are properly structured
        tools = [calculate, web_search, read_text_file, image_info]
        
        for tool in tools:
            assert hasattr(tool, 'get_schema')
            schema = tool.get_schema()
            assert "name" in schema
            assert "description" in schema
            assert "parameters" in schema
