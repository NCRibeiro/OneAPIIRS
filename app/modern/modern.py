from sqlalchemy import Column, String, Integer, Float, DateTime
from app.db.base import Base
from datetime import datetime

class ModernRecord(Base):
    __tablename__ = "modern_records"

    record_id = Column(Integer, primary_key=True, index=True)
    taxpayer_id = Column(String, index=True)
    income = Column(Integer)
    tax = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ModernRecord {self.record_id} - {self.taxpayer_id}>"
