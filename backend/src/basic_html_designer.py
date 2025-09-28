#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 기반 A4 규격 HTML 교재 생성기

config.json 설정을 읽어서 AI API 모듈을 활용해
가이드라인과 기본 구조를 참고하여 HTML 교재를 자동 생성합니다.
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime

# AI API 모듈 부트스트랩
sys.path.insert(0, str(Path(__file__).parent.parent / "ai_api_module_v3"))
try:
    from ai_api_module import AI
except ImportError:
    print("❌ AI API 모듈을 찾을 수 없습니다.")
    print("다음 경로를 확인해주세요: ai_api_module_v3/")
    sys.exit(1)


class HTMLDesigner:
    """AI 기반 HTML 교재 디자이너"""
    
    def __init__(self, config_path: str = None):
        """
        HTML 디자이너 초기화
        
        Args:
            config_path: config.json 파일 경로. None이면 자동 탐색
        """
        if config_path is None:
            self.config_path = self._find_config_file()
        else:
            self.config_path = Path(config_path)
        
        self.config = self._load_config()
        self.ai = None
        self._setup_logging()
        self._initialize_ai()
    
    def _find_config_file(self) -> Path:
        """config.json 파일을 자동으로 찾기"""
        # 현재 스크립트 위치
        current_script = Path(__file__).resolve()
        
        # 탐색할 경로들 (우선순위 순서)
        search_paths = [
            # 1. 현재 작업 디렉토리
            Path.cwd() / "config.json",
            Path.cwd() / "src/config.json",
            
            # 2. 스크립트와 같은 디렉토리
            current_script.parent / "config.json", 
            
            # 3. 스크립트 상위 디렉토리들
            current_script.parent.parent / "config.json",
            current_script.parent.parent / "src/config.json",
            
            # 4. 프로젝트 루트 추정 (ai_api_module_v3가 있는 곳)
            current_script.parent.parent / "src/config.json",
        ]
        
        # 첫 번째로 발견되는 config.json 반환
        for config_path in search_paths:
            if config_path.exists():
                print(f"✅ config.json 발견: {config_path}")
                return config_path
        
        # 모든 경로를 시도해봤지만 찾지 못함
        print("❌ config.json을 찾을 수 없습니다. 다음 경로들을 확인했습니다:")
        for path in search_paths:
            print(f"  - {path} ({'존재함' if path.exists() else '없음'})")
        
        # 기본값으로 현재 디렉토리의 config.json 반환
        default_path = Path.cwd() / "src/config.json"
        print(f"🔧 기본 경로 사용: {default_path}")
        return default_path
        
    def _load_config(self) -> Dict[str, Any]:
        """config.json 파일 로드"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print(f"✅ 설정 파일 로드 완료: {self.config_path}")
            return config
        except FileNotFoundError:
            print(f"❌ 설정 파일을 찾을 수 없습니다: {self.config_path}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ 설정 파일 형식 오류: {e}")
            sys.exit(1)
    
    def _setup_logging(self):
        """로깅 설정"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('html_designer.log', encoding='utf-8')
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def _initialize_ai(self):
        """AI 모듈 초기화"""
        try:
            ai_settings = self.config.get("ai_settings", {})
            
            self.ai = AI(
                model=ai_settings.get("model", "smart"),
                temperature=ai_settings.get("temperature", 0.7)
            )
            
            self.logger.info("✅ AI 모듈 초기화 완료")
            self.logger.info(f"🤖 모델: {ai_settings.get('model', 'smart')}")
            self.logger.info(f"🌡️ Temperature: {ai_settings.get('temperature', 0.7)}")
            
        except Exception as e:
            print(f"❌ AI 모듈 초기화 실패: {e}")
            print("API 키가 설정되어 있는지 확인해주세요:")
            print("export OPENAI_API_KEY='your-key'")
            print("export ANTHROPIC_API_KEY='your-key'") 
            print("export GOOGLE_API_KEY='your-key'")
            sys.exit(1)
    
    def _load_reference_files(self) -> Dict[str, str]:
        """참조 파일들 로드"""
        references = {}
        ai_settings = self.config.get("ai_settings", {})
        reference_files = ai_settings.get("reference", [])
        
        # config 파일 위치를 기준으로 상대 경로 해결
        config_dir = self.config_path.parent if self.config_path.is_absolute() else Path.cwd()
        
        for ref_path in reference_files:
            try:
                # 상대 경로를 config 파일 위치 기준으로 해결
                if not Path(ref_path).is_absolute():
                    file_path = config_dir / ref_path
                else:
                    file_path = Path(ref_path)
                
                # 파일 절대 경로로 변환
                file_path = file_path.resolve()
                
                self.logger.info(f"🔍 참조 파일 경로 확인: {file_path}")
                
                if file_path.exists():
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    references[file_path.name] = content
                    self.logger.info(f"✅ 참조 파일 로드 성공: {ref_path}")
                    self.logger.info(f"📄 파일 크기: {len(content):,} 문자")
                else:
                    self.logger.warning(f"⚠️ 참조 파일 없음: {file_path}")
                    # 대안 경로들도 시도
                    alternative_paths = [
                        Path.cwd() / ref_path,
                        Path(__file__).parent / ref_path,
                        Path(__file__).parent.parent / ref_path
                    ]
                    
                    for alt_path in alternative_paths:
                        if alt_path.exists():
                            self.logger.info(f"🔄 대안 경로에서 발견: {alt_path}")
                            with open(alt_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                            references[alt_path.name] = content
                            self.logger.info(f"✅ 대안 경로에서 로드 성공: {alt_path}")
                            break
                            
            except Exception as e:
                self.logger.error(f"❌ 참조 파일 로드 실패 {ref_path}: {e}")
        
        self.logger.info(f"📚 총 {len(references)}개 참조 파일 로드됨")
        for filename in references.keys():
            self.logger.info(f"  - {filename}")
        
        return references
    
    def _load_library_files(self) -> Dict[str, str]:
        """library 폴더의 파일들 로드 (fonts.md 등)"""
        library_files = {}
        
        # config 파일 위치를 기준으로 상대 경로 해결
        config_dir = self.config_path.parent if self.config_path.is_absolute() else Path.cwd()
        
        # library 폴더 경로 찾기
        library_candidates = [
            config_dir / "library",
            Path(__file__).parent / "library",
            Path.cwd() / "src/library",
            config_dir.parent / "src/library"
        ]
        
        library_dir = None
        for candidate in library_candidates:
            if candidate.exists():
                library_dir = candidate
                break
        
        if not library_dir:
            self.logger.info("📂 library 디렉토리를 찾을 수 없어 라이브러리 파일 로드를 건너뜁니다")
            return library_files
        
        self.logger.info(f"📂 library 디렉토리 발견: {library_dir}")
        
        # .md 파일들 찾기 (특히 fonts.md)
        library_files_list = list(library_dir.glob("*.md"))
        
        for lib_file in library_files_list:
            try:
                with open(lib_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                library_files[lib_file.name] = content
                self.logger.info(f"📖 라이브러리 파일 로드: {lib_file.name} ({len(content):,} 문자)")
                
            except Exception as e:
                self.logger.warning(f"⚠️ 라이브러리 파일 로드 실패 {lib_file.name}: {e}")
        
        self.logger.info(f"📚 총 {len(library_files)}개 라이브러리 파일 로드됨")
        return library_files
    
    def _find_input_files(self) -> List[Path]:
        """input 폴더의 파일들 직접 찾기 (AI가 직접 처리할 수 있는 파일들)"""
        input_files = []
        
        # config에서 파일 처리 설정 가져오기
        file_config = self.config.get("file_processing", {})
        
        # 파일 직접 첨부가 비활성화된 경우 빈 리스트 반환
        if not file_config.get("enable_direct_file_attachment", True):
            self.logger.info("🚫 파일 직접 첨부 기능이 비활성화되어 있습니다")
            return input_files
        
        # 입력 디렉토리 경로 결정
        input_dir_name = file_config.get("input_directory", "worktable/input")
        
        # 디렉토리 경로 찾기
        script_dir = Path(__file__).parent
        config_dir = self.config_path.parent if self.config_path.is_absolute() else Path.cwd()
        
        input_candidates = [
            config_dir / input_dir_name,              # config 파일 기준
            script_dir / input_dir_name,              # 스크립트 파일 기준
            Path.cwd() / input_dir_name,              # 현재 작업 디렉토리 기준
            script_dir / "worktable/input",           # 기본 경로들
            Path.cwd() / "src/worktable/input",
            script_dir.parent / "src/worktable/input"
        ]
        
        input_dir = None
        for candidate in input_candidates:
            if candidate.exists():
                input_dir = candidate
                break
        
        if not input_dir:
            self.logger.info("📂 input 디렉토리를 찾을 수 없어 파일 로드를 건너뜁니다")
            return input_files
        
        self.logger.info(f"📂 input 디렉토리 발견: {input_dir}")
        
        # 지원하는 파일 확장자들 (config에서 가져오기)
        supported_extensions = set(file_config.get("supported_file_types", [
            ".pdf", ".docx", ".doc", ".xlsx", ".xls", ".pptx", ".ppt",
            ".txt", ".md", ".csv", ".json", ".xml", ".html", ".htm",
            ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp",
            ".epub", ".zip"
        ]))
        
        # 파일 크기 및 개수 제한
        max_file_size_mb = file_config.get("max_file_size_mb", 10)
        max_files = file_config.get("max_files_per_request", 20)
        
        # 파일들 찾기 (재귀적으로 검색)
        for file_path in input_dir.rglob('*'):
            if len(input_files) >= max_files:
                self.logger.warning(f"⚠️ 최대 파일 개수({max_files}개)에 도달하여 추가 파일을 건너뜁니다")
                break
                
            if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                # 파일 크기 체크
                file_size_mb = file_path.stat().st_size / (1024 * 1024)
                if file_size_mb > max_file_size_mb:
                    self.logger.warning(f"⚠️ 파일 크기가 너무 큽니다({file_size_mb:.1f}MB): {file_path.name}")
                    continue
                
                input_files.append(file_path)
                self.logger.info(f"📄 발견된 파일: {file_path.name} ({file_path.stat().st_size:,} 바이트)")
        
        self.logger.info(f"📚 총 {len(input_files)}개 파일 발견됨")
        return input_files
    
    def _build_prompt(self, user_request: str, references: Dict[str, str], library_files: Dict[str, str]) -> str:
        """AI 프롬프트 구성 (파일 직접 전달 방식)"""
        prompts = self.config.get("prompts", {})
        
        # 시스템 프롬프트
        system_prompt = prompts.get("system_prompt", "")
        
        # 프리셋 프롬프트  
        preset_prompt = prompts.get("preset_prompt", "")
        
        # 참조 파일 내용 추가 (래퍼로 감싸기)
        reference_content = ""
        if references:
            reference_content = "\n\n" + "="*60 + "\n"
            reference_content += "📚 참조 자료 (REFERENCE MATERIALS)\n"
            reference_content += "="*60 + "\n"
            
            for filename, content in references.items():
                # 파일별로 명확한 래퍼 추가
                reference_content += f"\n\n📄 [{filename}] 시작\n"
                reference_content += "-" * 40 + "\n"
                reference_content += content.strip()
                reference_content += f"\n{'-' * 40}\n"
                reference_content += f"📄 [{filename}] 끝\n"
        
        # library 폴더의 파일들 추가 (fonts.md 등)
        library_content = ""
        if library_files:
            library_content = "\n\n" + "="*60 + "\n"
            library_content += "🎨 디자인 라이브러리 (DESIGN LIBRARY)\n"
            library_content += "="*60 + "\n"
            library_content += "💡 폰트와 디자인은 반드시 이 가이드라인을 따라주세요.\n\n"
            
            for filename, content in library_files.items():
                library_content += f"\n\n🎨 [{filename}] 시작\n"
                library_content += "-" * 40 + "\n"
                library_content += content.strip()
                library_content += f"\n{'-' * 40}\n"
                library_content += f"🎨 [{filename}] 끝\n"
        
        # 파일 직접 전달 안내 메시지 추가
        file_instruction = "\n\n" + "="*60 + "\n"
        file_instruction += "📁 첨부된 파일들 (ATTACHED FILES)\n"
        file_instruction += "="*60 + "\n"
        file_instruction += "💡 input 폴더의 파일들이 직접 첨부되었습니다.\n"
        file_instruction += "💡 첨부된 파일의 내용을 적극 활용하여 HTML 교재를 제작하세요.\n"
        file_instruction += "💡 문서, 이미지, 기타 파일들의 정보를 활용해주세요.\n"
        
        # 최종 프롬프트 조합
        full_prompt = f"""
{system_prompt}

{preset_prompt}

사용자 요청: {user_request}

{reference_content}

{library_content}

{file_instruction}

{"="*60}
🎯 중요한 규칙 (IMPORTANT RULES)
{"="*60}
1. 반드시 HTML 코드만 출력하고 ```html 코드블록으로 감싸주세요
2. A4 규격(210mm × 297mm)을 준수해주세요  
3. 주어진 basic_structure.html의 스타일과 구조를 기반으로 해주세요
4. 가이드라인을 엄격히 준수해주세요
5. 모던하고 세련된 디자인으로 만들어주세요
6. 프린트 최적화를 고려해주세요
7. 참조 자료의 CSS 스타일과 HTML 구조를 정확히 따라주세요
8. 💡 첨부된 파일들의 내용을 적극 활용하여 관련 내용으로 HTML 교재를 제작하세요
9. 🎨 폰트와 디자인은 반드시 디자인 라이브러리의 2025년 트렌드를 참고하세요

🔥 출력 형식:
```html
<!DOCTYPE html>
<html lang="ko">
<!-- 여기에 HTML 코드 작성 -->
</html>
```
        """.strip()
        
        return full_prompt
    
    def _get_max_tokens_for_model(self, model: str) -> int:
        """모델별 최대 토큰 수 반환"""
        model_token_limits = {
            # OpenAI 모델들
            "gpt-5": 128000,

            
            # Anthropic 모델들
            "claude-opus-4": 32000,
            "claude-sonnet-4": 64000,

            
            # Google 모델들
            "gemini-2.5-pro": 65536,

            
            # xAI 모델들
            "grok-4": 32768,
            "grok-3": 16384,
            "grok": 32768,
            
        }
        
        # 모델명에서 실제 토큰 한도 찾기
        for model_name, token_limit in model_token_limits.items():
            if model_name in model.lower():
                return token_limit
        
        # 기본값 (안전한 크기)
        return 16384

    def generate_html(self, user_request: Optional[str] = None) -> tuple[str, Dict[str, Any]]:
        """
        HTML 교재 생성 (파일 직접 전달 방식)
        
        Args:
            user_request: 사용자 요청. None이면 config에서 가져옴
            
        Returns:
            tuple: (생성된 HTML 코드, 응답 메타데이터)
        """
        # 사용자 요청 결정
        if user_request is None:
            user_request = self.config.get("prompts", {}).get("user_prompt", "")
            
        if not user_request.strip():
            raise ValueError("사용자 요청이 비어있습니다.")
        
        self.logger.info(f"🎨 HTML 생성 시작: {user_request[:50]}...")
        
        # 참조 파일 로드
        references = self._load_reference_files()
        
        # library 파일 로드
        library_files = self._load_library_files()
        
        # input 폴더의 파일들 찾기
        input_files = self._find_input_files()
        
        # 프롬프트 구성 (파일 직접 전달 방식)
        prompt = self._build_prompt(user_request, references, library_files)
        
        # 모델 및 최대 토큰 설정
        model = self.config.get("ai_settings", {}).get("model", "smart")
        max_tokens = self._get_max_tokens_for_model(model)
        
        self.logger.info(f"🤖 사용 모델: {model}")
        self.logger.info(f"🔢 최대 토큰: {max_tokens:,}")
        self.logger.info(f"📁 첨부할 파일 수: {len(input_files)}")
        
        try:
            # 파일 경로를 문자열 리스트로 변환
            file_paths = [str(file_path) for file_path in input_files] if input_files else None
            
            # AI로 HTML 생성 (파일 직접 첨부)
            response = self.ai.chat(
                prompt,
                model=model,
                temperature=self.config.get("ai_settings", {}).get("temperature", 1.0),
                max_tokens=max_tokens,
                files=file_paths  # 파일들을 직접 첨부
            )
            
            # AI 응답 출력 (디버깅 및 확인용)
            print("\n" + "="*60)
            print("🤖 AI 원본 응답:")
            print("="*60)
            print(response.text)
            print("="*60)
            
            # HTML 코드 추출
            html_content = self._extract_html_from_response(response.text)
            
            # 추출된 HTML 미리보기
            print(f"\n📄 추출된 HTML 미리보기 (처음 200자):")
            print(html_content[:200] + "..." if len(html_content) > 200 else html_content)
            
            # 메타데이터 수집
            metadata = {
                "model": response.model,
                "cost": response.cost,
                "tokens_used": getattr(response.usage, 'total_tokens', 0),
                "timestamp": datetime.now().isoformat(),
                "user_request": user_request,
                "attached_files": len(input_files),
                "file_list": [f.name for f in input_files] if input_files else [],
                "success": True,
                "raw_response": response.text[:500] + "..." if len(response.text) > 500 else response.text
            }
            
            self.logger.info(f"✅ HTML 생성 완료")
            self.logger.info(f"💰 비용: ${response.cost:.6f}")
            self.logger.info(f"🔢 토큰: {metadata['tokens_used']}")
            self.logger.info(f"📁 첨부된 파일: {metadata['attached_files']}개")
            
            return html_content, metadata
            
        except Exception as e:
            self.logger.error(f"❌ HTML 생성 실패: {e}")
            metadata = {
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "user_request": user_request,
                "attached_files": len(input_files),
                "success": False
            }
            raise Exception(f"HTML 생성 실패: {e}") from e
    
    def _extract_html_from_response(self, response_text: str) -> str:
        """AI 응답에서 HTML 코드 추출"""
        import re
        
        # 1. ```html 코드블록 패턴으로 찾기 (가장 정확한 방법)
        html_pattern = r'```html\s*\n(.*?)\n```'
        html_match = re.search(html_pattern, response_text, re.DOTALL | re.IGNORECASE)
        
        if html_match:
            html_content = html_match.group(1).strip()
            self.logger.info("✅ HTML 코드블록에서 성공적으로 추출")
            return html_content
        
        # 2. ```만 있는 코드블록 찾기
        general_pattern = r'```\s*\n(.*?)\n```'
        general_match = re.search(general_pattern, response_text, re.DOTALL)
        
        if general_match:
            content = general_match.group(1).strip()
            # HTML 태그가 있는지 확인
            if '<!DOCTYPE html>' in content or '<html' in content:
                self.logger.info("✅ 일반 코드블록에서 HTML 추출")
                return content
        
        # 3. 라인별로 찾기 (기존 방식 개선)
        lines = response_text.split('\n')
        html_lines = []
        in_html_block = False
        
        for line in lines:
            line_stripped = line.strip().lower()
            if line_stripped.startswith('```html') or line_stripped == '```html':
                in_html_block = True
                continue
            elif line_stripped == '```' and in_html_block:
                break
            elif in_html_block:
                html_lines.append(line)
        
        if html_lines:
            self.logger.info("✅ 라인별 파싱으로 HTML 추출")
            return '\n'.join(html_lines)
        
        # 4. HTML 태그가 직접 있는지 확인
        if '<!DOCTYPE html>' in response_text or '<html' in response_text:
            self.logger.warning("⚠️ 코드블록 없이 HTML 태그 발견, 전체 응답 사용")
            return response_text.strip()
        
        # 5. 실패 시 전체 응답 반환
        self.logger.warning("⚠️ HTML 코드블록을 찾을 수 없어 전체 응답을 반환합니다")
        return response_text
    
    def save_html(self, html_content: str, filename: Optional[str] = None) -> str:
        """
        HTML 파일 저장
        
        Args:
            html_content: HTML 내용
            filename: 파일명. None이면 자동 생성
            
        Returns:
            저장된 파일 경로 (상대 경로)
        """
        # 출력 디렉토리 설정 - 상대 경로로 처리
        output_dir_name = self.config.get("output", {}).get("output_directory", "worktable")
        
        # config 파일 위치를 기준으로 상대 경로 해결
        config_dir = self.config_path.parent if self.config_path.is_absolute() else Path.cwd()
        
        # 상대 경로 구성
        if Path(output_dir_name).is_absolute():
            # 절대 경로면 상대 경로로 변환
            try:
                output_dir = Path(output_dir_name).relative_to(Path.cwd())
            except ValueError:
                # 상대 경로 변환 실패 시 기본값 사용
                output_dir = Path("worktable")
        else:
            # config 파일 기준 상대 경로
            output_dir = config_dir / output_dir_name
            # 현재 작업 디렉토리 기준으로 상대 경로 만들기
            try:
                output_dir = output_dir.relative_to(Path.cwd())
            except ValueError:
                # 실패하면 그냥 output_dir_name 사용
                output_dir = Path(output_dir_name)
        
        self.logger.info(f"📁 출력 디렉토리: {output_dir}")
        
        # 디렉토리 생성
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 파일명 생성
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"html_material_{timestamp}.html"
        
        # 파일 저장
        output_path = output_dir / filename
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self.logger.info(f"💾 HTML 파일 저장 완료: {output_path}")
            return str(output_path)  # 상대 경로 반환
            
        except Exception as e:
            self.logger.error(f"❌ 파일 저장 실패: {e}")
            raise
    
    def generate_and_save(self, user_request: Optional[str] = None, filename: Optional[str] = None) -> Dict[str, Any]:
        """
        HTML 생성 및 저장 통합 기능
        
        Args:
            user_request: 사용자 요청
            filename: 저장할 파일명
            
        Returns:
            실행 결과 딕셔너리
        """
        try:
            # HTML 생성
            html_content, metadata = self.generate_html(user_request)
            
            # 파일 저장
            output_path = self.save_html(html_content, filename)
            
            # 결과 반환
            result = {
                **metadata,
                "output_path": output_path,
                "html_length": len(html_content)
            }
            
            return result
            
        except Exception as e:
            self.logger.error(f"❌ 전체 프로세스 실패: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }


def main():
    """메인 실행 함수"""
    print("🎨 AI 기반 HTML 교재 생성기")
    print("=" * 50)
    
    try:
        # HTML 디자이너 초기화
        designer = HTMLDesigner()
        
        # config에서 요청 가져오기 (자동 진행)
        config_user_prompt = designer.config.get("prompts", {}).get("user_prompt", "")
        
        if config_user_prompt.strip():
            print(f"📋 요청: {config_user_prompt}")
            user_request = None  # config에서 가져옴
        else:
            print("⚠️ config.json에 user_prompt가 설정되지 않았습니다.")
            print("기본 요청을 사용합니다.")
            user_request = "간단한 A4 규격 HTML 페이지를 만들어주세요."
        
        # HTML 생성 및 저장
        print("\n🤖 AI가 HTML을 생성 중입니다...")
        result = designer.generate_and_save(user_request)
        
        if result.get("success", False):
            print(f"\n✅ HTML 교재 생성 완료!")
            print(f"📁 파일 위치: {result['output_path']}")
            print(f"🤖 사용 모델: {result['model']}")
            print(f"💰 비용: ${result['cost']:.6f}")
            print(f"🔢 토큰 사용량: {result['tokens_used']}")
            print(f"📏 HTML 크기: {result['html_length']:,} 문자")
            
            # 자동으로 브라우저에서 열기
            print(f"\n🌐 브라우저에서 파일을 열고 있습니다...")
            try:
                import subprocess
                import platform
                
                # 운영체제별 브라우저 열기 명령
                if platform.system() == "Windows":
                    os.startfile(result["output_path"])
                elif platform.system() == "Darwin":  # macOS
                    subprocess.run(["open", result["output_path"]])
                else:  # Linux
                    subprocess.run(["xdg-open", result["output_path"]])
                    
                print("✅ 브라우저에서 파일을 열었습니다!")
                
            except Exception as e:
                print(f"⚠️ 브라우저 열기 실패: {e}")
                print(f"수동으로 파일을 열어주세요: {result['output_path']}")
        else:
            print(f"\n❌ 생성 실패: {result.get('error', '알 수 없는 오류')}")
            
    except KeyboardInterrupt:
        print("\n\n👋 사용자에 의해 중단되었습니다.")
    except Exception as e:
        print(f"\n❌ 실행 중 오류 발생: {e}")
        logging.exception("상세 오류:")


def cli_mode():
    """명령행 인터페이스 모드"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AI 기반 HTML 교재 생성기")
    parser.add_argument("request", nargs="?", help="HTML 생성 요청")
    parser.add_argument("-c", "--config", default=None, help="설정 파일 경로 (지정하지 않으면 자동 탐색)")
    parser.add_argument("-o", "--output", help="출력 파일명")
    parser.add_argument("--model", help="사용할 AI 모델")
    parser.add_argument("--temperature", type=float, help="Temperature 값")
    parser.add_argument("--no-browser", action="store_true", help="브라우저 자동 열기 비활성화")
    
    args = parser.parse_args()
    
    try:
        designer = HTMLDesigner(args.config)
        
        # 설정 오버라이드
        if args.model:
            designer.config["ai_settings"]["model"] = args.model
        if args.temperature is not None:
            designer.config["ai_settings"]["temperature"] = args.temperature
        
        # HTML 생성
        result = designer.generate_and_save(args.request, args.output)
        
        if result.get("success", False):
            print(f"✅ 완료: {result['output_path']}")
            
            # 브라우저 자동 열기 (옵션이 활성화된 경우)
            if not args.no_browser:
                try:
                    import subprocess
                    import platform
                    
                    if platform.system() == "Windows":
                        os.startfile(result["output_path"])
                    elif platform.system() == "Darwin":  # macOS
                        subprocess.run(["open", result["output_path"]])
                    else:  # Linux
                        subprocess.run(["xdg-open", result["output_path"]])
                        
                    print("🌐 브라우저에서 파일을 열었습니다!")
                    
                except Exception as e:
                    print(f"⚠️ 브라우저 열기 실패: {e}")
        else:
            print(f"❌ 실패: {result.get('error')}")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ 오류: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # 명령행 인자가 있으면 CLI 모드, 없으면 대화형 모드
    if len(sys.argv) > 1:
        cli_mode()
    else:
        main()
