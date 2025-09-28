# wkhtmltopdf Binary

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
