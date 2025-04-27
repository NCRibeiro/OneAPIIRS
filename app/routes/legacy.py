from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models.legacy import LegacyRecord
from app.models.taxpayer import Taxpayer

router = APIRouter()

# Função para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rota para criar um registro legado
@router.post("/legacy/")
def create_legacy_record(record: LegacyRecord, db: Session = Depends(get_db)):
    # Verificar se o contribuinte existe
    taxpayer = db.query(Taxpayer).filter(Taxpayer.taxpayer_id == record.taxpayer_id).first()
    if not taxpayer:
        raise HTTPException(status_code=404, detail="Taxpayer not found")
    
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

# Rota para listar os registros legados
@router.get("/legacy/")
def get_legacy_records(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    legacy_records = db.query(LegacyRecord).offset(skip).limit(limit).all()
    return legacy_records

# Rota para buscar um registro legado específico
@router.get("/legacy/{record_id}")
def get_legacy_record(record_id: int, db: Session = Depends(get_db)):
    record = db.query(LegacyRecord).filter(LegacyRecord.record_id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Legacy record not found")
    return record

# Rota para atualizar um registro legado
@router.put("/legacy/{record_id}")
def update_legacy_record(record_id: int, record: LegacyRecord, db: Session = Depends(get_db)):
    db_record = db.query(LegacyRecord).filter(LegacyRecord.record_id == record_id).first()
    if not db_record:
        raise HTTPException(status_code=404, detail="Legacy record not found")
    
    db_record.gross_income = record.gross_income
    db_record.tax_paid = record.tax_paid
    db_record.raw_line = record.raw_line
    db_record.timestamp = record.timestamp
    db.commit()
    db.refresh(db_record)
    
    return db_record

# Rota para excluir um registro legado
@router.delete("/legacy/{record_id}")
def delete_legacy_record(record_id: int, db: Session = Depends(get_db)):
    db_record = db.query(LegacyRecord).filter(LegacyRecord.record_id == record_id).first()
    if not db_record:
        raise HTTPException(status_code=404, detail="Legacy record not found")
    
    db.delete(db_record)
    db.commit()
    return {"detail": "Legacy record deleted"}
