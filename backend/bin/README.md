# wkhtmltopdf Binary

## �ڵ� �ٿ�ε� ���� �� ���� �ٿ�ε�

1. Linux 64��Ʈ ���̳ʸ� �ٿ�ε�:
   ```bash
   wget https://github.com/JazzCore/python-pdfkit/raw/master/bin/wkhtmltopdf
   chmod +x wkhtmltopdf
   ```

2. �Ǵ� ���� ��Ű������:
   ```bash
   wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.jammy_amd64.deb
   dpkg -x wkhtmltox_0.12.6.1-2.jammy_amd64.deb .
   cp usr/local/bin/wkhtmltopdf ./
   ```

3. Render ȯ�溯�� ����:
   ```
   WKHTMLTOPDF_PATH=/opt/render/project/src/backend/bin/wkhtmltopdf
   ```
