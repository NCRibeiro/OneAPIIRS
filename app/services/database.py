"""
Módulo de bancos de dados simulados para o APE Project.
Mantém coleções em memória para taxpayers, legacy records,
modern records e logs de auditoria.
"""

from typing import (
    List,
    Optional,
)  # Fixed: Split long line (import from typing)


from uuid import uuid4
from datetime import datetime

from app.schemas.taxpayer import TaxpayerCreate, TaxpayerRead, TaxpayerBatchResponse
from app.schemas.legacy import LegacyEntry, LegacyResponse, LegacyBatchResponse
from app.schemas.modern import (
    ModernCreate,
    ModernRead,
    ModernResponse,
    ModernBatchResponse,
)
from app.schemas.analytics import AuditError

# --------------------------------------------------
# Bancos de dados simulados em memória
# --------------------------------------------------
taxpayer_db: List[TaxpayerRead] = []
legacy_db: List[LegacyEntry] = []
modern_db: List[ModernRead] = []
audit_log: List[AuditError] = []

# --------------------------------------------------
# Taxpayer Functions
# --------------------------------------------------


def create_taxpayer(payload: TaxpayerCreate) -> TaxpayerRead:
    """
    Cria e armazena um novo contribuinte em memória.
    """
    new_id = len(taxpayer_db) + 1
    taxpayer = TaxpayerRead(id=new_id, **payload.dict())
    taxpayer_db.append(taxpayer)
    return taxpayer


def list_taxpayers(skip: int = 0, limit: Optional[int] = None) -> TaxpayerBatchResponse:
    """
    Recupera contribuintes cadastrados com paginação simples.
    """
    records = taxpayer_db[skip : skip + limit if limit else None]
    return TaxpayerBatchResponse(total=len(records), records=records)


# --------------------------------------------------
# Legacy Functions
# --------------------------------------------------


def create_legacy(payload: LegacyEntry) -> LegacyResponse:
    """
    Cria e armazena um registro legado em memória.
    """
    new_id = str(uuid4())
    payload.timestamp = payload.timestamp or datetime.utcnow()
    legacy_db.append(payload)
    return LegacyResponse(  # Fixed: Split long line
        id=new_id, timestamp=datetime.utcnow(), record=payload
    )


def list_legacy(skip: int = 0, limit: Optional[int] = None) -> LegacyBatchResponse:
    """
    Recupera registros legados com paginação simples.
    """
    records = legacy_db[skip : skip + limit if limit else None]
    return LegacyBatchResponse(
        id=str(uuid4()),
        timestamp=datetime.utcnow(),
        total=len(records),
        records=records,
    )


# --------------------------------------------------
# Modern Functions
# --------------------------------------------------


def create_modern(payload: ModernCreate) -> ModernResponse:
    """
    Cria e armazena um registro modernizado em memória.
    """
    new_id = str(uuid4())
    record = ModernRead(id=len(modern_db) + 1, **payload.dict())
    modern_db.append(record)
    return ModernResponse(id=new_id, timestamp=datetime.utcnow(), record=record)


def list_modern(skip: int = 0, limit: Optional[int] = None) -> ModernBatchResponse:
    """
    Recupera registros modernizados com paginação simples.
    """
    records = modern_db[skip : skip + limit if limit else None]
    return ModernBatchResponse(
        id=str(uuid4()),
        timestamp=datetime.utcnow(),
        total=len(records),
        records=records,
    )


# --------------------------------------------------
# Audit Log Functions
# --------------------------------------------------


def log_audit_error(error: AuditError) -> AuditError:
    """
    Adiciona um erro de auditoria ao log.
    """
    audit_log.append(error)
    return error


__all__ = [
    # Databases
    "taxpayer_db",
    "legacy_db",
    "modern_db",
    "audit_log",
    # Taxpayers
    "create_taxpayer",
    "list_taxpayers",
    # Legacy
    "create_legacy",
    "list_legacy",
    # Modern
    "create_modern",
    "list_modern",
    # Audit Log
    "log_audit_error",
    # "list_audit_errors",  # Removed: Function not in this module
]
