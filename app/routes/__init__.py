# app/routes/__init__.py
"""
Módulo central de roteamento para a API OneAPIIRS.
Agrega todas as rotas da aplicação com possibilidade de controle de versões.
"""

from fastapi import APIRouter

from app.routes import (audit, auth, external, legacy, modern_routes, taxpayer,
                        transform, user)
from core.settings import settings

from .analytics import router as analytics_router
from .audit import router as audit_router
# Importação dos routers de cada módulo
from .auth import router as auth_router
from .external import router as external_router
from .legacy import router as legacy_router
from .modern_routes import router as modern_router
from .taxpayer import router as taxpayer_router
from .transform import router as transform_router
from .user import router as user_router

# Roteador principal da API com prefixo versionado
api_router = APIRouter(prefix=settings.api_prefix)

# Registro dos routers
api_router.include_router(auth_router)
api_router.include_router(audit_router)
api_router.include_router(external_router)
api_router.include_router(modern_router)
api_router.include_router(legacy_router)
api_router.include_router(taxpayer_router)
api_router.include_router(transform_router)
api_router.include_router(analytics_router)
api_router.include_router(user_router)

__all__ = ["api_router"]

__title__ = "OneAPIIRS — APE Project"
__author__ = "Nívea C. Ribeiro"
__license__ = "MIT"
__copyright__ = "Copyright 2023 Nívea C. Ribeiro"
__url__ = "https://github.com/NCRibeiro"
__version_info__ = (2, 0, 0)
__version__ = ".".join(map(str, __version_info__))
__release__ = __version__
__status__ = "Development"
__maintainer__ = "Nívea C. Ribeiro"
__email__ = "contato@nivea.dev"
__github_username__ = "NCRibeiro"
__description__ = __doc__
__long_description__ = __doc__
__long_description_content_type__ = "text/markdown"
__package_name__ = "ape"
__module_name__ = "core"
