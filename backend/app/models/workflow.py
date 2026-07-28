from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.database.base import Base


class Workflow(Base):

    __tablename__ = "workflows"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    workflow_name = Column(
        String,
        nullable=False
    )


    department = Column(
        String,
        nullable=False
    )


    status = Column(
        String,
        default="Pending"
    )


    priority = Column(
        String,
        default="Medium"
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )