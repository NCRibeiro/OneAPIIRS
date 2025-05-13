# app/services/__init__.py
"""
Módulo de inicialização dos serviços do APE Project.

Este pacote contém serviços internos que encapsulam regras de negócio,
transformações de dados legados, análises modernas e integrações externas.
"""

# Importação de serviços internos
from .transformer import cobol_to_json, transform_legacy_to_modern
from .auditor import run_audit

# Importação de serviços externos simulados
from .external.federal_services import (
    validate_cpf_externally,
    fetch_income_score,
    check_debts,
)

__all__ = [
    # Serviços internos
    "cobol_to_json",
    "transform_legacy_to_modern",
    "run_audit",
    # Serviços externos
    "validate_cpf_externally",
    "fetch_income_score",
    "check_debts",
]
