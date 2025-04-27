"""
OneAPIIRS — APE Configurações Globais

API unificadora para integração com sistemas legados do IRS.
Transformação de dados estilo COBOL em JSON moderno.
Autenticação JWT, arquitetura escalável, pronta para nuvem.

Desenvolvido por Nívea C. Ribeiro — engenheira fullstack visionária.
"""

from datetime import timedelta
from typing import Literal, Optional

from pydantic import Field, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ───────────── Segurança • JWT ─────────────
    secret_key: str = Field(..., alias="ONEAPIIRS_SECRET_KEY")
    public_key: Optional[str] = Field(None, alias="ONEAPIIRS_PUBLIC_KEY")
    algorithm: str = Field("HS256", alias="ONEAPIIRS_ALGORITHM")
    access_token_expire_minutes: int = Field(30, alias="ONEAPIIRS_TOKEN_EXPIRE_MIN")

    # ───────────── Banco de Dados ──────────────
    database_url: str = Field(..., alias="DATABASE_URL")
    database_name: str = Field("ape_fiscal_db", alias="DATABASE_NAME")
    database_user: str = Field("postgres", alias="DATABASE_USER")
    database_password: str = Field("postgres", alias="DATABASE_PASSWORD")
    database_host: str = Field("db", alias="DATABASE_HOST")
    database_port: int = Field(5432, alias="DATABASE_PORT")
    database_driver: str = Field("postgresql", alias="DATABASE_DRIVER")

    # ───────────── Ambiente / Debug ────────────
    app_env: Literal["development", "staging", "production", "test"] = Field(
        "development", alias="APP_ENV"
    )
    debug: bool = Field(True, alias="DEBUG")
    testing: bool = Field(False, alias="TESTING")

    # ───────────── API / FastAPI ───────────────
    api_version: str = Field("v1", alias="API_VERSION")
    api_prefix: str = Field("/api/v1", alias="API_PREFIX")
    enable_docs: bool = Field(True, alias="ENABLE_DOCS")

    # ───────────── Helpers ─────────────────────
    @property
    def access_token_expire(self) -> timedelta:
        return timedelta(minutes=self.access_token_expire_minutes)

    # ───────────── Validações ──────────────────
    @validator("database_url", pre=True)
    def _db_url_must_be_postgres(cls, v: str) -> str:
        if not v.startswith("postgresql://"):
            raise ValueError("DATABASE_URL deve começar com 'postgresql://'")
        return v

    # ───────────── Configuração do Pydantic ─────
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

    # ───────────── Compatibilidade Legada ───────
    @property
    def API_PREFIX(self) -> str:  # noqa: N802
        return self.api_prefix


# ───────────── Instância Global ───────────────
settings = Settings()

# ───────────── Metadados do Projeto ───────────
__all__ = ["settings"]
__title__ = "OneAPIIRS — APE Project"
__author__ = "Nívea C. Ribeiro"
__license__ = "MIT"
__copyright__ = "Copyright 2023 Nívea C. Ribeiro"
__url__ = "https://github.com/NCRibeiro"
__version_info__ = (2, 0, 0)
__version__ = ".".join(map(str, __version_info__))
__release__ = __version__
__status__ = "Development"
__maintainer__ = "Nívea C. Ribeiro"
__email__ = "nc.chagasribeiro@gmail.com"
__github_username__ = "NCRibeiro"
__description__ = __doc__
__long_description__ = __doc__
__long_description_content_type__ = "text/markdown"
__package_name__ = "ape"
__module_name__ = "core"

