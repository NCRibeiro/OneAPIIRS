"""
Core package initialization for APE

Este módulo centraliza utilitários e singletons fundamentais que precisam ser
acessíveis em toda a aplicação, evitando importações circulares.

Somente componentes *essenciais* devem ser expostos aqui. Para funcionalidades
desacopladas, crie subpacotes específicos.
"""

from __future__ import annotations

import importlib.metadata as _metadata
import logging
import os
from pathlib import Path
from typing import Final

from core.settings import settings

# ───────────── Versão do Projeto ─────────────
try:
    __version__: str = _metadata.version("ape")
except _metadata.PackageNotFoundError:
    _default_version = "0.0.0"  # Default version if package not found
    __version__ = _default_version  # Reassignment is now allowed
    pass  # Ensures the except block is not empty

# ───────────── Ambiente ──────────────────────
ENV: Final[str] = os.getenv("APP_ENV", "development").lower()
PROJECT_ROOT: Final[Path] = Path(__file__).resolve().parent.parent

# ───────────── Logger Global ─────────────────
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler()],
    force=True,
)

logger: Final[logging.Logger] = logging.getLogger("ape.core")
logger.setLevel(logging.DEBUG)
logger.propagate = False

logger.info("Bootstrapping APE core (env=%s, version=%s)", ENV, __version__)
logger.debug("PROJECT_ROOT: %s", PROJECT_ROOT)
logger.debug("ENV: %s", ENV)

# ───────────── Exportações Públicas ──────────
__all__ = [
    "ENV",
    "PROJECT_ROOT",
    "logger",
    "settings",
]

# __version__ is already defined above as a Final variable.
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
__version__ = __version__  # Ensure __version__ is defined here
