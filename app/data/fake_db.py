from .legacy_mainframe import legacy_mainframe
from .legacy_x99 import legacy_x99
from typing import Dict, List

# Dados legados centralizados
legacy_data: Dict[str, Dict[str, dict]] = {
    "mainframe-alpha": legacy_mainframe,
    "legacy-x99": legacy_x99
}

# Descrição dos sistemas legados disponíveis
legacy_metadata = {
    "mainframe-alpha": {
        "description": "Sistema legado principal, rodando em COBOL desde 1982.",
        "origin": "Servidor Alpha 9000",
        "format": "COBOL-RAW",
        "records": len(legacy_mainframe)
    },
    "legacy-x99": {
        "description": "Sistema paralelo experimental da Receita, legado moderno.",
        "origin": "Storage Cloud S3 X99",
        "format": "TEXT-VINTAGE",
        "records": len(legacy_x99)
    }
}

# Funções utilitárias que simulam uma camada de dados
def get_all_records() -> Dict[str, Dict[str, dict]]:
    """Retorna todos os dados de todos os sistemas legados"""
    return legacy_data

def get_records_by_system(system: str) -> Dict[str, dict]:
    """Retorna os registros de um sistema específico, se existir"""
    return legacy_data.get(system, {})

def get_supported_systems() -> List[str]:
    """Retorna a lista de sistemas legados registrados"""
    return list(legacy_data.keys())

def get_legacy_metadata(system: str) -> dict:
    if system not in legacy_metadata:
        raise ValueError(f"Sistema legado '{system}' não encontrado.")
    return legacy_metadata[system]

    
