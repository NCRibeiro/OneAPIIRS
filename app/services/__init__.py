"""
Serviços internos e externos do APE Project.

Este módulo reúne transformações de dados, auditorias fiscais,
integrações simuladas com serviços federais e operações com Google Cloud.
"""

# ───── Serviços Internos ─────
from app.services.transformer import (
    cobol_to_json,
    transform_legacy_to_modern,
)

from app.services.auditor import run_audit

# ───── Serviços Externos Simulados ─────
from app.services.external.federal_services import (
    validate_cpf_externally,
    fetch_income_score,
    check_debts,
)

# ───── Integrações Google Cloud ─────
from app.services.pubsub_service import pubsub_message
from app.services.storage_service import upload_file
from app.services.bigquery_service import query_rows


__all__ = [
    # Internos
    "cobol_to_json",
    "transform_legacy_to_modern",
    "run_audit",

    # Externos simulados
    "validate_cpf_externally",
    "fetch_income_score",
    "check_debts",

    # Google Cloud
    "pubsub_message",
    "upload_file",
    "query_rows",
]
