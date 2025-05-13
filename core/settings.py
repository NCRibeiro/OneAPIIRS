# app/core/settings.py
"""
OneAPIIRS — Configurações Globais

Define todas as variáveis de ambiente e metadados da aplicação.
Usa `config_env.py` para injeção manual de variáveis.
"""
import config_env  # noqa: F401 (popula variáveis em os.environ)
from datetime import timedelta
from typing import List, Optional

# Pydantic v2: BaseSettings movido para pydantic-settings
from pydantic_settings import BaseSettings
from pydantic import validator, AnyHttpUrl


class Settings(BaseSettings):
    # ────────── Segurança • JWT ──────────
    SECRET_KEY: str
    REFRESH_SECRET_KEY: str
    # Ensure this matches the attribute in settings
    JWT_ALGORITHM: str = "HS256"
    algorithms = [JWT_ALGORITHM]  # Use the attribute defined in the class
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 1440

    # ────────── Banco de Dados ──────────
    DATABASE_URL: str

    # ────────── Execução / Ambiente ──────────
    APP_ENV: str = "development"
    DEBUG: bool = False
    RELOAD: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 1
    WORKER_CLASS: str = "uvicorn.workers.UvicornWorker"

    # ────────── FastAPI • Metadados ──────────
    API_PREFIX: str = "/api/v1"
    API_TITLE: str = "OneAPIIRS — APE Project"
    API_DESCRIPTION: str = (
        "API unificadora para integração com sistemas legados do IRS."
    )
    API_VERSION: str = "v1"
    API_DOCS_URL: Optional[str] = "/docs"
    API_REDOC_URL: Optional[str] = "/redoc"
    API_OPENAPI_URL: Optional[str] = "/openapi.json"
    ENABLE_DOCS: bool = True

    # ────────── CORS ──────────
    CORS_ORIGINS: List[AnyHttpUrl] = []

    # ────────── Logging ──────────
    LOG_LEVEL: str = "info"

    @property
    def access_token_expires(self) -> timedelta:
        return timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)

    @property
    def refresh_token_expires(self) -> timedelta:
        return timedelta(minutes=self.REFRESH_TOKEN_EXPIRE_MINUTES)

    @validator("DATABASE_URL", pre=True, always=True)
    def validate_db_url(cls, v):
        if not v:
            raise ValueError("DATABASE_URL não configurado")
        return v

    @validator("CORS_ORIGINS", pre=True)
    def split_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    class Config:
        env_prefix = "ONEAPIIRS_"
        env_file = None  # não carrega .env
        case_sensitive = True


# Instância global de configurações
settings = Settings(
    SECRET_KEY="your-secret-key",
    REFRESH_SECRET_KEY="your-refresh-secret-key",
    DATABASE_URL="your-database-url",
)
# settings.validate()

__all__ = [
    "settings",
]
__version__ = "1.0.0"
__author__ = "Nívea C. Ribeiro"
__license__ = "MIT"
__copyright__ = "Copyright 2023 Nívea C. Ribeiro"
__url__ = "https://github.com/NCRibeiro"
__description__ = "OneAPIIRS — Configurações Globais"
__long_description__ = __doc__
__long_description_content_type__ = "text/markdown"
__maintainer__ = "Nívea C. Ribeiro"
__email__ = "contato@nivea.dev"
__github_username__ = "NCRibeiro"
__status__ = "Development"
__title__ = "OneAPIIRS — APE Project"
