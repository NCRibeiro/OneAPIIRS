from pydantic import BaseModel, Field
from pydantic.types import constr
from typing import List
from datetime import datetime

class LegacyEntry(BaseModel):
    """
    Representa um registro de contribuinte em sistema legado.
    """
    id: int = Field(..., description="ID do contribuinte")
    name: str = Field(..., description="Nome completo")
    cpf: constr(pattern=r"\d{3}\.\d{3}\.\d{3}-\d{2}") = Field(
        ..., description="CPF no formato XXX.XXX.XXX-XX"
    )
    income: float = Field(..., description="Renda declarada")
    birth_date: datetime = Field(..., description="Data de nascimento do contribuinte")

# Exemplo de uso:
exemplo = LegacyEntry(
    id=1,
    name="Joana Prado",
    cpf="123.456.789-00",
    income=4800.0,
    birth_date=datetime(1990, 5, 20)
)

print(exemplo)

class LegacyResponse(BaseModel):
    """
    Resposta contendo um único registro legado.
    """
    id: str = Field(..., description="Identificador de rastreamento (UUID)")
    timestamp: str = Field(..., description="Data e hora da resposta (UTC)")
    record: LegacyEntry = Field(..., description="Registro legado retornado")

class LegacyBatchResponse(BaseModel):
    """
    Resposta contendo múltiplos registros legados.
    """
    id: str = Field(..., description="Identificador de rastreamento (UUID)")
    timestamp: str = Field(..., description="Data e hora da resposta (UTC)")
    total: int = Field(..., description="Total de registros retornados")
    records: List[LegacyEntry] = Field(..., description="Lista de registros legados")
