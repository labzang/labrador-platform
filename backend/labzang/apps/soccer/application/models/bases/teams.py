"""?€(Team) SQLAlchemy ëª¨ë¸."""

from sqlalchemy import Column, String, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

from labzang.shared.bases import Base


class Team(Base):
    """?€ ?•ë³´ë¥??€?¥í•˜??SQLAlchemy ëª¨ë¸.

    Attributes:
        id: ?€ ê³ ìœ  ?ë³„??(PK, BigInt)
        stadium_id: ê²½ê¸°??ID (FK -> stadiums.id)
        team_code: ?€ ì½”ë“œ
        region_name: ì§€??ª…
        team_name: ?€ëª?        e_team_name: ?ë¬¸ ?€ëª?        orig_yyyy: ì°½ë‹¨?„ë„
        zip_code1: ?°í¸ë²ˆí˜¸1
        zip_code2: ?°í¸ë²ˆí˜¸2
        address: ì£¼ì†Œ
        ddd: ì§€??²ˆ??        tel: ?„í™”ë²ˆí˜¸
        fax: ?©ìŠ¤ë²ˆí˜¸
        homepage: ?ˆí˜?´ì?
        owner: êµ¬ë‹¨ì£?    """

    __tablename__ = "teams"

    # ê¸°ë³¸ ??    id = Column(
        BigInteger,
        primary_key=True,
        comment="?€ ê³ ìœ  ?ë³„??
    )

    # ?¸ë˜ ??    stadium_id = Column(
        BigInteger,
        ForeignKey("stadiums.id"),
        nullable=True,
        comment="ê²½ê¸°??ID"
    )

    # ?€ ?•ë³´
    team_code = Column(
        String(10),
        nullable=True,
        comment="?€ ì½”ë“œ"
    )

    region_name = Column(
        String(10),
        nullable=True,
        comment="ì§€??ª…"
    )

    team_name = Column(
        String(40),
        nullable=True,
        comment="?€ëª?
    )

    e_team_name = Column(
        String(50),
        nullable=True,
        comment="?ë¬¸ ?€ëª?
    )

    orig_yyyy = Column(
        String(10),
        nullable=True,
        comment="ì°½ë‹¨?„ë„"
    )

    zip_code1 = Column(
        String(10),
        nullable=True,
        comment="?°í¸ë²ˆí˜¸1"
    )

    zip_code2 = Column(
        String(10),
        nullable=True,
        comment="?°í¸ë²ˆí˜¸2"
    )

    address = Column(
        String(80),
        nullable=True,
        comment="ì£¼ì†Œ"
    )

    ddd = Column(
        String(10),
        nullable=True,
        comment="ì§€??²ˆ??
    )

    tel = Column(
        String(20),
        nullable=True,
        comment="?„í™”ë²ˆí˜¸"
    )

    fax = Column(
        String(20),
        nullable=True,
        comment="?©ìŠ¤ë²ˆí˜¸"
    )

    homepage = Column(
        String(100),
        nullable=True,
        comment="?ˆí˜?´ì?"
    )

    owner = Column(
        String(50),
        nullable=True,
        comment="êµ¬ë‹¨ì£?
    )

    # ê´€ê³?    stadium = relationship(
        "Stadium",
        back_populates="teams"
    )

    players = relationship(
        "Player",
        back_populates="team",
        cascade="all, delete-orphan"
    )

    embeddings = relationship(
        "TeamEmbedding",
        back_populates="team",
        cascade="all, delete-orphan"
    )
