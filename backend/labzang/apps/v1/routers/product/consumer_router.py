"""?åÎπÑ??Consumer) API ?ºÏö∞??"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from labzang.apps.product.models.transfers.consumer_model import (
    ConsumerModel,
    ConsumerCreateModel,
    ConsumerUpdateModel,
)
from labzang.apps.product.hub.orchestrators.consumer_flow import ConsumerFlow

router = APIRouter()


class ConsumerRequest(BaseModel):
    """?åÎπÑ???îÏ≤≠ Î™®Îç∏."""
    action: str  # "create", "update", "get", "list", "delete"
    data: Optional[dict] = None
    consumer_id: Optional[int] = None
    use_policy: bool = False  # True: ?ïÏ±Ö Í∏∞Î∞ò, False: Í∑úÏπô Í∏∞Î∞ò


@router.post("/", response_model=dict)
async def handle_consumer_request(request: ConsumerRequest):
    """?åÎπÑ???îÏ≤≠ Ï≤òÎ¶¨ ?îÎìú?¨Ïù∏??

    Í∑úÏπô Í∏∞Î∞ò ?êÎäî ?ïÏ±Ö Í∏∞Î∞ò?ºÎ°ú ?îÏ≤≠??Ï≤òÎ¶¨?©Îãà??
    """
    try:
        flow = ConsumerFlow()
        result = await flow.process_request(
            action=request.action,
            data=request.data or {},
            consumer_id=request.consumer_id,
            use_policy=request.use_policy
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create", response_model=ConsumerModel)
async def create_consumer(consumer: ConsumerCreateModel, use_policy: bool = False):
    """?åÎπÑ???ùÏÑ±."""
    try:
        flow = ConsumerFlow()
        result = await flow.process_request(
            action="create",
            data=consumer.model_dump(),
            use_policy=use_policy
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{consumer_id}", response_model=ConsumerModel)
async def get_consumer(consumer_id: int, use_policy: bool = False):
    """?åÎπÑ??Ï°∞Ìöå."""
    try:
        flow = ConsumerFlow()
        result = await flow.process_request(
            action="get",
            consumer_id=consumer_id,
            use_policy=use_policy
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{consumer_id}", response_model=ConsumerModel)
async def update_consumer(
    consumer_id: int,
    consumer: ConsumerUpdateModel,
    use_policy: bool = False
):
    """?åÎπÑ???òÏ†ï."""
    try:
        flow = ConsumerFlow()
        result = await flow.process_request(
            action="update",
            data=consumer.model_dump(exclude_unset=True),
            consumer_id=consumer_id,
            use_policy=use_policy
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[ConsumerModel])
async def list_consumers(use_policy: bool = False, limit: int = 100, offset: int = 0):
    """?åÎπÑ??Î™©Î°ù Ï°∞Ìöå."""
    try:
        flow = ConsumerFlow()
        result = await flow.process_request(
            action="list",
            data={"limit": limit, "offset": offset},
            use_policy=use_policy
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{consumer_id}", response_model=dict)
async def delete_consumer(consumer_id: int, use_policy: bool = False):
    """?åÎπÑ????†ú."""
    try:
        flow = ConsumerFlow()
        result = await flow.process_request(
            action="delete",
            consumer_id=consumer_id,
            use_policy=use_policy
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

