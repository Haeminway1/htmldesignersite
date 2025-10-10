#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 기반 HTML 교재 생성기 - Flask 웹 애플리케이션
Render 배포용 웹 서비스
"""

import os
import sys
import json
import uuid
import logging
import tempfile
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import hashlib
import mimetypes

from flask import Flask, request, jsonify, send_file, send_from_directory, abort
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

# PDF 변환 라이브러리 임포트
# 우선순위: Chrome (Selenium) > weasyprint > pdfkit
PDF_BACKEND = None
PDF_BACKENDS_AVAILABLE = []

# Chrome (Selenium) 체크
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    PDF_BACKENDS_AVAILABLE.append('chrome')
except ImportError:
    pass

# WeasyPrint 체크
try:
    from weasyprint import HTML as WeasyHTML
    PDF_BACKEND = 'weasyprint'
    PDF_BACKENDS_AVAILABLE.append('weasyprint')
except ImportError:
    pass

# pdfkit 체크
try:
    import pdfkit
    if not PDF_BACKEND:
        PDF_BACKEND = 'pdfkit'
    PDF_BACKENDS_AVAILABLE.append('pdfkit')
except ImportError:
    pass

# AI API 모듈 가져오기
ai_module_paths = [
    Path(__file__).parent / "ai_api_module_v3",
    Path(__file__).parent.parent / "backend" / "ai_api_module_v3",
    Path(__file__).parent / "ai_api_module_v3" / "ai_api_module",
]

AI_AVAILABLE = False
AI = None

for ai_module_path in ai_module_paths:
    if ai_module_path.exists():
        sys.path.insert(0, str(ai_module_path))
        print(f"📦 AI 모듈 경로 추가: {ai_module_path}")

try:
    from ai_api_module import AI
    AI_AVAILABLE = True
    print("✅ AI API 모듈 로드 성공")
except ImportError as e:
    print(f"⚠️ AI API 모듈을 찾을 수 없습니다: {e}")
    print(f"확인한 경로들: {[str(p) for p in ai_module_paths]}")
    print(f"현재 sys.path: {sys.path[:3]}")
    print("🔄 AI API 모듈 없이 기본 서버로 실행합니다.")
    AI = None
    AI_AVAILABLE = False

# 기존 HTML 디자이너 클래스 가져오기
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))
try:
    from basic_html_designer import HTMLDesigner
    print("✅ HTMLDesigner 클래스 로드 성공")
except ImportError as e:
    print(f"❌ HTMLDesigner 클래스를 찾을 수 없습니다: {e}")
    print(f"src 경로: {src_path}")
    print(f"src 경로 존재 여부: {src_path.exists()}")
    if src_path.exists():
        print(f"src 디렉토리 내용: {list(src_path.iterdir())}")
    print("⚠️ AI 모듈 없이는 서버 실행이 불가능합니다.")
    if not AI_AVAILABLE:
        print("❌ AI 모듈과 HTMLDesigner 모두 로드 실패. 서버를 시작할 수 없습니다.")
        sys.exit(1)
    else:
        # AI가 있으면 일단 계속 진행
        HTMLDesigner = None
        print("⚠️ HTMLDesigner 없이 AI API만으로 실행합니다.")

# Flask 앱 초기화
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 20MB 제한
app.url_map.strict_slashes = False  # /api/convert 와 /api/convert/ 모두 허용

# CORS 설정
CORS(app, origins=["*"])  # 프로덕션에서는 특정 도메인으로 제한

# Rate Limiting 설정 (flask-limiter v3.x 호환)
# 단일 워커 환경이므로 in-memory storage 사용 (프로덕션에서도 안전)
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["200 per hour", "20 per minute"],  # 제한 완화
    storage_uri="memory://",  # 명시적으로 in-memory 지정 (경고 제거)
    strategy="fixed-window"  # 고정 윈도우 전략
)

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# PDF 백엔드 로깅
if 'chrome' in PDF_BACKENDS_AVAILABLE:
    logger.info("✅ Chrome (Selenium) 사용 가능 (최우선, 가장 정확한 PDF 변환)")
if PDF_BACKEND == 'weasyprint':
    logger.info("✅ WeasyPrint 폴백 사용 가능")
elif PDF_BACKEND == 'pdfkit':
    logger.info("✅ pdfkit 폴백 사용 가능 (wkhtmltopdf 필요)")

if not PDF_BACKENDS_AVAILABLE:
    logger.warning("⚠️ PDF 변환 라이브러리가 없습니다. HTML만 반환됩니다.")
else:
    logger.info(f"📦 사용 가능한 PDF 백엔드: {', '.join(PDF_BACKENDS_AVAILABLE)}")

# 전역 변수
TEMP_DIR = Path(tempfile.gettempdir()) / "html_designer"
TEMP_DIR.mkdir(exist_ok=True)

# 프런트엔드 정적 파일 디렉토리 (존재 시 사용)
FRONT_DIR = (Path(__file__).parent.parent / "frontend").resolve()

# PDF 파일 저장 및 캐시
PDF_CACHE = {}  # {hash: {"path": str, "created": datetime}}
PDF_CACHE_DURATION = timedelta(hours=24)

# 허용되는 파일 형식
ALLOWED_EXTENSIONS = {
    '.pdf', '.docx', '.doc', '.xlsx', '.xls', '.pptx', '.ppt',
    '.txt', '.md', '.csv', '.json', '.xml', '.html', '.htm',
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.avif', '.heic', '.heif', '.svg',
    '.epub', '.zip'
}

def is_allowed_file(filename):
    """허용된 파일 형식인지 확인"""
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS

def cleanup_temp_files():
    """임시 파일 정리"""
    try:
        current_time = datetime.now()
        for file_hash, info in list(PDF_CACHE.items()):
            if current_time - info["created"] > PDF_CACHE_DURATION:
                try:
                    os.unlink(info["path"])
                    del PDF_CACHE[file_hash]
                except:
                    pass
    except Exception as e:
        logger.warning(f"임시 파일 정리 실패: {e}")

def generate_content_hash(prompt: str, files_content: list) -> str:
    """프롬프트와 파일 내용으로 해시 생성"""
    content = prompt + "".join(files_content)
    return hashlib.md5(content.encode()).hexdigest()

class WebHTMLDesigner:
    """웹용 HTML 디자이너 래퍼 클래스"""
    
    def __init__(self):
        # config.json 경로 설정
        config_path = Path(__file__).parent / "src" / "config.json"
        self.designer = HTMLDesigner(str(config_path))
        
        # wkhtmltopdf 경로 설정
        self.wkhtmltopdf_path = os.getenv('WKHTMLTOPDF_PATH', 'wkhtmltopdf')
        
        # PDF 설정
        self.pdf_options = {
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'no-outline': None,
            'enable-local-file-access': None
        }
    
    def generate_html_from_files(self, prompt: str, uploaded_files: list) -> Dict[str, Any]:
        """파일들로부터 HTML 생성"""
        try:
            # 임시 input 디렉토리 생성
            temp_input_dir = TEMP_DIR / f"input_{uuid.uuid4().hex}"
            temp_input_dir.mkdir(exist_ok=True)
            
            # 업로드된 파일들을 임시 디렉토리에 저장
            saved_files = []
            for file_data in uploaded_files:
                filename = secure_filename(file_data['filename'])
                file_path = temp_input_dir / filename
                
                with open(file_path, 'wb') as f:
                    f.write(file_data['content'])
                
                saved_files.append(file_path)
                logger.info(f"임시 파일 저장: {file_path}")
            
            # config 파일 임시 수정 (input_directory 경로 변경)
            original_config = self.designer.config.copy()
            if 'file_processing' not in self.designer.config:
                self.designer.config['file_processing'] = {}
            self.designer.config['file_processing']['input_directory'] = str(temp_input_dir)
            
            # 프롬프트 임시 변경
            original_prompt = self.designer.config.get('prompts', {}).get('user_prompt', '')
            self.designer.config['prompts']['user_prompt'] = prompt
            
            # HTML 생성 (Google 실패 시 모델 자동 폴백)
            try:
                html_content, metadata = self.designer.generate_html()
            except Exception as gen_err:
                logger.warning(f"1차 생성 실패, 모델 폴백 시도: {gen_err}")
                original_model = self.designer.config.get('ai_settings', {}).get('model')
                # 우선 빠른 모델로 폴백
                self.designer.config['ai_settings']['model'] = 'fast'
                try:
                    html_content, metadata = self.designer.generate_html()
                except Exception as gen_err2:
                    logger.warning(f"2차 생성 실패, 스마트 모델 폴백 시도: {gen_err2}")
                    self.designer.config['ai_settings']['model'] = 'smart'
                    html_content, metadata = self.designer.generate_html()
            
            # config 복원
            self.designer.config = original_config
            
            # 임시 파일 정리
            for file_path in saved_files:
                try:
                    os.unlink(file_path)
                except:
                    pass
            temp_input_dir.rmdir()
            
            return {
                'success': True,
                'html': html_content,
                'metadata': metadata
            }
            
        except Exception as e:
            logger.error(f"HTML 생성 실패: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def html_to_pdf(self, html_content: str) -> Optional[str]:
        """
        HTML을 PDF로 변환
        우선순위: Chrome (Selenium) > weasyprint > pdfkit
        Chrome을 사용하면 브라우저에서 보이는 그대로 정확하게 PDF 변환
        """
        global PDF_BACKEND
        
        try:
            # PDF 파일 경로 생성
            pdf_filename = f"output_{uuid.uuid4().hex}.pdf"
            pdf_path = TEMP_DIR / pdf_filename
            
            # 1순위: Chrome (Selenium) 사용 - 가장 정확한 변환
            try:
                from selenium import webdriver
                from selenium.webdriver.chrome.service import Service
                from selenium.webdriver.chrome.options import Options
                import base64
                
                logger.info("🔄 Chrome 엔진으로 PDF 변환 시도...")
                
                # 임시 HTML 파일 생성 (Chrome이 로드할 수 있도록)
                temp_html_file = TEMP_DIR / f"temp_{uuid.uuid4().hex}.html"
                with open(temp_html_file, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                # Chrome 옵션 설정
                chrome_options = Options()
                chrome_options.add_argument('--headless')  # 백그라운드 실행
                chrome_options.add_argument('--disable-gpu')
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--disable-dev-shm-usage')
                chrome_options.add_argument('--disable-software-rasterizer')
                
                # Render/클라우드 환경에서 Chromium 바이너리 경로 설정
                chrome_binary = None
                if os.path.exists('/usr/bin/chromium-browser'):
                    chrome_binary = '/usr/bin/chromium-browser'
                elif os.path.exists('/usr/bin/chromium'):
                    chrome_binary = '/usr/bin/chromium'
                elif os.path.exists('/usr/bin/google-chrome'):
                    chrome_binary = '/usr/bin/google-chrome'
                
                if chrome_binary:
                    chrome_options.binary_location = chrome_binary
                    logger.info(f"Chrome 바이너리 경로 설정: {chrome_binary}")
                
                # Chrome 드라이버 실행
                driver = webdriver.Chrome(options=chrome_options)
                
                try:
                    # HTML 파일 열기 (절대 경로 사용)
                    html_path = temp_html_file.resolve()
                    driver.get(f"file:///{html_path}")
                    
                    # 페이지 로딩 대기 (이미지, 폰트 등)
                    driver.implicitly_wait(3)
                    
                    # Chrome의 인쇄 기능을 사용하여 PDF 생성
                    # Chrome 브라우저 "여백: 기본" 설정과 동일
                    print_options = {
                        'landscape': False,
                        'displayHeaderFooter': False,
                        'printBackground': True,
                        'preferCSSPageSize': False,
                        'paperWidth': 8.27,     # A4 width in inches (210mm)
                        'paperHeight': 11.69,   # A4 height in inches (297mm)
                        'marginTop': 0.4,       # Chrome 기본 여백 (약 10mm)
                        'marginBottom': 0.4,    # Chrome 기본 여백 (약 10mm)
                        'marginLeft': 0.4,      # Chrome 기본 여백 (약 10mm)
                        'marginRight': 0.4,     # Chrome 기본 여백 (약 10mm)
                        'scale': 1.0
                    }
                    
                    # Chrome DevTools Protocol을 사용하여 PDF 생성
                    result = driver.execute_cdp_cmd('Page.printToPDF', print_options)
                    
                    # Base64로 인코딩된 PDF 데이터를 파일로 저장
                    pdf_data = base64.b64decode(result['data'])
                    with open(pdf_path, 'wb') as f:
                        f.write(pdf_data)
                    
                    logger.info(f"✅ PDF 생성 완료 (Chrome): {pdf_path}")
                    return str(pdf_path)
                    
                finally:
                    driver.quit()
                    # 임시 HTML 파일 삭제
                    try:
                        os.unlink(temp_html_file)
                    except:
                        pass
                    
            except ImportError:
                logger.warning("⚠️ Selenium이 설치되지 않았습니다. 대체 방법으로 시도합니다.")
            except Exception as chrome_err:
                logger.warning(f"⚠️ Chrome 변환 실패: {chrome_err}. 대체 방법으로 시도합니다.")
                import traceback
                logger.debug(f"Chrome 오류 상세: {traceback.format_exc()}")
            
            # 2순위: WeasyPrint 사용
            if PDF_BACKEND == 'weasyprint':
                from weasyprint import HTML as WeasyHTML
                WeasyHTML(string=html_content, base_url='.').write_pdf(str(pdf_path))
                logger.info(f"✅ PDF 생성 완료 (WeasyPrint): {pdf_path}")
                return str(pdf_path)
            
            # 3순위: pdfkit 사용
            elif PDF_BACKEND == 'pdfkit':
                import pdfkit
                config = pdfkit.configuration(wkhtmltopdf=self.wkhtmltopdf_path)
                pdfkit.from_string(
                    html_content, 
                    str(pdf_path), 
                    options=self.pdf_options,
                    configuration=config
                )
                logger.info(f"✅ PDF 생성 완료 (pdfkit): {pdf_path}")
                return str(pdf_path)
            else:
                logger.warning("PDF 변환 라이브러리가 설치되지 않았습니다")
                return None
            
        except Exception as e:
            logger.error(f"❌ PDF 변환 실패: {e}")
            import traceback
            logger.error(f"상세 오류: {traceback.format_exc()}")
            return None

# 전역 디자이너 인스턴스
designer = None

def get_designer():
    """디자이너 인스턴스 가져오기 (lazy loading)"""
    global designer
    if designer is None:
        designer = WebHTMLDesigner()
    return designer

@app.before_request
def before_request():
    """요청 전 처리"""
    cleanup_temp_files()

@app.route('/', methods=['GET', 'HEAD'])
def root_index():
    """루트 경로: 프런트엔드 index.html 서빙 또는 상태 JSON"""
    if request.method == 'HEAD':
        return ("", 200)
    try:
        if FRONT_DIR.exists() and (FRONT_DIR / 'index.html').exists():
            return send_from_directory(str(FRONT_DIR), 'index.html')
    except Exception:
        pass
    return jsonify(status="ok", message="Backend is running"), 200

@app.route('/favicon.ico', methods=['GET'])
def favicon():
    """파비콘: 있으면 서빙, 없으면 204"""
    try:
        fav = FRONT_DIR / 'favicon.ico'
        if fav.exists():
            return send_from_directory(str(FRONT_DIR), 'favicon.ico')
    except Exception:
        pass
    return ("", 204)

@app.errorhandler(413)
def too_large(e):
    """파일 크기 초과 에러 처리"""
    return jsonify({
        'error': '파일 크기가 너무 큽니다. 최대 20MB까지 허용됩니다.',
        'code': 'FILE_TOO_LARGE',
        'max_size': '20MB'
    }), 413

@app.errorhandler(500)
def internal_error(e):
    """내부 서버 에러 처리"""
    import traceback
    error_trace = traceback.format_exc()
    logger.error(f"Internal server error: {e}")
    logger.error(f"Traceback: {error_trace}")
    
    # 디버그 모드에서는 자세한 에러 정보 반환
    if app.debug or os.getenv('FLASK_DEBUG', 'False').lower() == 'true':
        return jsonify({
            'error': '서버 내부 오류가 발생했습니다.',
            'code': 'INTERNAL_ERROR',
            'detail': str(e),
            'traceback': error_trace
        }), 500
    
    return jsonify({
        'error': '서버 내부 오류가 발생했습니다.',
        'code': 'INTERNAL_ERROR',
        'detail': str(e)
    }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """헬스 체크"""
    return jsonify({
        'ok': True, 
        'timestamp': datetime.now().isoformat(),
        'ai_available': AI_AVAILABLE,
        'status': 'ready' if AI_AVAILABLE else 'limited'
    })

# 정적 파일 서빙 (프런트 자산)
@app.route('/<path:path>')
def static_assets(path):
    try:
        if path.startswith('api/'):
            abort(404)
        candidate = FRONT_DIR / path
        if FRONT_DIR.exists() and candidate.exists() and candidate.is_file():
            return send_from_directory(str(FRONT_DIR), path)
    except Exception:
        pass
    # SPA 라우팅 호환: 알 수 없는 경로는 index.html로 폴백
    if FRONT_DIR.exists() and (FRONT_DIR / 'index.html').exists():
        return send_from_directory(str(FRONT_DIR), 'index.html')
    abort(404)

@app.route('/api/convert', methods=['POST', 'OPTIONS'])
@limiter.limit("10 per minute")  # Rate limit 완화
def convert_files():
    """파일들을 HTML로 변환 후 PDF 생성"""
    try:
        if request.method == 'OPTIONS':
            # Preflight 응답
            return ("", 204)
        
        # AI 모듈 사용 가능 여부 확인
        if not AI_AVAILABLE:
            logger.error("AI 모듈이 로드되지 않았습니다")
            return jsonify({
                'error': 'AI 서비스를 사용할 수 없습니다. 서버 관리자에게 문의하세요.',
                'code': 'AI_UNAVAILABLE',
                'detail': 'AI API 모듈이 로드되지 않았습니다. API 키를 확인하세요.'
            }), 503
        
        # 프롬프트 가져오기
        prompt = request.form.get('prompt', '').strip()
        if not prompt:
            return jsonify({
                'error': '프롬프트를 입력해주세요.',
                'code': 'MISSING_PROMPT'
            }), 400
        
        # 파일들 가져오기 (선택사항)
        files = request.files.getlist('files')
        logger.info(f"📎 요청에서 받은 파일 수: {len(files)}")
        
        # 파일 검증 및 데이터 수집
        uploaded_files = []
        total_size = 0
        
        for file in files:
            if file.filename == '':
                continue
            logger.info(f"📄 파일 처리 중: {file.filename}")
                
            if not is_allowed_file(file.filename):
                return jsonify({
                    'error': f'허용되지 않는 파일 형식입니다: {file.filename}',
                    'code': 'INVALID_FILE_TYPE'
                }), 400
            
            file_content = file.read()
            file_size = len(file_content)
            total_size += file_size
            
            if total_size > 20 * 1024 * 1024:  # 20MB
                return jsonify({
                    'error': '전체 파일 크기가 20MB를 초과합니다.',
                    'code': 'FILES_TOO_LARGE',
                    'max_size': '20MB',
                    'current_size': f'{total_size / 1024 / 1024:.2f}MB'
                }), 400
            
            uploaded_files.append({
                'filename': file.filename,
                'content': file_content,
                'size': file_size
            })
            logger.info(f"✅ 파일 추가됨: {file.filename} ({file_size / 1024:.2f} KB)")
        
        logger.info(f"📊 총 {len(uploaded_files)}개 파일 준비 완료 (총 {total_size / 1024 / 1024:.2f} MB)")
        
        # 파일이 하나도 없어도 진행 (텍스트 프롬프트만으로 생성)
        
        # 캐시 체크
        files_content = [f['content'].decode('utf-8', errors='ignore') for f in uploaded_files] if uploaded_files else []
        content_hash = generate_content_hash(prompt, files_content)
        
        if content_hash in PDF_CACHE:
            cache_info = PDF_CACHE[content_hash]
            if datetime.now() - cache_info["created"] < PDF_CACHE_DURATION:
                if os.path.exists(cache_info["path"]):
                    logger.info(f"캐시된 결과 반환: {content_hash}")
                    return jsonify({
                        'success': True,
                        'pdf_url': f'/api/file/{content_hash}.pdf',
                        'cached': True
                    })
        
        # HTML 생성 (파일 유무에 따라 분기)
        web_designer = get_designer()
        if uploaded_files:
            result = web_designer.generate_html_from_files(prompt, uploaded_files)
        else:
            # 파일 없이 생성: 기존 config의 입력 디렉토리를 건드리지 않고 프롬프트만 사용
            original_config = web_designer.designer.config.copy()
            try:
                web_designer.designer.config['prompts']['user_prompt'] = prompt
                html, meta = web_designer.designer.generate_html()
                result = { 'success': True, 'html': html, 'metadata': meta }
            finally:
                web_designer.designer.config = original_config
        
        if not result['success']:
            return jsonify({
                'error': f'HTML 생성 실패: {result["error"]}',
                'code': 'HTML_GENERATION_FAILED'
            }), 500
        
        # PDF 변환 (wkhtmltopdf가 있는 경우에만)
        pdf_path = None
        try:
            pdf_path = web_designer.html_to_pdf(result['html'])
        except Exception as e:
            logger.warning(f"PDF 변환 실패 (HTML은 정상 생성됨): {e}")
        
        if not pdf_path:
            # PDF 변환이 실패한 경우 HTML만 반환
            return jsonify({
                'success': True,
                'html': result['html'],
                'pdf_available': False,
                'metadata': result['metadata'],
                'message': 'HTML 생성 완료 (PDF 변환 불가능)'
            })
        
        # 캐시에 저장
        PDF_CACHE[content_hash] = {
            'path': pdf_path,
            'created': datetime.now()
        }
        
        return jsonify({
            'success': True,
            'pdf_url': f'/api/file/{content_hash}.pdf',
            'html': result['html'],  # HTML도 함께 반환
            'metadata': result['metadata'],
            'cached': False
        })
        
    except Exception as e:
        logger.error(f"변환 처리 실패: {e}")
        return jsonify({
            'error': '변환 처리 중 오류가 발생했습니다.',
            'code': 'CONVERSION_ERROR'
        }), 500

@app.route('/api/file/<file_id>.pdf', methods=['GET'])
def get_pdf_file(file_id):
    """PDF 파일 다운로드/미리보기"""
    try:
        # 캐시에 파일이 없는 경우
        if file_id not in PDF_CACHE:
            logger.warning(f"⚠️ PDF 파일이 캐시에 없습니다: {file_id} (서버 재시작으로 인한 캐시 소실 가능)")
            # HTML 에러 페이지 반환 (브라우저에서 보기 좋게)
            return '''
            <!DOCTYPE html>
            <html lang="ko">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>파일 만료</title>
                <style>
                    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; 
                           display: flex; align-items: center; justify-content: center; 
                           min-height: 100vh; margin: 0; background: #f3f4f6; }
                    .container { text-align: center; padding: 2rem; background: white; 
                                 border-radius: 1rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1); max-width: 500px; }
                    h1 { color: #ef4444; font-size: 3rem; margin: 0; }
                    h2 { color: #1f2937; margin: 1rem 0; }
                    p { color: #6b7280; line-height: 1.6; }
                    .btn { display: inline-block; margin-top: 1.5rem; padding: 0.75rem 1.5rem; 
                           background: #3b82f6; color: white; text-decoration: none; 
                           border-radius: 0.5rem; font-weight: 600; }
                    .btn:hover { background: #2563eb; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>⏱️</h1>
                    <h2>파일이 만료되었습니다</h2>
                    <p>서버가 재시작되어 임시 파일이 삭제되었습니다.<br>
                       메인 페이지로 돌아가서 다시 생성해주세요.</p>
                    <a href="/" class="btn">메인으로 돌아가기</a>
                </div>
            </body>
            </html>
            ''', 404
        
        pdf_path = PDF_CACHE[file_id]['path']
        
        # 파일이 실제로 존재하지 않는 경우
        if not os.path.exists(pdf_path):
            logger.warning(f"⚠️ PDF 파일이 디스크에 없습니다: {pdf_path}")
            del PDF_CACHE[file_id]
            return '''
            <!DOCTYPE html>
            <html lang="ko">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>파일 없음</title>
                <style>
                    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; 
                           display: flex; align-items: center; justify-content: center; 
                           min-height: 100vh; margin: 0; background: #f3f4f6; }
                    .container { text-align: center; padding: 2rem; background: white; 
                                 border-radius: 1rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1); max-width: 500px; }
                    h1 { color: #ef4444; font-size: 3rem; margin: 0; }
                    h2 { color: #1f2937; margin: 1rem 0; }
                    p { color: #6b7280; line-height: 1.6; }
                    .btn { display: inline-block; margin-top: 1.5rem; padding: 0.75rem 1.5rem; 
                           background: #3b82f6; color: white; text-decoration: none; 
                           border-radius: 0.5rem; font-weight: 600; }
                    .btn:hover { background: #2563eb; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>📁</h1>
                    <h2>파일을 찾을 수 없습니다</h2>
                    <p>파일이 삭제되었습니다.<br>
                       메인 페이지로 돌아가서 다시 생성해주세요.</p>
                    <a href="/" class="btn">메인으로 돌아가기</a>
                </div>
            </body>
            </html>
            ''', 404
        
        # download 쿼리 파라미터로 다운로드/미리보기 구분
        is_download = request.args.get('download', 'false').lower() == 'true'
        
        logger.info(f"📥 PDF 파일 전송: {pdf_path} (download={is_download})")
        
        return send_file(
            pdf_path,
            as_attachment=is_download,  # download=true일 때만 다운로드
            download_name=f'html_material_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf' if is_download else None,
            mimetype='application/pdf'
        )
        
    except Exception as e:
        logger.error(f"PDF 파일 전송 실패: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return '''
        <!DOCTYPE html>
        <html lang="ko">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>오류 발생</title>
            <style>
                body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; 
                       display: flex; align-items: center; justify-content: center; 
                       min-height: 100vh; margin: 0; background: #f3f4f6; }
                .container { text-align: center; padding: 2rem; background: white; 
                             border-radius: 1rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1); max-width: 500px; }
                h1 { color: #ef4444; font-size: 3rem; margin: 0; }
                h2 { color: #1f2937; margin: 1rem 0; }
                p { color: #6b7280; line-height: 1.6; }
                .btn { display: inline-block; margin-top: 1.5rem; padding: 0.75rem 1.5rem; 
                       background: #3b82f6; color: white; text-decoration: none; 
                       border-radius: 0.5rem; font-weight: 600; }
                .btn:hover { background: #2563eb; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>⚠️</h1>
                <h2>오류가 발생했습니다</h2>
                <p>파일 전송 중 문제가 발생했습니다.<br>
                   잠시 후 다시 시도해주세요.</p>
                <a href="/" class="btn">메인으로 돌아가기</a>
            </div>
        </body>
        </html>
        ''', 500

@app.route('/api/models', methods=['GET'])
def get_available_models():
    """사용 가능한 AI 모델 목록"""
    return jsonify({
        'models': [
            {'id': 'gemini-2.5-pro', 'name': 'Gemini 2.5 Pro', 'provider': 'google'},
            {'id': 'gpt-5', 'name': 'GPT-5', 'provider': 'openai'},
            {'id': 'claude-sonnet-4', 'name': 'Claude Sonnet 4', 'provider': 'anthropic'},
            {'id': 'grok-4', 'name': 'Grok 4', 'provider': 'xai'},
            {'id': 'smart', 'name': 'Smart (Auto)', 'provider': 'auto'},
            {'id': 'fast', 'name': 'Fast (Economy)', 'provider': 'auto'}
        ]
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    app.run(host='0.0.0.0', port=port, debug=debug)
