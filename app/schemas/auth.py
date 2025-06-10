"""
OneAPIIRS — Esquemas de Autenticação

Define os modelos de dados para login e validação de tokens JWT.
"""

from typing import Optional, Annotated
from pydantic import BaseModel, Field


class Token(BaseModel):
    """
    Representa o token JWT retornado no login.
    """

    access_token: Annotated[
        str,
        Field(
            description="JWT de acesso ao sistema",
            example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        )
    ]
    token_type: Annotated[
        str,
        Field(
            default="bearer",
            description="Tipo de token (geralmente 'bearer')",
            example="bearer"
        )
    ]
    csrf_token: Annotated[
        str,
        Field(
            description="Token CSRF para proteção contra ataques",
            example="XyZ123AbCd"
        )
    ]
    message: Annotated[
        str,
        Field(
            default="Login bem-sucedido!",
            description="Mensagem de confirmação de login",
            example="Login bem-sucedido!"
        )
    ]


class TokenData(BaseModel):
    """
    Dados extraídos do token JWT.
    Usado para validação de autorização de rotas.
    """

    sub: Annotated[
        Optional[str],
        Field(
            default=None,
            description="Identificador (username ou user_id)",
            example="usuario123"
        )
    ]


__all__ = [
    "Token",
    "TokenData",
]
