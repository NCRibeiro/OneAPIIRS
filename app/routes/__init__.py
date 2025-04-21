"""
Módulo central de roteamento para a API OneAPIIRS.
Agrega todas as rotas da aplicação com possibilidade de controle de versões.
"""

from fastapi import APIRouter
from app.core.config import settings

# Importação dos módulos de rota
from .auth import router as auth_router
from .taxpayer import router as taxpayer_router
from .legacy import router as legacy_router
from .transform import router as transform_router
from .modern_routes import router as modern_router

# Roteador principal da API
api_router = APIRouter(prefix=settings.API_PREFIX, tags=["API"])

# Inclusão de todas as rotas registradas
api_router.include_router(auth_router)
api_router.include_router(taxpayer_router)
api_router.include_router(legacy_router)
api_router.include_router(transform_router)
api_router.include_router(modern_router)


# Exportações públicas do pacote
__all__ = ["api_router"]

