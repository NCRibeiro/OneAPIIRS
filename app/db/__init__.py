"""
Pacote ``app.db``

- Cria o engine e a fábrica de sessões.
- Expõe Base declarativa para os modelos.
- Fornece a dependência ``get_db`` para FastAPI.
"""

import logging
from app.db.session import async_session  # Usando o async_session assíncrono
from app.db.init_db import init_db
from app.db.models import Base
from app.db.dependencies import get_current_user

# Configuração de log
logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────
# Dependência FastAPI
# ─────────────────────────────────────────────
def get_db():
    """
    Provides a generator function to yield a database session for asynchronous operations.

    Yields:
        AsyncSession: An asynchronous database session.

    Ensures:
        The database session is properly closed after use.
    """
    db = async_session()  # Usando o async_session para sessões assíncronas
    logger.debug("Sessão de banco de dados aberta.")
    try:
        yield db
    finally:
        db.close()  # Fechar a sessão assíncrona ao final
        logger.debug("Sessão de banco de dados fechada.")

# ─────────────────────────────────────────────
# Exposição de módulos e variáveis
# ─────────────────────────────────────────────
__all__ = ["async_session", "init_db", "Base", "get_db"]

# ─────────────────────────────────────────────
# Metadados do pacote
# ─────────────────────────────────────────────
__version__ = "2.0.0"
__author__ = "Nívea C. Ribeiro"
__license__ = "MIT"
__copyright__ = "Copyright 2023 Nívea C. Ribeiro"
__url__ = "https://github.com/NCRibeiro"
__description__ = __doc__
__long_description__ = __doc__
__long_description_content_type__ = "text/markdown"
__maintainer__ = "Nívea C. Ribeiro"
__email__ = "contato@nivea.dev"
__github_username__ = "NCRibeiro"
__status__ = "Development"
__title__ = "OneAPIIRS — APE Project"
__package_name__ = "ape"
__module_name__ = "db"




