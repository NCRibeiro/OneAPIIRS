"""
Módulo de dados simulados da OneAPIIRS (APE Project).

Esta pasta simula a estrutura de diferentes sistemas legados do IRS,
organizando dados de forma separada por origem e encapsulando acesso a esses
dados através de funções utilitárias que imitam uma camada de persistência.
"""

from .fake_db import (
    legacy_data,
    legacy_metadata,
    get_all_records,
    get_records_by_system,
    get_supported_systems,
    get_legacy_metadata
)

__all__ = [
    "get_all_records",
    "get_legacy_metadata",
    "get_records_by_system",
    "get_supported_systems",
    "legacy_data",
    "legacy_metadata"
]
