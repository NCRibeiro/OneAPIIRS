"""
Módulo de bancos de dados simulados para o APE Project.
Mantém coleções em memória para taxpayers, registros legados,
registros modernizados e logs de auditoria.
"""

from datetime import datetime, timezone
from typing import List, Optional
from uuid import uuid4

from app.schemas.analytics import AuditError
from app.schemas.legacy import LegacyBatchResponse, LegacyEntry, LegacyResponse, LegacyCreate
from app.schemas import ModernBatchResponse, ModernCreate, ModernEntry, ModernRead, ModernResponse
from app.schemas.taxpayer import TaxpayerBatchResponse, TaxpayerCreate, TaxpayerRead


# ─── In-Memory Data Stores ───
taxpayer_db: List[TaxpayerRead] = []
legacy_db: List[LegacyEntry] = []
modern_db: List[ModernRead] = []
audit_log: List[AuditError] = []


# ─── Taxpayer Functions ───

def create_taxpayer(payload: TaxpayerCreate) -> TaxpayerRead:
    """Cria um novo registro de taxpayer na base em memória."""
    new_id = len(taxpayer_db) + 1
    taxpayer = TaxpayerRead(id=new_id, **payload.dict())
    taxpayer_db.append(taxpayer)
    return taxpayer


def list_taxpayers(skip: int = 0, limit: Optional[int] = None) -> TaxpayerBatchResponse:
    """Lista taxpayers com paginação opcional."""
    records = taxpayer_db[skip: skip + limit if limit else None]
    return TaxpayerBatchResponse(
        total=len(records),
        timestamp=datetime.now(timezone.utc),
        taxpayers=records,
        id=len(taxpayer_db)
    )


# ─── Legacy Functions ───

def create_legacy(payload: LegacyCreate) -> LegacyResponse:
    """Cria um novo registro legado."""
    entry = LegacyEntry(id=len(legacy_db) + 1, **payload.dict())
    legacy_db.append(entry)
    return LegacyResponse(
        id=str(uuid4()),
        timestamp=datetime.now(timezone.utc),
        record=entry,
    )


def list_legacy(skip: int = 0, limit: Optional[int] = None) -> LegacyBatchResponse:
    """Lista registros legados com paginação opcional."""
    records = legacy_db[skip: skip + limit if limit else None]
    return LegacyBatchResponse(
        id=str(uuid4()),
        timestamp=datetime.now(timezone.utc),
        total=len(records),
        records=records,
    )


# ─── Modern Functions ───

def create_modern(payload: ModernCreate) -> ModernResponse:
    """Cria um novo registro modernizado."""
    new_id = str(uuid4())
    record = ModernRead(id=new_id, **payload.dict())
    modern_db.append(record)
    return ModernResponse(
        id=new_id,
        timestamp=datetime.now(timezone.utc),
        status=record.status
    )


def list_modern(skip: int = 0, limit: Optional[int] = None) -> ModernBatchResponse:
    """Lista registros modernizados com paginação opcional."""
    records = modern_db[skip: skip + limit if limit else None]
    return ModernBatchResponse(
        id=str(uuid4()),
        timestamp=datetime.now(timezone.utc),
        total=len(records),
        records=[ModernEntry(**r.dict()) for r in records]
    )


# ─── Audit Log ───

def log_audit_error(error: AuditError) -> AuditError:
    """
    Registra um erro de auditoria.
    """

    audit_log.append(error)
    return error


# ─── Exportação ───

__all__ = [
    # DB Stores
    "taxpayer_db",
    "legacy_db",
    "modern_db",
    "audit_log",
    # Taxpayer
    "create_taxpayer",
    "list_taxpayers",
    # Legacy
    "create_legacy",
    "list_legacy",
    # Modern
    "create_modern",
    "list_modern",
    # Audit
    "log_audit_error",
]
