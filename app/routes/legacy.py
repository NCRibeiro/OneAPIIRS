from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import LegacyData as LegacyModel
from app.db.models import TaxpayerData as TaxpayerModel
from app.schemas.legacy import LegacyCreate, LegacyEntry
from core.settings import settings
from dependencies import get_current_user, get_db

router = APIRouter(
    prefix=f"{settings.api_prefix}/legacy",
    tags=["Legacy Records"],
    dependencies=[Depends(get_current_user)],
)


@router.post("/", response_model=LegacyEntry, status_code=status.HTTP_201_CREATED)
async def create_legacy_record(
    payload: LegacyCreate,
    db: AsyncSession = Depends(get_db),
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
    new_record = LegacyModel(**payload.dict())
    db.add(new_record)
    await db.commit()
    await db.refresh(new_record)
    return new_record


@router.get("/", response_model=list[LegacyEntry])
async def list_legacy_records(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(LegacyModel).offset(skip).limit(limit),
    )
    return result.scalars().all()


@router.get("/{record_id}", response_model=LegacyEntry)
async def get_legacy_record(record_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(LegacyModel).filter(LegacyModel.id == record_id),
    )
    record = result.scalars().first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Legacy record not found"
        )
    return record


@router.put("/{record_id}", response_model=LegacyEntry)
async def update_legacy_record(
    record_id: int, payload: LegacyCreate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(LegacyModel).filter(LegacyModel.id == record_id),
    )
    record = result.scalars().first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Legacy record not found"
        )
    for field, value in payload.dict().items():
        setattr(record, field, value)
    await db.commit()
    await db.refresh(record)
    return record


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_legacy_record(record_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(LegacyModel).filter(LegacyModel.id == record_id),
    )
    record = result.scalars().first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Legacy record not found"
        )
    await db.delete(record)
    await db.commit()
    return {"detail": "Legacy record deleted"}
    return record
