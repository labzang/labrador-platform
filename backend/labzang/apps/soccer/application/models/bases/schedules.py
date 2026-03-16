"""ê²½ê¸° ?¼ì •(Schedule) SQLAlchemy ëª¨ë¸."""

from sqlalchemy import Column, String, Integer, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

from labzang.shared.bases import Base


class Schedule(Base):
    """ê²½ê¸° ?¼ì • ?•ë³´ë¥??€?¥í•˜??SQLAlchemy ëª¨ë¸.

    Attributes:
        id: ê²½ê¸° ?¼ì • ê³ ìœ  ?ë³„??(PK, BigInt)
        stadium_id: ê²½ê¸°??ID (FK -> stadiums.id)
        hometeam_id: ?ˆí? ID (FK -> teams.id)
        awayteam_id: ?ì •?€ ID (FK -> teams.id)
        stadium_code: ê²½ê¸°??ì½”ë“œ
        sche_date: ê²½ê¸° ?¼ì
        gubun: êµ¬ë¶„
        hometeam_code: ?ˆí? ì½”ë“œ
        awayteam_code: ?ì •?€ ì½”ë“œ
        home_score: ?ˆí? ?ìˆ˜
        away_score: ?ì •?€ ?ìˆ˜
    """

    __tablename__ = "schedules"

    # ê¸°ë³¸ ??    id = Column(
        BigInteger,
        primary_key=True,
        comment="ê²½ê¸° ?¼ì • ê³ ìœ  ?ë³„??
    )

    # ?¸ë˜ ??    stadium_id = Column(
        BigInteger,
        ForeignKey("stadiums.id"),
        nullable=True,
        comment="ê²½ê¸°??ID"
    )

    hometeam_id = Column(
        BigInteger,
        ForeignKey("teams.id"),
        nullable=True,
        comment="?ˆí? ID"
    )

    awayteam_id = Column(
        BigInteger,
        ForeignKey("teams.id"),
        nullable=True,
        comment="?ì •?€ ID"
    )

    # ê²½ê¸° ?•ë³´
    stadium_code = Column(
        String(10),
        nullable=True,
        comment="ê²½ê¸°??ì½”ë“œ"
    )

    sche_date = Column(
        String(10),
        nullable=True,
        comment="ê²½ê¸° ?¼ì"
    )

    gubun = Column(
        String(10),
        nullable=True,
        comment="êµ¬ë¶„"
    )

    hometeam_code = Column(
        String(10),
        nullable=True,
        comment="?ˆí? ì½”ë“œ"
    )

    awayteam_code = Column(
        String(10),
        nullable=True,
        comment="?ì •?€ ì½”ë“œ"
    )

    home_score = Column(
        Integer,
        nullable=True,
        comment="?ˆí? ?ìˆ˜"
    )

    away_score = Column(
        Integer,
        nullable=True,
        comment="?ì •?€ ?ìˆ˜"
    )

    # ê´€ê³?    stadium = relationship(
        "Stadium",
        back_populates="schedules"
    )

    hometeam = relationship(
        "Team",
        foreign_keys=[hometeam_id],
        backref="home_schedules"
    )

    awayteam = relationship(
        "Team",
        foreign_keys=[awayteam_id],
        backref="away_schedules"
    )

    embeddings = relationship(
        "ScheduleEmbedding",
        back_populates="schedule",
        cascade="all, delete-orphan"
    )
