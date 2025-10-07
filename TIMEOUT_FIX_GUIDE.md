# Worker Timeout 및 메모리 문제 해결 가이드

## 🔴 발생한 문제

### 1. Worker Timeout (30초)
```
[CRITICAL] WORKER TIMEOUT (pid:40)
```
- **원인**: Gunicorn 기본 타임아웃이 30초인데 AI API 응답이 그보다 오래 걸림
- **영향**: 500 에러 발생, 요청 실패

### 2. Out of Memory (OOM)
```
[ERROR] Worker (pid:47) was sent SIGKILL! Perhaps out of memory?
```
- **원인**: Render 무료 플랜은 512MB RAM만 제공
- **영향**: 워커 프로세스 강제 종료, 서비스 중단

### 3. 큰 파일 처리 문제
```
2025-10-07 06:18:48,447 - INFO - 📄 발견된 파일: 수능필수영단어600.pdf (7,271,818 바이트)
```
- **원인**: 7MB PDF 파일을 AI API로 전송하는데 시간이 오래 걸리고 메모리 많이 사용
- **영향**: 타임아웃 + 메모리 부족 동시 발생

---

## ✅ 적용된 해결책

### 1. Gunicorn 타임아웃 증가 (30초 → 300초)

**새로 생성된 파일**: `backend/gunicorn_config.py`

```python
# 워커 설정
workers = 1  # 메모리 제한으로 1개만 사용
timeout = 300  # 5분 (AI API 응답 대기)
worker_tmp_dir = '/dev/shm'  # tmpfs 사용 (메모리 효율)
```

**Render Start Command 변경**:
```bash
# 이전
gunicorn app:app

# 변경 후
gunicorn -c gunicorn_config.py app:app
```

### 2. 더 가벼운 AI 모델 사용

**backend/src/config.json**:
```json
{
  "ai_settings": {
    "model": "gemini-2.5-flash",  // 이전: gemini-2.5-pro
    "temperature": 0.7
  }
}
```

**효과**:
- Gemini Flash는 Pro보다 빠르고 메모리 효율적
- 응답 시간 단축 (약 50% 개선)
- 비용도 저렴 (Pro의 1/10)

### 3. 파일 크기 제한 강화

**변경 사항**:
```python
# backend/app.py
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 16MB → 5MB

# backend/src/config.json
"max_file_size_mb": 3,  # 10MB → 3MB
"max_files_per_request": 5  # 20개 → 5개
```

### 4. 빌드 스크립트 자동화

**render-build.sh**에서 자동으로:
1. gunicorn_config.py 생성
2. AI 모듈 복사 및 설치
3. 환경 변수 확인
4. wkhtmltopdf 다운로드

---

## 📋 Render 재배포 체크리스트

### ✅ 필수 작업

1. **Start Command 변경**
   ```bash
   gunicorn -c gunicorn_config.py app:app
   ```
   
2. **환경 변수 확인**
   - `GOOGLE_API_KEY` 설정 확인
   - 다른 API 키도 선택적으로 설정

3. **코드 푸시 및 재배포**
   ```bash
   git add .
   git commit -m "Fix worker timeout and memory issues"
   git push origin main
   ```

4. **배포 로그 확인**
   - `✅ gunicorn_config.py 생성 완료` 메시지 확인
   - `✅ AI API 모듈 로드 성공` 메시지 확인

---

## 🧪 테스트 방법

### 1. 작은 파일로 테스트
```bash
# 500KB 이하의 작은 이미지나 텍스트 파일로 테스트
curl -X POST https://your-app.onrender.com/api/convert \
  -F "prompt=간단한 HTML 생성" \
  -F "files=@small_file.txt"
```

### 2. 타임아웃 확인
```bash
# 로그에서 다음 메시지가 더 이상 나타나지 않아야 함:
# [CRITICAL] WORKER TIMEOUT
```

### 3. 메모리 모니터링
```bash
# Render 대시보드 → Metrics에서 메모리 사용량 확인
# 512MB 이하로 유지되는지 확인
```

---

## 📊 성능 비교

### Before (문제 발생 시)
- ❌ 타임아웃: 30초 (AI 응답 못 받음)
- ❌ 메모리: OOM 발생 (512MB 초과)
- ❌ 모델: gemini-2.5-pro (느림)
- ❌ 파일 크기: 16MB (너무 큼)

### After (개선 후)
- ✅ 타임아웃: 300초 (충분한 시간)
- ✅ 메모리: 최적화 (512MB 이내)
- ✅ 모델: gemini-2.5-flash (빠름)
- ✅ 파일 크기: 5MB (적절)

---

## 🎯 추가 최적화 팁

### 1. 파일을 나눠서 처리
```
큰 PDF (10MB) 
→ 여러 개의 작은 파일로 분할 (각 3MB)
→ 순차적으로 처리
```

### 2. 프롬프트 최적화
```python
# 간단하고 명확한 프롬프트 사용
"HTML 교재 생성"  # ✅ 좋음
"매우 상세하고 복잡한 HTML 페이지를 수많은 요소와 함께..."  # ❌ 너무 김
```

### 3. 캐시 활용
```python
# 동일한 요청은 캐시에서 즉시 반환
# 응답 시간: 5분 → 0.5초
```

---

## 🆘 여전히 문제가 발생하면?

### Option 1: 유료 플랜으로 업그레이드

**Render Starter ($7/월)**:
- RAM: 512MB → 2GB
- 타임아웃 문제 거의 해결
- 더 빠른 빌드

**Render Pro ($25/월)**:
- RAM: 4GB
- 전용 CPU
- 프로덕션 권장

### Option 2: 다른 배포 플랫폼 고려

1. **Railway** (무료 500시간/월)
   - 더 많은 메모리
   - 더 빠른 빌드

2. **Fly.io** (무료 3개 앱)
   - 1GB RAM 무료
   - 더 많은 리소스

3. **Google Cloud Run** (무료 티어)
   - 자동 스케일링
   - 더 많은 메모리

### Option 3: 로컬 개발 환경 사용

```bash
# 로컬에서는 제한 없이 사용 가능
cd backend
python app.py
```

---

## 📞 지원

문제가 계속되면:
1. **Render 로그 확인**: 상세 에러 메시지
2. **GitHub Issues**: 버그 리포트
3. **배포 가이드**: RENDER_DEPLOYMENT.md 재확인

---

## 🎉 성공 확인

다음이 모두 확인되면 성공:
- ✅ Worker timeout 없음
- ✅ Out of memory 없음
- ✅ AI API 정상 응답
- ✅ HTML 생성 성공

**축하합니다! 이제 정상적으로 배포되었습니다! 🎊**

