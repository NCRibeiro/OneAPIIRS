"""
Serviços externos simulados para integrações federais.
"""

from .federal_services import (
    validate_cpf_externally,
    fetch_income_score,
    check_debts,
)

__all__ = [
    "validate_cpf_externally",
    "fetch_income_score",
    "check_debts",
]
