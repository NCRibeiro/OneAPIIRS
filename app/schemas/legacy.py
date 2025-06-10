from datetime import datetime, timezone, date
from typing import Annotated, List

from pydantic import BaseModel, Field, field_validator


# ───── Base Schema ─────────────────────────────────────────
class LegacyBase(BaseModel):
    """Campos básicos compartilhados entre criação e leitura de registros legados."""

    name: Annotated[str, Field(description="Nome do contribuinte")]
    cpf: Annotated[
        str,
        Field(
            description="CPF no formato XXX.XXX.XXX-XX",
            pattern=r"^\d{3}\.\d{3}\.\d{3}-\d{2}$",
            min_length=11,
            max_length=14,
        ),
    ]
    birth_date: Annotated[date, Field(description="Data de nascimento")]
    gross_income: Annotated[float, Field(description="Renda bruta declarada", ge=0)]
    tax_paid: Annotated[float, Field(description="Imposto pago", ge=0)]
    raw_line: Annotated[str, Field(description="Linha original do registro COBOL")]
    timestamp: Annotated[
        datetime,
        Field(
            description="Data/hora (UTC) de criação no sistema legado",
            default_factory=lambda: datetime.now(timezone.utc),
            examples=["2025-05-06T14:28:41Z"],
        ),
    ]

    @field_validator("cpf", mode="before")
    @classmethod
    def normalize_cpf(cls, v: str) -> str:
        return v.strip().upper()

    @field_validator("timestamp", mode="before")
    @classmethod
    def ensure_utc(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v


# ───── Versões específicas ─────────────────────────────────────────

class LegacyCreate(LegacyBase):
    """Payload para criação de um novo registro legado."""


class LegacyUpdate(LegacyBase):
    """Payload para atualização de um registro legado."""
    id: Annotated[int, Field(description="ID do registro legado")]


class LegacyEntry(LegacyBase):
    """Modelo de leitura de registro legado."""
    id: Annotated[int, Field(description="ID do registro legado")]
    taxpayer_id: Annotated[int, Field(description="ID do contribuinte associado")]

    model_config = {"from_attributes": True}


# ───── Respostas com metadados ─────────────────────────────────────

class LegacyResponse(BaseModel):
    id: Annotated[str, Field(description="UUID de rastreamento da resposta")]
    timestamp: Annotated[datetime, Field(description="Timestamp UTC da resposta")]
    record: Annotated[LegacyEntry, Field(description="Registro legado retornado")]

    model_config = {"from_attributes": True}


class LegacyBatchResponse(BaseModel):
    id: Annotated[str, Field(description="UUID de rastreamento da resposta em lote")]
    timestamp: Annotated[datetime, Field(description="Timestamp da resposta")]
    total: Annotated[int, Field(description="Total de registros legados retornados")]
    records: List[LegacyEntry]

    model_config = {"from_attributes": True}


# ───── Exports ─────────────────────────────────────────

__all__ = [
    "LegacyBase",
    "LegacyCreate",
    "LegacyUpdate",
    "LegacyEntry",
    "LegacyResponse",
    "LegacyBatchResponse",
]
