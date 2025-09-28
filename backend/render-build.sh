#!/bin/bash

# Render 배포용 빌드 스크립트

echo "🚀 Render 배포용 빌드 시작..."

# Python 의존성 설치
echo "📦 Python 의존성 설치 중..."
pip install -r requirements.txt

# wkhtmltopdf 다운로드
echo "📥 wkhtmltopdf 다운로드 중..."
python download_wkhtmltopdf.py

# 실행 권한 설정
if [ -f "./bin/wkhtmltopdf" ]; then
    chmod +x ./bin/wkhtmltopdf
    echo "✅ wkhtmltopdf 실행 권한 설정 완료"
else
    echo "⚠️ wkhtmltopdf 바이너리를 찾을 수 없습니다. 수동 설치가 필요할 수 있습니다."
fi

echo "✅ 빌드 완료!"
