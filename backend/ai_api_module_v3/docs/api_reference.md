# docs/api_reference.md
"""
Complete API Reference
"""
# API Reference

Complete reference for all AI API Module classes and methods.

## Core Classes

### AI

Main interface class for interacting with AI providers.

```python
class AI:
    def __init__(
        self,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        budget_limit: Optional[float] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        debug: bool = False,
        **kwargs
    )
```

#### Methods

##### chat()
```python
def chat(
    self,
    message: str,
    *,
    model: Optional[str] = None,
    provider: Optional[str] = None,
    system: Optional[str] = None,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
    reasoning_effort: Optional[str] = None,
    tools: Optional[List[str]] = None,
    image: Optional[Union[str, Path]] = None,
    images: Optional[List[Union[str, Path]]] = None,
    files: Optional[List[Union[str, Path]]] = None,
    web_search: bool = False,
    stream: bool = False,
    format: Optional[str] = None,
    conversation_id: Optional[str] = None,
    use_memory: bool = False,
    **kwargs
) -> AIResponse
```

Send a chat message and get AI response.

**Parameters:**
- `message`: The message to send
- `model`: Model to use (e.g., "gpt", "claude", "smart", "fast")
- `provider`: Force specific provider
- `system`: System prompt
- `temperature`: Randomness (0-2)
- `max_tokens`: Maximum output tokens
- `reasoning_effort`: "minimal", "low", "medium", "high"
- `tools`: List of tool names to enable
- `image`: Single image path/URL
- `images`: Multiple image paths/URLs
- `files`: List of file paths for analysis
- `web_search`: Enable web search
- `stream`: Stream response
- `format`: Output format ("json", "markdown", etc.)
- `conversation_id`: Continue existing conversation
- `use_memory`: Use long-term memory

**Returns:** AIResponse object

##### async_chat()
```python
async def async_chat(self, message: str, **kwargs) -> AIResponse
```

Async version of chat().

##### batch_chat()
```python
async def batch_chat(
    self, 
    messages: List[str], 
    max_concurrent: int = 5,
    **kwargs
) -> List[AIResponse]
```

Process multiple messages concurrently.

##### stream_chat()
```python
def stream_chat(
    self, 
    message: str, 
    on_chunk=None, 
    on_complete=None,
    **kwargs
) -> AsyncGenerator[str, None]
```

Stream chat response with callbacks.

##### generate_image()
```python
def generate_image(
    self,
    prompt: str,
    *,
    model: Optional[str] = None,
    provider: Optional[str] = None,
    style: str = "natural",
    size: str = "1024x1024",
    quality: str = "standard",
    **kwargs
) -> AIResponse
```

Generate image from text prompt.

##### analyze_image()
```python
def analyze_image(
    self,
    image: Union[str, Path],
    prompt: str,
    **kwargs
) -> AIResponse
```

Analyze image with AI.

##### start_conversation()
```python
def start_conversation(
    self,
    name: Optional[str] = None,
    system: Optional[str] = None,
    **kwargs
) -> Conversation
```

Start a new conversation.

##### estimate_cost()
```python
def estimate_cost(
    self,
    message: str,
    model: Optional[str] = None,
    **kwargs
) -> float
```

Estimate cost before execution.

##### get_usage_stats()
```python
def get_usage_stats(self) -> Dict[str, Any]
```

Get usage statistics.

### AIResponse

Unified response object across all providers.

```python
@dataclass
class AIResponse:
    # Core content
    text: str = ""
    images: List[Image] = field(default_factory=list)
    audio: Optional[Audio] = None
    tool_calls: List[ToolCall] = field(default_factory=list)
    
    # Metadata
    model: str = ""
    provider: str = ""
    usage: Usage = field(default_factory=Usage)
    reasoning: Optional[str] = None
    
    # Context management
    conversation_id: Optional[str] = None
    message_id: str = ""
    
    # Quality metrics
    confidence: float = 1.0
    safety_flags: List[str] = field(default_factory=list)
    
    # Cost tracking
    cost: float = 0.0
    
    # Timing
    timestamp: datetime = field(default_factory=datetime.now)
    response_time: float = 0.0
```

#### Properties

- `has_images`: Check if response contains images
- `has_audio`: Check if response contains audio  
- `has_tool_calls`: Check if response contains tool calls

#### Methods

##### save_images()
```python
def save_images(self, directory: Union[str, Path] = "images")
```

Save all images to directory.

##### to_dict()
```python
def to_dict(self) -> Dict[str, Any]
```

Convert to dictionary.

### Conversation

Manages conversation context and history.

```python
class Conversation:
    def __init__(
        self,
        ai_instance: "AI",
        name: Optional[str] = None,
        system: Optional[str] = None,
        conversation_id: Optional[str] = None
    )
```

#### Methods

##### add_user_message()
```python
def add_user_message(self, content: str, **kwargs) -> "Conversation"
```

Add user message to conversation.

##### send()
```python
def send(self, message: Optional[str] = None, **kwargs) -> AIResponse
```

Send message and get response.

##### switch_model()
```python
def switch_model(self, model: str, provider: Optional[str] = None) -> "Conversation"
```

Switch to different model mid-conversation.

##### save()
```python
def save(self, file_path: Optional[Path] = None) -> Path
```

Save conversation to file.

##### load()
```python
@classmethod
def load(cls, file_path: Path, ai_instance: "AI") -> "Conversation"
```

Load conversation from file.

## Provider Classes

### BaseProvider

Base interface for AI providers.

```python
class BaseProvider(ABC):
    def __init__(self, api_key: str, config: Dict[str, Any])
    
    @abstractmethod
    def chat(self, request_data: Dict[str, Any]) -> AIResponse
    
    @abstractmethod
    async def async_chat(self, request_data: Dict[str, Any]) -> AIResponse
    
    @abstractmethod
    def stream_chat(self, request_data: Dict[str, Any]) -> AsyncGenerator[str, None]
```

### OpenAIProvider

OpenAI provider implementation.

### AnthropicProvider

Anthropic Claude provider implementation.

### GoogleProvider

Google Gemini provider implementation.

### XAIProvider

xAI Grok provider implementation.

## Tool System

### Tool

Base class for AI tools.

```python
class Tool(ABC):
    def __init__(self, name: str, description: str)
    
    @abstractmethod
    def execute(self, **kwargs) -> Any
    
    def get_schema(self) -> Dict[str, Any]
```

### @tool Decorator

```python
def tool(name: str = None, description: str = None):
    """Decorator to create tools from functions"""

@tool(name="calculator", description="Perform calculations")
def calculator(expression: str) -> float:
    return eval(expression)
```

## Configuration

### Config

Configuration management class.

```python
@dataclass
class Config:
    # Provider settings
    default_provider: Optional[str] = None
    default_model: str = "smart"
    
    # API Keys
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    google_api_key: Optional[str] = None
    xai_api_key: Optional[str] = None
    
    # Default parameters
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    
    # Budget and limits
    daily_budget_limit: Optional[float] = None
    monthly_budget_limit: Optional[float] = None
```

## Memory System

### Memory

Manages long-term memory and usage tracking.

```python
class Memory:
    def __init__(self, db_path: Optional[Path] = None)
    
    def add_fact(self, key: str, value: str, category: str = "general")
    def get_fact(self, key: str) -> Optional[str]
    def get_facts_by_category(self, category: str) -> Dict[str, str]
    
    def add_usage_record(self, record: Dict[str, Any])
    def get_daily_cost(self, date: Optional[datetime] = None) -> float
    def get_monthly_cost(self, year: int = None, month: int = None) -> float
```

## Async Features

### AsyncHandler

Handles async operations and batch processing.

```python
class AsyncHandler:
    async def chat(self, message: str, **kwargs) -> AIResponse
    async def batch_chat(
        self, 
        messages: List[str], 
        max_concurrent: int = 5,
        **kwargs
    ) -> List[AIResponse]
    async def parallel_providers(
        self,
        message: str,
        providers: List[str],
        **kwargs
    ) -> Dict[str, AIResponse]
```

### StreamingHandler

Handles streaming responses.

```python
class StreamingHandler:
    async def stream(self, request_data: Dict[str, Any]) -> AsyncGenerator[str, None]
    async def stream_with_callbacks(
        self,
        message: str,
        on_chunk: Optional[Callable[[str], None]] = None,
        on_complete: Optional[Callable[[AIResponse], None]] = None,
        **kwargs
    ) -> AsyncGenerator[str, None]
```

## Exceptions

```python
class AIError(Exception): 
    """Base exception"""

class ProviderError(AIError):
    """Provider-specific error"""

class RateLimitError(AIError):
    """Rate limit exceeded"""

class BudgetExceededError(AIError):
    """Budget limit exceeded"""

class ModelNotAvailableError(AIError):
    """Requested model not available"""

class AuthenticationError(AIError):
    """API authentication failed"""
```

## Model Registry

### ModelRegistry

Manages model aliases and routing.

```python
class ModelRegistry:
    def resolve(self, model: str, provider: Optional[str] = None) -> Tuple[str, str]
    def resolve_image_model(self, model: Optional[str], provider: Optional[str]) -> Tuple[str, str]
    def estimate_cost(self, text: str, model: str, **kwargs) -> float
    def get_cheapest_model(self, capability: str = "text") -> str
    def get_fastest_model(self, capability: str = "text") -> str
    def get_best_model(self, capability: str = "text") -> str
```

## CLI Reference

### Commands

```bash
# Chat
ai-api-module chat "message" [options]

# Image generation
ai-api-module image "prompt" [options]

# Conversation management
ai-api-module conversation start [options]
ai-api-module conversation continue file message
ai-api-module conversation list

# Audio
ai-api-module audio speak "text" [options]
ai-api-module audio transcribe file

# Utilities
ai-api-module providers
ai-api-module models
ai-api-module stats
ai-api-module config
ai-api-module estimate "message" [options]
```

### Options

Common options across commands:
- `--model, -m`: Model to use
- `--provider, -p`: Provider to use  
- `--output, -o`: Output file
- `--temperature, -t`: Temperature setting
- `--max-tokens`: Maximum output tokens
- `--stream`: Stream response
- `--web-search`: Enable web search

## Environment Variables

```bash
# API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...
XAI_API_KEY=xai-...

# Configuration
AI_DEFAULT_PROVIDER=openai
AI_DEFAULT_MODEL=smart
AI_DAILY_BUDGET_LIMIT=10.0
AI_MONTHLY_BUDGET_LIMIT=100.0
AI_DEBUG=false
AI_LOG_LEVEL=INFO
```