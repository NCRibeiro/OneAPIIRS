# app/services/analytics_service.py
"""
analytics_service.py – Lógica de agregação para o módulo Analytics.
"""

from collections import defaultdict
from datetime import datetime

# Schemas de resposta
from app.schemas.analytics import (AnalyticsSummary, AuditError,
                                   AuditErrorList, MonthlyBreakdown,
                                   MonthlyRecord)

# Importação de bancos simulados em memória
from .database import audit_log, legacy_db, modern_db, taxpayer_db

# ────────────────────────────────────────────────────────────────
# Funções de serviço
# ────────────────────────────────────────────────────────────────


def generate_summary() -> AnalyticsSummary:
    """Calcula métricas gerais do sistema."""
    total_taxpayers = len(taxpayer_db)
    total_legacy = len(legacy_db)
    total_modern = len(modern_db)
    total_errors = len(audit_log)
    error_rate = (total_errors / total_legacy * 100) if total_legacy > 0 else 0.0

    return AnalyticsSummary(
        total_taxpayers=total_taxpayers,
        total_legacy_records=total_legacy,
        total_modern_records=total_modern,
        error_rate_percent=round(error_rate, 2),
    )


def get_monthly_distribution() -> MonthlyBreakdown:
    """Retorna distribuição de registros legados por mês."""
    counts = defaultdict(int)
    for record in legacy_db:
        # espera que cada registro tenha atributo 'timestamp'
        ts = getattr(record, "timestamp", None)
        if ts:
            month = (
                datetime.fromisoformat(ts).strftime("%Y-%m")
                if isinstance(ts, str)
                else ts.strftime("%Y-%m")
            )
            counts[month] += 1

    # Constrói lista ordenada
    monthly = [MonthlyRecord(month=m, count=c) for m, c in sorted(counts.items())]
    return MonthlyBreakdown(records_by_month=monthly)


def list_audit_errors() -> AuditErrorList:
    """Lista todos os erros de auditoria registrados."""
    errors = [AuditError(taxpayer_id=e.taxpayer_id, issue=e.action) for e in audit_log]
    return AuditErrorList(errors=errors)
