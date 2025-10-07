# Render 배포 가이드

## 🚀 Render 배포 설정

### 1. Render 프로젝트 설정

1. **Render 대시보드**에 로그인하세요: https://dashboard.render.com
2. **New > Web Service**를 클릭하세요
3. GitHub 저장소를 연결하세요

### 2. 배포 설정

#### 기본 설정
- **Name**: `html-designer-site` (원하는 이름)
- **Region**: `Singapore` 또는 가장 가까운 지역
- **Branch**: `main`
- **Root Directory**: `backend`
- **Runtime**: `Python 3`
- **Build Command**: `./render-build.sh`
- **Start Command**: `gunicorn app:app`

#### 환경 변수 설정 (Environment Variables)

**필수 환경 변수** - 다음 중 **최소 하나**는 필수입니다:

```bash
# Google AI (권장)
GOOGLE_API_KEY=your_google_api_key_here

# OpenAI (선택)
OPENAI_API_KEY=sk-your_openai_key_here

# Anthropic (선택)
ANTHROPIC_API_KEY=sk-ant-your_anthropic_key_here

# xAI (선택)
XAI_API_KEY=xai-your_xai_key_here
```

**선택적 환경 변수**:

```bash
# Flask 설정
FLASK_DEBUG=False
PORT=10000

# wkhtmltopdf 경로 (자동 설치됨)
WKHTMLTOPDF_PATH=/opt/render/project/src/bin/wkhtmltopdf
```

### 3. API 키 발급 방법

#### Google AI API 키 (Gemini)
1. https://makersuite.google.com/app/apikey 방문
2. **Create API Key** 클릭
3. API 키를 복사하여 Render 환경 변수에 추가

#### OpenAI API 키
1. https://platform.openai.com/api-keys 방문
2. **Create new secret key** 클릭
3. API 키를 복사하여 Render 환경 변수에 추가

#### Anthropic API 키 (Claude)
1. https://console.anthropic.com/settings/keys 방문
2. **Create Key** 클릭
3. API 키를 복사하여 Render 환경 변수에 추가

### 4. 배포 진행

1. 모든 설정을 확인한 후 **Create Web Service** 클릭
2. 빌드 로그를 확인하면서 진행 상황을 모니터링하세요
3. 빌드가 완료되면 자동으로 배포됩니다

### 5. 배포 확인

배포가 완료되면 다음 엔드포인트로 확인할 수 있습니다:

```bash
# 헬스 체크
curl https://your-app.onrender.com/api/health

# 응답 예시:
{
  "ok": true,
  "timestamp": "2025-10-07T14:30:00",
  "ai_available": true,
  "status": "ready"
}
```

## 🔧 문제 해결

### 1. AI 모듈 로드 실패

**증상**: `AI_UNAVAILABLE` 에러 또는 `AI 서비스를 사용할 수 없습니다`

**해결 방법**:
- Render 대시보드에서 환경 변수가 올바르게 설정되었는지 확인
- 최소 하나의 AI API 키가 설정되어 있는지 확인
- 빌드 로그에서 `✅ AI API 모듈 로드 성공` 메시지 확인

### 2. 500 Internal Server Error

**증상**: API 호출 시 500 에러 발생

**해결 방법**:
1. **로그 확인**:
   - Render 대시보드 > Logs 탭에서 상세 에러 확인
   
2. **환경 변수 디버깅 활성화**:
   ```bash
   FLASK_DEBUG=True  # 임시로 설정하여 상세 에러 확인
   ```

3. **일반적인 원인**:
   - API 키 미설정
   - AI API 할당량 초과
   - 파일 경로 문제
   - 메모리 부족 (무료 플랜 제한)

### 3. wkhtmltopdf 설치 실패

**증상**: PDF 변환이 작동하지 않음

**해결 방법**:
- HTML 출력은 정상 작동하며, PDF 변환만 실패합니다
- 빌드 로그에서 wkhtmltopdf 다운로드 상태 확인
- 필요 시 수동으로 바이너리 업로드

### 4. 빌드 실패

**증상**: 빌드 단계에서 실패

**해결 방법**:
1. **requirements.txt 확인**:
   ```bash
   pip install -r backend/requirements.txt
   ```
   
2. **Python 버전 확인**:
   - Python 3.11 이상 권장
   
3. **빌드 스크립트 권한**:
   ```bash
   chmod +x backend/render-build.sh
   ```

## 📊 성능 최적화

### 무료 플랜 제한
- 메모리: 512MB
- CPU: 공유
- 15분간 요청이 없으면 자동 슬립

### 유료 플랜 권장 사항
- **Starter ($7/월)**: 512MB RAM, 더 빠른 빌드
- **Standard ($25/월)**: 2GB RAM, 프로덕션 권장

## 🔗 유용한 링크

- **Render 문서**: https://render.com/docs
- **Flask 배포 가이드**: https://flask.palletsprojects.com/en/latest/deploying/
- **Gunicorn 설정**: https://docs.gunicorn.org/en/stable/settings.html

## 📝 추가 팁

1. **커스텀 도메인 연결**:
   - Render 대시보드 > Settings > Custom Domains

2. **자동 배포 설정**:
   - GitHub 푸시 시 자동 배포 (기본 활성화)

3. **로그 모니터링**:
   - Render 대시보드 > Logs 실시간 모니터링

4. **환경 변수 관리**:
   - `.env` 파일은 **절대** 커밋하지 마세요
   - Render 대시보드에서만 설정하세요

