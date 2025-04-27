"""
OneAPIIRS — APE Session Manager

Gerencia a conexão assíncrona com o banco de dados PostgreSQL via SQLAlchemy.
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.settings import settings

# ───────────── Criação do Engine Assíncrono ─────────────
engine = create_async_engine(
    url=settings.database_url,
    echo=settings.debug,         # Exibe queries SQL em modo debug
    pool_pre_ping=True,           # Testa a conexão antes de usar
    pool_size=10,                 # Tamanho inicial do pool
    max_overflow=20,              # Número máximo de conexões extras
    future=True,                  # Estilo SQLAlchemy 2.x
)

# ───────────── Fábrica de Sessões ─────────────
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,        # Mantém objetos após commit
)

# ───────────── Dependência para FastAPI ─────────────
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependência que fornece uma sessão de banco de dados assíncrona."""
    db = async_session()
    try:
        yield db
    finally:
        db.close()

# ───────────── Exports ─────────────
__all__ = ["engine", "async_session", "get_db"]
