# app/routers/analytics.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.settings import settings
from app.dependencies import get_db, get_current_user
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
    prefix=f"{settings.api_prefix}/analytics",
    tags=["Analytics"],
    dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/summary",
    response_model=AnalyticsSummary,
    status_code=status.HTTP_200_OK,
    summary="Resumo analítico geral",
)
async def analytics_summary(
    db: AsyncSession = Depends(get_db),
) -> AnalyticsSummary:
    """Retorna métricas agregadas (totais, médias, etc.)."""
    return await generate_summary(db)


@router.get(
    "/by-month",
    response_model=MonthlyBreakdown,
    status_code=status.HTTP_200_OK,
    summary="Distribuição mensal",
)
async def analytics_by_month(
    db: AsyncSession = Depends(get_db),
) -> MonthlyBreakdown:
    """Retorna distribuição de valores por mês/ imposto."""
    return await get_monthly_distribution(db)


@router.get(
    "/errors",
    response_model=AuditErrorList,
    status_code=status.HTTP_200_OK,
    summary="Erros / Inconsistências de auditoria",
)
async def analytics_errors(
    db: AsyncSession = Depends(get_db),
) -> AuditErrorList:
    """Lista transações marcadas com inconsistência ou falha de auditoria."""
    return await list_audit_errors(db)
