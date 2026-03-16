"""ì£¼ë¬¸(Order) Pydantic ëª¨ë¸."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from labzang.apps.product.models.bases.orders import OrderStatus


class OrderModel(BaseModel):
    """ì£¼ë¬¸ ?•ë³´ë¥??„ì†¡?˜ê¸° ?„í•œ Pydantic ëª¨ë¸.

    SQLAlchemy Order ëª¨ë¸??transfer ê°ì²´?…ë‹ˆ??
    """

    id: Optional[int] = Field(None, description="ì£¼ë¬¸ ê³ ìœ  ?ë³„??)
    consumer_id: int = Field(..., description="?Œë¹„??ID", gt=0)
    product_id: int = Field(..., description="?í’ˆ ID", gt=0)
    quantity: int = Field(..., description="ì£¼ë¬¸ ?˜ëŸ‰", gt=0)
    unit_price: int = Field(..., description="?¨ê? (ì£¼ë¬¸ ?œì ??ê°€ê²?", ge=0)
    total_price: int = Field(..., description="ì´?ê°€ê²?(quantity * unit_price)", ge=0)
    status: OrderStatus = Field(..., description="ì£¼ë¬¸ ?íƒœ")
    order_date: Optional[datetime] = Field(None, description="ì£¼ë¬¸ ?¼ì‹œ")
    created_at: Optional[datetime] = Field(None, description="?ì„± ?¼ì‹œ")
    updated_at: Optional[datetime] = Field(None, description="?˜ì • ?¼ì‹œ")

    class Config:
        """Pydantic ?¤ì •."""

        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class OrderCreateModel(BaseModel):
    """ì£¼ë¬¸ ?ì„± ?”ì²­ ëª¨ë¸."""

    consumer_id: int = Field(..., description="?Œë¹„??ID", gt=0)
    product_id: int = Field(..., description="?í’ˆ ID", gt=0)
    quantity: int = Field(1, description="ì£¼ë¬¸ ?˜ëŸ‰", gt=0)
    unit_price: int = Field(..., description="?¨ê? (ì£¼ë¬¸ ?œì ??ê°€ê²?", ge=0)
    total_price: int = Field(..., description="ì´?ê°€ê²?(quantity * unit_price)", ge=0)
    status: OrderStatus = Field(OrderStatus.PENDING, description="ì£¼ë¬¸ ?íƒœ")


class OrderUpdateModel(BaseModel):
    """ì£¼ë¬¸ ?˜ì • ?”ì²­ ëª¨ë¸."""

    quantity: Optional[int] = Field(None, description="ì£¼ë¬¸ ?˜ëŸ‰", gt=0)
    unit_price: Optional[int] = Field(None, description="?¨ê?", ge=0)
    total_price: Optional[int] = Field(None, description="ì´?ê°€ê²?, ge=0)
    status: Optional[OrderStatus] = Field(None, description="ì£¼ë¬¸ ?íƒœ")


class OrderDetailModel(OrderModel):
    """ì£¼ë¬¸ ?ì„¸ ?•ë³´ ëª¨ë¸ (ê´€ê³??¬í•¨)."""

    consumer_name: Optional[str] = Field(None, description="?Œë¹„???´ë¦„")
    consumer_email: Optional[str] = Field(None, description="?Œë¹„???´ë©”??)
    product_name: Optional[str] = Field(None, description="?í’ˆëª?)
    product_price: Optional[int] = Field(None, description="?í’ˆ ?„ì¬ ê°€ê²?)

