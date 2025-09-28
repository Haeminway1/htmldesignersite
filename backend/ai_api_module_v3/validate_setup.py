# validate_setup.py
"""
Setup validation script
"""
import os
import sys
import importlib
from pathlib import Path

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version >= (3, 9):
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} (3.9+ required)")
        return False

def check_installation():
    """Check if package is installed"""
    try:
        import ai_api_module
        print(f"✅ ai_api_module {ai_api_module.__version__}")
        return True
    except ImportError:
        print("❌ ai_api_module not installed")
        return False

def check_dependencies():
    """Check required dependencies"""
    required = [
        "httpx", "pydantic", "yaml", "PIL", "asyncio", "tenacity"
    ]
    
    missing = []
    for dep in required:
        try:
            if dep == "yaml":
                import yaml
            elif dep == "PIL":
                from PIL import Image
            else:
                importlib.import_module(dep)
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep}")
            missing.append(dep)
    
    return len(missing) == 0

def check_optional_dependencies():
    """Check optional provider dependencies"""
    providers = {
        "openai": "openai",
        "anthropic": "anthropic", 
        "google": "google.genai",
        "xai": "xai_sdk"
    }
    
    available = []
    for provider, module in providers.items():
        try:
            importlib.import_module(module)
            print(f"✅ {provider} SDK")
            available.append(provider)
        except ImportError:
            print(f"⚠️  {provider} SDK (optional)")
    
    return available

def check_api_keys():
    """Check API keys"""
    keys = {
        "OpenAI": "OPENAI_API_KEY",
        "Anthropic": "ANTHROPIC_API_KEY",
        "Google": "GOOGLE_API_KEY", 
        "xAI": "XAI_API_KEY"
    }
    
    available = []
    for provider, env_var in keys.items():
        if os.getenv(env_var):
            print(f"✅ {provider} API key")
            available.append(provider)
        else:
            print(f"⚠️  {provider} API key")
    
    return available

def check_file_structure():
    """Check file structure"""
    required_files = [
        "ai_api_module/__init__.py",
        "ai_api_module/core/ai.py",
        "ai_api_module/providers/base.py",
        "examples/basic_usage.py",
        "README.md"
    ]
    
    missing = []
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing.append(file_path)
    
    return len(missing) == 0

def test_basic_functionality():
    """Test basic functionality"""
    try:
        from ai_api_module import AI
        from ai_api_module.core.response import AIResponse
        from ai_api_module.core.config import Config
        
        # Test config
        config = Config()
        print("✅ Config creation")
        
        # Test AI initialization
        ai = AI()
        print("✅ AI initialization")
        
        # Test model registry
        model, provider = ai.model_registry.resolve("fast", None)
        print("✅ Model resolution")
        
        print("✅ Basic functionality test passed")
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def main():
    """Main validation"""
    print("🔍 AI API Module - Setup Validation")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("Package Installation", check_installation),
        ("Core Dependencies", check_dependencies),
        ("File Structure", check_file_structure),
        ("Basic Functionality", test_basic_functionality),
    ]
    
    results = {}
    
    for check_name, check_func in checks:
        print(f"\n📋 {check_name}:")
        results[check_name] = check_func()
    
    print(f"\n📦 Optional Dependencies:")
    available_providers = check_optional_dependencies()
    
    print(f"\n🔑 API Keys:")
    available_keys = check_api_keys()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 SUMMARY")
    print("=" * 50)
    
    passed = sum(results.values())
    total = len(results)
    
    print(f"Core checks: {passed}/{total} passed")
    print(f"Provider SDKs: {len(available_providers)} available")
    print(f"API keys: {len(available_keys)} configured")
    
    if passed == total and (available_providers or available_keys):
        print("\n🎉 Setup looks good! You're ready to use AI API Module.")
        
        if available_keys:
            print(f"\n💡 You can use these providers: {', '.join(available_keys)}")
        
        print("\n🚀 Next steps:")
        print("  1. python quickstart.py")
        print("  2. python examples/basic_usage.py")
        print("  3. ai-api-module chat 'Hello world'")
        
    else:
        print("\n⚠️  Some issues found. Please check the details above.")
        
        if passed < total:
            print("\n🔧 To fix core issues:")
            print("  1. pip install -e '.[all]'")
            print("  2. Check Python version (3.9+ required)")
        
        if not available_keys:
            print("\n🔑 To add API keys:")
            print("  export OPENAI_API_KEY='your-key'")
            print("  export ANTHROPIC_API_KEY='your-key'")


if __name__ == "__main__":
    main()