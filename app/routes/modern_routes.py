from fastapi import APIRouter
from datetime import datetime
from uuid import uuid4

from app.schemas.modern import ModernResponse, ModernBatchResponse, ModernEntry
from app.schemas.legacy import LegacyEntry
from app.services.transformer import transform_legacy_to_modern

router = APIRouter(
    prefix="/modern",
    tags=["Modern"],
    responses={404: {"description": "Not found"}},
)

modern_db = []  # Banco de dados fictício moderno

@router.post("/", response_model=ModernResponse)
def add_modern_entry(legacy_entry: LegacyEntry):
    modern_entry = transform_legacy_to_modern(legacy_entry)
    modern_db.append(modern_entry)
    return ModernResponse(
        id=str(uuid4()),
        timestamp=datetime.utcnow().isoformat(),
        record=modern_entry
    )

@router.get("/", response_model=ModernBatchResponse)
def list_modern_entries():
    return ModernBatchResponse(
        id=str(uuid4()),
        timestamp=datetime.utcnow().isoformat(),
        total=len(modern_db),
        records=modern_db
    )