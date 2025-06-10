from datetime import datetime, date
from sqlalchemy import Column, Date, DateTime, Float, Integer, String
from app.db.base import Base


class LegacyRecord(Base):
    """
    Modelo de dados legados (pré-processamento/ETL).
    Usado para armazenar registros originais importados de sistemas antigos.
    """
    __tablename__ = "legacy_records"

    id = Column(Integer, primary_key=True, index=True)
    taxpayer_id = Column(String, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    cpf = Column(String(14), nullable=False, index=True)
    birth_date = Column(Date, nullable=True)
    income = Column(Float, nullable=True)
    raw_line = Column(String(200), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=True)

    def __repr__(self) -> str:
        return (
            f"<LegacyRecord id={self.id} taxpayer_id={self.taxpayer_id} "
            f"cpf={self.cpf} income={self.income}>"
        )
