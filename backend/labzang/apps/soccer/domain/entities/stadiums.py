# -*- coding: utf-8 -*-
"""???(Stadium) ? ??? ??? SQLAlchemy ??."""

from sqlalchemy import Column, Integer, BigInteger, String, Text, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector

from labzang.shared.bases import Base


class Stadium(Base):
    """??? ???/???? SQLAlchemy ??.

    Attributes:
        id: ??? ?? ???(PK, BigInt)
        stadium_code: ??? ??
        stadium_name: ??? ??
        hometeam_code: ?? ??
        seat_count: ?? ?
        address: ??
        ddd: ????
        tel: ????
    """

    __tablename__ = "stadiums"

    id = Column(
        BigInteger,
        primary_key=True,
        comment="??? ?? ???"
    )

    stadium_code = Column(
        String(10),
        nullable=True,
        comment="??? ??"
    )

    stadium_name = Column(
        String(40),
        nullable=True,
        comment="??? ??"
    )

    hometeam_code = Column(
        String(10),
        nullable=True,
        comment="?? ??"
    )

    seat_count = Column(
        Integer,
        nullable=True,
        comment="?? ?"
    )

    address = Column(
        String(60),
        nullable=True,
        comment="??"
    )

    ddd = Column(
        String(10),
        nullable=True,
        comment="????"
    )

    tel = Column(
        String(20),
        nullable=True,
        comment="????"
    )

    teams = relationship(
        "Team",
        back_populates="stadium"
    )

    schedules = relationship(
        "Schedule",
        back_populates="stadium"
    )

    embeddings = relationship(
        "StadiumEmbedding",
        back_populates="stadium",
        cascade="all, delete-orphan"
    )


class StadiumEmbedding(Base):
    """??? ??? ???.

    Attributes:
        id: ??? ???? ???(PK, BigInt)
        stadium_id: ??? ID (FK -> stadiums.id)
        content: ??? ??? ??? ?? ???
        embedding: 768?? ??? ?? (KoElectra)
        created_at: ??? ?? ??
    """
    __tablename__ = "stadium_embeddings"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        comment="??? ???? ???"
    )

    stadium_id = Column(
        BigInteger,
        ForeignKey("stadiums.id", ondelete="CASCADE"),
        nullable=False,
        comment="??? ID"
    )

    content = Column(
        Text,
        nullable=False,
        comment="??? ??? ??? ?? ???"
    )

    embedding = Column(
        Vector(768),
        nullable=False,
        comment="768?? ??? ?? (KoElectra)"
    )

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="??? ?? ??"
    )

    stadium = relationship(
        "Stadium",
        back_populates="embeddings"
    )
