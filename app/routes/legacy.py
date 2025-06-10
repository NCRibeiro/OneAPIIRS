from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Annotated
from app.models.legacy import LegacyRecord as LegacyModel
from app.schemas.legacy import LegacyCreate, LegacyEntry
from app.db.session import get_db as get_async_db

router = APIRouter(prefix="/legacy", tags=["Legacy"])

"""
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
    yield db
    finally: db.close()
"""

NOT_FOUND_MSG = "Legacy record not found"


@router.post("/", response_model=LegacyEntry, status_code=status.HTTP_201_CREATED)
async def create_legacy_entry(
    entry: LegacyCreate, db: Annotated[AsyncSession, Depends(get_async_db)]
) -> LegacyModel:
    db_entry = LegacyModel(
        taxpayer_id=0,  # LegacyCreate does not have taxpayer_id, setting a default or requiring it in schema is needed
        name=entry.name,
        cpf=entry.cpf,
        birth_date=entry.birth_date,
        gross_income=entry.gross_income,
        timestamp=entry.timestamp,
    )
    db.add(db_entry)
    await db.commit()
    await db.refresh(db_entry)
    return db_entry


@router.get("/", response_model=List[LegacyEntry])
async def list_legacy_entries(
    db: Annotated[AsyncSession, Depends(get_async_db)]
) -> List[LegacyEntry]:
    result = await db.execute(select(LegacyModel))
    return [LegacyEntry.model_validate(entry) for entry in result.scalars().all()]


@router.get("/{entry_id}", response_model=LegacyEntry)
async def get_legacy_entry(
    entry_id: int, db: Annotated[AsyncSession, Depends(get_async_db)]
) -> LegacyEntry:
    result = await db.execute(select(LegacyModel).filter(LegacyModel.id == entry_id))
    entry = result.scalars().first()
    if not entry:
        raise HTTPException(status_code=404, detail=NOT_FOUND_MSG)
    return LegacyEntry.model_validate(entry)


@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_legacy_entry(
    entry_id: int, db: Annotated[AsyncSession, Depends(get_async_db)]
) -> None:
    result = await db.execute(select(LegacyModel).filter(LegacyModel.id == entry_id))
    entry = result.scalars().first()
    if not entry:
        raise HTTPException(status_code=404, detail=NOT_FOUND_MSG)
    await db.delete(entry)
