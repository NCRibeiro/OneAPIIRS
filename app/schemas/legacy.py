# app/schemas/legacy.py

"""
OneAPIIRS — Esquemas de Registros Legados

Define modelos para payload de criação e leitura de registros legados.
"""

from datetime import datetime
from typing import List

from pydantic import BaseModel, Field, constr, validator


class LegacyBase(BaseModel):
    """
    Campos básicos compartilhados entre criação e leitura de registros legados.
    """

    name: str = Field(
        ...,
        example="João Silva",
        description="Nome completo do contribuinte",
    )
    cpf: constr(min_length=14, max_length=14) = Field(
        ...,
        example="123.456.789-10",
        description="CPF no formato XXX.XXX.XXX-XX",
        pattern=r"^\d{3}\.\d{3}\.\d{3}-\d{2}$",
    )
    gross_income: float = Field(
        ..., example=75000.50, ge=0, description="Renda bruta declarada"
    )
    tax_paid: float = Field(..., example=15000.75, ge=0, description="Imposto pago")
    raw_line: str = Field(
        ..., example="00001ABCD1234", description="Linha original do registro COBOL"
    )
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(datetime.timezone.utc),
        example=datetime(2025, 5, 6, 14, 28, 41, tzinfo=datetime.timezone.utc),
        description="Data/hora (UTC) de criação no sistema legado",
    )

    @validator("timestamp", pre=True)
    def ensure_utc(cls, v):
        if v.tzinfo is None:
            return v.replace(tzinfo=datetime.timezone.utc)
        return v

    def __str__(self) -> str:
        return (
            f"Name: {self.name},"
            f"CPF: {self.cpf},"
            f"Gross Income: {self.gross_income},"
            f"Tax Paid: {self.tax_paid},"
            f"Raw Line: {self.raw_line},"
            f"Timestamp: {self.timestamp.isoformat()}"
        )

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "João Silva",
                "cpf": "123.456.789-10",
                "gross_income": 75000.50,
                "tax_paid": 15000.75,
                "raw_line": "00001ABCD1234",
                "timestamp": "2025-05-06T14:28:41Z",
            }
        }


class LegacyCreate(LegacyBase):
    """Payload para criação de um novo registro legado."""

    pass


class LegacyUpdate(LegacyBase):
    """Payload para atualização de um registro legado (inclui ID)."""

    id: int = Field(
        ...,
        example=1,
        description="ID do registro legado",
    )


class LegacyEntry(LegacyBase):
    """Modelo de leitura de registro legado (inclui ID)."""

    id: int = Field(
        ...,
        example=1,
        description="ID do registro legado",
    )


class LegacyResponse(BaseModel):
    id: str = Field(
        ...,
        example="f47ac10b-58cc-4372-a567-0e02b2c3d479",
        description="UUID de rastreamento da resposta",
    )
    timestamp: datetime = Field(
        ...,
        example="2025-05-06T14:30:00Z",
        description="Timestamp UTC da resposta",
    )
    record: LegacyEntry = Field(
        ...,
        description="Registro legado retornado",
    )

    class Config:
        orm_mode = True


class LegacyBatchResponse(BaseModel):
    id: str = Field(
        ...,
        example="batch-9f8a7b6c",
        description="UUID de rastreamento da resposta em lote",
    )
    timestamp: datetime = Field(
        ...,
        example="2025-05-06T14:35:00Z",
        description="Timestamp UTC da resposta em lote",
    )
    total: int = Field(
        ...,
        example=3,
        description="Total de registros legados retornados",
    )
    records: List[LegacyEntry] = Field(
        ...,
        description="Lista de registros legados",
    )

    class Config:
        orm_mode = True


__all__ = [
    "LegacyBase",
    "LegacyCreate",
    "LegacyUpdate",
    "LegacyEntry",
    "LegacyResponse",
    "LegacyBatchResponse",
]
