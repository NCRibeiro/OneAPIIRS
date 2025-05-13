import logging
from datetime import datetime
from typing import Dict

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from core.settings import settings

# ── Logger ───────────────────────────────────────────────────────────
logger = logging.getLogger("security")
logging.basicConfig(level=logging.INFO)

# ── OAuth2 Esquema ───────────────────────────────────────────────────
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)  # ou DEBUG se quiser mais verbosidade

# ── Exceção padrão ───────────────────────────────────────────────────
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Não autorizado. Token inválido ou expirado.",
    headers={"WWW-Authenticate": "Bearer"},
)

# ── Decodificação do JWT ─────────────────────────────────────────────


def decode_jwt_token(token: str) -> Dict:
    """
    Decodifica e valida um token JWT.
    Lança exceção se estiver expirado, malformado ou inválido.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            # Ensure this matches the attribute in settings
            algorithms=[
                settings.algorithms[0]  # Ensure 'algorithms' is defined
                # in settings
                # and use the first one
            ],  # Ensure 'algorithm' is defined in settings
            audience="oneapiirs",
        )
        logger.info(f"[SECURITY] Token decodificado: {payload}")

        # Validações adicionais (opcional, mas recomendado)
        if payload.get("exp", 0) < datetime.utcnow().timestamp():
            logger.warning("[SECURITY] Token expirado")
            raise credentials_exception

        return payload

    except JWTError as e:
        logger.warning(f"[SECURITY] Falha ao decodificar JWT: {e}")
        raise credentials_exception


# ── Funções de dependência ───────────────────────────────────────────
def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    """
    Extrai o usuário (sub) do token JWT, se válido.
    """
    sub = decode_jwt_token(token).get("sub")
    if not isinstance(sub, str) or not sub:
        raise credentials_exception
    return sub


def get_current_session(token: str = Depends(oauth2_scheme)) -> str:
    """
    Extrai o ID da sessão (sid) do token JWT, se válido.
    """
    sid = decode_jwt_token(token).get("sid")
    if not isinstance(sid, str) or not sid:
        raise credentials_exception
    return sid


def get_user_payload(token: str = Depends(oauth2_scheme)) -> Dict:
    """
    Retorna o payload completo do JWT.
    Útil para acessos administrativos ou logs completos.
    """
    return decode_jwt_token(token)


# ── Exportações públicas ─────────────────────────────────────────────
__all__ = [
    "oauth2_scheme",
    "credentials_exception",
    "decode_jwt_token",
    "get_current_user",
    "get_current_session",
    "get_user_payload",
]
