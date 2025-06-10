from datetime import datetime
from typing import List, Annotated
from pydantic import BaseModel, Field


class ExternalCheckResult(BaseModel):
    """Resposta da verificação externa de CPF e situação financeira."""

    cpf: Annotated[str, Field(example="123.456.789-00", description="CPF consultado")]
    is_valid: Annotated[bool, Field(description="True se o CPF é válido")]
    income_score: Annotated[int, Field(ge=0, le=100, description="Score financeiro (0–100)")]
    has_debts: Annotated[bool, Field(description="Indica se há dívidas registradas")]
    checked_at: Annotated[datetime, Field(example="2025-05-13T16:40:00Z", description="Data/hora da consulta")]


class SupportedBank(BaseModel):
    """Banco compatível com integração externa."""

    name: Annotated[str, Field(example="Bank of Mars", description="Nome do banco")]
    code: Annotated[str, Field(example="001", description="Código identificador")]


class BanksResponse(BaseModel):
    """Resposta contendo lista de bancos suportados."""

    banks: Annotated[List[SupportedBank], Field(description="Lista de bancos suportados")]

    model_config = {
        "json_schema_extra": {
            "example": {
                "banks": [
                    {"name": "Bank of Mars", "code": "001"},
                    {"name": "Lunar Savings", "code": "002"},
                    {"name": "Intergalactic Credit Union", "code": "003"},
                ]
            }
        }
    }


__all__ = [
    "ExternalCheckResult",
    "SupportedBank",
    "BanksResponse",
]
