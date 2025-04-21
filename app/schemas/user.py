from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum
from datetime import datetime

class RoleEnum(str, Enum):
    admin = "admin"
    user = "user"
    auditor = "auditor"

class User(BaseModel):
    username: str = Field(..., description="Nome de usuário único no sistema")
    email: Optional[EmailStr] = Field(None, description="E-mail do usuário")
    full_name: Optional[str] = Field(None, description="Nome completo")
    disabled: Optional[bool] = Field(False, description="Status de ativação do usuário")
    role: RoleEnum = Field(..., description="Nível de acesso do usuário (admin, user, auditor)")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Data de criação do usuário")
    last_login: Optional[datetime] = Field(None, description="Último acesso do usuário")

class UserInDB(User):
    password: str = Field(..., description="Senha criptografada do usuário")
