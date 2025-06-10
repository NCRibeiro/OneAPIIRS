from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.taxpayer import Taxpayer
from app.schemas.taxpayer import TaxpayerCreate, TaxpayerRead
from core.settings import settings
from dependencies import get_current_user
from app.db.session import get_db

router = APIRouter(
    prefix=f"{settings.API_PREFIX}/taxpayers",
    tags=["Taxpayers"],
    dependencies=[Depends(get_current_user)],
)

NOT_FOUND_MSG = "Taxpayer not found"


@router.post("/", response_model=TaxpayerRead, status_code=status.HTTP_201_CREATED)
async def create_taxpayer(
    taxpayer: TaxpayerCreate,
    db: AsyncSession = Depends(get_db),
) -> Taxpayer:
    new_tp = Taxpayer(**taxpayer.model_dump())
    db.add(new_tp)
    await db.commit()
    await db.refresh(new_tp)
    return new_tp


@router.get("/", response_model=list[TaxpayerRead])
async def list_taxpayers(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
) -> list[Taxpayer]:
    result = await db.execute(
        select(Taxpayer).offset(skip).limit(limit),
    )
    return list(
        result.scalars().all()
    )


@router.get("/{taxpayer_id}", response_model=TaxpayerRead)
async def get_taxpayer(
    taxpayer_id: int,
    db: AsyncSession = Depends(get_db),
) -> Taxpayer:
    result = await db.execute(select(Taxpayer).filter(Taxpayer.id == taxpayer_id))
    tp = result.scalars().first()
    if not tp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND_MSG)
    return tp


@router.put("/{taxpayer_id}", response_model=TaxpayerRead)
async def update_taxpayer(
    taxpayer_id: int,
    payload: TaxpayerCreate,
    db: AsyncSession = Depends(get_db),
) -> Taxpayer:
    result = await db.execute(select(Taxpayer).filter(Taxpayer.id == taxpayer_id))
    tp = result.scalars().first()
    if not tp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND_MSG)

    for field, value in payload.model_dump().items():
        setattr(tp, field, value)
    await db.commit()
    await db.refresh(tp)
    return tp


@router.delete("/{taxpayer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_taxpayer(
    taxpayer_id: int,
    db: AsyncSession = Depends(get_db),
) -> None:
    result = await db.execute(select(Taxpayer).filter(Taxpayer.id == taxpayer_id))
    tp = result.scalars().first()
    if not tp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND_MSG)

    await db.delete(tp)
    await db.commit()
    return None
