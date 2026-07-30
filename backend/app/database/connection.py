from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://neondb_owner:npg_HORNDn4Q6Irl@ep-morning-morning-ax67mmap.c-4.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"


engine = create_engine(
    DATABASE_URL
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)