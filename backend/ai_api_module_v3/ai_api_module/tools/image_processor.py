"""
Image processing tool (basic)
"""
from typing import Tuple
from .base import tool
from ..utils.image_utils import get_image_info, process_image


@tool(name="image_info", description="Return basic image info (format, size, width, height)")
def image_info(path: str) -> dict:
    data, _ = process_image(path)
    return get_image_info(data)


