# session.py
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
    """
    Fornece uma sessão de banco de dados assíncrona para ser usada em endpoints FastAPI.

    O gerador cria uma nova sessão de banco de dados assíncrona no início do seu ciclo de vida,
    permitindo que seja utilizada em operações de banco de dados. Após a execução do código que
    utiliza a sessão, o gerador garante que a sessão seja fechada automaticamente.

    Exemplo de uso com FastAPI:
        db = Depends(get_db)
    
    O gerador segue o padrão de boas práticas de gerenciamento de conexões com o banco de dados,
    garantindo que a sessão seja corretamente fechada após o uso, evitando vazamento de recursos.
    """
    db = async_session()  # Cria uma nova sessão assíncrona
    try:
        yield db  # Retorna a sessão para ser usada no contexto da função dependente
    finally:
        await db.close()  # Garante o fechamento da sessão ao final, independentemente de sucesso ou erro
        

# ───────────── Exports ─────────────
__all__ = ["engine", "async_session", "get_db"]
