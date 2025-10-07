# 📚 HTML 교재 생성기 - 개발자 문서

> **마지막 업데이트**: 2025년 10월 7일  
> **프로젝트 상태**: Production (Render 배포 중)

---

## 📋 목차

1. [프로젝트 개요](#1-프로젝트-개요)
2. [기술 스택](#2-기술-스택)
3. [시스템 아키텍처](#3-시스템-아키텍처)
4. [로컬 개발 환경 설정](#4-로컬-개발-환경-설정)
5. [Render 배포 가이드](#5-render-배포-가이드)
6. [HTML 디자인 가이드라인](#6-html-디자인-가이드라인)
7. [프로젝트 구조](#7-프로젝트-구조)
8. [API 문서](#8-api-문서)
9. [주요 워크플로우](#9-주요-워크플로우)
10. [트러블슈팅](#10-트러블슈팅)

---

## 1. 프로젝트 개요

### 🎯 목적
파일(PDF, 이미지, 문서 등)을 업로드하면 **AI가 자동으로 세련된 HTML 교재를 생성**하고, 선택적으로 PDF로 변환해주는 웹 서비스입니다.

### ✨ 주요 기능
- 📁 **다양한 파일 형식 지원**: PDF, Word, Excel, PowerPoint, 이미지, 텍스트 등
- 🤖 **멀티 AI 모델**: Google Gemini, OpenAI GPT, Anthropic Claude, xAI Grok
- 📄 **HTML → PDF 변환**: 생성된 HTML을 즉시 다운로드 가능 (PDF 변환 실패 시 HTML 다운로드)
- ⚡ **캐싱 시스템**: 동일 요청 24시간 캐싱으로 빠른 응답
- 🔒 **보안 & 제한**: Rate Limiting, 파일 크기 제한, CORS 설정
- 📱 **반응형 UI**: 모바일, 태블릿, 데스크톱 지원

### 🎨 특징
- **미니멀리즘 디자인 철학**: 불필요한 장식 제거, 정보 전달에 집중
- **A4 인쇄 최적화**: 210×297mm 규격 준수
- **일관성 있는 타이포그래피**: 산세리프 중심, 명확한 위계 구조
- **충분한 여백(Whitespace)**: 고급스럽고 가독성 높은 레이아웃

---

## 2. 기술 스택

### 백엔드 (Backend)
| 기술 | 버전 | 용도 |
|------|------|------|
| **Python** | 3.13+ | 메인 언어 |
| **Flask** | 3.1.2 | 웹 프레임워크 |
| **Gunicorn** | 23.0.0 | WSGI 서버 (프로덕션) |
| **Flask-CORS** | 6.0.1 | CORS 처리 |
| **Flask-Limiter** | 4.0.0 | Rate Limiting |
| **pdfkit** | 1.0.0 | HTML → PDF 변환 (wkhtmltopdf 래퍼) |

### AI 통합
| 라이브러리 | 버전 | AI 모델 |
|-----------|------|---------|
| **google-genai** | 0.6.0+ | Google Gemini 2.5 Pro/Flash |
| **openai** | 1.35.0+ | GPT-4.1, GPT-5 |
| **anthropic** | 0.31.0+ | Claude Opus 4, Sonnet 4 |

### 프론트엔드 (Frontend)
| 기술 | 설명 |
|------|------|
| **HTML5** | 시맨틱 마크업 |
| **CSS3** | Tailwind CSS 스타일 |
| **JavaScript (ES6+)** | 바닐라 JS (프레임워크 없음) |

### 인프라 & 배포
| 서비스 | 용도 |
|--------|------|
| **Render** | 웹 서비스 호스팅 (프로덕션) |
| **Git/GitHub** | 버전 관리 |

### 외부 도구
- **wkhtmltopdf**: HTML을 고품질 PDF로 변환 (0.12.6)

---

## 3. 시스템 아키텍처

```
┌─────────────────────────────────────────────────────────────────┐
│                        사용자 브라우저                            │
│                    (HTML + CSS + JavaScript)                     │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTP/HTTPS
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Render 웹 서비스                            │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Gunicorn (WSGI Server)                     │   │
│  │  ┌──────────────────────────────────────────────────┐  │   │
│  │  │           Flask Application                      │  │   │
│  │  │  ┌────────────────────────────────────────────┐ │  │   │
│  │  │  │         Flask-CORS / Flask-Limiter        │ │  │   │
│  │  │  └────────────────────────────────────────────┘ │  │   │
│  │  │  ┌────────────────────────────────────────────┐ │  │   │
│  │  │  │      파일 업로드 핸들러 (Werkzeug)       │ │  │   │
│  │  │  └────────────────────────────────────────────┘ │  │   │
│  │  │  ┌────────────────────────────────────────────┐ │  │   │
│  │  │  │       AI API 모듈 (ai_api_module_v3)     │ │  │   │
│  │  │  │  ┌──────────────────────────────────────┐ │ │  │   │
│  │  │  │  │  Provider Router                    │ │ │  │   │
│  │  │  │  │  - Google (Gemini)                 │ │ │  │   │
│  │  │  │  │  - OpenAI (GPT)                    │ │ │  │   │
│  │  │  │  │  - Anthropic (Claude)              │ │ │  │   │
│  │  │  │  │  - xAI (Grok)                      │ │ │  │   │
│  │  │  │  └──────────────────────────────────────┘ │ │  │   │
│  │  │  └────────────────────────────────────────────┘ │  │   │
│  │  │  ┌────────────────────────────────────────────┐ │  │   │
│  │  │  │      HTMLDesigner (기존 로직)            │ │  │   │
│  │  │  │  - 가이드라인 로드                       │ │  │   │
│  │  │  │  - 파일 전처리                           │ │  │   │
│  │  │  │  - HTML 생성 로직                        │ │  │   │
│  │  │  └────────────────────────────────────────────┘ │  │   │
│  │  │  ┌────────────────────────────────────────────┐ │  │   │
│  │  │  │     pdfkit + wkhtmltopdf                 │ │  │   │
│  │  │  │     (HTML → PDF 변환)                    │ │  │   │
│  │  │  └────────────────────────────────────────────┘ │  │   │
│  │  │  ┌────────────────────────────────────────────┐ │  │   │
│  │  │  │      캐싱 시스템 (파일 기반)            │ │  │   │
│  │  │  │      - 24시간 TTL                        │ │  │   │
│  │  │  │      - MD5 해시 기반 키                  │ │  │   │
│  │  │  └────────────────────────────────────────────┘ │  │   │
│  │  └──────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    외부 AI API 서비스                            │
│  - Google Gemini API                                           │
│  - OpenAI API                                                  │
│  - Anthropic API                                               │
│  - xAI API                                                     │
└─────────────────────────────────────────────────────────────────┘
```

### 데이터 흐름
1. **사용자** → 파일 업로드 + 프롬프트 입력
2. **Flask** → 파일 유효성 검증 (크기, 형식, 개수)
3. **캐시 확인** → 동일 요청 캐시 확인 (MD5 해시)
4. **AI 모듈** → 파일 전처리 + AI API 호출 (Gemini/GPT/Claude)
5. **HTMLDesigner** → AI 응답 → HTML 생성
6. **pdfkit** → HTML → PDF 변환 (선택적)
7. **Flask** → PDF/HTML 파일 URL 반환
8. **사용자** → 파일 다운로드 또는 새 창에서 미리보기

---

## 4. 로컬 개발 환경 설정

### 4.1 사전 요구사항
- **Python 3.13+**
- **Git**
- **API 키**: Google, OpenAI, Anthropic 중 최소 1개

### 4.2 저장소 클론
```bash
git clone https://github.com/Haeminway1/htmldesignersite.git
cd htmldesignersite
```

### 4.3 백엔드 설정

#### Python 가상 환경 생성 (권장)
```bash
cd backend
python -m venv venv

# Windows
.\venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

#### 의존성 설치
```bash
pip install -r requirements.txt
```

#### 환경 변수 설정
```bash
# Windows PowerShell
$env:GOOGLE_API_KEY="your-google-api-key"
$env:OPENAI_API_KEY="sk-proj-your-openai-key"
$env:ANTHROPIC_API_KEY="sk-ant-your-anthropic-key"

# macOS/Linux
export GOOGLE_API_KEY="your-google-api-key"
export OPENAI_API_KEY="sk-proj-your-openai-key"
export ANTHROPIC_API_KEY="sk-ant-your-anthropic-key"
```

#### wkhtmltopdf 다운로드 (선택사항, PDF 변환용)
```bash
python download_wkhtmltopdf.py
```

#### 백엔드 서버 실행
```bash
python app.py
```

서버 실행 확인: http://localhost:5000/api/health

### 4.4 프론트엔드 설정

#### 단순 정적 파일 서버 실행
```bash
cd frontend
python -m http.server 3000
```

브라우저에서 접속: http://localhost:3000

#### API 연결 확인
`frontend/script.js`에서 `API_BASE` 변수가 로컬 백엔드를 가리키는지 확인:
```javascript
const API_BASE = 'http://localhost:5000';
```

---

## 5. Render 배포 가이드

### 5.1 Render 계정 설정
1. https://dashboard.render.com 에서 계정 생성
2. GitHub 저장소 연결 권한 부여

### 5.2 웹 서비스 생성

#### 단계별 설정
1. **New > Web Service** 클릭
2. **Repository 연결**: `htmldesignersite` 선택
3. **기본 설정**:
   - **Name**: `htmldesignersite` (또는 원하는 이름)
   - **Region**: 가장 가까운 지역 선택
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`

4. **Build & Deploy 설정**:
   - **Build Command**: 
     ```bash
     ./render-build.sh
     ```
   - **Start Command**: ⚠️ **매우 중요!**
     ```bash
     gunicorn -c gunicorn_config.py app:app
     ```

5. **Environment Variables (환경 변수)**:
   ```
   GOOGLE_API_KEY=your-actual-google-api-key
   OPENAI_API_KEY=sk-proj-your-actual-openai-key
   ANTHROPIC_API_KEY=sk-ant-your-actual-anthropic-key
   PORT=10000
   ```

6. **Plan 선택**:
   - **Free** (권장): 무료 티어로 시작
   - **Starter** ($7/mo): 더 많은 메모리/성능 필요 시

7. **Create Web Service** 클릭

### 5.3 배포 확인

#### 로그 확인
Render 대시보드 → Logs 탭에서 다음 메시지 확인:
```
✅ AI API 모듈 로드 성공
✅ HTMLDesigner 클래스 로드 성공
✅ Gunicorn 설정 파일 생성 완료
==> Your service is live 🎉
```

#### Health Check
배포된 URL + `/api/health` 접속:
```
https://htmldesignersite.onrender.com/api/health
```

응답:
```json
{
  "ok": true,
  "ai_available": true,
  "timestamp": "2025-10-07T..."
}
```

### 5.4 프론트엔드 연결

#### 옵션 1: 정적 사이트로 배포 (권장)
1. Render에서 **New > Static Site** 생성
2. **Settings**:
   - **Root Directory**: `frontend`
   - **Publish Directory**: `frontend`
   - **Build Command**: (비워둠)
3. `frontend/script.js`의 `API_BASE` 업데이트:
   ```javascript
   const API_BASE = 'https://htmldesignersite.onrender.com';
   ```

#### 옵션 2: 백엔드와 통합 (현재 방식)
`backend/app.py`가 `/` 경로에서 `frontend/index.html`을 제공합니다.
별도 배포 불필요.

### 5.5 중요 설정 파일

#### `render-build.sh`
Render 빌드 시 실행되는 스크립트:
```bash
#!/usr/bin/env bash
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

# AI 모듈 설치
# Gunicorn 설정 파일 생성
# wkhtmltopdf 다운로드 (현재 실패하지만 필수 아님)
# 환경 변수 확인
```

#### `gunicorn_config.py`
Gunicorn 프로덕션 설정:
```python
workers = 1                 # 메모리 제한으로 1개
timeout = 300              # 5분 (AI API 응답 대기)
bind = "0.0.0.0:10000"     # Render 포트
worker_tmp_dir = '/dev/shm'  # tmpfs 사용
```

---

## 6. HTML 디자인 가이드라인

> AI가 생성하는 HTML은 `backend/src/guideline/guideline.md`의 철학을 따릅니다.

### 6.1 핵심 철학
- **미니멀리즘**: 불필요한 장식 제거, 정보 전달에 집중
- **일관성**: 색·폰트·간격·정렬 전 페이지 통일
- **위계**: 타이포·크기·굵기·색·여백으로 중요도 차이 명확화
- **여백(Whitespace)**: 가독성·고급스러움·집중도 향상

### 6.2 색상 팔레트
- **기본 색상**: Neutral (White, Off-white, Light Gray)
- **포인트 컬러**: 1개 (Teal, Orange, Navy, Cobalt Blue 등)
- **대비**: 본문 텍스트 명암 대비 AA 이상
- **피해야 할 것**: 과도한 그라데이션, 이모티콘, 네온/형광 색

### 6.3 타이포그래피
```css
/* 글꼴 */
font-family: 'Pretendard', 'Noto Sans KR', sans-serif;

/* 크기 체계 */
H1: 28-36px / font-weight: 700
H2: 22-28px / font-weight: 700
H3: 18-22px / font-weight: 600
본문: 12-14px / font-weight: 400
캡션: 10-12px / font-weight: 400

/* 행간 */
line-height: 1.4-1.6 (본문)
line-height: 1.2-1.35 (제목)
```

### 6.4 레이아웃
- **A4 규격**: 210×297mm
- **여백**: 상·하 18-22mm, 좌·우 15-20mm
- **그리드**: 2-3 컬럼 그리드 권장
- **칼럼 간격**: 6-10mm
- **정렬**: 본문 좌측 정렬, 제목만 중앙 정렬

### 6.5 이미지 & 아이콘
- **해상도**: 300dpi 이상
- **관련성**: 내용과 직접 관련된 이미지만 사용
- **아이콘**: 미니멀 라인 스타일 (Feather Icons, Heroicons)
- **크기**: 일관된 크기 유지

### 6.6 피해야 할 디자인
❌ **금지 사항**:
- 과도한 무지개 그라데이션
- 이모티콘 남발
- 둥근 상자 과다 사용
- 저대비 색상 조합
- 한 페이지에 내용 과다 배치

✅ **권장 사항**:
- 충분한 여백
- 명확한 위계 구조
- 일관된 컬러 팔레트
- 고해상도 이미지
- 페이지당 적정 분량

---

## 7. 프로젝트 구조

```
htmldesignersite/
├── .gitignore                      # Git 무시 파일
├── README.md                       # 프로젝트 소개
├── dev_documentation.md            # 🔴 이 문서 (개발자 가이드)
│
├── backend/                        # 백엔드 애플리케이션
│   ├── app.py                     # Flask 메인 애플리케이션
│   ├── requirements.txt           # Python 의존성
│   ├── gunicorn_config.py         # Gunicorn 프로덕션 설정
│   ├── render-build.sh            # Render 빌드 스크립트
│   ├── download_wkhtmltopdf.py    # PDF 변환 도구 다운로드
│   │
│   ├── bin/                       # 바이너리 파일
│   │   ├── README.md
│   │   └── (wkhtmltopdf 바이너리 - 다운로드 후 위치)
│   │
│   ├── ai_api_module_v3/          # AI API 통합 모듈
│   │   ├── ai_api_module/
│   │   │   ├── core/             # 핵심 로직 (AI, 대화, 응답)
│   │   │   │   ├── ai.py         # 메인 AI 클래스
│   │   │   │   ├── conversation.py
│   │   │   │   ├── response.py
│   │   │   │   └── ...
│   │   │   ├── providers/        # AI 제공자 어댑터
│   │   │   │   ├── google_provider.py    # Gemini
│   │   │   │   ├── openai_provider.py    # GPT
│   │   │   │   ├── anthropic_provider.py # Claude
│   │   │   │   ├── xai_provider.py       # Grok
│   │   │   │   └── router.py
│   │   │   ├── models/           # 모델 레지스트리
│   │   │   ├── tools/            # 도구 (계산기, 파일 처리 등)
│   │   │   ├── features/         # 기능 (캐싱, 스트리밍 등)
│   │   │   └── utils/            # 유틸리티
│   │   ├── docs/
│   │   ├── examples/
│   │   ├── tests/
│   │   ├── requirements.txt
│   │   └── README.md
│   │
│   └── src/                       # 기존 HTML 디자이너 로직
│       ├── basic_html_designer.py # HTMLDesigner 클래스
│       ├── file_preprocessor.py   # 파일 전처리
│       ├── config.json            # AI 설정 (모델, 프롬프트 등)
│       │
│       ├── guideline/             # HTML 디자인 가이드라인
│       │   ├── guideline.md      # 🔴 디자인 철학 문서
│       │   └── basic_structure.html
│       │
│       ├── library/               # 폰트 등 리소스
│       │   └── fonts.md
│       │
│       └── worktable/             # 작업 디렉토리
│           ├── input/            # 업로드된 파일 임시 저장
│           └── output/           # 생성된 HTML/PDF 임시 저장
│
└── frontend/                      # 프론트엔드 (정적 파일)
    ├── index.html                # 메인 페이지
    └── script.js                 # JavaScript 로직
```

---

## 8. API 문서

### 8.1 Health Check
**엔드포인트**: `GET /api/health`

**설명**: 서버 상태 및 AI 가용성 확인

**응답**:
```json
{
  "ok": true,
  "ai_available": true,
  "timestamp": "2025-10-07T12:00:00.000Z"
}
```

---

### 8.2 파일 변환
**엔드포인트**: `POST /api/convert`

**설명**: 업로드된 파일들을 AI로 분석하여 HTML 교재 생성, 선택적으로 PDF 변환

**요청 (multipart/form-data)**:
```
POST /api/convert
Content-Type: multipart/form-data

- prompt: (string, 필수) 사용자 요청사항
  예: "영어 단어장을 만들어주세요"
  
- files: (file[], 선택) 업로드할 파일
  - 최대 10개
  - 각 파일 최대 5MB
  - 지원 형식: PDF, DOCX, XLSX, PPTX, TXT, MD, CSV, JSON, XML, HTML, JPG, PNG, GIF, BMP, TIFF, WEBP, EPUB, ZIP
```

**응답 (성공 - PDF 변환 성공)**:
```json
{
  "success": true,
  "pdf_url": "/api/file/abc123def456.pdf",
  "metadata": {
    "model": "gemini-2.5-pro",
    "cost": 0.002340,
    "tokens_used": 1247,
    "attached_files": 3,
    "file_list": ["image1.png", "document.pdf", "data.xlsx"]
  },
  "cached": false
}
```

**응답 (성공 - PDF 변환 실패, HTML만 제공)**:
```json
{
  "success": true,
  "html": "<html>...</html>",
  "metadata": {
    "model": "gemini-2.5-pro",
    "cost": 0.002340,
    "tokens_used": 1247
  },
  "cached": false
}
```

**응답 (실패)**:
```json
{
  "error": "오류 메시지",
  "code": "ERROR_CODE",
  "detail": "상세 정보"
}
```

**에러 코드**:
- `FILE_TOO_LARGE`: 파일 크기 초과 (5MB)
- `FILES_TOO_LARGE`: 전체 파일 크기 초과 (5MB)
- `TOO_MANY_FILES`: 파일 개수 초과 (10개)
- `AI_UNAVAILABLE`: AI 서비스 사용 불가
- `INTERNAL_ERROR`: 서버 내부 오류

---

### 8.3 파일 다운로드
**엔드포인트**: `GET /api/file/<filename>`

**설명**: 생성된 PDF 또는 HTML 파일 다운로드

**요청**:
```
GET /api/file/abc123def456.pdf
```

**응답**:
- Content-Type: `application/pdf` 또는 `text/html`
- 파일 스트림 반환

---

### 8.4 프론트엔드 제공
**엔드포인트**: `GET /`

**설명**: 프론트엔드 HTML 페이지 제공

**응답**:
- `frontend/index.html` 파일 반환

---

## 9. 주요 워크플로우

### 9.1 사용자 → HTML 생성 흐름

```mermaid
graph TD
    A[사용자: 파일 업로드 + 프롬프트 입력] --> B[프론트엔드: FormData 생성]
    B --> C[AJAX POST /api/convert]
    C --> D{Flask: 파일 검증}
    D -->|실패| E[에러 응답 400/413]
    D -->|성공| F[캐시 확인 MD5 해시]
    F -->|캐시 히트| G[캐시된 결과 반환]
    F -->|캐시 미스| H[AI 모듈: 파일 전처리]
    H --> I[AI API 호출 Gemini/GPT/Claude]
    I --> J[HTMLDesigner: HTML 생성]
    J --> K{PDF 변환 시도}
    K -->|성공| L[PDF 파일 저장]
    K -->|실패| M[HTML만 반환]
    L --> N[응답: pdf_url]
    M --> N
    N --> O[프론트엔드: 새 창에서 미리보기]
    O --> P[사용자: 다운로드 또는 인쇄]
```

### 9.2 AI 모듈 작동 방식

```python
# backend/app.py (간소화)
from ai_api_module import AI

ai = AI()  # 자동으로 사용 가능한 제공자 감지

# 파일과 프롬프트로 HTML 생성
response = ai.chat(
    message=user_prompt,
    files=file_paths,
    model="gemini-2.5-pro"
)

html_content = response.text
```

**AI 모듈 특징**:
- 자동 제공자 감지 (API 키 기반)
- 파일 자동 분류:
  - **이미지** (`image/*`) → `images` 배열
  - **문서** (PDF, DOCX 등) → 텍스트 추출 → `documents` 배열
  - **기타** → 텍스트 추출 시도
- 응답 정규화: 모든 제공자의 응답을 `AIResponse` 객체로 통일

### 9.3 캐싱 메커니즘

```python
# 캐시 키 생성
cache_key = hashlib.md5(
    f"{prompt}_{file_hashes}_{model}".encode()
).hexdigest()

# 캐시 확인
if cache_exists(cache_key) and not cache_expired(cache_key, 24*3600):
    return cached_result

# 캐시 저장
save_to_cache(cache_key, result, ttl=24*3600)
```

**캐시 정책**:
- **TTL**: 24시간
- **저장 위치**: `backend/src/worktable/output/.cache/`
- **키**: MD5(프롬프트 + 파일 해시 + 모델명)

---

## 10. 트러블슈팅

### 10.1 로컬 개발 문제

#### 문제: "AI 모듈을 찾을 수 없습니다"
**원인**: AI API 모듈 경로 문제

**해결**:
```bash
cd backend
pip install -r requirements.txt
python -c "from ai_api_module import AI; print('✅ AI 모듈 로드 성공')"
```

#### 문제: "API 키가 설정되지 않았습니다"
**원인**: 환경 변수 미설정

**해결**:
```bash
# 환경 변수 확인
echo $GOOGLE_API_KEY  # macOS/Linux
echo $env:GOOGLE_API_KEY  # Windows PowerShell

# 설정
export GOOGLE_API_KEY="your-key"  # macOS/Linux
$env:GOOGLE_API_KEY="your-key"  # Windows PowerShell
```

#### 문제: PDF 변환 실패
**원인**: wkhtmltopdf 미설치 또는 경로 문제

**해결**:
```bash
python download_wkhtmltopdf.py
# 또는
export WKHTMLTOPDF_PATH="/path/to/wkhtmltopdf"
```

PDF 변환 실패 시 **HTML 다운로드**로 대체 가능 (사용자가 브라우저에서 인쇄 → PDF 저장)

---

### 10.2 Render 배포 문제

#### 문제: "Worker timeout (pid:XX)"
**원인**: Gunicorn timeout 설정 (기본 30초)

**해결**:
1. **Start Command 확인**:
   ```bash
   gunicorn -c gunicorn_config.py app:app
   ```
2. `gunicorn_config.py`에서 `timeout = 300` 확인
3. Render 대시보드 → Settings → Start Command 업데이트
4. Manual Deploy 재시작

#### 문제: "Build failed - ./render-build.sh: No such file or directory"
**원인**: 스크립트 실행 권한 없음

**해결**:
```bash
# 로컬에서
git update-index --chmod=+x backend/render-build.sh
git commit -m "Fix: Add execute permission to render-build.sh"
git push origin main
```

#### 문제: "AI API 키 확인됨" 메시지가 안 나옴
**원인**: Render 환경 변수 미설정

**해결**:
1. Render 대시보드 → Settings → Environment
2. **Add Environment Variable** 클릭
3. 키/값 입력:
   ```
   GOOGLE_API_KEY=your-actual-key
   ```
4. Save Changes → Manual Deploy

#### 문제: Out of Memory (OOM)
**원인**: 무료 플랜 메모리 제한 (512MB)

**해결**:
- 파일 크기 제한 준수 (5MB)
- `config.json`에서 `max_file_size_mb` 감소
- 유료 플랜 업그레이드 (Starter: $7/mo, 512MB → 2GB)

---

### 10.3 프론트엔드 문제

#### 문제: CORS 오류
**원인**: 백엔드와 프론트엔드 도메인 불일치

**해결**:
```python
# backend/app.py
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://your-frontend.onrender.com"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})
```

#### 문제: 파일 업로드 후 아무 반응 없음
**원인**: JavaScript 오류 또는 API 엔드포인트 불일치

**해결**:
1. 브라우저 개발자 도구 → Console 확인
2. Network 탭에서 `/api/convert` 요청 확인
3. `script.js`의 `API_BASE` 변수 확인:
   ```javascript
   const API_BASE = 'https://htmldesignersite.onrender.com';
   ```

---

### 10.4 AI 관련 문제

#### 문제: "AI 서비스를 사용할 수 없습니다"
**원인**: 모든 AI API 키가 유효하지 않음

**해결**:
1. API 키 유효성 확인 (콘솔에서 직접 테스트)
2. API 할당량 확인 (무료 티어 한도 초과 여부)
3. 로그 확인:
   ```
   ✅ AI API 모듈 로드 성공
   ✅ AI API 키 확인됨
   ```

#### 문제: 이미지 파일이 인식되지 않음
**원인**: AI 모듈의 파일 분류 로직 문제 (해결됨)

**해결**: 최신 코드 사용 (`e598ec5` 이후 버전)
- `ai_api_module/core/ai.py`에서 이미지 파일 자동 감지 로직 추가됨

---

## 📝 개발 체크리스트

### 새 기능 추가 시
- [ ] 로컬에서 테스트 완료
- [ ] `config.json` 설정 확인
- [ ] API 엔드포인트 문서화
- [ ] 에러 핸들링 추가
- [ ] 로그 메시지 추가
- [ ] Git 커밋 & 푸시
- [ ] Render 자동 배포 확인

### 코드 리뷰 시 확인사항
- [ ] 가이드라인 준수 (미니멀리즘, 일관성, 여백)
- [ ] 에러 처리 완비
- [ ] 보안 취약점 없음 (파일 업로드, SQL 인젝션 등)
- [ ] 성능 최적화 (캐싱, 파일 크기 제한)
- [ ] 로그 레벨 적절 (DEBUG → INFO in production)

### 배포 전 확인사항
- [ ] Render 환경 변수 설정 완료
- [ ] Build Command: `./render-build.sh`
- [ ] Start Command: `gunicorn -c gunicorn_config.py app:app`
- [ ] Health Check 통과
- [ ] 실제 파일 업로드 테스트
- [ ] PDF 변환 테스트 (또는 HTML 다운로드)

---

## 🔗 유용한 링크

- **Render 대시보드**: https://dashboard.render.com
- **GitHub 저장소**: https://github.com/Haeminway1/htmldesignersite
- **AI API 문서**:
  - Google Gemini: https://ai.google.dev/docs
  - OpenAI GPT: https://platform.openai.com/docs
  - Anthropic Claude: https://docs.anthropic.com

---

## 📞 지원 및 문의

문제가 발생하거나 질문이 있으시면:
1. **GitHub Issues** 페이지에 문의
2. **로그 파일 확인**: Render 대시보드 → Logs
3. **브라우저 개발자 도구** 콘솔 확인
4. 이 문서의 **트러블슈팅** 섹션 참조

---

**마지막 업데이트**: 2025년 10월 7일  
**작성자**: 개발팀  
**버전**: 1.0.0 (e598ec5)
