"""
Inicialização do Banco de Dados — OneAPIIRS
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from app.db.base_class import Base
from app.db.session import async_session, engine
import app.models  # noqa

# ─────────────────────────────────────────────────────────────


async def init_db(drop: bool = False) -> None:
    """
    Inicializa o banco de dados.

    Args:
        drop (bool): Se True, dropa todas as tabelas antes de criar.
    """
    try:
        async with engine.begin() as conn:
            if drop:
                print("Dropando todas as tabelas...")
                await conn.run_sync(Base.metadata.drop_all)
                print("Tabelas removidas.")
            print("Criando tabelas...")
            await conn.run_sync(Base.metadata.create_all)
            print("Banco de dados pronto.")
    except SQLAlchemyError as e:
        print(f"Erro ao inicializar o banco de dados: {e}")
        raise

# ─────────────────────────────────────────────────────────────


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency do FastAPI para obter uma sessão assíncrona do DB.
    """
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
