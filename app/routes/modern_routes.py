# app/routers/modern.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.settings import settings  # Ensure this import is present

from dependencies import get_db, get_current_user

from app.db.models import ModernRecord as ModernModel, Taxpayer as TaxpayerModel
from app.schemas.modern import ModernCreate, ModernRead

router = APIRouter(
    prefix=f"{settings.api_prefix}/modern",
    tags=["Modern Records"],
    dependencies=[Depends(get_current_user)],
)


@router.post(
    "/",  # Adjusted to be within the character limit
    response_model=ModernRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_modern_record(
    payload: ModernCreate, db: AsyncSession = Depends(get_db)
):
    # Verifica se o contribuinte existe
    result = await db.execute(
        select(TaxpayerModel).filter(TaxpayerModel.id == payload.taxpayer_id)
    )
    taxpayer = result.scalars().first()
    if not taxpayer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Taxpayer not found"
        )
    new_record = ModernModel(**payload.dict())
    db.add(new_record)
    await db.commit()
    await db.refresh(new_record)
    return new_record


@router.get("/", response_model=list[ModernRead])
async def list_modern_records(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(ModernModel).offset(skip).limit(limit))
    return result.scalars().all()


@router.get("/{record_id}", response_model=ModernRead)
async def get_modern_record(record_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ModernModel).filter(ModernModel.id == record_id))
    record = result.scalars().first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Modern record not found"
        )
    return record


@router.put("/{record_id}", response_model=ModernRead)
async def update_modern_record(
    record_id: int, payload: ModernCreate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(ModernModel).filter(ModernModel.id == record_id))
    record = result.scalars().first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Modern record not found"
        )
    for field, value in payload.dict().items():
        setattr(record, field, value)
    await db.commit()
    await db.refresh(record)
    return record


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_modern_record(record_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ModernModel).filter(ModernModel.id == record_id))
    record = result.scalars().first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Modern record not found"
        )
    await db.delete(record)
    await db.commit()
    return {"detail": "Modern record deleted"}
    return record
