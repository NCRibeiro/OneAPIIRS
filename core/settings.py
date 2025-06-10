import json
from dotenv import load_dotenv
from datetime import timedelta
from typing import List, Optional, Any
from functools import lru_cache

from pydantic import AnyHttpUrl, Field, field_validator, ValidationError, parse_obj_as
from pydantic_settings import BaseSettings, SettingsConfigDict

# Carrega variáveis de ambiente de .env
load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="ONEAPIIRS_",
        case_sensitive=True,
    )

    SECRET_KEY: str
    REFRESH_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 1440

    DATABASE_URL: str

    APP_ENV: str = "development"
    DEBUG: bool = False
    RELOAD: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 1
    WORKER_CLASS: str = "uvicorn.workers.UvicornWorker"

    API_PREFIX: str = "/api/v1"
    API_TITLE: str = "OneAPIIRS - APE Project"
    API_DESCRIPTION: str = (
        "API unificadora para integração com sistemas legados do IRS."
    )
    API_VERSION: str = "v1"
    API_DOCS_URL: Optional[str] = "/docs"
    API_REDOC_URL: Optional[str] = "/redoc"
    API_OPENAPI_URL: Optional[str] = "/openapi.json"
    ENABLE_DOCS: bool = True

    # CORS
    CORS_ORIGINS: List[AnyHttpUrl] = Field(default_factory=list)

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def _split_cors_origins(cls, v: Any) -> List[AnyHttpUrl]:
        """
        Converte string CSV, JSON-array, wildcard ou vazio em List[AnyHttpUrl].
        """
        if isinstance(v, str):
            text = v.strip()
            if not text or text == "*":
                return []
            if text.startswith("[") and text.endswith("]"):
                try:
                    items = json.loads(text)
                except json.JSONDecodeError:
                    items = [u.strip().strip('"') for u in text.strip("[]").split(",") if u.strip()]
            else:
                items = [u.strip().strip('"') for u in text.split(",") if u.strip()]
        elif isinstance(v, list):
            items = v
        else:
            return []

        try:
            # Usa o parse_obj_as para validar a lista inteira de URLs
            return parse_obj_as(List[AnyHttpUrl], items)
        except ValidationError as e:
            raise ValueError(f"Invalid URLs in CORS_ORIGINS: {e}")

    LOG_LEVEL: str = "info"
    LOG_FORMAT: str = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

    @property
    def access_token_expires(self) -> timedelta:
        return timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)

    @property
    def refresh_token_expires(self) -> timedelta:
        return timedelta(minutes=self.REFRESH_TOKEN_EXPIRE_MINUTES)


@lru_cache()
def get_settings() -> Settings:
    return Settings()


# Instância global
settings = get_settings()
