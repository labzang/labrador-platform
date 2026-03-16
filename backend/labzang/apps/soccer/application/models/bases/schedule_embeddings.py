from sqlalchemy import Column, BigInteger, Text, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector

from labzang.shared.bases import Base


class ScheduleEmbedding(Base):
    """?„ë² ???ˆì½”??ëª¨ë¸.

    Attributes:
        id: ?„ë² ???ˆì½”??ê³ ìœ  ?ë³„??(PK, BigInt)
        schedule_id: ê²½ê¸° ?¼ì • ID (FK -> schedules.id)
        content: ?ë³¸ ?ìŠ¤???°ì´??(Text)
        embedding: 768ì°¨ì› KoElectra ?„ë² ??ë²¡í„° (Vector)
        created_at: ?ˆì½”???ì„± ?œê°„ (TIMESTAMP)
    """
    __tablename__ = "schedule_embeddings"

    # ê¸°ë³¸ ??    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        comment="?„ë² ???ˆì½”??ê³ ìœ  ?ë³„??
    )

    # ?¸ë˜ ??    schedule_id = Column(
        BigInteger,
        ForeignKey("schedules.id", ondelete="CASCADE"),
        nullable=False,
        comment="ê²½ê¸° ?¼ì • ID"
    )

    # ?ë³¸ ?ìŠ¤???°ì´??    content = Column(
        Text,
        nullable=False,
        comment="?„ë² ???ì„±???¬ìš©???ë³¸ ?ìŠ¤??
    )

    # 768ì°¨ì› KoElectra ë²¡í„° ?„ë² ??    embedding = Column(
        Vector(768),
        nullable=False,
        comment='768ì°¨ì› KoElectra ?„ë² ??ë²¡í„°'
    )

    # ?ì„± ?œê°„
    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment='?ˆì½”???ì„± ?œê°„'
    )

    # ê´€ê³??¤ì •
    schedule = relationship(
        "Schedule",
        back_populates="embeddings"
    )
