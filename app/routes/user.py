from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from core.logging_config import get_logger
from core.settings import settings
from dependencies import get_current_user
from app.db.session import get_db

from passlib.context import CryptContext

logger = get_logger("user")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix=f"{settings.API_PREFIX}/users",
    tags=["Usuários"],
    dependencies=[Depends(get_current_user)],
)


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Retorna os dados do usuário autenticado",
)
async def get_me(current_user: User = Depends(get_current_user)) -> UserResponse:
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas ou usuário não autenticado",
        )
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        full_name=getattr(current_user, "full_name", None),
        disabled=getattr(current_user, "disabled", False),
        role=getattr(current_user, "role", None),
        created_at=getattr(current_user, "created_at", None),
    )


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um novo usuário",
)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)) -> UserResponse:
    # Verifica username
    result = await db.execute(select(User).filter(User.username == user.username))
    if result.scalars().first():
        logger.warning(f"Username duplicado: {user.username}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nome de usuário já existe.",
        )

    # Verifica email
    result = await db.execute(select(User).filter(User.email == user.email))
    if result.scalars().first():
        logger.warning(f"E-mail duplicado: {user.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail já registrado.",
        )

    # Hash da senha
    hashed_password = pwd_context.hash(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        full_name=getattr(user, "full_name", None),
        disabled=getattr(user, "disabled", False),
        role=getattr(user, "role", None),
        created_at=None,  # O banco pode preencher automaticamente
        hashed_password=hashed_password,  # Ajuste para o nome correto do campo no seu modelo!
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    logger.info(f"Usuário '{user.username}' criado com sucesso.")

    return UserResponse(
        id=new_user.id,
        username=new_user.username,
        email=new_user.email,
        full_name=getattr(new_user, "full_name", None),
        disabled=getattr(new_user, "disabled", False),
        role=getattr(new_user, "role", None),
        created_at=getattr(new_user, "created_at", None),
    )
