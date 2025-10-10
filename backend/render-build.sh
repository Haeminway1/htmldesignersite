#!/bin/bash

# Render 배포용 빌드 스크립트
set -e  # 오류 시 중단

echo "🚀 Render 배포용 빌드 시작..."
echo "📁 현재 디렉토리: $(pwd)"
echo "📋 파일 목록:"
ls -la

# backend 디렉토리로 이동 (Root Directory가 backend/로 설정되어 있어야 함)
echo "📁 작업 디렉토리 확인..."
if [ -f "requirements.txt" ]; then
    echo "✅ requirements.txt 발견: $(pwd)/requirements.txt"
elif [ -f "backend/requirements.txt" ]; then
    echo "📁 backend 디렉토리로 이동..."
    cd backend
    echo "📁 새 작업 디렉토리: $(pwd)"
    ls -la
elif [ -f "../requirements.txt" ]; then
    echo "📁 상위 디렉토리에서 requirements.txt 발견"
    cd ..
    echo "📁 새 작업 디렉토리: $(pwd)"
else
    echo "❌ requirements.txt를 찾을 수 없습니다"
    echo "📋 전체 구조 확인:"
    find . -name "requirements.txt" -type f 2>/dev/null || echo "requirements.txt 파일이 없습니다"
    exit 1
fi

# Python 의존성 설치
echo "📦 Python 의존성 설치 중..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ requirements.txt 설치 완료"

# AI API 모듈 설치 (editable 대신 직접 설치)
echo "📦 AI API 모듈 설치 중..."
if [ -d "ai_api_module_v3/ai_api_module" ]; then
    # ai_api_module 디렉토리를 PYTHONPATH에 추가하기 위해 복사
    echo "📦 AI API 모듈을 Python 경로에 복사 중..."
    mkdir -p ~/.local/lib/python$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')/site-packages/
    cp -r ai_api_module_v3/ai_api_module ~/.local/lib/python$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')/site-packages/ || echo "⚠️ AI 모듈 복사 실패, 상대 경로 사용"
    echo "✅ AI API 모듈 설치 완료"
else
    echo "⚠️ ai_api_module 디렉토리를 찾을 수 없습니다"
fi

# Chrome 및 ChromeDriver 설치 (PDF 변환용 - 최우선)
echo "📥 Chrome 및 ChromeDriver 설치 중..."
# Render는 Ubuntu 기반이므로 apt-get 사용 가능
if command -v apt-get &> /dev/null; then
    echo "📦 Chrome 및 한글 폰트 설치 시도..."
    # Chrome dependencies 및 한글 폰트 설치
    apt-get update -qq || sudo apt-get update -qq || echo "⚠️ apt-get update 실패 (권한 제한)"
    apt-get install -y -qq wget gnupg chromium-browser chromium-chromedriver \
        fonts-noto-cjk fonts-noto-cjk-extra fonts-nanum fonts-nanum-coding || \
    sudo apt-get install -y -qq wget gnupg chromium-browser chromium-chromedriver \
        fonts-noto-cjk fonts-noto-cjk-extra fonts-nanum fonts-nanum-coding || \
    echo "⚠️ Chrome/폰트 설치 실패 (권한 제한), 웹폰트 사용"
    
    # ChromeDriver 경로 확인
    if command -v chromium-chromedriver &> /dev/null; then
        echo "✅ ChromeDriver 설치 완료: $(which chromium-chromedriver)"
    elif command -v chromedriver &> /dev/null; then
        echo "✅ ChromeDriver 설치 완료: $(which chromedriver)"
    else
        echo "⚠️ ChromeDriver를 찾을 수 없습니다. Selenium PDF 변환은 비활성화됩니다."
    fi
    
    # Chrome 경로 확인
    if command -v chromium-browser &> /dev/null; then
        echo "✅ Chrome 설치 완료: $(which chromium-browser)"
    elif command -v google-chrome &> /dev/null; then
        echo "✅ Chrome 설치 완료: $(which google-chrome)"
    else
        echo "⚠️ Chrome을 찾을 수 없습니다."
    fi
    
    # 한글 폰트 설치 확인
    if fc-list | grep -i "noto" &> /dev/null; then
        echo "✅ 한글 폰트 (Noto CJK) 설치 완료"
    else
        echo "⚠️ 한글 폰트를 찾을 수 없습니다. 웹폰트가 사용됩니다."
    fi
else
    echo "⚠️ apt-get을 사용할 수 없는 환경입니다. Chrome 및 한글 폰트 설치를 건너뜁니다."
fi

# wkhtmltopdf 다운로드 (폴백 옵션)
echo "📥 wkhtmltopdf 다운로드 중..."
if [ -f "download_wkhtmltopdf.py" ]; then
    python3 download_wkhtmltopdf.py || echo "⚠️ wkhtmltopdf 다운로드 실패 (계속 진행)"
else
    echo "⚠️ download_wkhtmltopdf.py 파일을 찾을 수 없습니다"
fi

# 실행 권한 설정
if [ -f "./bin/wkhtmltopdf" ]; then
    chmod +x ./bin/wkhtmltopdf
    echo "✅ wkhtmltopdf 실행 권한 설정 완료"
else
    echo "⚠️ wkhtmltopdf 바이너리를 찾을 수 없습니다. (Chrome 변환이 우선 사용됩니다)"
fi

# 환경 변수 확인
echo "🔍 환경 변수 확인..."
if [ -z "$GOOGLE_API_KEY" ] && [ -z "$OPENAI_API_KEY" ] && [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  경고: AI API 키가 설정되지 않았습니다!"
    echo "⚠️  Render 환경 변수에 다음 중 하나 이상을 설정해주세요:"
    echo "   - GOOGLE_API_KEY"
    echo "   - OPENAI_API_KEY"
    echo "   - ANTHROPIC_API_KEY"
else
    echo "✅ AI API 키 확인됨"
fi

# Gunicorn 설정 파일 생성
echo "⚙️  Gunicorn 설정 파일 생성 중..."
cat > gunicorn_config.py << 'EOF'
# Gunicorn 설정 (Render 최적화)
import multiprocessing
import os

# 워커 설정
workers = 1  # 메모리 제한으로 1개만 사용
worker_class = 'sync'
worker_connections = 1000
timeout = 300  # 5분 (AI API 응답 대기)
keepalive = 5
max_requests = 100
max_requests_jitter = 10

# 로깅
accesslog = '-'
errorlog = '-'
loglevel = 'info'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# 바인딩
bind = f"0.0.0.0:{os.environ.get('PORT', '10000')}"

# 프로세스 이름
proc_name = 'htmldesigner'

# 서버 재시작
preload_app = False
reload = False

# 메모리 관리
worker_tmp_dir = '/dev/shm'  # tmpfs 사용
EOF

echo "✅ gunicorn_config.py 생성 완료"
echo "✅ 빌드 완료!"
