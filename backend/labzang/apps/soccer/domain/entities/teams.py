# -*- coding: utf-8 -*-
"""?(Team) ? ? ??? SQLAlchemy ??."""

from sqlalchemy import Column, String, BigInteger, ForeignKey, Text, TIMESTAMP, func
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector

from labzang.shared.bases import Base


class Team(Base):
    """? ???/???? SQLAlchemy ??.

    Attributes:
        id: ? ?? ???(PK, BigInt)
        stadium_id: ??? ID (FK -> stadiums.id)
        team_code: ? ??
        region_name: ???
        team_name: ??
        e_team_name: ?? ??
        orig_yyyy: ????
        zip_code1: ????1
        zip_code2: ????2
        address: ??
        ddd: ????
        tel: ????
        fax: ????
        homepage: ????
        owner: ???
    """

    __tablename__ = "teams"

    id = Column(
        BigInteger,
        primary_key=True,
        comment="? ?? ???"
    )

    stadium_id = Column(
        BigInteger,
        ForeignKey("stadiums.id"),
        nullable=True,
        comment="??? ID"
    )

    team_code = Column(
        String(10),
        nullable=True,
        comment="? ??"
    )

    region_name = Column(
        String(10),
        nullable=True,
        comment="???"
    )

    team_name = Column(
        String(40),
        nullable=True,
        comment="??"
    )

    e_team_name = Column(
        String(50),
        nullable=True,
        comment="?? ??"
    )

    orig_yyyy = Column(
        String(10),
        nullable=True,
        comment="????"
    )

    zip_code1 = Column(
        String(10),
        nullable=True,
        comment="????1"
    )

    zip_code2 = Column(
        String(10),
        nullable=True,
        comment="????2"
    )

    address = Column(
        String(80),
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

    fax = Column(
        String(20),
        nullable=True,
        comment="????"
    )

    homepage = Column(
        String(100),
        nullable=True,
        comment="????"
    )

    owner = Column(
        String(50),
        nullable=True,
        comment="???"
    )

    stadium = relationship(
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


class TeamEmbedding(Base):
    """? ??? ???.

    Attributes:
        id: ??? ???? ???(PK, BigInt)
        team_id: ? ID (FK -> teams.id)
        content: ??? ??? ??? ?? ???
        embedding: 768?? KoElectra ??? ??
        created_at: ??? ?? ??
    """
    __tablename__ = "team_embeddings"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        comment="??? ???? ???"
    )

    team_id = Column(
        BigInteger,
        ForeignKey("teams.id", ondelete="CASCADE"),
        nullable=False,
        comment="? ID"
    )

    content = Column(
        Text,
        nullable=False,
        comment="??? ??? ??? ?? ???"
    )

    embedding = Column(
        Vector(768),
        nullable=False,
        comment="768?? KoElectra ??? ??"
    )

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="??? ?? ??"
    )

    team = relationship(
        "Team",
        back_populates="embeddings"
    )
