from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class SuspiciousRecord(BaseModel):
    id: str = Field(..., description="ID do contribuinte")
    name: str = Field(..., description="Nome do contribuinte")
    cpf: str = Field(..., description="CPF do contribuinte")
    reason: str = Field(..., description="Motivo da suspeita")


class AuditSummary(BaseModel):
    total_records: int
    suspicious_count: int
    timestamp: str


class AuditReport(BaseModel):
    summary: AuditSummary
    suspicious: List[SuspiciousRecord] = []