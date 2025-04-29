from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    secret_key: str  # Chave secreta para assinatura do JWT
    algorithm: str  # Algoritmo usado para codificar o JWT (ex: HS256)
    access_token_expire_minutes: int  # Tempo de expiração do token de acesso (em minutos)

    class Config:
        env_file = ".env"  # Carregar as variáveis de ambiente do arquivo .env

# Instanciando o objeto de configurações
settings = Settings()

# Cache para as configurações
@lru_cache
def get_settings():
    return settings  # Retorna a instância de configurações

# Garantindo que a função de configurações seja usada globalmente
settings = get_settings()

