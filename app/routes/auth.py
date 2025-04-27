from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from datetime import datetime, timedelta
from app.core.config import settings
import uuid
from pydantic import BaseModel
from app.core.logging_config import get_logger
import secrets
from fastapi.responses import JSONResponse

# Criando o logger
logger = get_logger()

# Funções para CSRF
def generate_csrf_token():
    # Gera um token CSRF aleatório de 32 caracteres
    return secrets.token_urlsafe(32)

# Exemplo de modelo de dados
class User(BaseModel):
    username: str

router = APIRouter(tags=["Auth"])

fake_users_db = {
    "bytequeen": {
        "username": "bytequeen",
        "full_name": "Nívea C. Ribeiro",
        "password": "Lumi"
    }
}

# Função de autenticação
def authenticate_user(username: str, password: str):
    user = fake_users_db.get(username)
    if not user or user["password"] != password:
        return None
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    to_encode["sid"] = str(uuid.uuid4())  # ID de sessão
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

# Rota de login
@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), response: Response = None):
    user = authenticate_user(form_data.username, form_data.password)
    
    if not user:
        logger.warning(f"Tentativa de login falha: Usuário '{form_data.username}' não encontrado ou senha incorreta.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    logger.info(f"Usuário '{form_data.username}' logado com sucesso.")  # Registro de login bem-sucedido
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )

    csrf_token = generate_csrf_token()  # Gerar o CSRF Token
    response.set_cookie(key="csrf_token", value=csrf_token, httponly=True)  # Definir o cookie CSRF no frontend
    
    logger.info(f"Token gerado para o usuário '{form_data.username}' com validade de {settings.access_token_expire_minutes} minutos.")
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "csrf_token": csrf_token,  # Retorna o token CSRF para o frontend
        "message": f"Bem-vinda, {user['full_name']}. Seu token é válido por {settings.access_token_expire_minutes} minutos."
    }

