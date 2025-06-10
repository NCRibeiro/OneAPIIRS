# app/db/session.py

"""
OneAPIIRS — APE Session Manager

Gerencia a conexão assíncrona com o banco de dados PostgreSQL via SQLAlchemy.
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker

# Corrigido para o import absoluto (roda dentro de /app)
from core.settings import settings

# 1) Cria o engine assíncrono (usa asyncpg por baixo)
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    # Se quiser pool tradicional, especifique poolclass=QueuePool etc.
    # pool_size=10,
    # max_overflow=20,
    future=True,
)

# 2) Cria a fábrica de sessões
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False  # type: ignore
)

async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


# 3) Dependência FastAPI
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Fornece uma sessão AsyncSession dentro de um `async with`,
    garantindo que o .close() seja chamado no final.
    """
    async with AsyncSessionLocal() as session:
        yield session
