# app/main.py
"""
OneAPIIRS — Módulo Principal do Projeto APE
"""

# 1) Injeta variáveis de ambiente (config_env.py deve popular os.environ)
import config_env  # noqa: F401

# 2) Importa e instancia configurações (settings.py)
from core.settings import settings

# 3) Importa e instancia o app FastAPI


from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
import time
from datetime import datetime
from app.routes import api_router
from dependencies import get_current_user
from core.logging_config import get_logger

# configura logger
logger = get_logger("ape-api")
logger.setLevel(settings.LOG_LEVEL.upper())
logger.info("Config carregada: %s", settings.dict())

# instancia FastAPI
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION,
    openapi_url=f"{settings.API_PREFIX}{settings.API_OPENAPI_URL}",
    docs_url=(
        f"{settings.API_PREFIX}{settings.API_DOCS_URL}"
        if settings.ENABLE_DOCS
        else None
    ),
    redoc_url=(
        f"{settings.API_PREFIX}{settings.API_REDOC_URL}"
        if settings.ENABLE_DOCS
        else None
    ),
    debug=settings.DEBUG,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# middlewares de headers


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    response.headers["X-Process-Time"] = str(time.time() - start)
    return response


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers.update(
        {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "Strict-Transport-Security": "max-age=63072000; includeSubDomains",
        }
    )
    return response


@app.middleware("http")
async def csrf_token_validation(request: Request, call_next):
    if request.method in ["POST", "PUT", "DELETE"]:
        token = request.headers.get("X-CSRF-Token")
        if not token or token != request.cookies.get("csrf_token"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="CSRF token inválido ou ausente.",
            )
    return await call_next(request)


# inclui todas as rotas com prefixo /api/v1
app.include_router(api_router, prefix=settings.API_PREFIX)

# rota raiz (health / info)


@app.get(f"{settings.API_PREFIX}/", tags=["Root"])
async def get_root(current_user=Depends(get_current_user)):
    return {
        "status": "online",
        "project": "OneAPIIRS - APE",
        "version": app.version,
        "message": "APE está vivo. A integração do legado começou.",
        "timestamp": datetime.utcnow().isoformat(),
        "user": getattr(current_user, "username", None),
        "docs": {
            "swagger": f"{settings.API_PREFIX}{settings.API_DOCS_URL}",
            "redoc": f"{settings.API_PREFIX}{settings.API_REDOC_URL}",
        },
    }


# tratadores de erro
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

    logger.error(f"[VALIDATION ERROR] {request.url.path} → {exc}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors(), "body": exc.body},
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"[ERRO] {request.url.path} → {exc}")
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Erro interno no servidor", "error": str(exc)},
    )


# eventos de startup/shutdown
@app.on_event("startup")
async def on_startup():
    logger.info("APE iniciando...")
    try:
        from app.db.init_db import init_db

        # init_db é síncrono; chama diretamente
        init_db(drop=False)
        logger.info("DB ready.")
    except Exception as e:
        logger.error(f"Erro ao inicializar DB: {e}")
        raise


@app.on_event("shutdown")
async def on_shutdown():
    logger.info("APE encerrando — Até a próxima!")


# execução direta
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.RELOAD
    )
