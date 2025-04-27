# app/routes/audit.py

from fastapi import APIRouter, Depends
from datetime import datetime
from uuid import uuid4

# Importação de serviços e funções específicas
from app.services.auditor import run_audit
from app.core.security import get_current_user

# Importação dos schemas de auditoria
from app.schemas.audit import AuditReport, AuditSummary, SuspiciousRecord

# Inicialização do router
router = APIRouter(
    prefix="/audit",
    tags=["Auditoria Fiscal"]
)

@router.get("/", response_model=AuditReport)
async def audit_legacy_data(user: str = Depends(get_current_user)):
    """
    Executa uma auditoria nos dados legados para identificar registros suspeitos.

    A lógica atual detecta:
    - Renda negativa
    - CPF com formato inválido
    - Nome vazio ou ausente
    """
    # Executa a auditoria e obtém os resultados
    result = run_audit()

    # Retorna o relatório de auditoria com o resumo e os registros suspeitos
    return AuditReport(
        id=str(uuid4()),  # Gera um ID único para o relatório
        summary=AuditSummary(
            total_checked=result["total_checked"],  # Total de registros verificados
            suspicious_count=len(result["suspicious"]),  # Contagem de registros suspeitos
            audit_date=datetime.utcnow().isoformat()  # Data da auditoria
        ),
        suspicious=[  # Mapeia os registros suspeitos para os schemas definidos
            SuspiciousRecord(**record) for record in result["suspicious"]
        ]
    )