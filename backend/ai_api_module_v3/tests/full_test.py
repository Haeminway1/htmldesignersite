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
