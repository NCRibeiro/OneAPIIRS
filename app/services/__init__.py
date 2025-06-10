"""
Serviços internos e externos do APE Project.

Este módulo reúne transformações de dados, auditorias fiscais
e integrações simuladas com serviços federais.
"""

# ───── Serviços Internos ─────
from app.services.transformer import (
    cobol_to_json,
    transform_legacy_to_modern,
)

from app.services.auditor import run_audit  # ← Importação explícita e direta

# ───── Serviços Externos Simulados ─────
from app.services.external.federal_services import (
    validate_cpf_externally,
    fetch_income_score,
    check_debts,
)

__all__ = [
    # Internos
    "cobol_to_json",
    "transform_legacy_to_modern",
    "run_audit",

    # Externos simulados
    "validate_cpf_externally",
    "fetch_income_score",
    "check_debts",
]
