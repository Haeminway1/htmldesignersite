# ai_api_module/utils/image_utils.py
"""
Image processing utilities
"""
import base64
import io
from pathlib import Path
from typing import Union, Tuple, Optional

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


def process_image(image_input: Union[str, Path, bytes]) -> Tuple[bytes, str]:
    """Process image and return bytes and format"""
    if isinstance(image_input, (str, Path)):
        image_path = Path(image_input)
        if image_path.exists():
            with open(image_path, 'rb') as f:
                image_data = f.read()
            format_ext = image_path.suffix.lower()[1:]
            return image_data, format_ext
        else:
            raise FileNotFoundError(f"Image file not found: {image_input}")
    elif isinstance(image_input, bytes):
        return image_input, "jpeg"  # Default format
    else:
        raise ValueError("Invalid image input type")


def encode_image_base64(image_data: bytes) -> str:
    """Encode image data as base64"""
    return base64.b64encode(image_data).decode('utf-8')


def decode_image_base64(base64_string: str) -> bytes:
    """Decode base64 image data"""
    return base64.b64decode(base64_string)


def resize_image(image_data: bytes, max_size: Tuple[int, int] = (1024, 1024)) -> bytes:
    """Resize image to maximum dimensions"""
    if not PIL_AVAILABLE:
        return image_data  # Return original if PIL not available
    
    image = Image.open(io.BytesIO(image_data))
    image.thumbnail(max_size, Image.Resampling.LANCZOS)
    
    output = io.BytesIO()
    image.save(output, format=image.format)
    return output.getvalue()


def get_image_info(image_data: bytes) -> dict:
    """Get image information"""
    if not PIL_AVAILABLE:
        return {"size": len(image_data)}
    
    image = Image.open(io.BytesIO(image_data))
    return {
        "format": image.format,
        "mode": image.mode,
        "size": image.size,
        "width": image.width,
        "height": image.height,
        "bytes": len(image_data)
    }
