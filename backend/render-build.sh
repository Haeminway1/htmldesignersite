#!/bin/bash

# Render 배포용 빌드 스크립트
set -e  # 오류 시 중단

echo "🚀 Render 배포용 빌드 시작..."
echo "📁 현재 디렉토리: $(pwd)"
echo "📋 파일 목록:"
ls -la

# Python 의존성 설치
echo "📦 Python 의존성 설치 중..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "✅ requirements.txt 설치 완료"
else
    echo "❌ requirements.txt 파일을 찾을 수 없습니다"
    exit 1
fi

# wkhtmltopdf 다운로드 (선택적)
echo "📥 wkhtmltopdf 다운로드 중..."
if [ -f "download_wkhtmltopdf.py" ]; then
    python download_wkhtmltopdf.py || echo "⚠️ wkhtmltopdf 다운로드 실패 (계속 진행)"
else
    echo "⚠️ download_wkhtmltopdf.py 파일을 찾을 수 없습니다"
fi

# 실행 권한 설정
if [ -f "./bin/wkhtmltopdf" ]; then
    chmod +x ./bin/wkhtmltopdf
    echo "✅ wkhtmltopdf 실행 권한 설정 완료"
else
    echo "⚠️ wkhtmltopdf 바이너리를 찾을 수 없습니다. 수동 설치가 필요할 수 있습니다."
fi

echo "✅ 빌드 완료!"
