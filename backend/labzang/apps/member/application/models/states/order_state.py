"""ì£¼ë¬¸(Order) ?íƒœ ë¨¸ì‹ ."""

from enum import Enum
from typing import Optional, Set
from datetime import datetime

from pydantic import BaseModel, Field

from labzang.apps.product.models.bases.orders import OrderStatus


class OrderState(BaseModel):
    """ì£¼ë¬¸ ?íƒœ ë¨¸ì‹  ?´ë˜??

    ì£¼ë¬¸???íƒœë¥?ê´€ë¦¬í•˜ê³??íƒœ ?„ì´ë¥?ê²€ì¦í•©?ˆë‹¤.
    """

    status: OrderStatus = Field(
        default=OrderStatus.PENDING,
        description="ì£¼ë¬¸ ?íƒœ"
    )
    last_status_change: Optional[datetime] = Field(
        None,
        description="ë§ˆì?ë§??íƒœ ë³€ê²??¼ì‹œ"
    )
    status_history: list[dict] = Field(
        default_factory=list,
        description="?íƒœ ë³€ê²??´ë ¥"
    )

    # ?íƒœ ?„ì´ ê·œì¹™
    _valid_transitions: dict[OrderStatus, Set[OrderStatus]] = {
        OrderStatus.PENDING: {
            OrderStatus.CONFIRMED,
            OrderStatus.CANCELLED
        },
        OrderStatus.CONFIRMED: {
            OrderStatus.PROCESSING,
            OrderStatus.CANCELLED
        },
        OrderStatus.PROCESSING: {
            OrderStatus.SHIPPED,
            OrderStatus.CANCELLED
        },
        OrderStatus.SHIPPED: {
            OrderStatus.DELIVERED,
            OrderStatus.CANCELLED  # ë°°ì†¡ ì¤?ì·¨ì†Œ???¹ìˆ˜ ì¼€?´ìŠ¤
        },
        OrderStatus.DELIVERED: set(),  # ë°°ì†¡ ?„ë£Œ ???„ì´ ë¶ˆê?
        OrderStatus.CANCELLED: set()  # ì·¨ì†Œ ???„ì´ ë¶ˆê?
    }

    def can_transition_to(self, new_status: OrderStatus) -> bool:
        """?íƒœ ?„ì´ê°€ ê°€?¥í•œì§€ ?•ì¸.

        Args:
            new_status: ?„ì´?˜ë ¤???ˆë¡œ???íƒœ

        Returns:
            ?„ì´ ê°€???¬ë?
        """
        if new_status == self.status:
            return True  # ê°™ì? ?íƒœë¡œì˜ ?„ì´???ˆìš©

        allowed_transitions = self._valid_transitions.get(self.status, set())
        return new_status in allowed_transitions

    def transition_to(self, new_status: OrderStatus, reason: Optional[str] = None) -> bool:
        """?íƒœë¥??„ì´.

        Args:
            new_status: ?„ì´?˜ë ¤???ˆë¡œ???íƒœ
            reason: ?íƒœ ë³€ê²??¬ìœ 

        Returns:
            ?„ì´ ?±ê³µ ?¬ë?

        Raises:
            ValueError: ? íš¨?˜ì? ?Šì? ?íƒœ ?„ì´??ê²½ìš°
        """
        if not self.can_transition_to(new_status):
            raise ValueError(
                f"?íƒœ ?„ì´ ë¶ˆê?: {self.status.value} -> {new_status.value}"
            )

        # ?íƒœ ?´ë ¥ ê¸°ë¡
        self.status_history.append({
            "from_status": self.status.value,
            "to_status": new_status.value,
            "timestamp": datetime.now().isoformat(),
            "reason": reason
        })

        self.status = new_status
        self.last_status_change = datetime.now()
        return True

    def is_completed(self) -> bool:
        """?„ë£Œ ?íƒœ?¸ì? ?•ì¸ (ë°°ì†¡ ?„ë£Œ ?ëŠ” ì·¨ì†Œ)."""
        return self.status in {OrderStatus.DELIVERED, OrderStatus.CANCELLED}

    def is_cancellable(self) -> bool:
        """ì·¨ì†Œ ê°€?¥í•œ ?íƒœ?¸ì? ?•ì¸."""
        return self.status not in {OrderStatus.DELIVERED, OrderStatus.CANCELLED}

    def is_shippable(self) -> bool:
        """ë°°ì†¡ ê°€?¥í•œ ?íƒœ?¸ì? ?•ì¸."""
        return self.status == OrderStatus.PROCESSING

    class Config:
        """Pydantic ?¤ì •."""

        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }

