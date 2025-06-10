"""
analytics_service.py – Lógica de agregação para o módulo Analytics.
"""

from collections import defaultdict
from datetime import datetime
from typing import Annotated, DefaultDict

from app.schemas.analytics import (
    AnalyticsSummary,
    AuditError,
    AuditErrorList,
    MonthlyBreakdown,
    MonthlyRecord,
)

# Bancos simulados em memória
from app.services.database import (
    audit_log,
    legacy_db,
    modern_db,
    taxpayer_db,
)


def generate_summary() -> Annotated[AnalyticsSummary, ...]:
    """
    Calcula métricas globais do sistema:
    - Total de contribuintes
    - Registros legados e modernos
    - Taxa de erro (%)
    """

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


def get_monthly_distribution() -> Annotated[MonthlyBreakdown, ...]:
    """
    Agrupa registros legados por mês (AAAA-MM).
    Ignora registros com timestamp inválido ou ausente.
    """

    counts: DefaultDict[str, int] = defaultdict(int)

    for record in legacy_db:
        ts = getattr(record, "timestamp", None)
        if ts:
            try:
                parsed = datetime.fromisoformat(ts) if isinstance(ts, str) else ts
                month = parsed.strftime("%Y-%m")
                counts[month] += 1
            except Exception:
                continue  # Ignora timestamps inválidos

    monthly = [
        MonthlyRecord(month=m, count=c)
        for m, c in sorted(counts.items())
    ]

    return MonthlyBreakdown(records_by_month=monthly)


def list_audit_errors() -> Annotated[AuditErrorList, ...]:
    """
    Retorna todos os erros de auditoria registrados no sistema.
    Cada erro contém o contribuinte e a descrição da ação.
    """
    errors = [
        AuditError(taxpayer_id=e.taxpayer_id, issue=e.issue)
        for e in audit_log
    ]

    return AuditErrorList(errors=errors)
