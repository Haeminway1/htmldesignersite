"""Bootstrap helpers to make ``ai_api_module`` importable from any location.

이 모듈은 소스 트리를 그대로 사용하는 경우(PIP 설치 전)에도
`import ai_api_module` 이 동작하도록 ``sys.path`` 를 정돈한다.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Iterable


def _candidate_roots() -> Iterable[Path]:
    here = Path(__file__).resolve()
    package_root = here.parent  # ai_api_module/
    yield package_root
    yield package_root.parent  # 프로젝트 루트


def ensure_path() -> None:
    """Ensure project paths are present in ``sys.path``.

    - 이미 설치된 wheel/site-packages 환경에서는 아무 영향이 없다.
    - 소스 트리에서 직접 실행할 때는 프로젝트 루트를 우선순위에 올려
      상대 위치에 상관없이 import 가 가능하도록 한다.
    - ``AI_API_MODULE_AUTO_PATH`` 환경변수가 ``'0'`` 로 설정되면 비활성화된다.
    """

    if os.getenv("AI_API_MODULE_AUTO_PATH", "1") in {"0", "false", "False"}:
        return

    for root in _candidate_roots():
        root_str = str(root)
        if root_str not in sys.path:
            sys.path.insert(0, root_str)


# 라이브러리 import 시 자동으로 보정한다.
ensure_path()


__all__ = ["ensure_path"]


