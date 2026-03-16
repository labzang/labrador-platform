"""상품(Product) 규칙 기반 서비스 - 스텁. 실제 구현 시 교체."""
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


class ProductService:
    """상품 규칙 기반 서비스 스텁."""

    def __init__(self):
        logger.warning("ProductService 스텁 사용 중")

    async def create_product(self, data: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError("ProductService.create_product 미구현")

    async def update_product(self, product_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError("ProductService.update_product 미구현")

    async def get_product(self, product_id: int) -> Optional[Dict[str, Any]]:
        raise NotImplementedError("ProductService.get_product 미구현")

    async def list_products(self, **kwargs: Any) -> List[Dict[str, Any]]:
        raise NotImplementedError("ProductService.list_products 미구현")

    async def delete_product(self, product_id: int) -> Dict[str, Any]:
        raise NotImplementedError("ProductService.delete_product 미구현")
