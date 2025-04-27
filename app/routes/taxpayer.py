from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models.taxpayer import Taxpayer
from app.core.config import settings
from app.security import get_current_user

router = APIRouter()

# Função para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rota para criar um contribuinte
@router.post("/taxpayer/")
def create_taxpayer(taxpayer: Taxpayer, db: Session = Depends(get_db)):
    db.add(taxpayer)
    db.commit()
    db.refresh(taxpayer)
    return taxpayer

# Rota para listar os contribuintes
@router.get("/taxpayers/")
def get_taxpayers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    taxpayers = db.query(Taxpayer).offset(skip).limit(limit).all()
    return taxpayers

# Rota para buscar um contribuinte específico
@router.get("/taxpayer/{taxpayer_id}")
def get_taxpayer(taxpayer_id: str, db: Session = Depends(get_db)):
    taxpayer = db.query(Taxpayer).filter(Taxpayer.taxpayer_id == taxpayer_id).first()
    if not taxpayer:
        raise HTTPException(status_code=404, detail="Taxpayer not found")
    return taxpayer

# Rota para atualizar um contribuinte
@router.put("/taxpayer/{taxpayer_id}")
def update_taxpayer(taxpayer_id: str, taxpayer: Taxpayer, db: Session = Depends(get_db)):
    db_taxpayer = db.query(Taxpayer).filter(Taxpayer.taxpayer_id == taxpayer_id).first()
    if not db_taxpayer:
        raise HTTPException(status_code=404, detail="Taxpayer not found")
    
    db_taxpayer.name = taxpayer.name
    db_taxpayer.status = taxpayer.status
    db.commit()
    db.refresh(db_taxpayer)
    
    return db_taxpayer

# Rota para excluir um contribuinte
@router.delete("/taxpayer/{taxpayer_id}")
def delete_taxpayer(taxpayer_id: str, db: Session = Depends(get_db)):
    db_taxpayer = db.query(Taxpayer).filter(Taxpayer.taxpayer_id == taxpayer_id).first()
    if not db_taxpayer:
        raise HTTPException(status_code=404, detail="Taxpayer not found")
    
    db.delete(db_taxpayer)
    db.commit()
    return {"detail": "Taxpayer deleted"}
