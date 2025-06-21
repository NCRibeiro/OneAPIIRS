from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class RoleEnum(str, Enum):
    admin = "admin"
    user = "user"
    auditor = "auditor"


class UserBase(BaseModel):
    username: str = Field(..., description="Nome de usuário único no sistema")
    email: Optional[EmailStr] = Field(None, description="E-mail do usuário")
    full_name: Optional[str] = Field(None, description="Nome completo do usuário")
    disabled: Optional[bool] = Field(False, description="Se o usuário está desativado")
    role: RoleEnum = Field(
        ...,
        description="Nível de acesso do usuário (admin, user, auditor)",
    )


class UserCreate(UserBase):
    password: str = Field(
        ..., description="Senha em texto puro (será criptografada no DB)"
    )


class UserRead(UserBase):
    id: int = Field(..., description="ID interno do usuário")
    created_at: datetime = Field(..., description="Data de criação do usuário")
    last_login: Optional[datetime] = Field(None, description="Último acesso do usuário")

    class Config:
        from_attributes = True


class UserInDB(UserRead):
    """
    Representação interna do usuário, com senha criptografada.
    Nunca deve ser exposta por rotas públicas.
    """
    hashed_password: str = Field(
        ..., description="Senha criptografada armazenada no banco"
    )


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    disabled: Optional[bool] = False
    role: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
