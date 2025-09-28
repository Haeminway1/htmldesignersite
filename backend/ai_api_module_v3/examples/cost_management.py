# examples/cost_management.py
"""
Cost management and optimization examples
"""
from ai_api_module import AI
import time

def main():
    """Run cost management examples"""
    print("💰 AI API Module - Cost Management Examples\n")
    
    ai = AI()
    
    print("=== Cost Estimation ===")
    prompts = [
        "Short question about AI",
        "Write a comprehensive analysis of machine learning algorithms, including detailed explanations of supervised, unsupervised, and reinforcement learning approaches with practical examples",
        "Generate a detailed technical specification document for a new software project"
    ]
    
    for i, prompt in enumerate(prompts, 1):
        estimate = ai.estimate_cost(prompt, model="smart")
        print(f"Prompt {i}: ${estimate:.4f} estimated")
        print(f"  Length: {len(prompt)} characters")
        print(f"  Preview: {prompt[:50]}...\n")
    
    print("=== Model Cost Comparison ===")
    test_prompt = "Explain the difference between AI and machine learning"
    
    models = ["fast", "smart", "creative"]
    for model in models:
        estimate = ai.estimate_cost(test_prompt, model=model)
        print(f"{model:10}: ${estimate:.4f} estimated")
    
    print("\n=== Budget Management ===")
    # Set budget limits
    ai.set_budget_limit(daily=0.50, monthly=10.0)
    
    print("Set daily budget: $0.50")
    print("Set monthly budget: $10.00")
    
    # Check current usage
    stats = ai.get_usage_stats()
    print(f"Current usage: ${stats['total_cost']:.4f}")
    
    print("\n=== Cost Optimization ===")
    ai.enable_cost_optimization(
        prefer_cheaper_models=True,
        aggressive_caching=True,
        smart_routing=True
    )
    
    print("Enabled cost optimization features")
    
    # Test with optimization
    questions = [
        "What is Python?",
        "What is Python?",  # Same question for cache test
        "Explain machine learning",
        "What is deep learning?"
    ]
    
    total_cost = 0
    for i, question in enumerate(questions, 1):
        start_time = time.time()
        response = ai.chat(question, model="cheap")
        end_time = time.time()
        
        total_cost += response.cost
        
        print(f"Q{i}: {question}")
        print(f"  Model used: {response.model}")
        print(f"  Cost: ${response.cost:.4f}")
        print(f"  Time: {end_time - start_time:.2f}s")
        print(f"  Cached: {hasattr(response, 'cached') and response.cached}")
        print(f"  Answer: {response.text[:80]}...\n")
    
    print(f"Total cost for batch: ${total_cost:.4f}")
    
    print("=== Usage Analytics ===")
    usage_stats = ai.get_usage_stats()
    print(f"Total requests: {usage_stats['request_count']}")
    print(f"Total cost: ${usage_stats['total_cost']:.4f}")
    
    # Detailed memory stats
    memory_stats = ai.memory.get_usage_stats(days=1)
    print(f"\nDetailed Usage (last 24h):")
    print(f"  Requests: {memory_stats['total_requests']}")
    print(f"  Cost: ${memory_stats['total_cost']:.4f}")
    print(f"  Avg cost/request: ${memory_stats['avg_cost_per_request']:.4f}")
    print(f"  Total tokens: {memory_stats['total_tokens']:,}")
    
    if memory_stats['model_usage']:
        print("\nModel Usage:")
        for model_stat in memory_stats['model_usage'][:3]:
            print(f"  {model_stat['model']}: {model_stat['requests']} requests, ${model_stat['cost']:.4f}")
    
    if memory_stats['provider_usage']:
        print("\nProvider Usage:")
        for provider_stat in memory_stats['provider_usage']:
            print(f"  {provider_stat['provider']}: {provider_stat['requests']} requests, ${provider_stat['cost']:.4f}")
    
    print("\n=== Cache Performance ===")
    if ai.cache:
        cache_stats = ai.cache.get_stats()
        print(f"Cache entries: {cache_stats['memory_entries']} in memory, {cache_stats['disk_entries']} on disk")
        print(f"Cache duration: {cache_stats['duration']} seconds")
        print(f"Max cache size: {cache_stats['max_size']} entries")
    else:
        print("Caching not enabled")
    
    print("\n=== Budget Alerts ===")
    try:
        # Try to exceed budget (will raise exception)
        expensive_response = ai.chat(
            "Write a very detailed 10,000 word essay about artificial intelligence" * 10,
            model="smart",
            max_tokens=8000
        )
    except Exception as e:
        print(f"Budget protection triggered: {e}")
    
    print("\n=== Recommendations ===")
    print("💡 Cost Optimization Tips:")
    print("1. Use 'fast' or 'cheap' models for simple tasks")
    print("2. Enable caching for repeated queries")
    print("3. Set budget limits to prevent overspending")
    print("4. Monitor usage with get_usage_stats()")
    print("5. Use estimate_cost() before expensive operations")
    print("6. Batch similar requests when possible")


if __name__ == "__main__":
    main()