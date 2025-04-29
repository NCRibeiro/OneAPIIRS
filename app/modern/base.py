from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Base do SQLAlchemy
Base = declarative_base()

# Banco de dados
DATABASE_URL = settings.database_url
engine = create_async_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=settings.debug)

# Session
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)
