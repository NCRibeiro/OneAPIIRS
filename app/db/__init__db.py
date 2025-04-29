"""
Inicializa o banco de dados: cria todas as tabelas definidas nos modelos ORM.
"""

import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import engine
from app.db import Base
from app.db.models import TaxpayerData, LegacyData, AuditLog  # Importando os modelos

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# Função para inicializar o banco de dados
async def init_db(drop: bool = False) -> None:
    """
    Cria (e opcionalmente recria) todas as tabelas no banco de dados.
    Parâmetro:
    - drop (bool): Se True, apagará todas as tabelas existentes antes de criar novas. Use com cautela!

    """

    try:
        if drop:
            logger.warning("DROP solicitado — apagando todas as tabelas…")
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)

        logger.info("Criando tabelas no banco de dados…")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Tabelas criadas com sucesso!")

    except Exception as e:
        logger.error("Erro ao inicializar o banco de dados.")
        logger.exception(e)

if __name__ == "__main__":
    # Altere para drop=True se quiser limpar o banco antes
    import asyncio
    asyncio.run(init_db(drop=False))
