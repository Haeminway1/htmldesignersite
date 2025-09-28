# ai_api_module/quickstart.py
"""
Quick start interactive script
"""
import os
import sys
from pathlib import Path

def main():
    """Interactive quickstart script"""
    print("🤖 AI API Module - Quick Start Setup")
    print("=" * 50)
    
    # Check installation
    try:
        from ai_api_module import AI
        print("✅ AI API Module is installed")
    except ImportError:
        print("❌ AI API Module not found. Please install it first:")
        print("   pip install -e .")
        return
    
    # Check API keys
    api_keys = {
        "OpenAI": os.getenv("OPENAI_API_KEY"),
        "Anthropic": os.getenv("ANTHROPIC_API_KEY"),
        "Google": os.getenv("GOOGLE_API_KEY"),
        "xAI": os.getenv("XAI_API_KEY")
    }
    
    available_providers = []
    print("\n🔑 API Key Status:")
    for provider, key in api_keys.items():
        if key:
            print(f"  ✅ {provider}: Set")
            available_providers.append(provider.lower())
        else:
            print(f"  ❌ {provider}: Not set")
    
    if not available_providers:
        print("\n⚠️  No API keys found!")
        print("Please set at least one API key:")
        print("  export OPENAI_API_KEY='your-key'")
        print("  export ANTHROPIC_API_KEY='your-key'")
        print("  export GOOGLE_API_KEY='your-key'")
        print("  export XAI_API_KEY='your-key'")
        return
    
    print(f"\n🚀 Found {len(available_providers)} provider(s): {', '.join(available_providers)}")
    
    # Interactive demo
    print("\n" + "=" * 50)
    print("Interactive Demo")
    print("=" * 50)
    
    try:
        ai = AI()
        
        print("Let's try a simple chat:")
        
        while True:
            user_input = input("\n💬 You (or 'quit' to exit): ")
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
            
            if not user_input.strip():
                continue
            
            try:
                print("🤔 Thinking...")
                response = ai.chat(user_input, model="fast")
                
                print(f"🤖 AI: {response.text}")
                print(f"💰 Cost: ${response.cost:.4f} | 🔧 Model: {response.model}")
                
            except Exception as e:
                print(f"❌ Error: {e}")
    
    except KeyboardInterrupt:
        print("\n\n👋 Thanks for trying AI API Module!")
    except Exception as e:
        print(f"\n❌ Setup error: {e}")
        return
    
    # Show next steps
    print("\n" + "=" * 50)
    print("🎯 Next Steps:")
    print("1. Try the examples: python examples/basic_usage.py")
    print("2. Read the documentation: README.md")
    print("3. Explore advanced features: examples/advanced_features.py")
    print("4. Use the CLI: ai-api-module chat 'Hello world'")
    print("5. Check usage stats: ai-api-module stats")
    print("\n📖 Documentation: https://github.com/your-org/ai-api-module")
    print("🐛 Issues: https://github.com/your-org/ai-api-module/issues")


if __name__ == "__main__":
    main()