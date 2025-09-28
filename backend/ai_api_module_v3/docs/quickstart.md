# docs/quickstart.md
"""
Quick Start Guide
"""
# Quick Start Guide

This guide will get you up and running with AI API Module in under 5 minutes.

## Prerequisites

- Python 3.9 or higher
- At least one AI provider API key

## Installation

### Option 1: Git Clone (Recommended)

```bash
git clone https://github.com/your-org/ai-api-module
cd ai-api-module
chmod +x install.sh
./install.sh
```

### Option 2: Package Install

```bash
pip install ai-api-module[all]
```

## Setup API Keys

Set environment variables for your AI providers:

```bash
# At least one is required
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export GOOGLE_API_KEY="..."
export XAI_API_KEY="xai-..."
```

### Getting API Keys

- **OpenAI**: https://platform.openai.com/api-keys
- **Anthropic**: https://console.anthropic.com/settings/keys
- **Google**: https://console.cloud.google.com/apis/credentials
- **xAI**: https://console.x.ai/settings/keys

## Verify Installation

```bash
python validate_setup.py
```

## First Steps

### 1. Interactive Quickstart

```bash
python quickstart.py
```

### 2. Basic Usage

```python
from ai_api_module import AI

# Initialize
ai = AI()

# Simple chat
response = ai.chat("What is machine learning?")
print(response.text)
```

### 3. CLI Usage

```bash
# Chat
ai-api-module chat "Explain quantum computing"

# Generate image
ai-api-module image "A sunset over mountains" --output sunset.png

# Check stats
ai-api-module stats
```

## Example Workflows

### Smart Model Selection

```python
ai = AI()

# Automatic model selection based on task
ai.chat("Complex reasoning problem")  # → Uses best reasoning model
ai.chat("Simple question", model="fast")  # → Uses fastest model
ai.chat("Creative writing", model="creative")  # → Uses creative model
```

### Conversation Management

```python
# Start conversation
conversation = ai.start_conversation(
    name="Project Planning",
    system="You are a helpful project manager"
)

# Send messages
conversation.add_user_message("What are the key phases?")
response = conversation.send()

# Continue conversation
response = conversation.send("How long should each phase take?")

# Save conversation
conversation.save("project_planning.json")
```

### Cost Management

```python
# Set budget
ai.set_budget_limit(daily=5.0)

# Estimate cost before sending
cost = ai.estimate_cost("Long message...", model="smart")
print(f"Estimated cost: ${cost:.4f}")

# Enable cost optimization
ai.enable_cost_optimization(prefer_cheaper_models=True)
```

## Common Use Cases

### 1. Content Generation

```python
# Blog post
response = ai.chat(
    "Write a blog post about AI safety",
    model="creative",
    max_tokens=1000
)

# Code generation
response = ai.chat(
    "Write a Python function to sort a list",
    model="coding"
)
```

### 2. Data Analysis

```python
# Analyze document
response = ai.analyze_document(
    "report.pdf",
    "Summarize the key findings and recommendations"
)

# Analyze image
response = ai.analyze_image(
    "chart.png", 
    "What trends do you see in this data?"
)
```

### 3. Research Assistant

```python
# Web search
response = ai.chat(
    "What are the latest developments in renewable energy?",
    web_search=True
)

# Multi-provider comparison
results = await ai.async_handler.parallel_providers(
    "What is the future of AI?",
    ["openai", "anthropic"]
)
```

## Running Examples

```bash
# Run all examples
python run_examples.py

# Run specific example
python examples/basic_usage.py
python examples/advanced_features.py
python examples/multimodal_examples.py
```

## Troubleshooting

### Common Issues

1. **No API keys found**
   ```bash
   export OPENAI_API_KEY="your-key-here"
   ```

2. **Import errors**
   ```bash
   pip install -e ".[all]"
   ```

3. **Provider not available**
   ```bash
   ai-api-module providers  # Check available providers
   ```

### Getting Help

- Check the [full documentation](README.md)
- Run `ai-api-module --help`
- Look at [examples/](examples/)
- Open an issue on GitHub

## Next Steps

Once you're comfortable with the basics:

1. **Explore Advanced Features**: async, streaming, tools
2. **Set Up Monitoring**: usage tracking, cost optimization
3. **Build Integrations**: add custom tools and providers
4. **Deploy**: use in production applications

You're now ready to build amazing AI-powered applications! 🚀
