#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
파일 전처리기 - MarkItDown을 사용한 다양한 파일 형식을 Markdown으로 변환

markitdown 패키지를 사용하여 다음 파일들을 처리합니다:
- PDF, Word, Excel, PowerPoint
- 이미지 (OCR), 오디오 (전사), 비디오
- HTML, CSV, JSON, XML
- ZIP 파일, EPub
- YouTube URL 등
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
import shutil

try:
    from markitdown import MarkItDown
    _MARKITDOWN_IMPORT_ERROR = None
except ImportError as e:
    MarkItDown = None  # type: ignore[assignment]
    _MARKITDOWN_IMPORT_ERROR = e


class MarkItDownUnavailableError(RuntimeError):
    """markitdown 패키지가 준비되지 않은 경우 발생하는 예외"""

    def __init__(self, original_error: Optional[BaseException] = None):
        message = (
            "markitdown 패키지가 설치되어 있지 않아 파일 전처리를 진행할 수 없습니다. "
            "pip install markitdown[all] 명령으로 설치하거나, 프로젝트 번들 버전을 설치해주세요."
        )
        super().__init__(message)
        self.original_error = original_error


class FilePreprocessor:
    """파일 전처리기 - 다양한 형식을 Markdown으로 변환"""
    
    def __init__(self, input_dir: str = "worktable/input", output_dir: str = "worktable/output"):
        """
        전처리기 초기화

        Args:
            input_dir: 입력 파일 디렉토리
            output_dir: 출력 디렉토리
        """
        if MarkItDown is None:
            raise MarkItDownUnavailableError(_MARKITDOWN_IMPORT_ERROR)

        # 스크립트 위치 기준으로 경로 해결
        script_dir = Path(__file__).parent
        
        # 입력 디렉토리 경로 해결
        if Path(input_dir).is_absolute():
            self.input_dir = Path(input_dir)
        else:
            # 상대 경로인 경우 여러 후보 경로 시도
            candidate_paths = [
                Path.cwd() / input_dir,                    # 현재 작업 디렉토리 기준
                script_dir / input_dir,                    # 스크립트와 같은 디렉토리  
                Path.cwd() / "src" / input_dir,            # 프로젝트 루트에서 src/worktable/input
                script_dir / input_dir,                    # src/worktable/input
                script_dir.parent / "src" / input_dir,     # 상위 디렉토리의 src/worktable/input
            ]
            
            # 존재하는 첫 번째 경로 사용
            for candidate in candidate_paths:
                if candidate.exists():
                    self.input_dir = candidate
                    print(f"📁 입력 디렉토리 발견: {self.input_dir}")
                    break
            else:
                # 아무것도 없으면 기본값 사용하고 생성
                self.input_dir = script_dir / input_dir
                print(f"📂 입력 디렉토리 생성: {self.input_dir}")
                self.input_dir.mkdir(parents=True, exist_ok=True)
        
        # 출력 디렉토리 경로 해결  
        if Path(output_dir).is_absolute():
            self.output_dir = Path(output_dir)
        else:
            # 입력 디렉토리와 같은 부모 디렉토리 사용
            self.output_dir = self.input_dir.parent / output_dir
        
        print(f"📤 출력 디렉토리: {self.output_dir}")
        
        self.markitdown = MarkItDown()
        
        # 로깅 설정
        self._setup_logging()
        
        # 디렉토리 생성
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 지원하는 파일 확장자
        self.supported_extensions = {
            # 문서
            '.pdf', '.docx', '.doc', '.xlsx', '.xls', '.pptx', '.ppt',
            # 텍스트
            '.txt', '.md', '.csv', '.json', '.xml', '.html', '.htm',
            # 이미지
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp',
            # 오디오
            '.mp3', '.wav', '.m4a', '.flac', '.ogg',
            # 비디오
            '.mp4', '.avi', '.mkv', '.mov', '.wmv',
            # 압축
            '.zip', '.epub',
            # 노트북
            '.ipynb',
            # 이메일
            '.msg'
        }
    
    def _setup_logging(self):
        """로깅 설정"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('file_preprocessor.log', encoding='utf-8')
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def scan_input_directory(self) -> List[Path]:
        """입력 디렉토리에서 지원하는 파일들 스캔"""
        if not self.input_dir.exists():
            self.logger.warning(f"입력 디렉토리가 존재하지 않습니다: {self.input_dir}")
            return []
        
        files = []
        for file_path in self.input_dir.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in self.supported_extensions:
                files.append(file_path)
        
        self.logger.info(f"📁 {len(files)}개의 지원 파일 발견")
        return files
    
    def convert_file_to_markdown(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """
        단일 파일을 Markdown으로 변환
        
        Args:
            file_path: 변환할 파일 경로
            
        Returns:
            변환 결과 정보 딕셔너리
        """
        try:
            self.logger.info(f"🔄 변환 시작: {file_path.name}")
            
            # markitdown으로 변환
            result = self.markitdown.convert(str(file_path))
            
            if not result or not result.text_content:
                self.logger.warning(f"⚠️ 변환 결과가 비어있음: {file_path.name}")
                return None
            
            # 출력 파일명 생성
            output_filename = file_path.stem + '.md'
            output_path = self.output_dir / output_filename
            
            # 중복 파일명 처리
            counter = 1
            original_output_path = output_path
            while output_path.exists():
                output_path = original_output_path.parent / f"{original_output_path.stem}_{counter}.md"
                counter += 1
            
            # Markdown 파일 저장
            with open(output_path, 'w', encoding='utf-8') as f:
                # 메타데이터 추가
                metadata = f"""---
original_file: {file_path.name}
original_path: {file_path}
converted_at: {datetime.now().isoformat()}
file_size: {file_path.stat().st_size}
file_type: {file_path.suffix}
---

# {file_path.stem}

"""
                f.write(metadata)
                f.write(result.text_content)
            
            # 변환 결과 정보
            convert_info = {
                'original_file': str(file_path),
                'output_file': str(output_path),
                'file_size': file_path.stat().st_size,
                'markdown_size': len(result.text_content),
                'success': True,
                'timestamp': datetime.now().isoformat()
            }
            
            self.logger.info(f"✅ 변환 완료: {file_path.name} → {output_path.name}")
            return convert_info
            
        except Exception as e:
            self.logger.error(f"❌ 변환 실패 {file_path.name}: {e}")
            return {
                'original_file': str(file_path),
                'error': str(e),
                'success': False,
                'timestamp': datetime.now().isoformat()
            }
    
    def convert_url_to_markdown(self, url: str) -> Optional[Dict[str, Any]]:
        """
        URL을 Markdown으로 변환 (YouTube, 웹페이지 등)
        
        Args:
            url: 변환할 URL
            
        Returns:
            변환 결과 정보 딕셔너리
        """
        try:
            self.logger.info(f"🌐 URL 변환 시작: {url}")
            
            # markitdown으로 URL 변환
            result = self.markitdown.convert(url)
            
            if not result or not result.text_content:
                self.logger.warning(f"⚠️ URL 변환 결과가 비어있음: {url}")
                return None
            
            # 파일명 생성 (URL에서 안전한 파일명 만들기)
            safe_filename = url.replace('://', '_').replace('/', '_').replace('?', '_').replace('&', '_')
            safe_filename = ''.join(c for c in safe_filename if c.isalnum() or c in '_-')[:50]
            output_filename = f"url_{safe_filename}.md"
            output_path = self.output_dir / output_filename
            
            # Markdown 파일 저장
            with open(output_path, 'w', encoding='utf-8') as f:
                metadata = f"""---
source_url: {url}
converted_at: {datetime.now().isoformat()}
content_type: web_content
---

# {url}

"""
                f.write(metadata)
                f.write(result.text_content)
            
            convert_info = {
                'source_url': url,
                'output_file': str(output_path),
                'markdown_size': len(result.text_content),
                'success': True,
                'timestamp': datetime.now().isoformat()
            }
            
            self.logger.info(f"✅ URL 변환 완료: {url} → {output_path.name}")
            return convert_info
            
        except Exception as e:
            self.logger.error(f"❌ URL 변환 실패 {url}: {e}")
            return {
                'source_url': url,
                'error': str(e),
                'success': False,
                'timestamp': datetime.now().isoformat()
            }
    
    def process_all_files(self) -> Dict[str, Any]:
        """
        입력 디렉토리의 모든 파일을 처리
        
        Returns:
            전체 처리 결과 요약
        """
        print("📂 파일 전처리기 시작")
        print("=" * 50)
        
        # 파일 스캔
        files = self.scan_input_directory()
        
        if not files:
            print("⚠️ 처리할 파일이 없습니다.")
            return {
                'total_files': 0,
                'processed': 0,
                'failed': 0,
                'results': []
            }
        
        print(f"📋 처리할 파일: {len(files)}개")
        
        # 파일별 변환 진행
        results = []
        success_count = 0
        failed_count = 0
        
        for i, file_path in enumerate(files, 1):
            print(f"\n🔄 [{i}/{len(files)}] {file_path.name}")
            
            result = self.convert_file_to_markdown(file_path)
            if result:
                results.append(result)
                if result.get('success', False):
                    success_count += 1
                    print(f"✅ 성공: {result.get('output_file', '')}")
                else:
                    failed_count += 1
                    print(f"❌ 실패: {result.get('error', '')}")
        
        # 결과 요약 저장
        summary = {
            'timestamp': datetime.now().isoformat(),
            'input_directory': str(self.input_dir),
            'output_directory': str(self.output_dir),
            'total_files': len(files),
            'processed': success_count,
            'failed': failed_count,
            'results': results
        }
        
        summary_path = self.output_dir / 'conversion_summary.json'
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        # 최종 결과 출력
        print("\n" + "=" * 50)
        print("📊 처리 완료 요약")
        print("=" * 50)
        print(f"📁 총 파일: {len(files)}개")
        print(f"✅ 성공: {success_count}개")
        print(f"❌ 실패: {failed_count}개")
        print(f"📂 출력 디렉토리: {self.output_dir}")
        print(f"📄 요약 파일: {summary_path}")
        
        return summary
    
    def get_file_info(self, file_path: Path) -> Dict[str, Any]:
        """파일 정보 조회"""
        try:
            stat = file_path.stat()
            return {
                'name': file_path.name,
                'path': str(file_path),
                'size': stat.st_size,
                'size_mb': round(stat.st_size / (1024 * 1024), 2),
                'extension': file_path.suffix,
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'supported': file_path.suffix.lower() in self.supported_extensions
            }
        except Exception as e:
            return {'error': str(e)}
    
    def list_supported_formats(self):
        """지원하는 파일 형식 목록 출력"""
        print("📋 지원하는 파일 형식:")
        print("=" * 30)
        
        format_groups = {
            '📄 문서': ['.pdf', '.docx', '.doc', '.xlsx', '.xls', '.pptx', '.ppt'],
            '📝 텍스트': ['.txt', '.md', '.csv', '.json', '.xml', '.html', '.htm'],
            '🖼️ 이미지': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'],
            '🎵 오디오': ['.mp3', '.wav', '.m4a', '.flac', '.ogg'],
            '🎬 비디오': ['.mp4', '.avi', '.mkv', '.mov', '.wmv'],
            '📦 기타': ['.zip', '.epub', '.ipynb', '.msg']
        }
        
        for category, extensions in format_groups.items():
            print(f"\n{category}:")
            for ext in extensions:
                print(f"  • {ext}")


def main():
    """메인 실행 함수"""
    import argparse
    
    parser = argparse.ArgumentParser(description="파일 전처리기 - MarkItDown 기반 Markdown 변환")
    parser.add_argument("-i", "--input", default="input", help="입력 디렉토리 (기본: input)")
    parser.add_argument("-o", "--output", default="output", help="출력 디렉토리 (기본: output)")
    parser.add_argument("--url", help="변환할 URL (YouTube, 웹페이지 등)")
    parser.add_argument("--list-formats", action="store_true", help="지원하는 파일 형식 목록 표시")
    parser.add_argument("--file", help="특정 파일만 변환")
    
    args = parser.parse_args()
    
    try:
        preprocessor = FilePreprocessor(args.input, args.output)
    except MarkItDownUnavailableError as exc:
        print(f"❌ {exc}")
        if exc.original_error:
            print(f"원인: {exc.original_error}")
        return
    
    if args.list_formats:
        preprocessor.list_supported_formats()
        return
    
    if args.url:
        # URL 변환
        result = preprocessor.convert_url_to_markdown(args.url)
        if result and result.get('success'):
            print(f"✅ URL 변환 완료: {result['output_file']}")
        else:
            print(f"❌ URL 변환 실패: {result.get('error') if result else '알 수 없는 오류'}")
        return
    
    if args.file:
        # 특정 파일 변환
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"❌ 파일을 찾을 수 없습니다: {file_path}")
            return
        
        result = preprocessor.convert_file_to_markdown(file_path)
        if result and result.get('success'):
            print(f"✅ 파일 변환 완료: {result['output_file']}")
        else:
            print(f"❌ 파일 변환 실패: {result.get('error') if result else '알 수 없는 오류'}")
        return
    
    # 전체 디렉토리 처리
    preprocessor.process_all_files()


if __name__ == "__main__":
    main()
