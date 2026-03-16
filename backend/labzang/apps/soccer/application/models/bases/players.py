"""? ìˆ˜(Player) SQLAlchemy ëª¨ë¸."""

from sqlalchemy import Column, String, Integer, BigInteger, Date, ForeignKey
from sqlalchemy.orm import relationship

from labzang.shared.bases import Base


class Player(Base):
    """? ìˆ˜ ?•ë³´ë¥??€?¥í•˜??SQLAlchemy ëª¨ë¸.

    Attributes:
        id: ? ìˆ˜ ê³ ìœ  ?ë³„??(PK, BigInt)
        team_id: ?€ ID (FK -> teams.id)
        player_name: ? ìˆ˜ëª?        e_player_name: ?ë¬¸ ? ìˆ˜ëª?        nickname: ë³„ëª…
        join_yyyy: ?…ë‹¨?„ë„
        position: ?¬ì???        back_no: ?±ë²ˆ??        nation: êµ? 
        birth_date: ?ë…„?”ì¼
        solar: ?‘ë ¥/?Œë ¥ êµ¬ë¶„
        height: ??(cm)
        weight: ëª¸ë¬´ê²?(kg)
    """

    __tablename__ = "players"

    # ê¸°ë³¸ ??    id = Column(
        BigInteger,
        primary_key=True,
        comment="? ìˆ˜ ê³ ìœ  ?ë³„??
    )

    # ?¸ë˜ ??    team_id = Column(
        BigInteger,
        ForeignKey("teams.id"),
        nullable=True,
        comment="?€ ID"
    )

    # ? ìˆ˜ ?•ë³´
    player_name = Column(
        String(20),
        nullable=True,
        comment="? ìˆ˜ëª?
    )

    e_player_name = Column(
        String(40),
        nullable=True,
        comment="?ë¬¸ ? ìˆ˜ëª?
    )

    nickname = Column(
        String(30),
        nullable=True,
        comment="ë³„ëª…"
    )

    join_yyyy = Column(
        String(10),
        nullable=True,
        comment="?…ë‹¨?„ë„"
    )

    position = Column(
        String(10),
        nullable=True,
        comment="?¬ì???
    )

    back_no = Column(
        Integer,
        nullable=True,
        comment="?±ë²ˆ??
    )

    nation = Column(
        String(20),
        nullable=True,
        comment="êµ? "
    )

    birth_date = Column(
        Date,
        nullable=True,
        comment="?ë…„?”ì¼"
    )

    solar = Column(
        String(10),
        nullable=True,
        comment="?‘ë ¥/?Œë ¥ êµ¬ë¶„"
    )

    height = Column(
        Integer,
        nullable=True,
        comment="??(cm)"
    )

    weight = Column(
        Integer,
        nullable=True,
        comment="ëª¸ë¬´ê²?(kg)"
    )

    # ê´€ê³?    team = relationship(
        "Team",
        back_populates="players"
    )

    embeddings = relationship(
        "PlayerEmbedding",
        back_populates="player",
        cascade="all, delete-orphan"
    )
