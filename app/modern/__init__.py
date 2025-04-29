# Importa as rotas do módulo moderno
from fastapi import APIRouter

# Importa as rotas definidas no arquivo modern_routes.py
from .modern_routes import router as modern_router

# Cria o APIRouter para o módulo moderno
router = APIRouter()

# Inclui as rotas do arquivo modern_routes.py no APIRouter principal
router.include_router(modern_router, prefix="/modern", tags=["modern"])
