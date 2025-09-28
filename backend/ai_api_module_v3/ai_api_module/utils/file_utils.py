# ai_api_module/utils/file_utils.py
"""
File handling utilities
"""
import mimetypes
from pathlib import Path
from typing import Union, Tuple, Optional


def load_file(file_path: Union[str, Path]) -> bytes:
    """Load file as bytes"""
    with open(file_path, 'rb') as f:
        return f.read()


def get_file_type(file_path: Union[str, Path]) -> str:
    """Get file MIME type"""
    mime_type, _ = mimetypes.guess_type(str(file_path))
    return mime_type or "application/octet-stream"


def is_image_file(file_path: Union[str, Path]) -> bool:
    """Check if file is an image"""
    mime_type = get_file_type(file_path)
    return mime_type.startswith('image/')


def is_audio_file(file_path: Union[str, Path]) -> bool:
    """Check if file is audio"""
    mime_type = get_file_type(file_path)
    return mime_type.startswith('audio/')


def is_video_file(file_path: Union[str, Path]) -> bool:
    """Check if file is video"""
    mime_type = get_file_type(file_path)
    return mime_type.startswith('video/')


def is_document_file(file_path: Union[str, Path]) -> bool:
    """Check if file is a document"""
    mime_type = get_file_type(file_path)
    return mime_type in [
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'text/plain',
        'text/markdown'
    ]


def get_file_size(file_path: Union[str, Path]) -> int:
    """Get file size in bytes"""
    return Path(file_path).stat().st_size


def ensure_directory(directory: Union[str, Path]) -> Path:
    """Ensure directory exists"""
    dir_path = Path(directory)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path
