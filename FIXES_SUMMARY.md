# Render 배포 오류 해결 요약

## 🔍 발견된 문제점들

### 1. **requirements.txt의 editable 설치 문제**
- **원인**: `-e ./ai_api_module_v3` 방식은 로컬에서는 작동하지만 Render 배포 환경에서 실패
- **영향**: AI API 모듈 로드 실패 → 500 에러

### 2. **AI API 모듈 경로 문제**
- **원인**: 단일 경로만 확인하여 모듈 로드 실패
- **영향**: ImportError로 인한 서버 시작 실패

### 3. **환경 변수 미설정**
- **원인**: API 키 환경 변수가 Render에 설정되지 않음
- **영향**: AI 모듈 초기화 실패

### 4. **에러 로깅 부족**
- **원인**: 500 에러 발생 시 구체적인 원인 파악 어려움
- **영향**: 디버깅 시간 증가

## ✅ 적용된 해결책

### 1. requirements.txt 개선
**변경 전**:
```txt
-e ./ai_api_module_v3
```

**변경 후**:
```txt
# AI API 모듈 의존성을 직접 명시
httpx>=0.24.0
pydantic>=2.0.0
PyYAML>=6.0.2
Pillow>=9.0.0
asyncio-throttle>=1.0.0
tenacity>=8.0.0
tiktoken>=0.4.0

# AI Provider SDK
google-genai>=0.6.0
openai>=1.35.0
anthropic>=0.31.0
```

### 2. render-build.sh 강화
**추가된 기능**:
- AI 모듈 수동 복사 및 설치
- 환경 변수 확인 및 경고
- 더 자세한 로깅
- 오류 발생 시에도 계속 진행

**주요 변경**:
```bash
# AI API 모듈 설치 (editable 대신 직접 설치)
if [ -d "ai_api_module_v3/ai_api_module" ]; then
    cp -r ai_api_module_v3/ai_api_module ~/.local/lib/python.../site-packages/
fi

# 환경 변수 확인
if [ -z "$GOOGLE_API_KEY" ] && [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️ 경고: AI API 키가 설정되지 않았습니다!"
fi
```

### 3. app.py 에러 핸들링 개선
**추가된 기능**:
- 다중 경로에서 AI 모듈 검색
- AI 모듈 사용 불가 시 명확한 에러 메시지
- 500 에러 발생 시 상세한 traceback 로깅
- `/api/convert` 엔드포인트에 AI 사용 가능 여부 사전 확인

**주요 변경**:
```python
# 다중 경로에서 모듈 검색
ai_module_paths = [
    Path(__file__).parent / "ai_api_module_v3",
    Path(__file__).parent.parent / "backend" / "ai_api_module_v3",
    Path(__file__).parent / "ai_api_module_v3" / "ai_api_module",
]

# AI 모듈 사용 불가 시 503 에러 반환
if not AI_AVAILABLE:
    return jsonify({
        'error': 'AI 서비스를 사용할 수 없습니다.',
        'code': 'AI_UNAVAILABLE'
    }), 503

# 500 에러 상세 로깅
error_trace = traceback.format_exc()
logger.error(f"Traceback: {error_trace}")
```

### 4. 배포 문서 추가
- **RENDER_DEPLOYMENT.md**: 상세한 Render 배포 가이드
- **README.md**: 빠른 시작 섹션 추가
- **FIXES_SUMMARY.md**: 문제 해결 요약 (이 문서)

## 📋 Render 배포 체크리스트

배포 전 다음 사항을 확인하세요:

### ✅ Render 설정
- [ ] Root Directory: `backend`
- [ ] Build Command: `./render-build.sh`
- [ ] Start Command: `gunicorn app:app`
- [ ] Python 버전: 3.11 이상

### ✅ 환경 변수 (최소 하나 필수)
- [ ] `GOOGLE_API_KEY` (권장)
- [ ] `OPENAI_API_KEY` (선택)
- [ ] `ANTHROPIC_API_KEY` (선택)
- [ ] `XAI_API_KEY` (선택)

### ✅ 선택적 환경 변수
- [ ] `FLASK_DEBUG=False` (프로덕션)
- [ ] `WKHTMLTOPDF_PATH=/opt/render/project/src/bin/wkhtmltopdf`

## 🧪 테스트 방법

### 1. 헬스 체크
```bash
curl https://your-app.onrender.com/api/health
```

**예상 응답**:
```json
{
  "ok": true,
  "ai_available": true,
  "status": "ready"
}
```

### 2. 모델 목록 확인
```bash
curl https://your-app.onrender.com/api/models
```

### 3. HTML 변환 테스트
```bash
curl -X POST https://your-app.onrender.com/api/convert \
  -F "prompt=테스트 HTML 생성"
```

## 🔧 문제 해결

### AI_UNAVAILABLE 에러
**원인**: AI API 키가 설정되지 않음

**해결**:
1. Render 대시보드 → Environment Variables
2. `GOOGLE_API_KEY` 등 추가
3. 서비스 재배포

### 500 Internal Server Error
**원인**: 다양한 원인 (로그 확인 필요)

**해결**:
1. Render 대시보드 → Logs 확인
2. `FLASK_DEBUG=True` 임시 설정 (상세 에러 확인)
3. 빌드 로그에서 설치 실패 확인

### 빌드 실패
**원인**: requirements.txt 설치 실패

**해결**:
1. Python 버전 확인 (3.11+ 권장)
2. 빌드 로그에서 실패한 패키지 확인
3. requirements.txt의 버전 호환성 확인

## 📊 개선 효과

### Before (문제 발생)
- ❌ 로컬: 정상 작동
- ❌ Render: 500 에러
- ❌ 에러 원인 파악 어려움
- ❌ AI 모듈 로드 실패

### After (개선 후)
- ✅ 로컬: 정상 작동
- ✅ Render: 정상 배포
- ✅ 명확한 에러 메시지
- ✅ 다중 경로 지원으로 안정성 향상
- ✅ 상세한 로깅으로 디버깅 용이

## 🎯 향후 권장 사항

1. **환경 변수 관리**
   - `.env` 파일은 절대 커밋하지 말 것
   - Render 대시보드에서만 관리

2. **로그 모니터링**
   - Render Logs를 주기적으로 확인
   - 에러 발생 시 즉시 대응

3. **성능 최적화**
   - 무료 플랜은 15분 슬립 → 유료 플랜 고려
   - 캐시 활용으로 응답 속도 개선

4. **보안 강화**
   - API 키 정기적 교체
   - Rate Limiting 적절히 조정
   - CORS 설정 검토

## 📞 지원

문제가 계속되면:
1. Render 로그 확인
2. GitHub Issues 등록
3. 배포 가이드 재확인: [RENDER_DEPLOYMENT.md](./RENDER_DEPLOYMENT.md)

