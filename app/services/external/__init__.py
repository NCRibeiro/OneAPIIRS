"""
Exporta serviços simulados de integração com sistemas federais externos.
"""

from .federal_services import (
    check_debts,
    fetch_income_score,
    validate_cpf_externally,
)

__all__ = [
    "validate_cpf_externally",
    "fetch_income_score",
    "check_debts",
]
