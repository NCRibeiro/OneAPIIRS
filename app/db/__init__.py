# app/db/__init__.py

"""
OneAPIIRS — Pacote de Banco de Dados

Este pacote expõe:
- Base: classe base declarativa para modelos ORM
- engine: AsyncEngine do SQLAlchemy (AsyncPG)
- async_session: factory de sessões AsyncSession
- get_db: dependência FastAPI para injeção de sessão
- init_db: utilitário assíncrono para criar (e opcionalmente recriar)tabelas
- init_db_sync: utilitário síncrono para criar (e opcionalmente recriar)tabelas
- main: CLI entrypoint para rodar init_db via linha de comando
"""

import argparse
import asyncio
import logging
from typing import Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine

import app.models  # noqa: F401 Register models for Base.metadata
from app.models import Base  # noqa: F401

from .session import AsyncSessionLocal, engine, get_db  # noqa: F401

# Configura o logger para este módulo
logger = logging.getLogger("app.db")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.INFO)


__all__ = [
    "Base",
    "engine",
    "AsyncSessionLocal",
    "get_db",
    "init_db",
    "init_db_sync",
    "main",
]


async def init_db(
    drop: bool = False,
    db_engine: Optional[AsyncEngine] = None,
) -> None:
    """
    Cria (ou recria) tabelas definidas em Base.metadata.

    Args:
        drop (bool): apaga tabelas existentes se True.
        db_engine (AsyncEngine): engine a usar
            (padrão session.engine).
    """
    engine_obj = db_engine or engine
    try:
        async with engine_obj.begin() as conn:
            if drop:
                logger.warning("DROP solicitado - apagando tabelas existentes")
                await conn.run_sync(Base.metadata.drop_all)

            logger.info("Criando tabelas no banco de dados")
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Tabelas criadas com sucesso")
    except SQLAlchemyError as err:
        logger.error("Erro ao (re)criar tabelas: %s", err)

    except Exception as exc:
        logger.exception("Falha inesperada na inicialização do DB: %s", exc)


def init_db_sync(drop: bool = False) -> None:
    """
    Versão síncrona de init_db para uso em scripts CLI.

    Exemplo:
        python -c "from app.db import init_db_sync; init_db_sync(drop=True)"
    """

    try:
        asyncio.run(init_db(drop=drop))
    except Exception:
        logger.critical("init_db_sync falhou")


def main() -> None:
    """
    CLI entrypoint para inicializar o banco via linha de comando.
    """
    parser = argparse.ArgumentParser(
        description="Inicializa o banco de dados para OneAPIIRS — APE."
    )
    parser.add_argument(
        "--drop",
        action="store_true",
        help="Dropa tabelas existentes antes de criar novas.",
    )
    args = parser.parse_args()

    logger.info(
        "Iniciando init_db (drop=%s) usando engine %s",  # noqa: E501
        args.drop,
        engine.url,
    )
    try:
        asyncio.run(init_db(drop=args.drop))
    except Exception as e:
        logger.exception("Falha na inicialização do banco: %s", e)
        exit(1)


if __name__ == "__main__":
    main()
