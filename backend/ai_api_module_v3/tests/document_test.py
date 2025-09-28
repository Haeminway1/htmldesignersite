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
