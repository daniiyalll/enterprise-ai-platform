from sqlalchemy import Column, Integer, String, Boolean
from app.database.base import Base


class Workflow(Base):
    __tablename__ = "workflows"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    status = Column(String, default="pending")
    is_active = Column(Boolean, default=True)