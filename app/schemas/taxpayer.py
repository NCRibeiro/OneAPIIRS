from pydantic import BaseModel, Field
from typing import List

class Taxpayer(BaseModel):
    id: str = Field(..., description="Identificador único (geralmente CPF ou código)")
    name: str = Field(..., description="Nome completo do contribuinte")
    birth_date: str = Field(..., description="Data de nascimento no formato YYYY-MM-DD")
    status: str = Field(..., description="Status cadastral do contribuinte")
    last_filing: str = Field(..., description="Data da última declaração fiscal")
    income: str = Field(..., description="Renda anual declarada (ex: $45,000)")

class TaxpayerBatchResponse(BaseModel):
    id: str
    total: int
    timestamp: str
    taxpayers: List[Taxpayer]

    class Config:
        orm_mode = True


        