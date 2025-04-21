from fastapi import APIRouter
from datetime import datetime
import uuid
from typing import List

from app.schemas.legacy import LegacyEntry, LegacyResponse, LegacyBatchResponse

router = APIRouter(
    prefix="/legacy",
    tags=["Legacy"],
    responses={404: {"description": "Not found"}},
)

# Simulando um "banco de dados legado"
fake_legacy_db = [
    LegacyEntry(
        id=1,
        name="Joana Prado",
        cpf="123.456.789-00",
        income=4800.0,
        birth_date=datetime(1990, 5, 20)
    ),
    LegacyEntry(
        id=2,
        name="Carlos Silva",
        cpf="987.654.321-00",
        income=5200.0,
        birth_date=datetime(1985, 11, 3)
    ),
    LegacyEntry(
        id=3,
        name="Ana Lima",
        cpf="111.222.333-44",
        income=6100.0,
        birth_date=datetime(1978, 1, 15)
    ),
]

@router.get("/", response_model=LegacyBatchResponse)
async def get_legacy_data():
    return LegacyBatchResponse(
        id=str(uuid.uuid4()),
        timestamp=str(datetime.utcnow()),
        total=len(fake_legacy_db),
        records=fake_legacy_db
    )


@router.get("/{entry_id}", response_model=LegacyResponse)
async def get_legacy_entry(entry_id: int):
    entry = next((item for item in fake_legacy_db if item.id == entry_id), None)
    if not entry:
        return {"error": "Registro não encontrado"}
    return LegacyResponse(
        id=str(uuid.uuid4()),
        timestamp=str(datetime.utcnow()),
        record=entry
    )
