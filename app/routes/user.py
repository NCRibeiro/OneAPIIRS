# app/routers/user.py

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.settings import settings
from app.dependencies import get_db, get_current_user
from app.db.models import User as UserModel
from app.schemas.user import UserCreate, UserResponse
from core.logging_config import get_logger

logger = get_logger("user")

router = APIRouter(
    prefix=f"{settings.api_prefix}/users",
    tags=["Usuários"],
    dependencies=[Depends(get_current_user)],
)


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Retorna os dados do usuário autenticado",
)
async def get_me(current_user: UserModel = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas ou usuário não autenticado",
        )

    return current_user


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um novo usuário",
)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Verifica username
    result = await db.execute(
        select(UserModel).filter(UserModel.username == user.username)
    )
    if result.scalars().first():
        logger.warning(f"Username duplicado: {user.username}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Nome de usuário já existe."
        )
    # Verifica email (linha longa)
    result = await db.execute(select(UserModel).filter(UserModel.email == user.email))
    if result.scalars().first():
        logger.warning(f"E-mail duplicado: {user.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="E-mail já registrado."
        )

    new_user = UserModel(
        username=user.username,
        email=user.email,
        password=user.password,  # lembre-se de hash na model ou em service
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    logger.info(f"Usuário '{user.username}' criado com sucesso.")

    return new_user
