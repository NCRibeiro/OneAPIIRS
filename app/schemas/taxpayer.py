from datetime import date, datetime
from typing import Annotated, List, Optional
from pydantic import BaseModel, Field


class TaxpayerBase(BaseModel):
    """Campos comuns a todas as operações com contribuintes."""

    name: Annotated[str, Field(description="Nome completo do contribuinte")]
    status: Annotated[str, Field(description="Status cadastral do contribuinte")]


class TaxpayerCreate(TaxpayerBase):
    """Dados esperados ao criar um contribuinte."""

    birth_date: Annotated[Optional[date], Field(
        default=None, description="Data de nascimento no formato YYYY-MM-DD"
    )]
    last_filing: Annotated[Optional[date], Field(
        default=None, description="Data da última declaração fiscal"
    )]
    income: Annotated[Optional[float], Field(
        default=None, description="Renda anual declarada (em reais)"
    )]


class TaxpayerRead(TaxpayerBase):
    """Resposta completa de um contribuinte cadastrado."""

    id: Annotated[int, Field(description="Identificador único (ID no banco)")]
    birth_date: Annotated[date, Field(description="Data de nascimento")]
    last_filing: Annotated[date, Field(description="Data da última declaração fiscal")]
    income: Annotated[float, Field(description="Renda anual declarada (em reais)")]

    model_config = {"from_attributes": True}


class TaxpayerBatchResponse(BaseModel):
    """Resposta em lote com metadados da consulta."""

    id: int
    total: Annotated[int, Field(description="Total de contribuintes retornados")]
    timestamp: Annotated[datetime, Field(description="Data/hora da resposta no formato ISO")]
    taxpayers: List[TaxpayerRead]

    model_config = {"from_attributes": True}
