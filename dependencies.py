"""
Módulo de dependências e autenticação para o APE Project.
Define injeções de sessão, validação de tokens JWT e recuperação de usuários.
"""

from typing import Any, Dict

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.settings import settings
from app.db import get_db
from app.models import User

# Configuração do OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_PREFIX}/token")


class TokenData(BaseModel):
    """Dados extraídos do token JWT."""

    sub: str | None = None


def decode_token(token: str) -> Dict[str, Any]:
    """
    Decodifica um JWT e retorna o payload.
    Levanta HTTPException se o token for inválido ou expirado.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False},
        )
        return payload
    except JWTError:
        raise credentials_exception


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
) -> User:
    """
    Recupera o usuário atual a partir do token JWT.
    """
    payload = decode_token(token)
    username: str | None = payload.get("sub")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido: 'sub' não encontrado.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        result = await db.execute(select(User).where(User.username == username))
        user = result.scalars().first()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao consultar usuário: {e}",
        )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não autenticado.",
        )
    return user


async def verify_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Verifica se o usuário atual possui privilégios de administrador.
    """
    if not getattr(current_user, "is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado: requer privilégios de administrador.",
        )
    return current_user


__all__ = [
    "get_db",
    "oauth2_scheme",
    "TokenData",
    "decode_token",
    "get_current_user",
    "verify_admin_user",
]
