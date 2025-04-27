import logging
from typing import Dict

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.core.config import settings

# ── Logger ───────────────────────────────────────────────────────────
logger = logging.getLogger("security")
logging.basicConfig(level=logging.INFO)

# ── OAuth2 Esquema ───────────────────────────────────────────────────
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) # ou DEBUG se quiser mais verbosidade

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
            settings.secret_key,
            algorithms=[settings.algorithm],
            audience="oneapiirs",  # Protege contra tokens emitidos para outros sistemas
        )

        if not payload.get("sub") or not payload.get("sid"):
            logger.warning("[SECURITY] Token sem sub ou sid")
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
    return decode_jwt_token(token).get("sub")

def get_current_session(token: str = Depends(oauth2_scheme)) -> str:
    """
    Extrai o ID da sessão (sid) do token JWT, se válido.
    """
    return decode_jwt_token(token).get("sid")

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
