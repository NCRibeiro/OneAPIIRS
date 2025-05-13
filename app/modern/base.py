from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from core.settings import settings

# ─── Base do ORM ──────────────────────────────────────
Base = declarative_base()

# ─── Engine assíncrono (usa asyncpg via URL em settings) ─
engine = create_async_engine(
    settings.DATABASE_URL,  # Ex: postgresql+asyncpg://user:pass@db:5432/dbname
    echo=settings.DEBUG,
    future=True,  # Recomenda usar API 2.0 do SQLAlchemy
)

# ─── Fábrica de sessões assíncronas ────────────────────
AsyncSessionLocal = sessionmaker(  # type: ignore
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)
