from fastapi import APIRouter, HTTPException, Depends, status
from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.user import UserResponse
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from app.core.logging_config import get_logger  # Importando o logger


# Criando o logger
logger = get_logger()

router = APIRouter()

# Model de criação de usuário
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

# Rota para obter o usuário logado
@router.get("/me", response_model=UserResponse, tags=["Usuário"])
def get_me(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas ou usuário não autenticado"
        )
    
    return current_user

# Rota para criação de usuário
@router.post("/create_user", response_model=UserResponse, tags=["Usuário"])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Verificar se o nome de usuário já existe
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        logger.warning(f"Tentativa de criação de usuário com nome '{user.username}' já existente.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nome de usuário já existe."
        )

    # Verificar se o email já está registrado
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        logger.warning(f"Tentativa de criação de usuário com e-mail '{user.email}' já registrado.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail já registrado."
        )

    # Criação do novo usuário
    new_user = User(
        username=user.username,
        email=user.email,
        password=user.password  # A senha aqui deve ser tratada de forma segura (hashing)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    logger.info(f"Usuário '{user.username}' criado com sucesso.")
    
    return new_user
