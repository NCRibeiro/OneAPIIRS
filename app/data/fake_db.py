# app/data/fake_db.py
"""
Módulo de dados simulados: centraliza registros e metadados de
sistemas legados.
"""

from .legacy_mainframe import legacy_mainframe
from .legacy_x99 import legacy_x99
from typing import Dict, List, Any

# --------------------------------------------------
# Dados legados centralizados por sistema
# --------------------------------------------------
legacy_data: Dict[str, Dict[str, Any]] = {
    "mainframe-alpha": legacy_mainframe,
    "legacy-x99": legacy_x99,
}

# --------------------------------------------------
# Metadados para cada sistema legado
# --------------------------------------------------
legacy_metadata: Dict[str, Any] = {
    system: {
        "description": meta.get("description"),
        "origin": meta.get("origin"),
        "format": meta.get("format"),
        "records": len(legacy_data.get(system, {})),
    }
    for system, meta in {
        "mainframe-alpha": {
            "description": ("Sistema legado principal, rodando em COBOL desde 1982."),
            "origin": "Servidor Alpha 9000",
            "format": "COBOL-RAW",
        },
        "legacy-x99": {
            "description": (
                "Sistema paralelo experimental da Receita, " "legado moderno."
            ),
            "origin": "Storage Cloud S3 X99",
            "format": "TEXT-VINTAGE",
        },
    }.items()
}

# --------------------------------------------------
# Funções utilitárias de acesso aos dados
# --------------------------------------------------


def get_all_records() -> Dict[str, Dict[str, Any]]:
    """
    Retorna todos os registros de todos os sistemas legados.
    """
    return legacy_data


def get_records_by_system(system: str) -> Dict[str, Any]:
    """
    Retorna os registros de um sistema específico.

    Args:
        system: Nome do sistema legado.
    Returns:
        Dicionário de registros, ou vazio se não existir.
    """
    return legacy_data.get(system, {})


def get_supported_systems() -> List[str]:
    """
    Retorna a lista de sistemas legados disponíveis.
    """
    return list(legacy_data.keys())


def get_legacy_metadata(system: str) -> Dict[str, Any]:
    """
    Retorna os metadados de um sistema legado específico.

    Args:
        system: Nome do sistema legado.
    Raises:
        KeyError: Se o sistema não estiver registrado.
    """
    if system not in legacy_metadata:
        raise KeyError(f"Sistema legado '{system}' não encontrado.")
    return legacy_metadata[system]


def get_all_legacy_metadata() -> Dict[str, Any]:
    """
    Retorna os metadados de todos os sistemas legados.
    """
    return legacy_metadata


__all__ = [
    "legacy_data",
    "legacy_metadata",
    "get_all_records",
    "get_records_by_system",
    "get_supported_systems",
    "get_legacy_metadata",
    "get_all_legacy_metadata",
]
