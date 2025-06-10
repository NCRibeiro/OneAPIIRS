from datetime import date, datetime
from typing import List, Annotated
from pydantic import BaseModel, Field

# =====================
# 🏛️ Modelos Legados
# =====================


class LegacyBase(BaseModel):
    """Campos básicos compartilhados entre criação e leitura de registros legados."""

    name: Annotated[str, Field(example="João Silva", description="Nome completo do contribuinte")]
    cpf: Annotated[str, Field(
        example="123.456.789-10",
        min_length=11,
        max_length=14,
        description="CPF no formato XXX.XXX.XXX-XX",
        pattern=r"^\d{3}\.\d{3}\.\d{3}-\d{2}$"
    )]
    birth_date: Annotated[date, Field(example="1990-01-01", description="Data de nascimento do contribuinte")]
    gross_income: Annotated[float, Field(example=75000.50, ge=0, description="Renda bruta declarada")]
    tax_paid: Annotated[float, Field(example=15000.75, ge=0, description="Imposto pago")]
    raw_line: Annotated[str, Field(example="00001ABCD1234", description="Linha original do registro COBOL")]
    timestamp: Annotated[datetime, Field(default_factory=datetime.utcnow, example="2025-05-06T14:28:41Z", description="Timestamp de criação")]

    model_config = {"from_attributes": True}


class LegacyCreate(LegacyBase):
    """Payload para criação de um novo registro legado."""


class LegacyUpdate(LegacyBase):
    """Payload para atualização de um registro legado."""

    id: Annotated[int, Field(example=1, description="ID do registro legado")]


class LegacyEntry(LegacyBase):
    """Modelo de leitura de registro legado."""

    id: Annotated[int, Field(example=1, description="ID do registro legado")]


class LegacyResponse(BaseModel):
    """Resposta detalhada de um único registro legado."""

    id: Annotated[str, Field(example="uuid-response-123")]
    timestamp: Annotated[datetime, Field(example="2025-05-06T14:30:00Z")]
    record: LegacyEntry

    model_config = {"from_attributes": True}


class LegacyBatchResponse(BaseModel):
    """Resposta com múltiplos registros legados e metadados."""

    id: Annotated[str, Field(example="batch-uuid-123")]
    timestamp: Annotated[datetime, Field(example="2025-05-06T14:35:00Z")]
    total: Annotated[int, Field(example=3)]
    records: List[LegacyEntry]

    model_config = {"from_attributes": True}


# ================================
# 🚀 Modelo Moderno (Pós-ETL)
# ================================

class ModernRead(BaseModel):
    """Modelo moderno após transformação dos dados legados."""

    full_name: Annotated[str, Field(example="João Silva", description="Nome completo")]
    cpf: Annotated[str, Field(example="123.456.789-10", description="CPF formatado")]
    birth_date: Annotated[date, Field(example="1990-01-01", description="Data de nascimento")]
    income: Annotated[float, Field(example=75000.50, description="Renda bruta")]
    taxes: Annotated[float, Field(example=15000.75, description="Impostos pagos")]
    status: Annotated[str, Field(example="Ativo", description="Status do contribuinte")]
    timestamp: Annotated[datetime, Field(default_factory=datetime.utcnow, example="2025-05-06T14:28:41Z", description="Timestamp de transformação")]

    model_config = {"from_attributes": True}


class ModernEntry(BaseModel):
    id: str
    full_name: str
    cpf: str
    birth_date: date
    income: float
    taxes: float
    status: str
    timestamp: datetime


class ModernBatchResponse(BaseModel):
    id: str
    timestamp: datetime
    total: int
    records: List[ModernEntry] = []
    errors: List[str] = []
    warnings: List[str] = []

    model_config = {"from_attributes": True}


class ModernCreate(BaseModel):
    name: Annotated[str, ...]
    cpf: Annotated[str, ...]
    income: Annotated[float, Field(...)]
    full_name: Annotated[str, ...]
    birth_date: Annotated[date, Field(...)]
    status: Annotated[str, Field(...)]
    timestamp: Annotated[datetime, Field(...)]
    submitted_at: Annotated[datetime, Field(default_factory=datetime.utcnow)]


class ModernResponse(BaseModel):
    id: Annotated[int, ...]
    status: Annotated[str, ...]
    timestamp: datetime

    model_config = {"from_attributes": True}


# ======================
# 🔗 Exportação dos modelos
# ======================

__all__ = [
    "LegacyBase",
    "LegacyCreate",
    "LegacyUpdate",
    "LegacyEntry",
    "LegacyResponse",
    "LegacyBatchResponse",
    "ModernRead",
    "ModernEntry",
    "ModernBatchResponse",
    "ModernCreate",
    "ModernResponse",
]
