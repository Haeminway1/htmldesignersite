# examples/advanced_features.py
"""
Advanced features examples
"""
import asyncio
from ai_api_module import AI

async def main():
    """Run advanced examples"""
    print("🚀 AI API Module - Advanced Features\n")
    
    ai = AI()
    
    print("=== Conversation Management ===")
    conversation = ai.start_conversation(
        name="Project Planning",
        system="You are a helpful project manager"
    )
    
    conversation.add_user_message("What are the key phases of software development?")
    response1 = conversation.send()
    print(f"PM: {response1.text[:150]}...\n")
    
    conversation.add_user_message("How long should each phase take for a small team?")
    response2 = conversation.send()
    print(f"PM: {response2.text[:150]}...\n")
    
    # Switch models mid-conversation
    conversation.switch_model("creative")
    response3 = conversation.send("What creative approaches could we try?")
    print(f"Creative PM: {response3.text[:150]}...\n")
    
    print(f"Conversation summary:\n{conversation.get_summary()}\n")
    
    print("=== Async Batch Processing ===")
    questions = [
        "What is machine learning?",
        "Explain deep learning",
        "What is natural language processing?",
        "Define computer vision",
        "What is reinforcement learning?"
    ]
    
    responses = await ai.batch_chat(questions, max_concurrent=3, model="fast")
    
    for i, response in enumerate(responses):
        print(f"Q{i+1}: {questions[i]}")
        print(f"A{i+1}: {response.text[:100]}...\n")
    
    print("=== Streaming Response ===")
    print("Streaming story generation:")
    
    async for chunk in ai.stream_chat(
        "Tell me a short story about an AI learning to be creative",
        model="creative"
    ):
        print(chunk, end="", flush=True)
    print("\n\n")
    
    print("=== Provider Comparison ===")
    question = "What is the meaning of life?"
    
    providers = ["openai", "anthropic", "google", "xai"]
    available_providers = [p for p in providers if getattr(ai.config, f"{p}_api_key")]
    
    if len(available_providers) > 1:
        async_handler = ai.async_handler
        results = await async_handler.parallel_providers(
            question, 
            available_providers[:2]  # Compare first 2 available
        )
        
        for provider, response in results.items():
            print(f"{provider.upper()}: {response.text[:100]}...")
            print(f"Cost: ${response.cost:.4f}\n")
    else:
        print("Multiple providers needed for comparison")
    
    print("=== Custom Tools ===")
    @ai.tool
    def get_weather(location: str, unit: str = "celsius") -> dict:
        """Get weather information (mock implementation)"""
        return {
            "location": location,
            "temperature": 22,
            "condition": "sunny",
            "unit": unit
        }
    
    response = ai.chat(
        "What's the weather like in Tokyo?",
        tools=["get_weather"]
    )
    print(f"Tool usage: {response.text}")
    if response.tool_calls:
        print(f"Tool called: {response.tool_calls[0].name}")
        print(f"Arguments: {response.tool_calls[0].arguments}")
    
    print("\n=== Memory System ===")
    ai.memory.add_fact("user_preference", "Prefers concise explanations")
    ai.memory.add_fact("project_type", "Building an AI chatbot")
    
    response = ai.chat(
        "Give me advice for my project",
        use_memory=True
    )
    print(f"Memory-aware response: {response.text}")
    
    print("\n=== Cost Management ===")
    ai.set_budget_limit(daily=1.0)  # $1 daily limit
    
    cost_estimate = ai.estimate_cost(
        "Write a very long detailed analysis of artificial intelligence",
        model="smart"
    )
    print(f"Estimated cost: ${cost_estimate:.4f}")
    
    budget_status = ai.get_usage_stats()
    print(f"Budget remaining: ${budget_status.get('budget_remaining', {}).get('daily', 'unlimited')}")


if __name__ == "__main__":
    asyncio.run(main())