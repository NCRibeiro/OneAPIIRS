"""
Core package initialization for APE

Este módulo centraliza utilitários e singletons fundamentais que precisam ser
acessíveis em toda a aplicação, evitando importações circulares.

Somente componentes *essenciais* devem ser expostos aqui. Para funcionalidades
desacopladas, crie subpacotes específicos.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Final

import importlib.metadata as _metadata
from app.core.settings import settings

# ───────────── Versão do Projeto ─────────────
try:
    __version__: Final[str] = _metadata.version("ape")
except _metadata.PackageNotFoundError:
    __version__ = "0.0.0-dev"

# ───────────── Ambiente ──────────────────────
ENV: Final[str] = os.getenv("APE_ENV", "development").lower()
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

__version__ = __version__
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
__module_name__ = "core"


