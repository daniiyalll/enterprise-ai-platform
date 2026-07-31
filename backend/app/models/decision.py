from sqlalchemy import Column, Integer, String, Float
from app.database.base import Base


class Decision(Base):

    __tablename__ = "decisions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    agent_name = Column(
        String
    )

    decision = Column(
        String
    )

    reason = Column(
        String
    )

    confidence = Column(
        Float
    )