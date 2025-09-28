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
