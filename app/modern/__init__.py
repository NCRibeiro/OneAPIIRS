# modern/__init__.py
"""
Pacote de rotas do módulo Modern.
Agrupa as rotas relacionadas ao sistema moderno.
"""

from fastapi import APIRouter

# Importa o roteador específico do módulo moderno
from .modern_routes import router as modern_router

# Roteador raiz do módulo moderno
router = APIRouter(
    prefix="/modern",
    tags=["modern"],
)

# Inclui todas as rotas definidas em modern_routes
router.include_router(
    modern_router,
    prefix="",
    tags=["modern"],
)

__all__ = ["router"]
