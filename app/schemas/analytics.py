# app/schemas/analytics.py

from typing import List

from pydantic import BaseModel, Field


class AnalyticsSummary(BaseModel):
    total_taxpayers: int = Field(
        ..., description="Número total de contribuintes cadastrados"
    )
    total_legacy_records: int = Field(
        ..., description="Número total de registros legados processados"
    )
    total_modern_records: int = Field(
        ..., description="Número total de registros modernizados"
    )

    error_rate_percent: float = Field(
        ..., description="Percentual de erros/inconsistências detectadas"
    )


class MonthlyRecord(BaseModel):
    month: str = Field(..., description="Mês no formato AAAA-MM")
    count: int = Field(..., description="Quantidade de registros no mês")


class MonthlyBreakdown(BaseModel):
    records_by_month: List[MonthlyRecord] = Field(
        ..., description="Lista de contagens mensais"
    )


class AuditError(BaseModel):
    taxpayer_id: int = Field(..., description="ID do contribuinte com erro")
    issue: str = Field(..., description="Descrição do problema detectado")


class AuditErrorList(BaseModel):
    errors: List[AuditError] = Field(
        ..., description="Lista de erros/inconsistências de auditoria"
    )
