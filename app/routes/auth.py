# app/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from datetime import datetime, timedelta as _tdelta

# Removed unused import of settings
from core.logging_config import get_logger
from dependencies import get_current_user
from app.schemas.auth import Token

# Removed duplicate import of get_logger
import secrets
import uuid
from fastapi.responses import JSONResponse

# Add your existing settings code here


class LocalSettings:
    def __init__(self):
        # Existing attributes
        self.api_prefix = "/api"  # Define the api_prefix attribute
        # with a default value


# Add your existing settings code here


class Settings:
    # Existing attributes
    secret_key: str = "your_secret_key_here"  # Add the secret_key attribute
    algorithm: str = "HS256"  # Ensure algorithm is also defined
    access_token_expires: _tdelta = _tdelta(minutes=30)  # Example value


settings = Settings()


# Create an instance of the LocalSettings class
local_settings = LocalSettings()

router = APIRouter(prefix=f"{local_settings.api_prefix}/auth", tags=["Auth"])

logger = get_logger("auth")

# ─── Autenticação (fake users) ──────────────────
fake_users_db = {
    "bytequeen": {
        "username": "bytequeen",
        "full_name": "Nívea C. Ribeiro",
        "password": "Lumi2025",
    }
}

# ─── Funções auxiliares ───────────────────────────


def authenticate_user(username: str, password: str):
    user = fake_users_db.get(username)
    if not user or user.get("password") != password:
        return None
    return user


def create_access_token(data: dict, expires_delta: _tdelta | None = None):
    to_encode = data.copy()
    to_encode["sid"] = str(uuid.uuid4())
    expire = datetime.utcnow() + (expires_delta or settings.access_token_expires)

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def generate_csrf_token():
    return secrets.token_urlsafe(32)


# ─── Rota de login ───────────────────────────────
@router.post(
    "/token",
    response_model=Token,
    summary="Obter access token via credenciais de usuário",
)
def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):

    # Autentica usuário
    user = authenticate_user(form_data.username, form_data.password)

    if not user:
        logger.warning(f"Tentativa de login falha: '{form_data.username}'")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    logger.info(f"Usuário '{form_data.username}' autenticado com sucesso.")

    # Gera JWT
    expires = settings.access_token_expires
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=expires
    )

    # Gera CSRF token
    csrf_token = generate_csrf_token()
    response.set_cookie(key="csrf_token", value=csrf_token, httponly=True)

    # Retorna resposta no formato de dicionário
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "csrf_token": csrf_token,
        "message": (
            f"Bem-vinda, {user['full_name']}! Token válido por "
            f"{settings.access_token_expires.total_seconds() // 60} min."
        ),
    }


# ─── Rota de logout ──────────────────────────────
@router.post(
    "/logout",
    summary="Logout e remoção do cookie CSRF",
    dependencies=[Depends(get_current_user)],
)
async def logout(response: Response):
    response.delete_cookie(key="csrf_token")
    return JSONResponse(
        {"message": "Logout efetuado com sucesso."}, status_code=status.HTTP_200_OK
    )
