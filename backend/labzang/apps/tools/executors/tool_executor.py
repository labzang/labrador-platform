"""툴 실행기 - 스텁. 실제 구현 시 교체."""
import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class SimpleToolExecutor:
    """단순 툴 실행기 스텁."""

    def __init__(self, tools: List[Any]):
        self.tools = tools or []
        logger.warning("SimpleToolExecutor 스텁 사용 중 (tools=%d)", len(self.tools))

    async def run(self, tool_name: str, inputs: Dict[str, Any]) -> Any:
        raise NotImplementedError("SimpleToolExecutor.run 미구현")
