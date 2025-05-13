# modern/modern.py

from sqlalchemy import Column, String, Integer, Float, DateTime, func
from modern.base import Base


class ModernRecord(Base):
    __tablename__ = "modern_records"

    record_id = Column(Integer, primary_key=True, index=True)
    taxpayer_id = Column(String(50), nullable=False, index=True)
    income = Column(Float, nullable=False)
    tax = Column(Float, nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    def __repr__(self) -> str:
        return f"<ModernRecord {self.record_id} — Taxpayer: {self.taxpayer_id}>"
