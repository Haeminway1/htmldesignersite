# README.md
"""
AI API Module - Complete README
"""
# 🤖 AI API Module

A unified, production-ready interface for multiple AI providers (OpenAI, Anthropic, Google, xAI) with advanced features like cost management, conversation handling, and multimodal capabilities.

## ✨ Features

- **🔄 Unified Interface**: Single API for OpenAI, Anthropic, Google, and xAI
- **💰 Cost Management**: Built-in budget tracking and optimization
- **🗣️ Conversation Management**: Persistent conversations with context
- **🚀 Async Support**: Batch processing and concurrent requests
- **🎨 Multimodal**: Text, images, audio, and document processing
- **⚡ Streaming**: Real-time response streaming
- **🧠 Memory**: Long-term memory and fact storage
- **🔧 Tools**: Custom function calling and tool integration
- **📊 Analytics**: Detailed usage tracking and insights
- **🎯 Smart Routing**: Automatic model selection for tasks

## 🚀 완전 초보자 가이드 (복사-붙여넣기 가능)

### 1단계: 프로젝트 설치

```bash
# 저장소 클론
git clone https://github.com/your-org/ai-api-module
cd ai-api-module

# 모든 AI 프로바이더 설치
pip install -e ".[all]"

# 특정 프로바이더만 설치하려면
pip install -e ".[openai,anthropic]"
```

### 2단계: API 키 설정

**Windows (PowerShell):**
```powershell
# 임시 설정 (터미널 세션 동안만 유효)
$env:OPENAI_API_KEY="sk-proj-..."
$env:ANTHROPIC_API_KEY="sk-ant-..."
$env:GOOGLE_API_KEY="AIza..."
$env:XAI_API_KEY="xai-..."

# 영구 설정 (재부팅 후에도 유지)
[Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "sk-proj-...", "User")
[Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "sk-ant-...", "User")
```

**macOS/Linux (bash/zsh):**
```bash
# 터미널에서 실행
export OPENAI_API_KEY="sk-proj-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export GOOGLE_API_KEY="AIza..."
export XAI_API_KEY="xai-..."

# 영구 설정을 원한다면 ~/.bashrc 또는 ~/.zshrc에 추가
echo 'export OPENAI_API_KEY="sk-proj-..."' >> ~/.bashrc
echo 'export ANTHROPIC_API_KEY="sk-ant-..."' >> ~/.bashrc
```

**Python 코드 내에서 직접 설정:**
```python
import os
os.environ["OPENAI_API_KEY"] = "sk-proj-..."
os.environ["ANTHROPIC_API_KEY"] = "sk-ant-..."
```

### 3단계: 기본 사용법 (복사해서 바로 실행)

```python
# 가장 기본적인 AI 채팅
from ai_api_module import AI

ai = AI()
response = ai.chat("안녕하세요! 오늘 날씨가 어때요?")
print(response.text)
```

### 4단계: 완전한 예제 스크립트 (test_basic.py)

이 스크립트를 파일로 저장하고 실행하세요:

```python
# test_basic.py
from ai_api_module import AI
import json

def main():
    # AI 인스턴스 생성
    ai = AI()
    
    print("🤖 AI API Module 테스트 시작!")
    print("="*50)
    
    # 1. 기본 텍스트 생성
    print("\n1️⃣ 기본 텍스트 생성 테스트")
    response = ai.chat("파이썬으로 'Hello World'를 출력하는 코드를 작성해주세요.")
    print(f"📝 응답: {response.text}")
    print(f"💰 비용: ${response.cost:.6f}")
    print(f"🤖 모델: {response.model}")
    
    # 2. JSON 형식 출력
    print("\n2️⃣ JSON 형식 출력 테스트")
    response = ai.chat(
        "파이썬의 장점 3가지를 JSON 형식으로 말해줘",
        format="json"
    )
    print(f"📊 구조화된 데이터: {json.dumps(response.structured_data, indent=2, ensure_ascii=False)}")
    
    # 3. 특정 모델 사용
    print("\n3️⃣ 특정 모델 사용 테스트")
response = ai.chat(
        "머신러닝을 한 줄로 설명해주세요",
        model="fast",  # 빠른 모델 사용
        max_tokens=50
    )
    print(f"⚡ 빠른 응답: {response.text}")
    
    print("\n✅ 모든 기본 테스트 완료!")

if __name__ == "__main__":
    main()
```

### 5단계: 이미지 생성 및 분석 (image_test.py)

```python
# image_test.py
from ai_api_module import AI
import os

def test_image_features():
    ai = AI()
    
    print("🎨 이미지 기능 테스트 시작!")
    print("="*40)
    
    # 1. 이미지 생성
    print("\n1️⃣ 이미지 생성 테스트")
    try:
        response = ai.generate_image(
            "아름다운 일몰이 있는 산과 호수",
            style="photorealistic",
            size="1024x1024"
        )
        
        if response.images:
            image_path = "generated_sunset.png"
            response.images[0].save(image_path)
            print(f"✅ 이미지 생성 완료: {image_path}")
            print(f"💰 비용: ${response.cost:.6f}")
        else:
            print("❌ 이미지 생성 실패")
    except Exception as e:
        print(f"❌ 이미지 생성 오류: {e}")
    
    # 2. 이미지 분석 (생성된 이미지가 있다면)
    if os.path.exists("generated_sunset.png"):
        print("\n2️⃣ 이미지 분석 테스트")
        try:
            response = ai.analyze_image(
                "generated_sunset.png",
                "이 이미지에서 무엇을 볼 수 있나요? 색감과 분위기도 설명해주세요."
            )
            print(f"🔍 이미지 분석 결과: {response.text}")
            print(f"💰 비용: ${response.cost:.6f}")
        except Exception as e:
            print(f"❌ 이미지 분석 오류: {e}")

if __name__ == "__main__":
    test_image_features()
```

### 6단계: 문서 처리 (document_test.py)

```python
# document_test.py
from ai_api_module import AI
import tempfile
import os

def test_document_features():
    ai = AI()
    
    print("📄 문서 처리 테스트 시작!")
    print("="*40)
    
    # 임시 텍스트 파일 생성
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
        f.write("""
        프로젝트 계획서
        
        1. 목표: AI 기반 채팅봇 개발
        2. 기간: 3개월
        3. 예산: 50만원
        4. 팀원: 3명 (개발자 2명, 디자이너 1명)
        5. 주요 기술: Python, FastAPI, OpenAI API
        
        주요 일정:
        - 1개월차: 기본 설계 및 프로토타입
        - 2개월차: 핵심 기능 개발
        - 3개월차: 테스트 및 배포
        """)
        temp_file = f.name
    
    try:
        # 문서 분석
        print("\n📋 문서 분석 테스트")
        response = ai.analyze_document(
            temp_file,
            "이 문서의 핵심 내용을 요약하고 프로젝트의 성공 요인을 분석해주세요.",
            format="json"
        )
        
        print(f"📊 분석 결과:")
        if response.structured_data:
            import json
            print(json.dumps(response.structured_data, indent=2, ensure_ascii=False))
        else:
            print(response.text)
        
        print(f"💰 비용: ${response.cost:.6f}")
        
    except Exception as e:
        print(f"❌ 문서 분석 오류: {e}")
    
    finally:
        # 임시 파일 삭제
        os.unlink(temp_file)

if __name__ == "__main__":
    test_document_features()
```

### 7단계: 대화 관리 (conversation_test.py)

```python
# conversation_test.py
from ai_api_module import AI

def test_conversation():
    ai = AI()
    
    print("💬 대화 관리 테스트 시작!")
    print("="*40)
    
    # 대화 시작
    conversation = ai.start_conversation(
        name="학습 도우미",
        system="당신은 친근하고 도움이 되는 학습 도우미입니다. 항상 격려하는 톤으로 답변해주세요."
    )
    
    # 여러 차례 대화
    messages_and_responses = [
        "파이썬을 처음 배우는데 어떤 순서로 공부하면 좋을까요?",
        "변수와 데이터 타입에 대해 간단히 설명해주세요.",
        "실습 프로젝트로 뭘 만들어보면 좋을까요?"
    ]
    
    for i, message in enumerate(messages_and_responses, 1):
        print(f"\n🙋‍♂️ 질문 {i}: {message}")
        
        conversation.add_user_message(message)
        response = conversation.send()
        
        print(f"🤖 답변 {i}: {response.text}")
        print(f"💰 누적 비용: ${conversation.total_cost:.6f}")
    
    # 대화 저장
    conversation.save("learning_conversation.json")
    print(f"\n💾 대화 저장 완료: learning_conversation.json")
    
    # 저장된 대화 불러오기
    loaded_conversation = ai.load_conversation("learning_conversation.json")
    print(f"📂 대화 로드 완료. 메시지 수: {len(loaded_conversation.messages)}")

if __name__ == "__main__":
    test_conversation()
```

### 8단계: 비동기 처리 (async_test.py)

```python
# async_test.py
import asyncio
from ai_api_module import AI

async def test_async_features():
    ai = AI()
    
    print("⚡ 비동기 처리 테스트 시작!")
    print("="*40)
    
    # 1. 단일 비동기 요청
    print("\n1️⃣ 단일 비동기 요청")
    response = await ai.async_chat("비동기 처리의 장점을 3가지 말해주세요")
    print(f"📝 응답: {response.text}")
    
    # 2. 배치 처리
    print("\n2️⃣ 배치 처리 테스트")
    questions = [
        "파이썬이란 무엇인가요?",
        "자바스크립트의 특징은?",
        "SQL 기초 문법을 알려주세요"
    ]
    
    responses = await ai.batch_chat(questions, max_concurrent=3)
    
    for i, response in enumerate(responses):
        print(f"📋 질문 {i+1} 답변: {response.text[:100]}...")
        print(f"💰 비용: ${response.cost:.6f}")
    
    print(f"\n✅ 총 {len(responses)}개 질문 처리 완료!")

if __name__ == "__main__":
    asyncio.run(test_async_features())
```

### 9단계: 모든 기능 통합 테스트 (full_test.py)

```python
# full_test.py
from ai_api_module import AI
import asyncio
import json
import tempfile
import os

async def comprehensive_test():
    ai = AI()
    
    print("🚀 완전 통합 테스트 시작!")
    print("="*50)
    
    total_cost = 0.0
    
    # 1. 기본 설정 확인
    print("\n⚙️ 설정 확인")
    print(f"기본 프로바이더: {ai.config.default_provider}")
    print(f"일일 예산 한도: ${ai.config.daily_budget_limit}")
    
    # 2. 스마트 라우팅 테스트
    print("\n🧠 스마트 라우팅 테스트")
    test_cases = [
        ("간단한 질문입니다", "fast"),
        ("복잡한 수학 문제를 풀어주세요: 미적분의 기본 정리 증명", "smart"),
        ("창의적인 이야기를 써주세요", "creative")
    ]
    
    for query, expected_type in test_cases:
        response = ai.chat(query, model=expected_type, max_tokens=100)
        print(f"📊 {expected_type} 모델 테스트: {response.model}")
        total_cost += response.cost
    
    # 3. 멀티모달 테스트
    print("\n🎨 멀티모달 테스트")
    
    # 임시 이미지 설명 파일 생성
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
        f.write("이 이미지는 아름다운 자연 풍경을 보여줍니다.")
        temp_desc_file = f.name
    
    try:
        # 이미지 생성 시도
        try:
            img_response = ai.generate_image("평화로운 호수와 산", size="512x512")
            if img_response.images:
                img_response.images[0].save("test_lake.png")
                print("✅ 이미지 생성 성공")
                total_cost += img_response.cost
            else:
                print("❌ 이미지 생성 실패")
        except Exception as e:
            print(f"⚠️ 이미지 생성 건너뜀: {e}")
        
        # 문서 분석
        doc_response = ai.analyze_document(
            temp_desc_file,
            "이 텍스트의 감정을 분석해주세요",
    format="json"
)
        print("✅ 문서 분석 성공")
        total_cost += doc_response.cost
        
    finally:
        os.unlink(temp_desc_file)
        if os.path.exists("test_lake.png"):
            os.unlink("test_lake.png")
    
    # 4. 대화 흐름 테스트
    print("\n💬 대화 흐름 테스트")
    conversation = ai.start_conversation(
        name="통합 테스트",
        system="간결하고 도움이 되는 답변을 해주세요."
    )
    
    conversation.add_user_message("안녕하세요")
    response1 = conversation.send()
    total_cost += response1.cost
    
    conversation.add_user_message("AI의 미래는 어떨까요?")
    response2 = conversation.send()
    total_cost += response2.cost
    
    print(f"💬 대화 완료. 총 메시지: {len(conversation.messages)}")
    
    # 5. 비용 관리 테스트
    print("\n💰 비용 관리 테스트")
    usage_stats = ai.get_usage_stats()
    print(f"오늘 사용량: ${usage_stats.get('daily_cost', 0):.6f}")
    print(f"이번 테스트 비용: ${total_cost:.6f}")
    
    # 6. 스트리밍 테스트 (옵션)
    print("\n⚡ 스트리밍 테스트")
    try:
        print("스트리밍 응답: ", end="")
        async for chunk in ai.stream_chat("숫자 1부터 5까지 세어주세요"):
            print(chunk, end="", flush=True)
        print("\n✅ 스트리밍 완료")
    except Exception as e:
        print(f"⚠️ 스트리밍 건너뜀: {e}")
    
    print(f"\n🎉 통합 테스트 완료! 총 비용: ${total_cost:.6f}")

if __name__ == "__main__":
    asyncio.run(comprehensive_test())
```

### 10단계: 문제 해결 가이드

**자주 발생하는 문제들:**

1. **API 키 오류**
```python
# API 키 확인
import os
print("OpenAI:", "✅" if os.getenv("OPENAI_API_KEY") else "❌")
print("Anthropic:", "✅" if os.getenv("ANTHROPIC_API_KEY") else "❌")
```

2. **모듈 임포트 오류**
```bash
# 개발 모드로 재설치
pip uninstall ai-api-module
pip install -e ".[all]"
```

3. **의존성 오류**
```bash
# 요구사항 재설치
pip install -r requirements.txt
```

## 📖 상세 문서

## 📖 Documentation

### Core Classes

#### AI Class - Main Interface

```python
from ai_api_module import AI

# Basic initialization
ai = AI()

# Custom configuration
ai = AI(
    provider="anthropic",
    model="smart",
    temperature=0.7,
    budget_limit=5.0,
    debug=True
)
```

#### Model Selection

```python
# Automatic smart routing
ai.chat("Complex reasoning task")  # → Uses best reasoning model

# Model aliases
ai.chat("Hello", model="gpt")      # → Latest GPT
ai.chat("Hello", model="claude")   # → Latest Claude
ai.chat("Hello", model="fast")     # → Fastest available
ai.chat("Hello", model="cheap")    # → Most cost-effective

# Specific models
ai.chat("Hello", model="gpt-5")
ai.chat("Hello", model="claude-sonnet-4")

# Quick document smoke-test (testing.py)
# --------------------------------------
# 파이썬 스크립트로 간단히 PDF 분석을 확인하고 싶다면 다음 파일을 그대로 실행하세요.
# 네이티브 업로드를 지원하는 모델(예: Gemini 2.5 Pro)이라면 PDF 원본을 그대로 전송하고,
# 그렇지 않은 모델은 자동으로 텍스트를 추출해 분석합니다.

python testing.py

# testing.py 내용 요약
# from ai_api_module import AI
# ai = AI()
# response = ai.analyze_documents(["19-3.pdf"], "18번 문제 풀이를 요약해줘", model="gemini-2.5-pro", format="json")
# print(response.structured_data or response.text)
```

#### Conversation Management

```python
# Start conversation
conversation = ai.start_conversation(
    name="Project Planning",
    system="You are a helpful project manager"
)

# Send messages
conversation.add_user_message("What are the project phases?")
response = conversation.send()

# Send messages with documents and structured JSON output
conversation.add_user_message(
    "Summarize the attached plan and list project phases",
    files=["docs/roadmap.docx"],
    format="json"
)
response = conversation.send()
print(response.structured_data)

# Continue conversation
response = conversation.send("How long should each phase take?")

# Switch models mid-conversation
conversation.switch_model("creative")
response = conversation.send("What creative approaches can we try?")

# Save/load conversations
conversation.save("project_chat.json")
loaded = ai.load_conversation("project_chat.json")
```

### Advanced Features

#### Async Operations

```python
import asyncio

async def main():
    ai = AI()
    
    # Single async request
    response = await ai.async_chat("Hello world")
    
    # Batch processing
    responses = await ai.batch_chat([
        "Question 1",
        "Question 2", 
        "Question 3"
    ], max_concurrent=3)
    
    # Parallel providers
    results = await ai.async_handler.parallel_providers(
        "What is AI?",
        ["openai", "anthropic"]
    )

asyncio.run(main())
```

#### Streaming

```python
# Stream response
async for chunk in ai.stream_chat("Tell me a story"):
    print(chunk, end="", flush=True)

# Stream with callbacks
def on_chunk(chunk):
    print(f"Received: {chunk}")

def on_complete(response):
    print(f"Total cost: ${response.cost:.4f}")

ai.stream_chat(
    "Explain machine learning",
    on_chunk=on_chunk,
    on_complete=on_complete
)
```

#### Custom Tools

```python
@ai.tool
def get_weather(location: str, unit: str = "celsius") -> dict:
    """Get weather information"""
    # Your implementation
    return {"temperature": 22, "condition": "sunny"}

# Use in conversation
response = ai.chat(
    "What's the weather in Tokyo?",
    tools=["get_weather"]
)
```

#### Cost Management

```python
# Set budget limits
ai.set_budget_limit(daily=10.0, monthly=100.0)

# Estimate costs
cost = ai.estimate_cost("Long prompt here...", model="gpt-5")
print(f"Estimated: ${cost:.4f}")

# Enable optimization
ai.enable_cost_optimization(
    prefer_cheaper_models=True,
    aggressive_caching=True,
    smart_routing=True
)

# Get usage stats
stats = ai.get_usage_stats()
print(f"Total cost: ${stats['total_cost']:.4f}")
```

#### Memory System

```python
# Add facts
ai.memory.add_fact("user_preference", "Likes concise answers")
ai.memory.add_fact("project_type", "Web application")

# Use memory in chat
response = ai.chat(
    "Give me advice for my project",
    use_memory=True
)
```

### Multimodal Capabilities

#### Images

```python
# Generate images
image = ai.generate_image(
    "A futuristic city at night",
    style="photorealistic",
    size="1024x1024",
    quality="high"
)
image.save("city.png")

# Analyze images
response = ai.analyze_image(
    "photo.jpg",
    "Describe what you see in detail"
)

# Multiple images
response = ai.analyze_images(
    ["image1.jpg", "image2.jpg"],
    "Compare these images"
)
```

#### Audio

```python
# Text to speech
audio = ai.generate_speech(
    "Hello, this is a test",
    voice="natural",
    speed=1.0
)
audio.save("speech.mp3")

# Speech to text
text = ai.transcribe_audio("recording.mp3")
print(text)
```

#### Documents

```python
# Analyze documents
response = ai.analyze_document(
    "report.pdf",
    "Summarize the key findings"
)

# Multiple documents
response = ai.analyze_documents(
    ["doc1.pdf", "doc2.docx"],
    "Find common themes and output JSON",
    format="json"
)
print(response.structured_data)
```

## 🔧 Configuration

### Environment Variables

```bash
# API Keys (at least one required)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...
XAI_API_KEY=xai-...

# Default Settings
AI_DEFAULT_PROVIDER=openai
AI_DEFAULT_MODEL=smart
AI_DAILY_BUDGET_LIMIT=10.0
AI_MONTHLY_BUDGET_LIMIT=100.0

# Features
AI_ENABLE_CACHE=true
AI_ENABLE_WEB_SEARCH=true
AI_DEBUG=false
AI_LOG_LEVEL=INFO
```

### Model Catalog

The module uses a catalog system for model aliases:

```yaml
# Automatic aliases
smart: gpt-5                    # Best reasoning
fast: gpt-5-mini               # Fastest response
cheap: gpt-4.1-nano           # Most cost-effective
creative: claude-sonnet-4      # Best for creative tasks

# Provider shortcuts
gpt: gpt-5
claude: claude-sonnet-4
gemini: gemini-2.5-flash
grok: grok-4

# Task-specific
coding: grok-code-fast-1
analysis: claude-opus-4
vision: claude-sonnet-4
```

## 💡 Examples

See the `examples/` directory for comprehensive examples:

- `basic_usage.py` - Getting started examples
- `advanced_features.py` - Async, streaming, conversations
- `multimodal_examples.py` - Images, audio, documents
- `cost_management.py` - Budget control and optimization

## 🧪 Testing

```bash
# Run basic tests
python -m pytest tests/

# Test specific provider
python -m pytest tests/test_providers.py::TestOpenAIProvider

# Integration tests (requires API keys)
python -m pytest tests/test_integration.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🙋‍♂️ Support

- GitHub Issues: Report bugs and request features
- Documentation: Check `docs/` for detailed guides
- Examples: See `examples/` for usage patterns

## 🔄 Changelog

### v0.1.0 (Initial Release)
- Unified interface for 4 major AI providers
- Conversation management
- Cost tracking and budget controls
- Multimodal capabilities
- Async support and streaming
- Memory system and caching
- Tool integration framework

---

Made with ❤️ for the AI development community