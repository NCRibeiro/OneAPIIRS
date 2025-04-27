"""
OneAPIIRS — Módulo Principal do Projeto APE
"""

# ────── Imports padrão Python ──────
from datetime import datetime
import logging
import secrets

# ────── Imports FastAPI ──────
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from datetime import datetime
import logging

# ────── Imports locais ──────
from app.routes import router as api_router
from app.routers.auth import router as auth_router
from app.routers.taxpayer import router as taxpayer_router
from app.routers.legacy import router as legacy_router
from app.routers.transform import router as transform_router
from app.routers.analytics import router as analytics_router
from app.dependencies import get_db, get_current_user  # Importando o get_current_user para autenticação
from app.db.session import SessionLocal, engine
from app.db.models import Base
from app.db import init__db
from app.core.settings import settings

# ────── Variáveis de Ambiente ──────
from dotenv import load_dotenv
import sys
import os

load_dotenv()
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ────── Configuração do Logger ──────
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("APE")

# ────── Instância principal da aplicação ──────
app = FastAPI(
    title="OneAPIIRS — APE Project",
    description=(
        "API unificadora para integração com sistemas legados do IRS.\n"
        "Transformação de dados estilo COBOL em JSON moderno.\n"
        "Autenticação JWT, arquitetura escalável, pronta para nuvem.\n\n"
        "Desenvolvido por Nívea C. Ribeiro — engenheira fullstack visionária."
    ),
    version="2.0.0",
    contact={
        "name": "Nívea C. Ribeiro",
        "url": "https://github.com/NCRibeiro",
        "email": "contato@nivea.dev"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    },
    docs_url="/docs" if settings.ENABLE_DOCS else None,
    redoc_url="/redoc" if settings.ENABLE_DOCS else None
)

# ────── Middleware de CORS ──────
# Definição das configurações de CORS, permitindo todas as origens (ajuste conforme necessário)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos os domínios (ajuste conforme necessário)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# ────── Middleware de Segurança ──────
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"  # Impede que o navegador interprete o conteúdo como outro tipo
    response.headers["X-Frame-Options"] = "DENY"  # Impede que a aplicação seja carregada em frames (protege contra clickjacking)
    response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains"  # Força o uso de HTTPS
    return response

# ────── Middleware CSRF ──────
@app.middleware("http")
async def csrf_token_validation(request: Request, call_next):
    if request.method in ["POST", "PUT", "DELETE"]:
        csrf_token = request.headers.get("X-CSRF-Token")
        if not csrf_token or csrf_token != request.cookies.get("csrf_token"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="CSRF token inválido ou ausente."
            )
    response = await call_next(request)
    return response

# ────── Registro de Rotas ──────
app.include_router(auth_router)
app.include_router(taxpayer_router)
app.include_router(legacy_router)
app.include_router(transform_router)
app.include_router(analytics_router)

# ────── Rota Raiz (diagnóstico) ──────
@app.get("/", tags=["Root"])
async def get_root(current_user: Depends(get_current_user)):  # Dependência de autenticação global
    return {
        "status": "online",
        "project": "OneAPIIRS - APE",
        "version": app.version,
        "message": "APE está vivo. A integração do legado começou.",
        "modules": ["auth", "taxpayer", "legacy", "transform", "analytics"],
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        },
        "timestamp": datetime.utcnow().isoformat(),
        "user": current_user.username  # Exibindo o nome do usuário autenticado
    }

# ────── Tratamento Global de Erros ──────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"[ERRO] {request.url.path} → {exc}")
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Erro interno no servidor",
            "error": str(exc),
            "path": request.url.path
        }
    )

# ────── Eventos de Ciclo de Vida ──────
@app.on_event("startup")
async def on_startup():
    # Inicializa o banco de dados (cria as tabelas)
    logger.info("Iniciando a criação das tabelas no banco de dados...")
    try:
        init__db(drop=False)  # Se quiser limpar e recriar as tabelas, passe drop=True
        logger.info("Tabelas criadas com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao inicializar o banco de dados: {e}")
    
    logger.info("APE iniciado — Infraestrutura pronta para integração com legado.")

@app.on_event("shutdown")
async def on_shutdown():
    logger.info("APE encerrando — Obrigado por pilotar essa missão, Nívea.")
