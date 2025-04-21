from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.core.config import settings
from typing import Dict
import logging

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) # ou DEBUG se quiser mais verbosidade

# Exceção padrão de credenciais
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Não autorizado. Token inválido ou expirado.",
    headers={"WWW-Authenticate": "Bearer"},
)

def decode_jwt_token(token: str) -> Dict:
    """
    Decodifica um token JWT e valida campos essenciais.
    Levanta exceção se inválido, expirado ou malformado.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            audience="oneapiirs"  # Protege contra uso indevido entre sistemas
        )

        # Valida se o token tem 'sub' (usuário) e 'sid' (session)
        if not payload.get("sub") or not payload.get("sid"):
            raise credentials_exception

        return payload

    except JWTError as e:
        # Aqui poderíamos logar o erro real com traceback, se desejado
        logger.warning(f"[SECURITY] Token inválido: {e}")
        raise credentials_exception

def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    """
    Extrai o usuário (sub) do token JWT, se válido.
    """
    payload = decode_jwt_token(token)
    return payload.get("sub")

def get_current_session(token: str = Depends(oauth2_scheme)) -> str:
    """
    Extrai o ID da sessão atual a partir do token.
    """
    payload = decode_jwt_token(token)
    return payload.get("sid")

def get_user_payload(token: str = Depends(oauth2_scheme)) -> Dict:
    """
    Retorna o payload JWT completo para uso avançado.
    """
    return decode_jwt_token(token)

# Exportações públicas
__all__ = ["oauth2_scheme", "credentials_exception",
           "decode_jwt_token", "get_current_user", "get_current_session",
           "get_user_payload"]


