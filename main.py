from datetime import datetime, timezone
import time
from typing import Any, Callable, Awaitable
import os

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from app.db import init_db
from app.routes.api_router import api_router              # <-- Só este!
from core.logging_config import get_logger
from core.settings import settings, get_settings
from dependencies import get_current_user

# ─── Logger ─────────────────────────────────────
logger = get_logger("ape-api")
logger.setLevel(settings.LOG_LEVEL.upper())
logger.info("Configuração carregada com sucesso.")

# ─── Instância da Aplicação ─────────────────────
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION,
    openapi_url=f"{settings.API_PREFIX}{settings.API_OPENAPI_URL}",
    docs_url=f"{settings.API_PREFIX}{settings.API_DOCS_URL}" if settings.ENABLE_DOCS else None,
    redoc_url=f"{settings.API_PREFIX}{settings.API_REDOC_URL}" if settings.ENABLE_DOCS else None,
    debug=settings.DEBUG,
)

# Recarrega configurações atualizadas
settings = get_settings()

# Montagem de arquivos estáticos em /static (não sobrescreve root)
app.mount(
    "/static", StaticFiles(directory="static", html=True), name="static"
)

# Inclui o roteador principal sob o prefixo da API
app.include_router(api_router, prefix=settings.API_PREFIX)


# ─── Middleware CORS ────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Middleware: Tempo de Processamento ─────────
@app.middleware("http")
async def add_process_time_header(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    start = time.time()
    response = await call_next(request)
    response.headers["X-Process-Time"] = str(round(time.time() - start, 4))
    return response


# ─── Middleware: Headers de Segurança ───────────
@app.middleware("http")
async def add_security_headers(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    response = await call_next(request)
    response.headers.update({
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "Strict-Transport-Security": "max-age=63072000; includeSubDomains",
    })
    return response


# ─── Middleware: CSRF ───────────────────────────
@app.middleware("http")
async def csrf_token_validation(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    if request.method in ["POST", "PUT", "DELETE"]:
        token: str | None = request.headers.get("X-CSRF-Token")
        if not token or token != request.cookies.get("csrf_token"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="CSRF token inválido ou ausente.",
            )
    return await call_next(request)


# ─── Healthcheck ────────────────────────────────
@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    return {"status": "online"}


# Rota raiz simples para checks rápidos
@app.get("/", include_in_schema=False)
async def root_health() -> dict[str, str]:
    return {"status": "ok"}


# ─── Root Protegido ─────────────────────────────
@app.get(f"{settings.API_PREFIX}/", tags=["Root"])
async def get_root(current_user: Any = Depends(get_current_user)) -> dict[str, Any]:
    return {
        "status": "online",
        "project": "OneAPIIRS - APE",
        "version": app.version,
        "message": "APE está vivo. A integração do legado começou.",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "user": getattr(current_user, "username", None),
        "docs": {
            "swagger": f"{settings.API_PREFIX}{settings.API_DOCS_URL}",
            "redoc": f"{settings.API_PREFIX}{settings.API_REDOC_URL}",
        },
    }


# ─── Handler: Erros de Validação ────────────────
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    logger.error(f"[VALIDATION ERROR] {request.url.path} → {exc}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors(), "body": exc.body},
    )


# ─── Handler: Erros Globais ─────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(f"[ERRO] {request.url.path} → {exc}")
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error", "error": str(exc)},
    )


# ─── Evento: Startup ────────────────────────────
@app.on_event("startup")
async def on_startup() -> None:
    logger.info("APE iniciando...")
    if settings.APP_ENV == "development":
        try:
            await init_db(drop=False)
            logger.info("🗄️ Banco de dados pronto.")
        except Exception as e:
            logger.error(f"Erro ao inicializar DB: {e}")
            raise


# ─── Evento: Shutdown ───────────────────────────
@app.on_event("shutdown")
async def on_shutdown() -> None:
    logger.info("APE encerrando — Até breve!")


# ─── Execução Local ─────────────────────────────

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
