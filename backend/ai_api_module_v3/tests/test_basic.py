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
