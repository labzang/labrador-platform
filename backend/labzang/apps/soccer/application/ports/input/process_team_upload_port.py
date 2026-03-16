"""팀 업로드 처리 입력 포트 (유스케이스 계약).

adapter/input(라우터)는 이 포트를 호출합니다.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List


class ProcessTeamUploadInputPort(ABC):
    """팀 업로드 처리 유스케이스 인터페이스."""

    @abstractmethod
    async def execute(self, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """팀 JSONL 항목을 처리합니다."""
        ...
