"""EXAONE 판정 툴 - 스텁. 실제 구현 시 교체."""
import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

# 스텁: 빈 리스트 또는 실제 툴 목록으로 교체
exaone_tools: List[Any] = []


class _ExaoneQuickVerdictStub:
    """exaone_quick_verdict 스텁 (ainvoke 지원)."""
    async def ainvoke(self, inputs: Dict[str, Any]) -> str:
        logger.warning("exaone_quick_verdict 스텁 호출됨")
        return "uncertain"


exaone_quick_verdict = _ExaoneQuickVerdictStub()
