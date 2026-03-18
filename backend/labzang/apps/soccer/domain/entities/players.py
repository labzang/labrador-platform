# -*- coding: utf-8 -*-
"""??(Player) ? ?? ??? SQLAlchemy ??."""

from sqlalchemy import Column, String, Integer, BigInteger, Date, ForeignKey, Text, TIMESTAMP, func
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector

from labzang.shared.bases import Base


class Player(Base):
    """

    Attributes:
        id → 선수 고유 식별자(PK, BigInt)
        team_id → 팀 ID (FK -> teams.id)
        player_name → 선수명
        e_player_name → 영문 선수명
        nickname → 닉네임
        join_yyyy → 입단년도
        position → 포지션
        back_no → 등번호
        nation → 국적
        birth_date → 생년월일
        solar → 양력/음력 구분
        height → 키(cm)
        weight → 몸무게(kg)
    """

    __tablename__ = "players"

    id = Column(
        BigInteger,
        primary_key=True,
        comment="?? ?? ???"
    )

    team_id = Column(
        BigInteger,
        ForeignKey("teams.id"),
        nullable=True,
        comment="? ID"
    )

    player_name = Column(
        String(20),
        nullable=True,
        comment="???"
    )

    e_player_name = Column(
        String(40),
        nullable=True,
        comment="?? ???"
    )

    nickname = Column(
        String(30),
        nullable=True,
        comment="???"
    )

    join_yyyy = Column(
        String(10),
        nullable=True,
        comment="????"
    )

    position = Column(
        String(10),
        nullable=True,
        comment="???"
    )

    back_no = Column(
        Integer,
        nullable=True,
        comment="???"
    )

    nation = Column(
        String(20),
        nullable=True,
        comment="??"
    )

    birth_date = Column(
        Date,
        nullable=True,
        comment="????"
    )

    solar = Column(
        String(10),
        nullable=True,
        comment="??/?? ??"
    )

    height = Column(
        Integer,
        nullable=True,
        comment="?(cm)"
    )

    weight = Column(
        Integer,
        nullable=True,
        comment="???(kg)"
    )

    team = relationship(
        "Team",
        back_populates="players"
    )

    embeddings = relationship(
        "PlayerEmbedding",
        back_populates="player",
        cascade="all, delete-orphan"
    )
