"""
analytics_service.py – Lógica de agregação para o módulo Analytics.
"""

from collections import defaultdict
from datetime import datetime

# Bancos simulados (dict ou list) já carregados em memória
from app.services.database import taxpayer_db, legacy_db, modern_db, audit_log


# Schemas de resposta
from app.schemas.analytics import (
    AnalyticsSummary,
    MonthlyBreakdown,
    MonthlyRecord,
    AuditError,
    AuditErrorList,
)

# ────────────────────────────────────────────────────────────────
# Funções de serviço
# ────────────────────────────────────────────────────────────────

def generate_summary() -> AnalyticsSummary:
    """Calcula métricas gerais do sistema."""
    total_taxpayers = len(taxpayer_db)
    total_legacy = len(legacy_db)
    total_modern = len(modern_db)
    total_errors = len(audit_log)

    error_rate = (total_errors / max(1, total_legacy)) * 100

    return AnalyticsSummary(
        total_taxpayers=total_taxpayers,
        total_legacy_records=total_legacy,
        total_modern_records=total_modern,
        error_rate_percent=round(error_rate, 2),
    )


def get_monthly_distribution() -> MonthlyBreakdown:
    """Conta registros modernos por mês (YYYY‑MM)."""
    monthly_counts: dict[str, int] = defaultdict(int)

    for record in modern_db:
        ts = record.get("timestamp") or record.get("created_at")
        if ts:
            month_key = datetime.fromisoformat(ts).strftime("%Y-%m")
            monthly_counts[month_key] += 1

    records = [
        MonthlyRecord(month=month, count=count)
        for month, count in sorted(monthly_counts.items())
    ]

    return MonthlyBreakdown(records_by_month=records)


def list_audit_errors() -> AuditErrorList:
    """Retorna lista de inconsistências detectadas na auditoria."""
    errors = [
        AuditError(taxpayer_id=entry["taxpayer_id"], issue=entry["issue"])
        for entry in audit_log
    ]
    return AuditErrorList(errors=errors)
