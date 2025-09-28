# examples/basic_usage.py
"""
Basic usage examples for AI API Module
"""
import os
from ai_api_module import AI

def main():
    """Run basic examples"""
    print("🤖 AI API Module - Basic Usage Examples\n")
    
    # Initialize AI
    ai = AI()
    
    print("=== Basic Text Generation ===")
    response = ai.chat("Write a haiku about programming")
    print(f"Response: {response.text}")
    print(f"Model: {response.model}")
    print(f"Cost: ${response.cost:.4f}\n")
    
    print("=== With System Prompt ===")
    response = ai.chat(
        "Explain quantum computing",
        system="You are a physics professor. Be concise but accurate.",
        temperature=0.3
    )
    print(f"Response: {response.text}")
    print(f"Usage: {response.usage.total_tokens} tokens\n")
    
    print("=== Using Different Models ===")
    for model in ["fast", "smart", "creative"]:
        response = ai.chat(f"Tell me about {model} AI", model=model)
        print(f"{model.upper()}: {response.text[:100]}...")
        print(f"Model used: {response.model}, Cost: ${response.cost:.4f}\n")
    
    print("=== Image Analysis (if image file exists) ===")
    try:
        response = ai.analyze_image(
            "example_image.jpg",  # You'd need to provide this
            "What do you see in this image?"
        )
        print(f"Image analysis: {response.text}")
    except FileNotFoundError:
        print("No example image found, skipping image analysis")
    
    print("=== Web Search (if enabled) ===")
    try:
        response = ai.chat(
            "What are the latest developments in AI?",
            web_search=True
        )
        print(f"Web search result: {response.text[:200]}...")
    except Exception as e:
        print(f"Web search not available: {e}")
    
    print("=== Usage Statistics ===")
    stats = ai.get_usage_stats()
    print(f"Total cost: ${stats['total_cost']:.4f}")
    print(f"Total requests: {stats['request_count']}")


if __name__ == "__main__":
    main()
