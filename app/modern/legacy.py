from sqlalchemy import Column, String, Integer, Float, DateTime
from app.db.base import Base
from datetime import datetime

class LegacyRecord(Base):
    __tablename__ = "legacy_records"

    record_id = Column(Integer, primary_key=True, index=True)
    taxpayer_id = Column(String, index=True)
    gross_income = Column(Integer)
    tax_paid = Column(Integer)
    raw_line = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<LegacyRecord {self.record_id} - {self.taxpayer_id}>"
