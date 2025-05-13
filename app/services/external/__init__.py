"""
Serviços externos simulados para integrações federais.
"""

from .federal_services import (check_debts, fetch_income_score,
                               validate_cpf_externally)

__all__ = [
    "validate_cpf_externally",
    "fetch_income_score",
    "check_debts",
]
