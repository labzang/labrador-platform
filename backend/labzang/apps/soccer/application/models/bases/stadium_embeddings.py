from sqlalchemy import Column, BigInteger, Text, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector

from labzang.shared.bases import Base

class StadiumEmbedding(Base):
    """ê²½ê¸°???„ë² ???•ë³´ë¥??€?¥í•˜??SQLAlchemy ëª¨ë¸.

    Attributes:
        id: ?„ë² ???ˆì½”??ê³ ìœ  ?ë³„??(PK, BigInt)
        stadium_id: ê²½ê¸°??ID (FK -> stadiums.id)
        content: ?ë³¸ ?ìŠ¤???°ì´??        embedding: ê²½ê¸°?¥ì„ ?œí˜„?˜ëŠ” 768ì°¨ì› ë²¡í„° ?„ë² ??        created_at: ?ˆì½”???ì„± ?œê°„
    """
    __tablename__ = "stadium_embeddings"

    # ê¸°ë³¸ ??    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='?„ë² ???ˆì½”??ê³ ìœ  ?ë³„??)

    # ê²½ê¸°???°ê? ??    stadium_id = Column(BigInteger, ForeignKey("stadiums.id", ondelete="CASCADE"), nullable=False, comment='ê²½ê¸°??ID')

    # ?ë³¸ ?ìŠ¤??ë°?ë²¡í„° ?°ì´??    content = Column(Text, nullable=False, comment='?„ë² ???ì„±???¬ìš©???ë³¸ ?ìŠ¤??)
    embedding = Column(Vector(768), nullable=False, comment='768ì°¨ì› ?„ë² ??ë²¡í„° (KoElectra)')

    # ?ì„± ?œê°„
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, comment='?ˆì½”???ì„± ?œê°„')

    # ê´€ê³??¤ì •
    stadium = relationship("Stadium", back_populates="embeddings")

# ì£¼ì„: ê´€ê³??•ì˜ ?„ë£Œ
# stadiums.py?€ ?¼ê??±ì„ ? ì??˜ë©° ?‘ì„±?˜ì—ˆ?µë‹ˆ??
# ëª¨ë“  Column??ì£¼ì„??ì¶”ê??˜ì—ˆ?¼ë©°, SQLAlchemy???œì? ?¤í??¼ì„ ?°ë?µë‹ˆ??
