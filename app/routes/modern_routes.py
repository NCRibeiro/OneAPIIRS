from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Annotated, Generator

from app.models.modern import ModernRecord
from app.schemas.modern import ModernCreate, ModernEntry
from app.db.session import get_db as get_async_db

router = APIRouter(prefix="/modern", tags=["Modern"])

NOT_FOUND_MSG = "Modern record not found"


@router.post("/", response_model=ModernEntry, status_code=status.HTTP_201_CREATED)
async def create_modern_entry(
    entry: ModernCreate,
    db: Annotated[AsyncSession, Depends(get_async_db)]
) -> ModernEntry:
    db_entry = ModernRecord(
        full_name=entry.name,  # Use name from ModernCreate for full_name
        cpf=entry.cpf,
        income=entry.income,
        status="Pending",  # Default status for new modern records
    )
    db.add(db_entry)
    await db.commit()
    await db.refresh(db_entry)
    return ModernEntry.model_validate(db_entry)


@router.get("/", response_model=List[ModernEntry])
async def list_modern_entries(db: Annotated[AsyncSession, Depends(get_async_db)]) -> List[ModernEntry]:
    result = await db.execute(select(ModernRecord))
    return [
        ModernEntry.model_validate(entry)
        for entry in
        result.scalars().all()
    ]


@router.get("/{entry_id}", response_model=ModernEntry)
async def get_modern_entry(entry_id: int, db: Annotated[AsyncSession, Depends(get_async_db)]) -> ModernEntry:
    result = await db.execute(select(ModernRecord).filter(ModernRecord.id == entry_id))
    entry = result.scalars().first()
    if not entry:
        raise HTTPException(status_code=404, detail=NOT_FOUND_MSG)
    return ModernEntry.model_validate(entry)


@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_modern_entry(entry_id: int, db: Annotated[AsyncSession, Depends(get_async_db)]) -> None:
    result = await db.execute(select(ModernRecord).filter(ModernRecord.id == entry_id))
    entry = result.scalars().first()
    if not entry:
        raise HTTPException(status_code=404, detail=NOT_FOUND_MSG)
    await db.delete(entry)
    await db.commit()
