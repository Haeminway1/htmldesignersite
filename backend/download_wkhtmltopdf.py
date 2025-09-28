#!/usr/bin/env python3
"""
wkhtmltopdf 정적 바이너리 다운로드 스크립트
Render 배포를 위한 리눅스 바이너리 다운로드
"""

import os
import requests
import stat
from pathlib import Path

def download_wkhtmltopdf():
    """wkhtmltopdf 리눅스 바이너리 다운로드"""
    
    # 바이너리 URL (Ubuntu/Debian 64비트용)
    WKHTMLTOPDF_URL = "https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.jammy_amd64.deb"
    
    bin_dir = Path(__file__).parent / "bin"
    bin_dir.mkdir(exist_ok=True)
    
    # 정적 바이너리 URL (더 간단한 방법)
    STATIC_BINARY_URL = "https://github.com/JazzCore/python-pdfkit/raw/master/bin/wkhtmltopdf"
    
    binary_path = bin_dir / "wkhtmltopdf"
    
    if binary_path.exists():
        print(f"✅ wkhtmltopdf가 이미 존재합니다: {binary_path}")
        return str(binary_path)
    
    print(f"📥 wkhtmltopdf 다운로드 중...")
    print(f"URL: {STATIC_BINARY_URL}")
    
    try:
        response = requests.get(STATIC_BINARY_URL, stream=True)
        response.raise_for_status()
        
        with open(binary_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        # 실행 권한 부여
        os.chmod(binary_path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)
        
        print(f"✅ wkhtmltopdf 다운로드 완료: {binary_path}")
        print(f"📁 파일 크기: {binary_path.stat().st_size:,} 바이트")
        
        return str(binary_path)
        
    except Exception as e:
        print(f"❌ 다운로드 실패: {e}")
        
        # README 파일 생성
        readme_path = bin_dir / "README.md"
        with open(readme_path, 'w') as f:
            f.write("""# wkhtmltopdf Binary

## 자동 다운로드 실패 시 수동 다운로드

1. Linux 64비트 바이너리 다운로드:
   ```bash
   wget https://github.com/JazzCore/python-pdfkit/raw/master/bin/wkhtmltopdf
   chmod +x wkhtmltopdf
   ```

2. 또는 공식 패키지에서:
   ```bash
   wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.jammy_amd64.deb
   dpkg -x wkhtmltox_0.12.6.1-2.jammy_amd64.deb .
   cp usr/local/bin/wkhtmltopdf ./
   ```

3. Render 환경변수 설정:
   ```
   WKHTMLTOPDF_PATH=/opt/render/project/src/backend/bin/wkhtmltopdf
   ```
""")
        
        return None

if __name__ == "__main__":
    result = download_wkhtmltopdf()
    if result:
        print(f"\n🎉 성공! 환경변수 설정:")
        print(f"WKHTMLTOPDF_PATH={result}")
    else:
        print("\n⚠️ 수동 다운로드가 필요합니다. bin/README.md를 참고하세요.")
