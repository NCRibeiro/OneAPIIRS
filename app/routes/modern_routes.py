from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models.modern import ModernRecord
from app.models.taxpayer import Taxpayer

router = APIRouter()

# Função para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rota para criar um registro modernizado
@router.post("/")
def create_modern_record(record: ModernRecord, db: Session = Depends(get_db)):
    # Verificar se o contribuinte existe
    taxpayer = db.query(Taxpayer).filter(Taxpayer.taxpayer_id == record.taxpayer_id).first()
    if not taxpayer:
        raise HTTPException(status_code=404, detail="Taxpayer not found")
    
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

# Rota para listar os registros modernizados
@router.get("/")
def get_modern_records(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    modern_records = db.query(ModernRecord).offset(skip).limit(limit).all()
    return modern_records

# Rota para buscar um registro modernizado específico
@router.get("/{record_id}")
def get_modern_record(record_id: int, db: Session = Depends(get_db)):
    record = db.query(ModernRecord).filter(ModernRecord.record_id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Modern record not found")
    return record

# Rota para atualizar um registro modernizado
@router.put("/{record_id}")
def update_modern_record(record_id: int, record: ModernRecord, db: Session = Depends(get_db)):
    db_record = db.query(ModernRecord).filter(ModernRecord.record_id == record_id).first()
    if not db_record:
        raise HTTPException(status_code=404, detail="Modern record not found")
    
    # Atualiza os campos do registro
    db_record.income = record.income
    db_record.tax = record.tax
    db_record.created_at = record.created_at
    db.commit()
    db.refresh(db_record)
    
    return db_record

# Rota para excluir um registro modernizado
@router.delete("/{record_id}")
def delete_modern_record(record_id: int, db: Session = Depends(get_db)):
    db_record = db.query(ModernRecord).filter(ModernRecord.record_id == record_id).first()
    if not db_record:
        raise HTTPException(status_code=404, detail="Modern record not found")
   
    db.delete(db_record)
    db.commit()
    return {"detail": "Modern record deleted"}
    
    return db_record

