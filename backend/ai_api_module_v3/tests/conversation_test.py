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
