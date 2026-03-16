"""?í’ˆ(Products) SQLAlchemy ëª¨ë¸."""

from sqlalchemy import Column, Integer, String, Text, Boolean, CheckConstraint, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from labzang.shared.bases import Base


class Product(Base):
    """?í’ˆ ?•ë³´ë¥??€?¥í•˜??SQLAlchemy ëª¨ë¸.

    Attributes:
        id: ?í’ˆ ê³ ìœ  ?ë³„??(?ë™ ì¦ê?)
        name: ?í’ˆëª?        description: ?í’ˆ ?¤ëª… (?„ë² ???ë¬¸??
        price: ê°€ê²?(???¨ìœ„, 0 ?´ìƒ)
        category: ì¹´í…Œê³ ë¦¬
        brand: ë¸Œëœ??        is_active: ?ë§¤ ?¬ë?
        created_at: ?ì„± ?¼ì‹œ
        updated_at: ?˜ì • ?¼ì‹œ
    """

    __tablename__ = "products"

    # ê¸°ë³¸ ??    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="?í’ˆ ê³ ìœ  ?ë³„??
    )

    # ?í’ˆ ?•ë³´
    name = Column(
        Text,
        nullable=False,
        comment="?í’ˆëª?
    )

    description = Column(
        Text,
        nullable=True,
        comment="?í’ˆ ?¤ëª… (?„ë² ???ë¬¸??"
    )

    price = Column(
        Integer,
        nullable=False,
        comment="ê°€ê²?(???¨ìœ„)"
    )

    category = Column(
        String(100),
        nullable=True,
        comment="ì¹´í…Œê³ ë¦¬"
    )

    brand = Column(
        String(100),
        nullable=True,
        comment="ë¸Œëœ??
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
        comment="?ë§¤ ?¬ë?"
    )

    # ?€?„ìŠ¤?¬í”„
    created_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        nullable=False,
        comment="?ì„± ?¼ì‹œ"
    )

    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="?˜ì • ?¼ì‹œ"
    )

    # ?œì•½ì¡°ê±´
    __table_args__ = (
        CheckConstraint("price >= 0", name="check_price_non_negative"),
    )

    # ê´€ê³?    orders = relationship(
        "Order",
        back_populates="product",
        cascade="all, delete-orphan",
        comment="ì£¼ë¬¸ ëª©ë¡"
    )

    def __repr__(self) -> str:
        """ê°ì²´ ?œí˜„ ë¬¸ì??"""
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"

