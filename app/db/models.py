# models.py

from __future__ import annotations
from typing import TYPE_CHECKING  # For type hinting during static analysis

if TYPE_CHECKING:
    pass  # LegacyData is defined in the same module, no import needed
from datetime import datetime
from typing import Optional, List
from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# ─── Contribuintes Modernos ───────────────────────


class TaxpayerData(Base):
    __tablename__ = "taxpayer_data"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    tax_id: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    region: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    payment_status: Mapped[str] = mapped_column(String(50), nullable=False)
    amount_due: Mapped[Numeric] = mapped_column(Numeric(14, 2), nullable=False)
    amount_paid: Mapped[Numeric] = mapped_column(Numeric(14, 2), nullable=False)
    if TYPE_CHECKING:
        pass  # No import needed as LegacyData is defined in the same module
    else:
        legacy_data_id: Mapped[int] = mapped_column(
            Integer, ForeignKey("legacy_data.id"), nullable=True
        )
        audit_log_id: Mapped[int] = mapped_column(
            Integer, ForeignKey("audit_log.id"), nullable=True
        )
        legacy_data: Mapped[List["LegacyData"]] = relationship(
            "LegacyData",
            back_populates="taxpayer",
            cascade="all, delete-orphan",
        )
        audit_logs: Mapped[List["AuditLog"]] = relationship(
            "AuditLog",
            back_populates="taxpayer",
            cascade="all, delete-orphan",
        )


# ─── Dados Legados ────────────────────────────────


class LegacyData(Base):
    __tablename__ = "legacy_data"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    record_data: Mapped[str] = mapped_column(String(1024), nullable=False)
    taxpayer_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("taxpayer_data.id"), nullable=False
    )

    taxpayer: Mapped[TaxpayerData] = relationship(
        "TaxpayerData",
        back_populates="legacy_data",
    )


# ─── Auditoria ────────────────────────────────────


# Tabela: Auditoria
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

    related_taxpayer: Mapped[TaxpayerData] = relationship(
        "TaxpayerData",
        back_populates="audit_logs",
    )


# Metadados
__all__ = ["TaxpayerData", "LegacyData", "AuditLog"]
__version__ = "2.0.0"
__author__ = "Nívea C. Ribeiro"
__license__ = "MIT"
__copyright__ = "Copyright 2023 Nívea C. Ribeiro"
__url__ = "https://github.com/NCRibeiro"

# Ensure __doc__ is explicitly defined if needed
__description__ = "Database models for the APE Project"
__doc__ = __description__
__long_description__ = (
    "This module contains the database models for the APE Project, including "
    "TaxpayerData, LegacyData, and AuditLog."
)
__long_description_content_type__ = "text/markdown"
__maintainer__ = "Nívea C. Ribeiro"
__email__ = "nc.chagasribeiro@gmail.com"
__github_username__ = "NCRibeiro"
__status__ = "Development"
__title__ = "OneAPIIRS — APE Project"
__package_name__ = "ape"
__module_name__ = "db"


# Blank line added to comply with PEP 8
