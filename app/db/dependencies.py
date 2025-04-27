from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import async_session
from app.models.user import User  # Ajuste o modelo conforme sua estrutura

# Dependência para obter uma sessão de banco de dados
async def get_db():
    db = async_session()  # Sessão assíncrona
    try:
        yield db
    finally:
        await db.close()  # Fechar a sessão de forma assíncrona

# Dependência de autenticação de usuário com token JWT
async def get_current_user(token: str = Depends(decode_token), db: AsyncSession = Depends(get_db)) -> User:
    result = await db.execute(select(User).filter(User.username == token["sub"]))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não autenticado",
        )
    return user
