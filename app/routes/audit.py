# app/routes/audit.py

from fastapi import APIRouter, Depends, status
from datetime import datetime
from uuid import uuid4

# Removed unused import of settings
from dependencies import get_current_user

# Removed redundant import of get_db
from app.services.auditor import run_audit

# Removed redundant import of get_current_user
from app.schemas.audit import AuditReport, AuditSummary, SuspiciousRecord


router = APIRouter(
    prefix="/api/audit",
    # Replace with a hardcoded prefix or the correct attribute
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
async def audit_legacy_data():
    """
    Executa uma auditoria nos dados legados para identificar
    registros suspeitos.

    A lógica atual detecta:
    - Renda negativa
    - CPF com formato inválido
    - Nome vazio ou ausente
    """
    result = await run_audit()
    return AuditReport(
        id=str(uuid4()),
        summary=AuditSummary(
            total_checked=result["total_checked"],
            suspicious_count=len(result["suspicious"]),
            audit_date=datetime.utcnow(),
        ),
        suspicious=[SuspiciousRecord(**record) for record in result["suspicious"]],
    )
