# AI 기반 HTML 교재 생성기 사용법

## 🎯 개요

이 도구는 AI API 모듈을 활용하여 A4 규격의 HTML 교재를 자동 생성하는 Python 스크립트입니다.

## 📋 주요 기능

- ✅ **config.json 설정 기반** 자동 실행
- ✅ **가이드라인 자동 첨부** (guideline.md, basic_structure.html)
- ✅ **A4 규격 강제** (210mm × 297mm)
- ✅ **다양한 AI 모델 지원** (GPT-5, Claude, Gemini, Grok)
- ✅ **대화형 & CLI 모드** 지원
- ✅ **비용 추적** 및 사용량 모니터링
- ✅ **자동 파일 저장** 및 브라우저 열기

## 🚀 설치 및 설정

### 1. API 키 설정

최소 하나 이상의 API 키를 설정해주세요:

```bash
# Windows PowerShell
$env:OPENAI_API_KEY="sk-proj-..."
$env:ANTHROPIC_API_KEY="sk-ant-..."
$env:GOOGLE_API_KEY="AIza..."
$env:XAI_API_KEY="xai-..."

# macOS/Linux
export OPENAI_API_KEY="sk-proj-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export GOOGLE_API_KEY="AIza..."
export XAI_API_KEY="xai-..."
```

### 2. AI API 모듈 설치

```bash
cd ai_api_module_v3
pip install -e ".[all]"
```

## 📖 사용법

### 방법 1: 대화형 모드 (추천)

```bash
cd src
python basic_html_designer.py
```

실행하면 다음과 같은 대화형 인터페이스가 나타납니다:

```
🎨 AI 기반 HTML 교재 생성기
==================================================
✅ 설정 파일 로드 완료: src/config.json
✅ AI 모듈 초기화 완료
🤖 모델: gpt-5
🌡️ Temperature: 0.6

📋 설정에서 발견된 요청: 새로운 헬스장 광고 디자인 진행해줘. 세련된 하늘색 기반으로 2페이지 짜리로 만들어줘. 근육헬스장 이라는 이름이야.
🤔 설정의 요청을 사용하시겠습니까? (y/n): 
```

### 방법 2: CLI 모드

```bash
# config.json의 요청 사용
python basic_html_designer.py ""

# 직접 요청 입력
python basic_html_designer.py "카페 메뉴판을 만들어주세요"

# 고급 옵션 사용
python basic_html_designer.py "회사 소개서" --model smart --temperature 0.8 --output company.html
```

### 방법 3: 코드에서 직접 사용

```python
from basic_html_designer import HTMLDesigner

# 초기화
designer = HTMLDesigner("src/config.json")

# HTML 생성 및 저장
result = designer.generate_and_save("레스토랑 메뉴 만들어주세요")

if result["success"]:
    print(f"완료: {result['output_path']}")
    print(f"비용: ${result['cost']:.6f}")
```

## ⚙️ 설정 파일 (config.json)

```json
{
    "ai_settings": {
        "model": "gpt-5",           // AI 모델 선택
        "temperature": 0.6,         // 창의성 수준 (0-2)
        "reference": [              // 자동 첨부할 참조 파일
            "src/guideline/guideline.md",
            "src/guideline/basic_structure.html"
        ]
    },
    "prompts": {
        "system_prompt": "너는 매우 유능하고 정확하고 실수를 절대 용납하지 않는 ENTJ 워커홀릭 html 교재 디자이너야...",
        "preset_prompt": "결과물은 쓸데없는 응답없이 ```html``` 로 감싸서 출력해...",
        "user_prompt": "새로운 헬스장 광고 디자인 진행해줘..."  // 기본 요청
    },
    "output": {
        "output_directory": "worktable"  // 출력 디렉토리
    }
}
```

### 주요 설정 옵션

#### AI 모델 선택
- `"gpt-5"`: 최고 성능 (높은 비용)
- `"smart"`: 균형잡힌 성능
- `"fast"`: 빠른 응답 (저렴)
- `"claude"`: Anthropic Claude
- `"gemini"`: Google Gemini

#### Temperature 값
- `0.0-0.3`: 일관된, 정확한 결과
- `0.4-0.7`: 균형잡힌 창의성
- `0.8-1.0`: 높은 창의성
- `1.1-2.0`: 매우 창의적/실험적

## 🧪 테스트

기능 테스트를 실행하려면:

```bash
python src/test_designer.py
```

테스트는 다음을 확인합니다:
- AI API 모듈 연결
- 설정 파일 로드
- 참조 파일 읽기
- HTML 생성 및 저장
- 다양한 모델 지원

## 📁 출력 파일

생성된 HTML 파일은 다음 위치에 저장됩니다:
- 기본: `worktable/html_material_YYYYMMDD_HHMMSS.html`
- 사용자 지정: `worktable/your_filename.html`

## 🎨 디자인 특징

생성되는 HTML은 다음 특징을 가집니다:

### A4 규격 준수
```css
@page {
    size: A4;           /* 210mm × 297mm */
    margin: 0;
}
.page {
    width: 210mm;
    height: 297mm;
    padding: 20mm;      /* 적절한 여백 */
}
```

### 프린트 최적화
- 페이지 분할 제어
- 자동 페이지 번호
- 헤더/푸터 지원
- 웹/프린트 양용 스타일

### 모던 디자인
- Google Fonts (Noto Sans KR, Inter)
- 반응형 레이아웃
- 일관된 타이포그래피
- 색상 시스템

## 📊 사용량 모니터링

스크립트 실행 시 다음 정보가 표시됩니다:

```
✅ HTML 교재 생성 완료!
📁 파일 위치: worktable/html_material_20241228_143022.html
🤖 사용 모델: gpt-5
💰 비용: $0.002340
🔢 토큰 사용량: 1,247
📏 HTML 크기: 8,432 문자
```

## 🛠️ 문제 해결

### 자주 발생하는 문제

1. **API 키 오류**
   ```
   ❌ AI 모듈 초기화 실패: No API key provided
   ```
   → API 키를 환경변수로 설정해주세요

2. **모듈 임포트 오류**
   ```
   ❌ AI API 모듈을 찾을 수 없습니다.
   ```
   → AI API 모듈을 설치하거나 경로를 확인해주세요

3. **참조 파일 없음**
   ```
   ⚠️ 참조 파일 없음: src/guideline/guideline.md
   ```
   → 가이드라인 파일이 있는지 확인해주세요

4. **출력 디렉토리 오류**
   ```
   ❌ 파일 저장 실패: Permission denied
   ```
   → 출력 디렉토리 권한을 확인해주세요

### 로그 확인

상세한 로그는 `html_designer.log` 파일에서 확인할 수 있습니다:

```bash
tail -f html_designer.log
```

## 💡 팁과 요령

### 1. 효과적인 요청 작성
```
❌ 나쁜 예: "웹사이트 만들어줘"
✅ 좋은 예: "카페 메뉴판을 만들어주세요. 2페이지 구성이고, 따뜻한 브라운 색상으로 아메리카노, 라떼, 디저트 메뉴를 포함해주세요."
```

### 2. 모델 선택 가이드
- **간단한 전단지**: `"fast"` 모델 (저렴, 빠름)
- **복잡한 교재**: `"smart"` 또는 `"gpt-5"` (고품질)
- **창의적 디자인**: `temperature: 0.8-1.0`

### 3. 비용 절약
- 짧고 명확한 요청 작성
- `"fast"` 모델 우선 시도
- 불필요한 재생성 피하기

### 4. 품질 향상
- 구체적인 색상, 크기 지정
- 참고 자료나 스타일 명시
- 타겟 대상 명확히 설명

## 🔄 업데이트 및 확장

### 새로운 참조 파일 추가
`config.json`의 `reference` 배열에 파일 경로 추가:

```json
"reference": [
    "src/guideline/guideline.md",
    "src/guideline/basic_structure.html",
    "src/library/custom_styles.css",    // 새로 추가
    "src/examples/sample_layout.html"   // 새로 추가
]
```

### 커스텀 프롬프트 템플릿
```json
"prompts": {
    "system_prompt": "당신은 전문 웹 디자이너입니다...",
    "preset_prompt": "HTML 출력 시 다음 규칙을 준수하세요...",
    "user_prompt": "기본 요청 내용..."
}
```

## 📞 지원

문제가 발생하거나 개선 제안이 있으시면:
1. `html_designer.log` 파일 확인
2. `test_designer.py` 실행하여 환경 점검
3. GitHub Issues 또는 문의 채널 활용

---

Made with ❤️ for efficient HTML material creation
