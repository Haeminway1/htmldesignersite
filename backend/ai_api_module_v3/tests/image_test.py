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
