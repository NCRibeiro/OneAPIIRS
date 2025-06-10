from typing import List, Annotated
from pydantic import BaseModel, Field


class AnalyticsSummary(BaseModel):
    """Resumo geral dos dados processados e analisados."""
    total_taxpayers: Annotated[int, ...]
    total_legacy_records: Annotated[int, ...]
    total_modern_records: Annotated[int, ...]
    error_rate_percent: Annotated[float, ...]


class MonthlyRecord(BaseModel):
    month: Annotated[str, ...]
    count: Annotated[int, ...]


class MonthlyBreakdown(BaseModel):
    records_by_month: Annotated[List[MonthlyRecord], ...]


class AuditError(BaseModel):
    taxpayer_id: Annotated[int, ...]
    issue: Annotated[str, ...]


class AuditErrorList(BaseModel):
    errors: Annotated[List[AuditError], ...]


__all__ = [
    "AnalyticsSummary",
    "MonthlyRecord",
    "MonthlyBreakdown",
    "AuditError",
    "AuditErrorList",
]
