"""경기??Stadium) SQLAlchemy 모델."""

from sqlalchemy import Column, Integer, BigInteger, String
from sqlalchemy.orm import relationship

from labzang.shared.bases import Base


class Stadium(Base):
    """경기???�보�??�?�하??SQLAlchemy 모델.

    Attributes:
        id: 경기??고유 ?�별??(PK, BigInt)
        stadium_code: 경기??코드
        stadium_name: 경기???�름
        hometeam_code: ?��? 코드
        seat_count: 좌석 ??        address: 주소
        ddd: 지??��??        tel: ?�화번호
    """

    __tablename__ = "stadiums"

    # 기본 ??    id = Column(
        BigInteger,
        primary_key=True,
        comment="경기??고유 ?�별??
    )

    # 경기???�보
    stadium_code = Column(
        String(10),
        nullable=True,
        comment="경기??코드"
    )

    stadium_name = Column(
        String(40),
        nullable=True,
        comment="경기???�름"
    )

    hometeam_code = Column(
        String(10),
        nullable=True,
        comment="?��? 코드"
    )

    seat_count = Column(
        Integer,
        nullable=True,
        comment="좌석 ??
    )

    address = Column(
        String(60),
        nullable=True,
        comment="주소"
    )

    ddd = Column(
        String(10),
        nullable=True,
        comment="지??��??
    )

    tel = Column(
        String(20),
        nullable=True,
        comment="?�화번호"
    )

    # 관�?    teams = relationship(
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
