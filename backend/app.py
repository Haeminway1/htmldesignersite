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

from flask import Flask, request, jsonify, send_file, abort
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import pdfkit

# AI API 모듈 가져오기
ai_module_path = Path(__file__).parent / "ai_api_module_v3"
if not ai_module_path.exists():
    ai_module_path = Path(__file__).parent.parent / "backend" / "ai_api_module_v3"
sys.path.insert(0, str(ai_module_path))

try:
    from ai_api_module import AI
except ImportError as e:
    print(f"❌ AI API 모듈을 찾을 수 없습니다: {e}")
    print(f"확인한 경로: {ai_module_path}")
    print("AI API 모듈 없이 실행합니다.")
    AI = None

# 기존 HTML 디자이너 클래스 가져오기
sys.path.insert(0, str(Path(__file__).parent / "src"))
try:
    from basic_html_designer import HTMLDesigner
except ImportError as e:
    print(f"❌ HTMLDesigner 클래스를 찾을 수 없습니다: {e}")
    print("src/basic_html_designer.py 파일이 있는지 확인하세요.")
    sys.exit(1)

# Flask 앱 초기화
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB 제한

# CORS 설정
CORS(app, origins=["*"])  # 프로덕션에서는 특정 도메인으로 제한

# Rate Limiting 설정
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour", "5 per minute"]
)

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 전역 변수
TEMP_DIR = Path(tempfile.gettempdir()) / "html_designer"
TEMP_DIR.mkdir(exist_ok=True)

# PDF 파일 저장 및 캐시
PDF_CACHE = {}  # {hash: {"path": str, "created": datetime}}
PDF_CACHE_DURATION = timedelta(hours=24)

# 허용되는 파일 형식
ALLOWED_EXTENSIONS = {
    '.pdf', '.docx', '.doc', '.xlsx', '.xls', '.pptx', '.ppt',
    '.txt', '.md', '.csv', '.json', '.xml', '.html', '.htm',
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp',
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
            
            # HTML 생성
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
        """HTML을 PDF로 변환"""
        try:
            # PDF 파일 경로 생성
            pdf_filename = f"output_{uuid.uuid4().hex}.pdf"
            pdf_path = TEMP_DIR / pdf_filename
            
            # wkhtmltopdf 설정
            config = pdfkit.configuration(wkhtmltopdf=self.wkhtmltopdf_path)
            
            # HTML을 PDF로 변환
            pdfkit.from_string(
                html_content, 
                str(pdf_path), 
                options=self.pdf_options,
                configuration=config
            )
            
            logger.info(f"PDF 생성 완료: {pdf_path}")
            return str(pdf_path)
            
        except Exception as e:
            logger.error(f"PDF 변환 실패: {e}")
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

@app.errorhandler(413)
def too_large(e):
    """파일 크기 초과 에러 처리"""
    return jsonify({
        'error': '파일 크기가 너무 큽니다. 최대 16MB까지 허용됩니다.',
        'code': 'FILE_TOO_LARGE'
    }), 413

@app.errorhandler(500)
def internal_error(e):
    """내부 서버 에러 처리"""
    logger.error(f"Internal server error: {e}")
    return jsonify({
        'error': '서버 내부 오류가 발생했습니다.',
        'code': 'INTERNAL_ERROR'
    }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """헬스 체크"""
    return jsonify({'ok': True, 'timestamp': datetime.now().isoformat()})

@app.route('/api/convert', methods=['POST'])
@limiter.limit("3 per minute")
def convert_files():
    """파일들을 HTML로 변환 후 PDF 생성"""
    try:
        # 프롬프트 가져오기
        prompt = request.form.get('prompt', '').strip()
        if not prompt:
            return jsonify({
                'error': '프롬프트를 입력해주세요.',
                'code': 'MISSING_PROMPT'
            }), 400
        
        # 파일들 가져오기
        files = request.files.getlist('files')
        if not files:
            return jsonify({
                'error': '최소 1개의 파일을 업로드해주세요.',
                'code': 'MISSING_FILES'
            }), 400
        
        # 파일 검증 및 데이터 수집
        uploaded_files = []
        total_size = 0
        
        for file in files:
            if file.filename == '':
                continue
                
            if not is_allowed_file(file.filename):
                return jsonify({
                    'error': f'허용되지 않는 파일 형식입니다: {file.filename}',
                    'code': 'INVALID_FILE_TYPE'
                }), 400
            
            file_content = file.read()
            file_size = len(file_content)
            total_size += file_size
            
            if total_size > 16 * 1024 * 1024:  # 16MB
                return jsonify({
                    'error': '전체 파일 크기가 16MB를 초과합니다.',
                    'code': 'FILES_TOO_LARGE'
                }), 400
            
            uploaded_files.append({
                'filename': file.filename,
                'content': file_content,
                'size': file_size
            })
        
        if not uploaded_files:
            return jsonify({
                'error': '유효한 파일이 없습니다.',
                'code': 'NO_VALID_FILES'
            }), 400
        
        # 캐시 체크
        files_content = [f['content'].decode('utf-8', errors='ignore') for f in uploaded_files]
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
        
        # HTML 생성
        web_designer = get_designer()
        result = web_designer.generate_html_from_files(prompt, uploaded_files)
        
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
    """PDF 파일 다운로드/스트리밍"""
    try:
        if file_id not in PDF_CACHE:
            abort(404)
        
        pdf_path = PDF_CACHE[file_id]['path']
        if not os.path.exists(pdf_path):
            del PDF_CACHE[file_id]
            abort(404)
        
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=f'html_material_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf',
            mimetype='application/pdf'
        )
        
    except Exception as e:
        logger.error(f"PDF 파일 전송 실패: {e}")
        abort(500)

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
