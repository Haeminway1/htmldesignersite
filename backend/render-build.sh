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

# wkhtmltopdf 다운로드 (선택적)
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
    echo "⚠️ wkhtmltopdf 바이너리를 찾을 수 없습니다. PDF 변환 기능이 비활성화됩니다."
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

echo "✅ 빌드 완료!"
