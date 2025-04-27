"""
Módulo central de roteamento para a API OneAPIIRS.
Agrega todas as rotas da aplicação com possibilidade de controle de versões.
"""

from fastapi import APIRouter
from app.routes import auth, audit, legacy, modern_routes, taxpayer, transform, external, user

# Roteador principal da API
# ------------------------------------------------------------------
api_router = APIRouter(prefix=settings.API_PREFIX, tags=["API"])

# ------------------------------------------------------------------
# Importação e registro das rotas
# (importar DEPOIS de criar api_router evita referências circulares)
# ------------------------------------------------------------------
from .auth import router as auth_router          # noqa: E402
from .taxpayer import router as taxpayer_router  # noqa: E402
from .legacy import router as legacy_router      # noqa: E402
from .transform import router as transform_router  # noqa: E402
from .modern_routes import router as modern_router  # noqa: E402
from .audit import router as audit_router        # noqa: E402
from .external import router as external_router  # noqa: E402
from .analytics import router as analytics_router  # noqa: E402

api_router.include_router(auth_router,     prefix="/auth",      tags=["auth"])
api_router.include_router(audit_router,    prefix="/audit",     tags=["audit"])
api_router.include_router(external_router, prefix="/external",  tags=["external"])
api_router.include_router(modern_router,   prefix="/modern",    tags=["modern"])
api_router.include_router(legacy_router,   prefix="/legacy",    tags=["legacy"])
api_router.include_router(taxpayer_router, prefix="/taxpayer",  tags=["taxpayer"])
api_router.include_router(transform_router, prefix="/transform", tags=["transform"])
api_router.include_router(analytics_router, prefix="/analytics", tags=["analytics"])
api_router.include_router(user.router, prefix="/users", tags=["users"])

__all__ = ["api_router"]

