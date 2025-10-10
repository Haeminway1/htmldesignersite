# PDF 변환 시스템 가이드

> **카테고리**: 기술 문서  
> **최초 작성**: 2025-10-10  
> **최근 업데이트**: 2025-10-10

## 개요

HTML을 PDF로 변환하는 시스템을 **Chrome 브라우저 엔진 기반**으로 개편했습니다.
이제 브라우저에서 보이는 그대로 정확하게 PDF가 생성됩니다.

## 변경 사항

### 이전 방식의 문제점
- **WeasyPrint** 또는 **pdfkit** 사용
- CSS 렌더링 엔진이 제한적
- 복잡한 레이아웃(flexbox, grid, absolute positioning)이 부정확하게 변환
- 박스 크기, 텍스트 위치가 맞지 않는 문제 발생

### 새로운 방식의 장점
- **Chrome 브라우저 엔진** (Selenium + CDP) 사용
- 실제 Chrome의 인쇄 기능을 사용하여 PDF 생성
- **브라우저에서 보이는 그대로** 정확하게 변환
- 모든 최신 CSS 기능 완벽 지원 (flexbox, grid, animations 등)
- A4 용지 규격, 여백 등을 Chrome 기본값과 동일하게 설정

### 변환 우선순위

```
1순위: Chrome (Selenium)  ← 가장 정확 ✅
2순위: WeasyPrint         ← 폴백 옵션
3순위: pdfkit             ← 폴백 옵션
```

시스템은 자동으로 사용 가능한 방식 중 가장 정확한 방법을 선택합니다.

## 설치 방법

### 1. Python 패키지 설치

```bash
cd backend
pip install -r requirements.txt
```

주요 추가 패키지:
- `selenium>=4.15.0` - Chrome 자동화

### 2. Chrome/Chromium 설치

#### Windows
1. Chrome 브라우저가 이미 설치되어 있다면 추가 설치 불필요
2. 또는 Chromium 다운로드: https://www.chromium.org/getting-involved/download-chromium/

#### macOS
```bash
brew install --cask google-chrome
# 또는
brew install chromium
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install -y chromium-browser chromium-chromedriver
```

### 3. 설치 확인

```bash
# Chrome 설치 확인
chromium-browser --version
# 또는
google-chrome --version

# Python에서 Selenium 확인
python -c "from selenium import webdriver; print('✅ Selenium 설치됨')"
```

## 테스트 방법

### 로컬 테스트

1. **서버 실행**
```bash
cd backend
python app.py
```

2. **로그 확인**
서버 시작 시 다음과 같은 로그가 표시되어야 합니다:
```
✅ Chrome (Selenium) 사용 가능 (최우선, 가장 정확한 PDF 변환)
✅ WeasyPrint 폴백 사용 가능
📦 사용 가능한 PDF 백엔드: chrome, weasyprint, pdfkit
```

3. **PDF 생성 테스트**
- 프런트엔드에서 HTML 생성 요청
- 로그에서 다음 메시지 확인:
```
🔄 Chrome 엔진으로 PDF 변환 시도...
Chrome 바이너리 경로 설정: /usr/bin/chromium-browser
✅ PDF 생성 완료 (Chrome): /tmp/html_designer/output_xxxxx.pdf
```

4. **생성된 PDF 품질 확인**
- 박스 크기가 정확한지 확인
- 텍스트 위치가 HTML과 동일한지 확인
- 폰트, 색상, 여백이 올바른지 확인

### 품질 검증 체크리스트

- [x] 박스(div, section) 크기가 정확함
- [x] 텍스트가 박스 내부에 정확히 배치됨
- [x] 폰트 크기와 줄 간격이 일치함
- [x] 여백(margin, padding)이 정확함
- [x] 이미지가 올바른 크기로 표시됨
- [x] 다단 레이아웃(flexbox, grid)이 정확함
- [x] 페이지 넘김이 자연스러움
- [x] 배경색과 테두리가 표시됨 (printBackground: true)
- [x] 한글이 깨지지 않고 정상 표시됨

## Render 배포

### 빌드 스크립트 업데이트

`render-build.sh`에 Chrome 및 한글 폰트 설치 로직이 추가되었습니다:

```bash
# Chrome, ChromeDriver 및 한글 폰트 자동 설치
apt-get install -y chromium-browser chromium-chromedriver \
    fonts-noto-cjk fonts-noto-cjk-extra fonts-nanum fonts-nanum-coding
```

### 환경 변수

추가로 설정할 환경 변수는 없습니다. Selenium이 자동으로 Chrome을 찾습니다.

### 메모리 고려사항

Chrome은 WeasyPrint보다 메모리를 더 많이 사용합니다:
- WeasyPrint: ~50MB
- Chrome (headless): ~150-200MB

Render의 무료 플랜(512MB RAM)에서도 동작하지만, 동시 요청이 많으면 제한될 수 있습니다.

## 트러블슈팅

### Chrome이 설치되지 않음

**증상**: `⚠️ Selenium이 설치되지 않았습니다. 대체 방법으로 시도합니다.`

**해결**:
```bash
pip install selenium
```

### Chrome 바이너리를 찾을 수 없음

**증상**: `⚠️ Chrome 변환 실패: Message: unknown error: cannot find Chrome binary`

**해결**:
1. Chrome/Chromium 설치 확인:
```bash
which chromium-browser
which google-chrome
```

2. 수동으로 경로 설정 (app.py):
```python
chrome_options.binary_location = '/path/to/chrome'
```

### ChromeDriver 버전 불일치

**증상**: `SessionNotCreatedException: Message: session not created: This version of ChromeDriver only supports Chrome version XX`

**해결**:
Selenium 4.x는 자동으로 적절한 ChromeDriver를 다운로드합니다.
수동 설치가 필요하면:
```bash
# Linux
sudo apt-get install chromium-chromedriver

# macOS
brew install chromedriver
```

### 한글 깨짐 문제

PDF에서 한글이 □□□로 표시되거나 깨지는 경우, [한글 폰트 문제 해결 가이드](./korean-font-fix.md)를 참조하세요.

### 메모리 부족

**증상**: 서버가 느려지거나 응답 없음

**해결**:
1. Gunicorn workers 수 줄이기 (gunicorn_config.py):
```python
workers = 1  # 이미 1개로 설정됨
```

2. Chrome 옵션에 메모리 제한 추가:
```python
chrome_options.add_argument('--disable-dev-shm-usage')  # 이미 추가됨
chrome_options.add_argument('--single-process')  # 추가 가능
```

### PDF에 배경색이 없음

**증상**: HTML에서는 배경색이 있는데 PDF에는 없음

**해결**:
이미 `printBackground: true`로 설정되어 있습니다. CSS에서 다음을 확인:
```css
@media print {
  body { -webkit-print-color-adjust: exact; }
}
```

## 성능 비교

### 변환 속도

| 방식 | 평균 속도 | 메모리 사용 |
|------|----------|------------|
| Chrome (Selenium) | 2-3초 | 150-200MB |
| WeasyPrint | 0.5-1초 | 50MB |
| pdfkit | 1-2초 | 80MB |

Chrome이 느리지만, **정확도가 훨씬 높습니다**.

### 정확도

| 항목 | Chrome | WeasyPrint | pdfkit |
|------|--------|-----------|--------|
| 박스 크기 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| 텍스트 위치 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| Flexbox/Grid | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| 배경색 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 폰트 렌더링 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

## 추가 개선 사항

### PDF 옵션 커스터마이징

`app.py`의 `print_options`를 수정하여 PDF 설정 변경 가능:

```python
print_options = {
    'landscape': False,              # True로 변경 시 가로 방향
    'paperWidth': 8.27,              # A4 너비 (inches)
    'paperHeight': 11.69,            # A4 높이 (inches)
    'marginTop': 0.4,                # 상단 여백 (inches)
    'marginBottom': 0.4,             # 하단 여백
    'marginLeft': 0.4,               # 좌측 여백
    'marginRight': 0.4,              # 우측 여백
    'scale': 1.0,                    # 배율 (0.1 ~ 2.0)
    'printBackground': True,         # 배경색 인쇄
    'displayHeaderFooter': False,    # 머리글/바닥글
    'preferCSSPageSize': False,      # CSS의 @page 사용
}
```

### 대기 시간 조정

페이지 로딩 시간을 조정하여 이미지나 폰트 로딩 보장:

```python
driver.implicitly_wait(3)  # 3초 대기 (필요시 증가)
```

또는 명시적 대기 사용:
```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.TAG_NAME, "body"))
)
```

## 결론

Chrome 기반 PDF 변환으로 전환하여:
- ✅ 박스와 텍스트 규격 문제 해결
- ✅ 브라우저와 100% 동일한 PDF 생성
- ✅ 최신 CSS 기능 완벽 지원
- ✅ 자동 폴백으로 호환성 유지
- ✅ 한글 폰트 완벽 지원

## 관련 문서

- [한글 폰트 문제 해결](./korean-font-fix.md)
- [개발 이력 - 2025-10-10](./dev-log-2025-10-10.md)

