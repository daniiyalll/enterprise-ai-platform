from app.database.connection import engine
from app.database.base import Base

from app.models.user import User
from app.models.project import Project
from app.models.dataset import Dataset
from app.models.ai_model import AIModel


print("Creating database tables...")

Base.metadata.create_all(bind=engine)

print("Tables created successfully!")