import secrets
import uuid
from datetime import datetime, timedelta as _tdelta, timezone
from typing import Optional, Any, cast

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt

from app.schemas.auth import Token
from core.logging_config import get_logger
from core.settings import settings
from dependencies import get_current_user

router = APIRouter(prefix=f"{settings.API_PREFIX}/auth", tags=["Auth"])

logger = get_logger("auth")

# ─── Autenticação (usuário mock para prototipagem) ─────
fake_users_db: dict[str, dict[str, str]] = {
    "bytequeen": {
        "username": "bytequeen",
        "full_name": "Nívea C. Ribeiro",
        "password": "Lumi2025",
    }
}


# ─── Funções auxiliares ───────────────────────────────
def authenticate_user(username: str, password: str) -> Optional[dict[str, str]]:
    user = fake_users_db.get(username)
    if not user or user.get("password") != password:
        return None
    return user


def create_access_token(
    data: dict[str, Any], expires_delta: Optional[_tdelta] = None
) -> str:  # Returning Any from function declared to return "str"
    to_encode = data.copy()
    to_encode["sid"] = str(uuid.uuid4())

    expire = datetime.now(timezone.utc) + (
        expires_delta or settings.access_token_expires
    )
    to_encode["exp"] = expire

    return cast(str, jwt.encode(
        to_encode,
        getattr(settings, "secret_key", "dev-secret"),
        algorithm=getattr(settings, "algorithm", "HS256")
    ))


def generate_csrf_token() -> str:
    return secrets.token_urlsafe(32)


# ─── Rota de login ────────────────────────────────────
@router.post(
    "/token",
    response_model=Token,
    summary="Obter access token via credenciais de usuário",
)
def login(
    response: Response, form_data: OAuth2PasswordRequestForm = Depends()
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)

    if not user:
        logger.warning(f"Tentativa de login falha: '{form_data.username}'")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    logger.info(f"Usuário '{form_data.username}' autenticado com sucesso.")

    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=settings.access_token_expires,
    )
    csrf_token = generate_csrf_token()
    response.set_cookie(key="csrf_token", value=csrf_token, httponly=True)

    return Token(
        access_token=access_token,
        token_type="bearer",
        csrf_token=csrf_token,
        message=(
            f"Bem-vinda, {user['full_name']}! Token válido por "
            f"{settings.access_token_expires.total_seconds() // 60} min."
        ),
    )


# ─── Rota de logout ───────────────────────────────────
@router.post(
    "/logout",
    summary="Logout e remoção do cookie CSRF",
    dependencies=[Depends(get_current_user)],
)
async def logout(response: Response) -> JSONResponse:
    response.delete_cookie(key="csrf_token")
    return JSONResponse(
        {"message": "Logout efetuado com sucesso."},
        status_code=status.HTTP_200_OK,
    )
