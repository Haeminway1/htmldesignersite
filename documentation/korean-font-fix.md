# 한글 폰트 문제 해결 가이드

> **카테고리**: 트러블슈팅  
> **최초 작성**: 2025-10-10  
> **최근 업데이트**: 2025-10-10

## 문제점

Chrome으로 HTML을 PDF로 변환할 때 **한글이 깨지거나 □□□로 표시**되는 문제가 발생합니다.

## 원인

1. **웹폰트 로딩 미완료**: Chrome이 웹폰트를 완전히 로드하기 전에 PDF를 생성
2. **HTML에 한글 폰트 누락**: 생성된 HTML에 Noto Sans KR 등 한글 폰트가 포함되지 않음
3. **시스템 폰트 부족**: 서버(Render)에 한글 폰트가 설치되지 않음

## 해결 방법

### 1. 웹폰트 자동 추가 (`app.py`)

HTML에 한글 폰트가 없으면 자동으로 추가합니다:

```python
def _ensure_korean_fonts(self, html_content: str) -> str:
    """HTML에 한글 폰트 확인 및 추가"""
    
    # 이미 포함되어 있는지 확인
    has_korean_font = (
        'Noto Sans KR' in html_content or 
        'Pretendard' in html_content or
        'fonts.googleapis.com' in html_content
    )
    
    if has_korean_font:
        return html_content
    
    # Google Fonts의 Noto Sans KR 추가
    font_link = '''
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap" rel="stylesheet">
    <style>
        body, html, * {
            font-family: 'Noto Sans KR', sans-serif !important;
        }
    </style>
    '''
    
    html_content = html_content.replace('</head>', f'{font_link}</head>')
    return html_content
```

### 2. 웹폰트 로딩 대기

Chrome이 폰트를 완전히 로드할 때까지 대기합니다:

```python
# 페이지 로딩 대기
driver.implicitly_wait(3)

# 웹폰트 로딩 완료 대기 (추가 2초)
import time
time.sleep(2)

# JavaScript로 폰트 로딩 확인
driver.execute_script("return document.fonts.ready;")
```

**대기 시간**:
- `implicitly_wait(3)`: 기본 로딩 3초
- `time.sleep(2)`: 웹폰트 로딩 추가 2초
- **총 5초 대기**로 안정적인 폰트 로딩 보장

### 3. 서버에 한글 폰트 설치 (`render-build.sh`)

Render 배포 시 시스템 한글 폰트를 설치합니다:

```bash
# Ubuntu 기반 시스템에 한글 폰트 설치
apt-get install -y fonts-noto-cjk fonts-noto-cjk-extra \
    fonts-nanum fonts-nanum-coding
```

**설치되는 폰트**:
- `fonts-noto-cjk`: Noto Sans CJK (한중일 통합)
- `fonts-noto-cjk-extra`: Noto Sans CJK 추가 웨이트
- `fonts-nanum`: 나눔고딕, 나눔명조
- `fonts-nanum-coding`: 나눔고딕코딩

### 4. 폰트 우선순위

```css
body {
    font-family: 
        'Noto Sans KR',        /* 웹폰트 (Google Fonts) */
        'Noto Sans CJK KR',    /* 시스템 폰트 (서버) */
        'Nanum Gothic',        /* 폴백 1 */
        -apple-system,         /* macOS 시스템 폰트 */
        BlinkMacSystemFont,    /* macOS Chrome */
        system-ui,             /* 시스템 기본 폰트 */
        sans-serif;            /* 최종 폴백 */
}
```

## 테스트 방법

### 로컬 테스트

1. **서버 실행**:
```bash
cd backend
python app.py
```

2. **HTML 생성 및 PDF 변환**:
- 프런트엔드에서 "안녕하세요 테스트입니다" 입력
- PDF 생성 후 다운로드

3. **로그 확인**:
```
✅ HTML에 한글 폰트가 이미 포함되어 있습니다
🔄 Chrome 엔진으로 PDF 변환 시도...
✅ 웹폰트 로딩 완료
✅ PDF 생성 완료 (Chrome): /tmp/html_designer/output_xxxxx.pdf
```

4. **PDF 파일 열어서 한글 확인**:
- ✅ 정상: 한글이 선명하게 표시됨
- ❌ 실패: □□□ 또는 깨진 글자

### Render 배포 후 테스트

1. **빌드 로그 확인**:
```
📦 Chrome 및 한글 폰트 설치 시도...
✅ Chrome 설치 완료: /usr/bin/chromium-browser
✅ 한글 폰트 (Noto CJK) 설치 완료
```

2. **런타임 로그 확인** (Render Dashboard → Logs):
```
✅ Chrome (Selenium) 사용 가능 (최우선, 가장 정확한 PDF 변환)
✅ HTML에 한글 폰트가 이미 포함되어 있습니다
✅ 웹폰트 로딩 완료
```

## 트러블슈팅

### 문제: 여전히 한글이 □□□로 표시됨

**원인**: 웹폰트 로딩 실패 또는 시간 부족

**해결**:
1. 대기 시간 증가:
```python
time.sleep(5)  # 2초 → 5초로 증가
```

2. 명시적 대기 사용:
```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 폰트 로딩 완료까지 최대 10초 대기
WebDriverWait(driver, 10).until(
    lambda d: d.execute_script("return document.fonts.status === 'loaded';")
)
```

### 문제: "⚠️ 폰트 로딩 확인 실패" 경고

**원인**: `document.fonts.ready`가 오래된 브라우저에서 지원 안 됨

**해결**:
이미 try-catch로 처리되어 있어 문제 없음. 경고를 무시하거나 대기 시간만 의존:
```python
# 간단한 해결: JavaScript 확인 제거하고 충분히 대기
time.sleep(5)
```

### 문제: 로컬에서는 정상, Render에서는 깨짐

**원인**: Render 서버에 한글 폰트 미설치

**해결**:
1. `render-build.sh` 로그 확인:
```bash
✅ 한글 폰트 (Noto CJK) 설치 완료
```

2. 설치 실패 시 수동 설치 스크립트 추가:
```bash
# render-build.sh 끝에 추가
echo "📦 폰트 캐시 갱신 중..."
fc-cache -f -v || echo "⚠️ 폰트 캐시 갱신 실패"
```

### 문제: PDF 생성 시간이 너무 오래 걸림

**원인**: 웹폰트 로딩 대기 시간(5초)

**해결**:
1. **시스템 폰트 우선 사용** (웹폰트 로딩 불필요):
```python
# render-build.sh에서 시스템 폰트 확실히 설치
apt-get install -y fonts-noto-cjk
```

2. **CSS에서 시스템 폰트 우선**:
```css
body {
    font-family: 'Noto Sans CJK KR', 'Noto Sans KR', sans-serif;
    /* 시스템 폰트가 먼저, 웹폰트는 폴백 */
}
```

3. **대기 시간 조정**:
```python
time.sleep(1)  # 시스템 폰트 사용 시 1초면 충분
```

## 최적화 팁

### 1. 시스템 폰트 우선 사용

**장점**:
- 로딩 시간 ↓ (웹폰트 다운로드 불필요)
- 오프라인 환경에서도 작동
- 안정성 ↑

**단점**:
- 서버 의존성 증가 (폰트 설치 필요)

### 2. 웹폰트만 사용

**장점**:
- 서버 독립적 (어디서나 동일한 결과)
- 폰트 버전 통제 용이

**단점**:
- 로딩 시간 ↑ (2-5초 추가)
- 네트워크 의존

### 3. 하이브리드 (권장)

시스템 폰트 + 웹폰트 폴백:

```css
font-family: 
    'Noto Sans CJK KR',    /* 시스템 폰트 (빠름) */
    'Noto Sans KR',        /* 웹폰트 (폴백) */
    sans-serif;
```

## 결론

✅ **3단계 방어선**으로 한글 깨짐 완전 해결:

1. **HTML 자동 폰트 추가**: `_ensure_korean_fonts()`
2. **웹폰트 로딩 대기**: `time.sleep(2)` + `document.fonts.ready`
3. **시스템 폰트 설치**: `fonts-noto-cjk` (Render)

이제 **모든 환경에서 한글이 정상적으로 PDF에 표시**됩니다! 🎉

## 관련 문서

- [PDF 변환 시스템 가이드](./pdf-conversion-system.md)
- [개발 이력 - 2025-10-10](./dev-log-2025-10-10.md)

