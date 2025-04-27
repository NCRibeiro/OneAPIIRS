"""
analytics.py – Rotas de relatórios/insights fiscais (Fase 5)
"""

from fastapi import APIRouter, status
from app.services.analytics_service import (
    generate_summary,
    get_monthly_distribution,
    list_audit_errors,
)
from app.schemas.analytics import (
    AnalyticsSummary,
    MonthlyBreakdown,
    AuditErrorList,
)

router = APIRouter(
    prefix="/api/v1/analytics",
    tags=["Analytics"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/summary",
    response_model=AnalyticsSummary,
    status_code=status.HTTP_200_OK,
    summary="Resumo analítico geral",
)
def analytics_summary() -> AnalyticsSummary:
    """Retorna métricas agregadas (totais, médias, etc.)."""
    return generate_summary()


@router.get(
    "/by-month",
    response_model=MonthlyBreakdown,
    status_code=status.HTTP_200_OK,
    summary="Distribuição mensal",
)
def analytics_by_month() -> MonthlyBreakdown:
    """Retorna distribuição de valores por mês/ imposto."""
    return get_monthly_distribution()


@router.get(
    "/errors",
    response_model=AuditErrorList,
    status_code=status.HTTP_200_OK,
    summary="Erros / Inconsistências de auditoria",
)
def analytics_errors() -> AuditErrorList:
    """Lista transações marcadas com inconsistência ou falha de auditoria."""
    return list_audit_errors()
