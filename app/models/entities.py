from datetime import datetime
from typing import Optional, List
from sqlalchemy import DateTime, ForeignKey, Numeric, String, func, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class TaxpayerData(Base):
    __tablename__ = "taxpayer_data"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    tax_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    region: Mapped[Optional[str]] = mapped_column(String(100))
    payment_status: Mapped[str] = mapped_column(String(50), nullable=False)
    amount_due: Mapped[Numeric] = mapped_column(  # type: ignore
        Numeric(14, 2), nullable=False
    )
    amount_paid: Mapped[Numeric] = mapped_column(  # type: ignore
        Numeric(14, 2), nullable=False
    )
    legacy_data: Mapped[List["LegacyData"]] = relationship(
        "LegacyData", back_populates="taxpayer"
    )
    audit_logs: Mapped[List["AuditLog"]] = relationship(
        "AuditLog", back_populates="related_taxpayer"
    )


class LegacyData(Base):
    __tablename__ = "legacy_data"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    record_data: Mapped[str] = mapped_column(String(1024), nullable=False)
    taxpayer_id: Mapped[int] = mapped_column(ForeignKey("taxpayer_data.id"))
    taxpayer: Mapped[TaxpayerData] = relationship(
        "TaxpayerData", back_populates="legacy_data"
    )


class AuditLog(Base):
    __tablename__ = "audit_log"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    taxpayer_id: Mapped[int] = mapped_column(ForeignKey("taxpayer_data.id"))
    action: Mapped[str] = mapped_column(String(255), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    details: Mapped[Optional[str]] = mapped_column(String(1024))
    related_taxpayer: Mapped[TaxpayerData] = relationship(
        "TaxpayerData", back_populates="audit_logs"
    )
