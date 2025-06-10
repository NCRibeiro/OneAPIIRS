from datetime import datetime, date
from typing import List, Annotated
from pydantic import BaseModel, Field


class SuspiciousRecord(BaseModel):
    id: Annotated[str, ...]
    name: Annotated[str, ...]
    cpf: Annotated[str, ...]
    taxpayer_id: Annotated[int, ...]
    reason: Annotated[str, ...]


class AuditSummary(BaseModel):
    total_checked: Annotated[int, ...]
    suspicious_count: Annotated[int, ...]
    audit_date: Annotated[date, ...]


class AuditReport(BaseModel):
    id: Annotated[str, ...]
    total_records: Annotated[int, ...]
    total_suspect: Annotated[int, ...]
    suspicious: Annotated[List[SuspiciousRecord], ...]
    summary: Annotated[AuditSummary, ...]


class AuditError(BaseModel):
    taxpayer_id: Annotated[int, Field(description="ID do contribuinte com erro")]
    issue: Annotated[str, Field(description="Descrição resumida do erro")]


class AuditErrorList(BaseModel):
    errors: List[AuditError]


__all__ = [
    "SuspiciousRecord",
    "AuditSummary",
    "AuditReport",
    "AuditError",
    "AuditErrorList",
]
