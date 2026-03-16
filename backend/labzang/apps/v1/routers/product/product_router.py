"""?í’ˆ(Product) API ?¼ìš°??"""

import logging
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
import json

from labzang.apps.product.models.transfers.product_model import (
    ProductModel,
    ProductCreateModel,
    ProductUpdateModel,
)
from labzang.apps.product.hub.orchestrators.product_flow import ProductFlow

router = APIRouter()
logger = logging.getLogger(__name__)


class ProductRequest(BaseModel):
    """?í’ˆ ?”ì²­ ëª¨ë¸."""
    action: str  # "create", "update", "get", "list", "delete", "recommend"
    data: Optional[dict] = None
    product_id: Optional[int] = None
    use_policy: bool = False  # True: ?•ì±… ê¸°ë°˜, False: ê·œì¹™ ê¸°ë°˜


@router.post("/", response_model=dict)
async def handle_product_request(request: ProductRequest):
    """?í’ˆ ?”ì²­ ì²˜ë¦¬ ?”ë“œ?¬ì¸??

    ê·œì¹™ ê¸°ë°˜ ?ëŠ” ?•ì±… ê¸°ë°˜?¼ë¡œ ?”ì²­??ì²˜ë¦¬?©ë‹ˆ??
    """
    try:
        flow = ProductFlow()
        result = await flow.process_request(
            action=request.action,
            data=request.data or {},
            product_id=request.product_id,
            use_policy=request.use_policy
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create", response_model=ProductModel)
async def create_product(product: ProductCreateModel, use_policy: bool = False):
    """?í’ˆ ?ì„±."""
    try:
        flow = ProductFlow()
        result = await flow.process_request(
            action="create",
            data=product.model_dump(),
            use_policy=use_policy
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{product_id}", response_model=ProductModel)
async def get_product(product_id: int, use_policy: bool = False):
    """?í’ˆ ì¡°íšŒ."""
    try:
        flow = ProductFlow()
        result = await flow.process_request(
            action="get",
            product_id=product_id,
            use_policy=use_policy
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{product_id}", response_model=ProductModel)
async def update_product(
    product_id: int,
    product: ProductUpdateModel,
    use_policy: bool = False
):
    """?í’ˆ ?˜ì •."""
    try:
        flow = ProductFlow()
        result = await flow.process_request(
            action="update",
            data=product.model_dump(exclude_unset=True),
            product_id=product_id,
            use_policy=use_policy
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[ProductModel])
async def list_products(use_policy: bool = False, limit: int = 100, offset: int = 0):
    """?í’ˆ ëª©ë¡ ì¡°íšŒ."""
    try:
        flow = ProductFlow()
        result = await flow.process_request(
            action="list",
            data={"limit": limit, "offset": offset},
            use_policy=use_policy
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{product_id}", response_model=dict)
async def delete_product(product_id: int, use_policy: bool = False):
    """?í’ˆ ?? œ."""
    try:
        flow = ProductFlow()
        result = await flow.process_request(
            action="delete",
            product_id=product_id,
            use_policy=use_policy
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/recommend", response_model=dict)
async def recommend_products(
    request: Request,
    use_policy: bool = False
):
    """?í’ˆ ì¶”ì²œ.

    Args:
        request: FastAPI Request ê°ì²´ (JSON bodyë¥?ë°›ê¸° ?„í•¨)
        use_policy: Trueë©??•ì±… ê¸°ë°˜(Agent), Falseë©?ê·œì¹™ ê¸°ë°˜(Service)
    """
    try:
        # Request bodyë¥?JSON?¼ë¡œ ?Œì‹±
        body = await request.json()

        # ?„ì†¡??ë©”ì‹œì§€ ?„ë¦°??ë°?ë¡œê¹…
        message = body.get("message", "") if body else ""
        print("=" * 60)
        print(f"[?í’ˆì¶”ì²œ ?”ì²­] ?„ì†¡??ë©”ì‹œì§€: {message}")
        print(f"[?í’ˆì¶”ì²œ ?”ì²­] ?„ì²´ ?°ì´?? {json.dumps(body, ensure_ascii=False, indent=2)}")
        print("=" * 60)

        logger.info("=" * 60)
        logger.info(f"[?í’ˆì¶”ì²œ ?”ì²­] ?„ì†¡??ë©”ì‹œì§€: {message}")
        logger.info(f"[?í’ˆì¶”ì²œ ?”ì²­] ?„ì²´ ?°ì´?? {body}")
        logger.info("=" * 60)

        # sys.stdout??ê°•ì œë¡?flush?˜ì—¬ ì¦‰ì‹œ ì¶œë ¥
        import sys
        sys.stdout.flush()

        flow = ProductFlow()
        result = await flow.process_request(
            action="recommend",
            data=body or {},
            use_policy=use_policy
        )
        return result
    except json.JSONDecodeError as e:
        logger.error(f"[?¤ë¥˜] JSON ?Œì‹± ?¤íŒ¨: {e}")
        raise HTTPException(status_code=400, detail=f"?˜ëª»??JSON ?•ì‹: {str(e)}")
    except Exception as e:
        logger.error(f"[?¤ë¥˜] ?í’ˆì¶”ì²œ ì²˜ë¦¬ ?¤íŒ¨: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

