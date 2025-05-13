# app/schemas/external.py

from pydantic import BaseModel, Field
from typing import List


class ExternalCheckResult(BaseModel):
    cpf: str = Field(..., description="CPF consultado, no formato XXX.XXX.XXX-XX")
    is_valid: bool = Field(
        ..., description="Indica se o CPF é válido no sistema federal"
    )
    income_score: int = Field(..., description="Score financeiro retornado, de 0 a 100")
    has_debts: bool = Field(
        ..., description="True se há pendências financeiras registradas"
    )
    checked_at: str = Field(..., description="Timestamp UTC da consulta")


class SupportedBank(BaseModel):
    name: str = Field(..., description="Nome do banco")
    code: str = Field(..., description="Código identificador do banco")


class BanksResponse(BaseModel):
    banks: List[SupportedBank] = Field(..., description="Lista de bancos suportados")


class Config:
    schema_extra = {
        "example": {
            "banks": [
                {"name": "Bank of Mars", "code": "001"},
                {"name": "Lunar Savings", "code": "002"},
                {"name": "Intergalactic Credit Union", "code": "003"},
            ]
        }
    }
