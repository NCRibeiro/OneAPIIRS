from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Taxpayer(Base):
    __tablename__ = "taxpayers"

    taxpayer_id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    registered_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String)

    legacy_records = relationship("LegacyRecord", back_populates="taxpayer")
    modern_records = relationship("ModernRecord", back_populates="taxpayer")

class LegacyRecord(Base):
    __tablename__ = "legacy_records"

    record_id = Column(Integer, primary_key=True, index=True)
    taxpayer_id = Column(String, ForeignKey("taxpayers.taxpayer_id"))
    gross_income = Column(Integer)
    tax_paid = Column(Integer)
    raw_line = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

    taxpayer = relationship("Taxpayer", back_populates="legacy_records")

class ModernRecord(Base):
    __tablename__ = "modern_records"

    record_id = Column(Integer, primary_key=True, index=True)
    taxpayer_id = Column(String, ForeignKey("taxpayers.taxpayer_id"))
    income = Column(Integer)
    tax = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    taxpayer = relationship("Taxpayer", back_populates="modern_records")
