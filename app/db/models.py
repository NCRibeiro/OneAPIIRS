from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base

if TYPE_CHECKING:
    from .models import LegacyData, AuditLog

# Tabela: Contribuintes Modernos
class TaxpayerData(Base):
    __tablename__ = "taxpayer_data"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    tax_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    region: Mapped[Optional[str]] = mapped_column(String(100))
    payment_status: Mapped[str] = mapped_column(String(50), nullable=False)
    amount_due: Mapped[Numeric] = mapped_column(Numeric(14, 2), nullable=False)
    amount_paid: Mapped[Numeric] = mapped_column(Numeric(14, 2), nullable=False)

    legacy_data: Mapped[List["LegacyData"]] = relationship(
        back_populates="taxpayer", cascade="all, delete-orphan"
    )
    audit_logs: Mapped[List["AuditLog"]] = relationship(
        back_populates="taxpayer", cascade="all, delete-orphan"
    )

# Tabela: Dados Legados
class LegacyData(Base):
    __tablename__ = "legacy_data"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    record_data: Mapped[str] = mapped_column(String, nullable=False)
    taxpayer_id: Mapped[int] = mapped_column(ForeignKey("taxpayer_data.id"), nullable=False)

    taxpayer: Mapped["TaxpayerData"] = relationship(back_populates="legacy_data")

# Tabela: Auditoria
class AuditLog(Base):
    __tablename__ = "audit_log"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    taxpayer_id: Mapped[int] = mapped_column(ForeignKey("taxpayer_data.id"), nullable=False)
    action: Mapped[str] = mapped_column(String(255), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    details: Mapped[Optional[str]] = mapped_column(String)

    taxpayer: Mapped["TaxpayerData"] = relationship(back_populates="audit_logs")

# Metadados
__all__ = ["TaxpayerData", "LegacyData", "AuditLog"]
__version__ = "2.0.0"
__author__ = "Nívea C. Ribeiro"
__license__ = "MIT"
__copyright__ = "Copyright 2023 Nívea C. Ribeiro"
__url__ = "https://github.com/NCRibeiro"
__description__ = __doc
__long_description__ = __doc
__long_description_content_type__ = "text/markdown"
__maintainer__="Nívea C. Ribeiro"
__email__="nc.chagasribeiro@gmail.com"
__github_username__="NCRibeiro"
__status__="Development"
__title__="OneAPIIRS — APE Project"
__package_name__="ape"
__module_name__="db"



