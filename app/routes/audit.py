from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.legacy import LegacyEntry
from app.models.legacy import LegacyRecord as LegacyModel
from app.services.auditor import run_audit
from dependencies import get_current_user
from app.db.session import get_db
from app.schemas.audit import AuditReport


router = APIRouter(
    prefix="/api/v1/audit",
    tags=["Auditoria Fiscal"],
    dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/",
    response_model=AuditReport,
    status_code=status.HTTP_200_OK,
    summary="Executa auditoria nos dados legados e retorna relatório",
)
async def audit_legacy_data(db: AsyncSession = Depends(get_db)) -> AuditReport:
    """
    Executa uma auditoria nos dados legados para identificar
    registros suspeitos.
    """
    result = await db.execute(select(LegacyModel))
    raw_data = result.scalars().all()

    # Converte modelo ORM → schema Pydantic
    legacy_entries = [LegacyEntry.model_validate(obj) for obj in raw_data]

    return run_audit(data=legacy_entries)
