# app/schemas/auth.py

"""
OneAPIIRS — Esquemas de Autenticação

Define os modelos de dados para login e validação de tokens JWT.
"""

from pydantic import BaseModel, Field


class Token(BaseModel):
    """
    Representa o token JWT retornado no login.
    """

    access_token: str = Field(
        ...,  # required
        description="JWT de acesso ao sistema",
        json_schema_extra={
            "example": (
                "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
                "eyJzdWIiOiJ1c3VhcmlvMTIzIn0."
                "SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
            )
        },
    )
    token_type: str = Field(
        "bearer",
        description="Tipo de token (geralmente 'bearer')",
        json_schema_extra={"example": "bearer"},
    )
    csrf_token: str = Field(
        ...,  # required
        description="Token CSRF para proteção contra ataques",
        json_schema_extra={"example": "XyZ123AbCd"},
    )
    message: str = Field(
        "Login bem-sucedido!",
        description="Mensagem de confirmação de login",
        json_schema_extra={"example": "Login bem-sucedido!"},
    )


class TokenData(BaseModel):
    """
    Dados extraídos do token JWT.

    Usado para validação de autorização de rotas.
    """

    sub: str | None = Field(
        None,
        description="Identificador (username ou user_id)",
        json_schema_extra={"example": "usuario123"},
    )


__all__ = [
    "Token",
    "TokenData",
]
