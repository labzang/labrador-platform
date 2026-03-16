from sqlalchemy import Column, BigInteger, Text, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector

from labzang.shared.bases import Base


class PlayerEmbedding(Base):
    """?„ë² ???ˆì½”??ëª¨ë¸.

    Attributes:
        id: ?„ë² ???ˆì½”??ê³ ìœ  ?ë³„??(PK, BigInt, autoincrement)
        player_id: ? ìˆ˜ ID (FK -> Player.id)
        content: ?ë³¸ ?ìŠ¤???°ì´??        embedding: KoElectra ê¸°ë°˜ 768ì°¨ì› ë²¡í„° ?„ë² ??        created_at: ?ˆì½”???ì„± ?œê°„
    """
    __tablename__ = "player_embeddings"

    # ê¸°ë³¸ ??    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        comment="?„ë² ???ˆì½”??ê³ ìœ  ?ë³„??
    )

    # ?¸ë˜ ??    player_id = Column(
        BigInteger,
        ForeignKey("players.id", ondelete="CASCADE"),
        nullable=False,
        comment="? ìˆ˜ ID"
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
    player = relationship(
        "Player",
        back_populates="embeddings"
    )
