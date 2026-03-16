from sqlalchemy import Column, BigInteger, Text, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector

from labzang.shared.bases import Base

class TeamEmbedding(Base):
    """?€ ?„ë² ???•ë³´ë¥??€?¥í•˜??SQLAlchemy ëª¨ë¸.

    Attributes:
        id: ?„ë² ???ˆì½”??ê³ ìœ  ?ë³„??(PK, BigInt)
        team_id: ?€ ID (FK -> teams.id)
        content: ?ë³¸ ?ìŠ¤???°ì´??        embedding: 768ì°¨ì› KoElectra ?„ë² ??ë²¡í„°
        created_at: ?ˆì½”???ì„± ?œê°„
    """
    __tablename__ = "team_embeddings"

    # ê¸°ë³¸ ??    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        comment='?„ë² ???ˆì½”??ê³ ìœ  ?ë³„??
    )

    # ?€ê³¼ì˜ ê´€ê³?    team_id = Column(
        BigInteger,
        ForeignKey("teams.id", ondelete="CASCADE"),
        nullable=False,
        comment='?€ ID'
    )

    # ?ë³¸ ?ìŠ¤???°ì´??    content = Column(
        Text,
        nullable=False,
        comment='?„ë² ???ì„±???¬ìš©???ë³¸ ?ìŠ¤??
    )

    # 768ì°¨ì› ?„ë² ??ë²¡í„°
    embedding = Column(
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
    team = relationship(
        "Team",
        back_populates="embeddings"
    )

# Example usage of the database engine creation (for completeness, not required in script execution)
# engine = create_engine('postgresql://user:password@localhost/dbname')
# Base.metadata.create_all(engine)
