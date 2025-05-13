# app/schemas/user.py

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
    role: RoleEnum = Field(  # Fixed closing parenthesis alignment
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

    class Config:  # Fixed closing parenthesis alignment
        orm_mode = True


# Schema para uso interno (inclui senha criptografada)
class UserInDB(UserRead):
    hashed_password: str = Field(
        ..., description="Senha criptografada armazenada no banco"
    )
