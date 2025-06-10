from sqlalchemy import Column, Integer, String, Date, Float, DateTime, func
from app.db.base import Base


class Taxpayer(Base):
    """
    Modelo ORM do contribuinte para persistência no banco de dados.
    Compatível com os schemas TaxpayerCreate e TaxpayerRead.
    """

    __tablename__ = "taxpayers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    cpf = Column(String(14), unique=True, nullable=False, index=True)
    birth_date = Column(Date, nullable=False)
    gross_income = Column(Float, nullable=False)
    tax_paid = Column(Float, nullable=False)
    raw_line = Column(String(200), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"<Taxpayer(id={self.id}, cpf={self.cpf})>"
