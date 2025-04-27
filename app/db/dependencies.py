from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User  # Ajuste o modelo conforme sua estrutura
from app.db.session import async_session
from app.core.config import settings
from jose import jwt
from typing import Dict

# Dependência para obter uma sessão de banco de dados assíncrona
async def get_db() -> AsyncSession:
    db = async_session()  # Sessão assíncrona
    try:
        yield db
    finally:
        await db.close()  # Fechar a sessão de forma assíncrona

# Função para decodificar o token JWT
def decode_token(token: str) -> Dict:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
        )

# Dependência de autenticação de usuário com token JWT
async def get_current_user(
    token: str = Depends(decode_token), db: AsyncSession = Depends(get_db)
) -> User:
    # Verificar se o 'sub' existe no token (que é o username)
    if "sub" not in token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
        )

    # Obter o usuário associado ao token
    result = await db.execute(select(User).filter(User.username == token["sub"]))
    user = result.scalars().first()

    # Se o usuário não for encontrado
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não autenticado",
        )
    
    return user
