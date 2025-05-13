# modern/legacy.py

from sqlalchemy import Column, String, Integer, Float, DateTime, func
from modern.base import Base  # Ajuste para importar do seu módulo modern/base


class LegacyRecord(Base):
    __tablename__ = "legacy_records"

    record_id = Column(Integer, primary_key=True, index=True)
    taxpayer_id = Column(String, nullable=False, index=True)
    gross_income = Column(Float, nullable=False)
    tax_paid = Column(Float, nullable=False)
    raw_line = Column(String, nullable=False)
    timestamp = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


def __repr__(self) -> str:
    return f"<LegacyRecord {self.record_id} — Taxpayer: {self.taxpayer_id}>"


def __eq__(self, other: Base):
    return self.record_id == other.record_id


def __ne__(self, other: Base):
    return not self.__eq__(other)
