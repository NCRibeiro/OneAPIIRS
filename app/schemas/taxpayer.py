# app/schemas/taxpayer.py

from pydantic import BaseModel, Field
from typing import List, Optional


class TaxpayerBase(BaseModel):
    name: str = Field(..., description="Nome completo do contribuinte")
    status: str = Field(..., description="Status cadastral do contribuinte")


class TaxpayerCreate(TaxpayerBase):
    birth_date: Optional[str] = Field(
        None, description="Data de nascimento no formato YYYY-MM-DD"
    )
    last_filing: Optional[str] = Field(
        None, description="Data da última declaração fiscal"
    )
    income: Optional[str] = Field(
        None, description="Renda anual declarada (ex: $45,000)"
    )


class TaxpayerRead(TaxpayerBase):
    id: int = Field(
        ...,
        description="Identificador único (geralmente incremental no banco)",
    )
    birth_date: str = Field(..., description="Data de nascimento no formato YYYY-MM-DD")
    last_filing: str = Field(..., description="Data da última declaração fiscal")
    income: str = Field(..., description="Renda anual declarada (ex: $45,000)")

    class Config:
        orm_mode = True


# Caso precise de resposta em lote:
class TaxpayerBatchResponse(BaseModel):
    id: int
    total: int = Field(..., description="Total de contribuintes retornados")
    timestamp: str = Field(..., description="Timestamp da resposta no formato ISO")
    taxpayers: List[TaxpayerRead]

    class Config:
        orm_mode = True
