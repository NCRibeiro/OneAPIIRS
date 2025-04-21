from pydantic import BaseModel, Field
from typing import Optional

class Token(BaseModel):
    access_token: str = Field(..., description="JWT token de acesso")
    token_type: str = Field(..., description="Tipo de token (geralmente 'bearer')")
    expires_in: Optional[int] = Field(1800, description="Tempo de expiração em segundos (padrão 30 min)")
    refresh_token: Optional[str] = Field(None, description="JWT token de atualização (opcional)")
    refresh_expires_in: Optional[int] = Field(None, description="Tempo de expiração do refresh token (opcional)")


    