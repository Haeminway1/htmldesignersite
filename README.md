# 🤖 AI 기반 HTML 교재 생성기

파일을 업로드하면 AI가 자동으로 멋진 HTML 교재를 생성하고 PDF로 변환해주는 웹 서비스입니다.

## ✨ 주요 기능

- 📁 **다양한 파일 형식 지원**: PDF, Word, Excel, PowerPoint, 이미지, 텍스트 등
- 🤖 **다중 AI 모델**: Gemini, GPT, Claude, Grok 등 다양한 AI 모델 선택 가능
- 📄 **PDF 자동 변환**: 생성된 HTML을 고품질 PDF로 자동 변환
- ⚡ **빠른 처리**: 캐시 시스템으로 동일한 요청은 즉시 처리
- 🔒 **안전한 업로드**: 파일 크기 및 형식 제한, Rate Limiting 적용
- 📱 **반응형 디자인**: 모바일, 태블릿, 데스크톱 모든 기기에서 사용 가능

## 🚀 빠른 시작

### Render 배포 (권장)

**5분 안에 배포 완료!** 

1. **Render 가입**: https://dashboard.render.com
2. **New > Web Service** 클릭
3. 이 저장소 연결
4. 다음 설정 적용:
   - **Root Directory**: `backend`
   - **Build Command**: `./render-build.sh`
   - **Start Command**: `gunicorn app:app`
5. **환경 변수 추가** (최소 하나 필수):
   ```bash
   GOOGLE_API_KEY=your_key_here
   ```
6. **Create Web Service** 클릭

**상세 가이드**: [RENDER_DEPLOYMENT.md](./RENDER_DEPLOYMENT.md) 참조

---

## 🛠️ 로컬 개발 환경 설정

### 1. 저장소 클론
```bash
git clone <repository-url>
cd htmldesignersite
```

### 2. 백엔드 설정
```bash
cd backend

# Python 의존성 설치
pip install -r requirements.txt

# wkhtmltopdf 다운로드 (선택사항)
python download_wkhtmltopdf.py
```

### 3. 환경변수 설정
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

### 4. 백엔드 서버 실행
```bash
cd backend
python app.py
```

### 5. 프론트엔드 실행
```bash
# 단순 정적 파일이므로 HTTP 서버로 실행
cd frontend
python -m http.server 3000
```

브라우저에서 `http://localhost:3000` 접속

## 🌐 Render 배포 가이드

### 백엔드 배포 (Web Service)

1. **Render에서 새 Web Service 생성**
2. **설정값:**
   - **Root Directory:** `backend/`
   - **Build Command:** `bash render-build.sh`
   - **Start Command:** `gunicorn app:app`
   - **Environment Variables:**
     ```
     GOOGLE_API_KEY=your-actual-api-key
     OPENAI_API_KEY=sk-proj-your-actual-key
     ANTHROPIC_API_KEY=sk-ant-your-actual-key
     WKHTMLTOPDF_PATH=/opt/render/project/src/backend/bin/wkhtmltopdf
     PORT=10000
     ```

### 프론트엔드 배포 (Static Site)

1. **Render에서 새 Static Site 생성**
2. **설정값:**
   - **Root Directory:** `frontend/`
   - **Publish Directory:** `frontend/`
   - **Build Command:** (비워둠)

3. **배포 후 설정:**
   - `frontend/script.js`에서 `API_BASE` URL을 실제 백엔드 URL로 변경
   ```javascript
   const API_BASE = 'https://your-backend.onrender.com';
   ```

## 📁 프로젝트 구조

```
htmldesignersite/
├── backend/                 # Flask 백엔드
│   ├── app.py              # 메인 웹 애플리케이션
│   ├── requirements.txt    # Python 의존성
│   ├── render-build.sh     # Render 빌드 스크립트
│   ├── download_wkhtmltopdf.py # PDF 변환 도구 설치
│   ├── bin/                # wkhtmltopdf 바이너리
│   ├── ai_api_module_v3/   # AI API 모듈
│   └── src/                # 기존 HTML 디자이너 로직
│       ├── basic_html_designer.py
│       ├── config.json
│       ├── guideline/
│       └── library/
├── frontend/               # 정적 웹사이트
│   ├── index.html         # 메인 페이지
│   ├── styles.css         # 스타일시트
│   └── script.js          # JavaScript 로직
└── README.md
```

## 🔧 API 엔드포인트

### `GET /api/health`
서버 상태 확인
```json
{
  "ok": true,
  "timestamp": "2025-09-28T12:00:00"
}
```

### `POST /api/convert`
파일들을 HTML로 변환 후 PDF 생성

**요청:**
- `prompt`: 생성 요청사항 (텍스트)
- `files`: 업로드할 파일들 (최대 20개, 16MB)

**응답:**
```json
{
  "success": true,
  "pdf_url": "/api/file/abc123.pdf",
  "metadata": {
    "model": "gemini-2.5-pro",
    "cost": 0.002340,
    "tokens_used": 1247
  },
  "cached": false
}
```

### `GET /api/file/<id>.pdf`
생성된 PDF 파일 다운로드

## ⚙️ 설정 옵션

### config.json 설정
```json
{
  "ai_settings": {
    "model": "gemini-2.5-pro",
    "temperature": 0.7
  },
  "file_processing": {
    "enable_direct_file_attachment": true,
    "max_file_size_mb": 10,
    "max_files_per_request": 20
  }
}
```

### 지원하는 파일 형식
- **문서**: PDF, Word, Excel, PowerPoint
- **텍스트**: TXT, Markdown, CSV, JSON, XML, HTML
- **이미지**: JPG, PNG, GIF, BMP, TIFF, WebP
- **기타**: EPUB, ZIP

## 🔒 보안 및 제한사항

- **Rate Limiting**: 분당 3회, 시간당 100회
- **파일 크기**: 최대 16MB
- **파일 개수**: 최대 20개
- **CORS**: 특정 도메인만 허용 (프로덕션)
- **캐시**: 24시간 동안 동일 결과 재사용

## 🛠️ 문제 해결

### 1. PDF 생성 실패
- wkhtmltopdf 바이너리가 올바르게 설치되었는지 확인
- `WKHTMLTOPDF_PATH` 환경변수 경로 확인

### 2. AI API 오류
- API 키가 올바르게 설정되었는지 확인
- API 한도를 초과하지 않았는지 확인

### 3. 파일 업로드 실패
- 파일 크기가 16MB 이하인지 확인
- 지원하는 파일 형식인지 확인

## 📞 지원

문제가 발생하거나 개선 제안이 있으시면:
1. GitHub Issues 페이지에 문의
2. 로그 파일 확인 (`backend/app.log`)
3. 브라우저 개발자 도구 콘솔 확인

---

Made with ❤️ for efficient educational material creation
