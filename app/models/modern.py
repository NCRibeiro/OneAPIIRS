from __future__ import annotations

from datetime import datetime, date
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    DateTime,
    ForeignKey,
    Numeric,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


# ─── Contribuintes Modernos ───────────────────────

class ModernRecord(Base):
    __tablename__ = "modern_record"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    taxpayer_id: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    birth_date: Mapped[date] = mapped_column(Date, nullable=False)
    income: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    submitted_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


# ─── Dados Legados ────────────────────────────────

class LegacyData(Base):
    __tablename__ = "legacy_data"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    record_data: Mapped[str] = mapped_column(String(1024), nullable=False)
    taxpayer_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("taxpayer_data.id"), nullable=False
    )


# ─── Tabela de Contribuintes ───────────────────────

class TaxpayerData(Base):
    __tablename__ = "taxpayer_data"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    tax_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    region: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    payment_status: Mapped[str] = mapped_column(String(50), nullable=False)
    amount_due: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)
    amount_paid: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)

    legacy_data: Mapped[List[LegacyData]] = relationship("LegacyData", backref="taxpayer")
    audit_logs: Mapped[List["AuditLog"]] = relationship("AuditLog", backref="taxpayer")


# ─── Auditoria ────────────────────────────────────

class AuditLog(Base):
    __tablename__ = "audit_log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    taxpayer_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("taxpayer_data.id"), nullable=False
    )
    action: Mapped[str] = mapped_column(String(255), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    details: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)


# ─── Metadados ────────────────────────────────────

__all__ = ["ModernRecord", "TaxpayerData", "LegacyData", "AuditLog"]
__version__ = "2.0.0"
__author__ = "Nívea C. Ribeiro"
__license__ = "MIT"
__description__ = "Database models for the APE Project"
__status__ = "Development"
__module_name__ = "db"
__package_name__ = "ape"
__maintainer__ = "Nívea C. Ribeiro",
__email__ = "contato@nivea.dev"
__github_username__ = "NCRibeiro"
