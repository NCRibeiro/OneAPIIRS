# app/routes/api_router.py

from fastapi import APIRouter
from core.settings import settings

# importe todos os seus módulos de rota
from app.routes import (
    auth,
    taxpayer,
    legacy,
    modern_routes,
    audit,
    external,
    analytics,
)

# roteador principal, já montado sob o prefixo de versão da API
api_router = APIRouter(prefix=settings.API_PREFIX)

# autenticação / login / tokens
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Auth"],
)

# rotas de contribuinte (taxpayer)
api_router.include_router(
    taxpayer.router,
    prefix="/taxpayer",
    tags=["Taxpayer"],
)

# rotas legadas (legacy)
api_router.include_router(
    legacy.router,
    prefix="/legacy",
    tags=["Legacy"],
)

# rotas modernas (modern_routes)
api_router.include_router(
    modern_routes.router,
    prefix="/modern",
    tags=["Modern"],
)

# auditoria fiscal (audit)
api_router.include_router(
    audit.router,
    prefix="/audit",
    tags=["Audit"],
)

# integrações externas (external)
api_router.include_router(
    external.router,
    prefix="/external",
    tags=["External"],
)

# análises e relatórios (analytics)
api_router.include_router(
    analytics.router,
    prefix="/analytics",
    tags=["Analytics"],
)
