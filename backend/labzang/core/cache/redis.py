"""BullMQ/Redis 연동 - 스텁. 실제 구현 시 교체."""
import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)


def add_bullmq_job(
    queue_name: str,
    job_name: str,
    payload: Optional[dict] = None,
    **kwargs: Any,
) -> Optional[str]:
    """BullMQ 작업 추가 스텁. Redis 연동 시 구현."""
    logger.warning("add_bullmq_job 스텁 호출됨: queue=%s job=%s", queue_name, job_name)
    return None


def get_bullmq_job_status(job_id: str) -> Optional[dict]:
    """BullMQ 작업 상태 조회 스텁. Redis 연동 시 구현."""
    logger.warning("get_bullmq_job_status 스텁 호출됨: job_id=%s", job_id)
    return None
