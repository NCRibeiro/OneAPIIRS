"""
Módulo de inicialização dos serviços do APE Project.

Este pacote contém serviços internos que encapsulam regras de negócio,
transformações de dados legados, análises modernas e integrações externas.
"""

# Importa os serviços principais
from .transformer import cobol_to_json, transform_legacy_to_modern
from .auditor import run_audit

# Importa os serviços externos simulados
from app.services.external.federal_services import (
    validate_cpf_externally,
    fetch_income_score,
    check_debts
)

__all__ = [
    "cobol_to_json",
    "transform_legacy_to_modern",
    "run_audit",
    "validate_cpf_externally",
    "fetch_income_score",
    "check_debts"
]
