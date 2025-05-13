# app/schemas/audit.py

from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class SuspiciousRecord(BaseModel):
    id: str = Field(..., description="ID do registro suspeito (UUID)")
    taxpayer_id: int = Field(..., description="ID do contribuinte associado")
    name: str = Field(..., description="Nome do contribuinte")
    cpf: str = Field(..., description="CPF do contribuinte")
    reason: str = Field(..., description="Motivo da suspeita")


class AuditSummary(BaseModel):
    total_checked: int = Field(..., description="Total de registros verificados")

    suspicious_count: int = Field(
        ..., description="Quantidade de registros suspeitos encontrados"
    )

    audit_date: datetime = Field(
        ..., description="Data e hora em que a auditoria foi realizada (UTC)"
    )


class AuditReport(BaseModel):
    id: str = Field(..., description="Identificador único do relatório de auditoria")

    summary: AuditSummary = Field(..., description="Resumo da auditoria")

    suspicious: List[SuspiciousRecord] = Field(
        default_factory=list, description="Lista de registros suspeitos"
    )
