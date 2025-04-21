from datetime import timedelta
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # Segurança
    secret_key: str = Field("Lumi", alias="ONEAPIIRS_SECRET_KEY")
    algorithm: str = Field("HS256", alias="ONEAPIIRS_ALGORITHM")
    access_token_expire_minutes: int = Field(30, alias="ONEAPIIRS_TOKEN_EXPIRE_MIN")

    # Ambiente
    APP_ENV: str = "development"  # production | staging | test
    DEBUG: bool = True
    TESTING: bool = False

    # Info da API
    API_VERSION: str = "v1"
    API_PREFIX: str = "/api/v1"
    ENABLE_DOCS: bool = True

    @property
    def ACCESS_TOKEN_EXPIRE(self):
        return timedelta(minutes=self.access_token_expire_minutes)

    class Config:
        env_file = ".env"
        case_sensitive = True
        env_file_encoding = "utf-8"
        # Isso aqui é importante pra aceitar os aliases
        populate_by_name = True

# Instância global que será importada onde necessário
settings = Settings()
__all__ = ["settings"]
