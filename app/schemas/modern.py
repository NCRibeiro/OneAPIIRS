from pydantic import BaseModel, Field, constr
from typing import List
from datetime import date

class ModernEntry(BaseModel):
    """
    Representa um contribuinte no sistema moderno.
    """
    id: int = Field(..., description="ID do contribuinte no sistema moderno")
    full_name: str = Field(..., description="Nome completo")
    ssn: constr(pattern=r"\d{3}-\d{2}-\d{4}") = Field(..., description="SSN no formato 000-00-0000")
    annual_income: float = Field(..., gt=0, description="Renda anual em dólares")
    birth_date: date = Field(..., description="Data de nascimento no formato YYYY-MM-DD")

class ModernResponse(BaseModel):
    id: str = Field(..., description="UUID de rastreamento da operação")
    timestamp: str = Field(..., description="Data e hora do processamento (UTC)")
    record: ModernEntry = Field(..., description="Registro moderno retornado")

class ModernBatchResponse(BaseModel):
    id: str = Field(..., description="UUID da operação em lote")
    timestamp: str = Field(..., description="Data e hora do processamento (UTC)")
    total: int = Field(..., description="Total de registros retornados")
    records: List[ModernEntry] = Field(..., description="Lista de registros modernos")
