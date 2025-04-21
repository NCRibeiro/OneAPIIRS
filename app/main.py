"""
OneAPIIRS — Módulo Principal do Projeto APE
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from datetime import datetime
import logging

from app.routes.auth import router as auth_router
from app.routes.taxpayer import router as taxpayer_router
from app.routes.legacy import router as legacy_router
from app.routes.transform import router as transform_router
from app.core.config import settings

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("APE")

# Instância principal da aplicação FastAPI
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

# Middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Inclusão de rotas
app.include_router(auth_router)
app.include_router(taxpayer_router)
app.include_router(legacy_router)
app.include_router(transform_router)

# Rota raiz (diagnóstico)
@app.get("/", tags=["Root"])
async def get_root():
    return {
        "status": "online",
        "project": "OneAPIIRS - APE",
        "version": app.version,
        "message": "APE está vivo. A integração do legado começou.",
        "modules": ["auth", "taxpayer", "legacy", "transform"],
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        },
        "timestamp": datetime.utcnow().isoformat()
    }

# Middleware de erro global
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

# Eventos de ciclo de vida
@app.on_event("startup")
async def on_startup():
    logger.info("APE iniciado — Infraestrutura pronta para integração com legado.")

@app.on_event("shutdown")
async def on_shutdown():
    logger.info("APE encerrando — Obrigado por pilotar essa missão, Nívea.")
