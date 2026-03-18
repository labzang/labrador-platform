# -*- coding: utf-8 -*-
"""?? ???(Schedule) ? ?? ??? SQLAlchemy ??."""

from sqlalchemy import Column, String, Integer, BigInteger, ForeignKey, Text, TIMESTAMP, func
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector

from labzang.shared.bases import Base


class Schedule(Base):
    """?? ??? ???/???? SQLAlchemy ??.

    Attributes:
        id: ?? ??? ?? ???(PK, BigInt)
        stadium_id: ??? ID (FK -> stadiums.id)
        hometeam_id: ?? ID (FK -> teams.id)
        awayteam_id: ??? ID (FK -> teams.id)
        stadium_code: ??? ??
        sche_date: ?? ??
        gubun: ??
        hometeam_code: ?? ??
        awayteam_code: ??? ??
        home_score: ?? ??
        away_score: ??? ??
    """

    __tablename__ = "schedules"

    id = Column(
        BigInteger,
        primary_key=True,
        comment="?? ??? ?? ???"
    )

    stadium_id = Column(
        BigInteger,
        ForeignKey("stadiums.id"),
        nullable=True,
        comment="??? ID"
    )

    hometeam_id = Column(
        BigInteger,
        ForeignKey("teams.id"),
        nullable=True,
        comment="?? ID"
    )

    awayteam_id = Column(
        BigInteger,
        ForeignKey("teams.id"),
        nullable=True,
        comment="??? ID"
    )

    stadium_code = Column(
        String(10),
        nullable=True,
        comment="??? ??"
    )

    sche_date = Column(
        String(10),
        nullable=True,
        comment="?? ??"
    )

    gubun = Column(
        String(10),
        nullable=True,
        comment="??"
    )

    hometeam_code = Column(
        String(10),
        nullable=True,
        comment="?? ??"
    )

    awayteam_code = Column(
        String(10),
        nullable=True,
        comment="??? ??"
    )

    home_score = Column(
        Integer,
        nullable=True,
        comment="?? ??"
    )

    away_score = Column(
        Integer,
        nullable=True,
        comment="??? ??"
    )

    stadium = relationship(
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

