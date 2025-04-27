from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

class Taxpayer(Base):
    __tablename__ = "taxpayers"

    taxpayer_id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    registered_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="ACTIVE")

    # Relacionamentos, se necessário
    # Exemplo: relationship("Income", back_populates="taxpayer")
    
    def __repr__(self):
        return f"<Taxpayer {self.name} ({self.taxpayer_id})>"

