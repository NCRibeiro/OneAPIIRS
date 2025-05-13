# app/routers/taxpayer.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.models import Taxpayer as TaxpayerModel
from app.dependencies import get_current_user, get_db
from app.schemas.taxpayer import TaxpayerCreate, TaxpayerRead

router = APIRouter(prefix="/taxpayers", tags=["Taxpayers"])


@router.post(
    "/",
    response_model=TaxpayerRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_user)],
)
def create_taxpayer(
    taxpayer: TaxpayerCreate,
    db: Session = Depends(get_db),
):
    new_tp = TaxpayerModel(**taxpayer.dict())
    db.add(new_tp)
    db.commit()
    db.refresh(new_tp)
    return new_tp


@router.get(
    "/", response_model=list[TaxpayerRead], dependencies=[Depends(get_current_user)]
)
def list_taxpayers(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    return db.query(TaxpayerModel).offset(skip).limit(limit).all()


@router.get(
    "/{taxpayer_id}",
    response_model=TaxpayerRead,
    dependencies=[Depends(get_current_user)],
)
def get_taxpayer(
    taxpayer_id: int,
    db: Session = Depends(get_db),
):
    tp = db.query(TaxpayerModel).filter(TaxpayerModel.id == taxpayer_id).first()
    if not tp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Taxpayer not found"
        )
    return tp


@router.put(
    "/{taxpayer_id}",
    response_model=TaxpayerRead,
    dependencies=[Depends(get_current_user)],
)
def update_taxpayer(
    taxpayer_id: int,
    payload: TaxpayerCreate,
    db: Session = Depends(get_db),
):
    tp = db.query(TaxpayerModel).filter(TaxpayerModel.id == taxpayer_id).first()
    if not tp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Taxpayer not found"
        )
    for field, value in payload.dict().items():
        setattr(tp, field, value)
    db.commit()
    db.refresh(tp)
    return tp


@router.delete(
    "/{taxpayer_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_user)],
)
def delete_taxpayer(
    taxpayer_id: int,
    db: Session = Depends(get_db),
):
    tp = db.query(TaxpayerModel).filter(TaxpayerModel.id == taxpayer_id).first()
    if not tp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Taxpayer not found"
        )
    db.delete(tp)
    db.commit()
    return {"detail": "Taxpayer deleted"}
