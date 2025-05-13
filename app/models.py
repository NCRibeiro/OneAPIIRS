# tools/models.py
"""
models.py — Definição de modelos ORM para scripts de manutenção
e geração de dados do APE.
"""
from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import relationship


# Define Base as the declarative base for ORM models
@as_declarative()
class Base:
    pass


# Ensure Base and models are properly exposed for external references
__all__ = ["Base", "TaxpayerData", "LegacyData", "AuditLog", "User"]


class TaxpayerData(Base):
    __tablename__ = "taxpayer_data"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    tax_id = Column(String(50), unique=True, nullable=False, index=True)
    region = Column(String(100), nullable=True)
    payment_status = Column(String(50), nullable=False)
    amount_due = Column(Float, nullable=False)
    amount_paid = Column(Float, nullable=False)

    legacy_data = relationship(
        "LegacyData", back_populates="taxpayer", cascade="all, delete-orphan"
    )
    audit_logs = relationship(
        "AuditLog", back_populates="taxpayer", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<TaxpayerData id={self.id} tax_id={self.tax_id}>"


class LegacyData(Base):
    __tablename__ = "legacy_data"

    id = Column(Integer, primary_key=True, index=True)
    record_data = Column(String, nullable=False)
    taxpayer_id = Column(Integer, ForeignKey("taxpayer_data.id"), nullable=False)

    timestamp = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    taxpayer = relationship("TaxpayerData", back_populates="legacy_data")

    def __repr__(self) -> str:
        return f"<LegacyData id={self.id} taxpayer_id={self.taxpayer_id}>"


class AuditLog(Base):
    __tablename__ = "audit_log"

    id = Column(Integer, primary_key=True, index=True)
    taxpayer_id = Column(Integer, ForeignKey("taxpayer_data.id"), nullable=False)

    action = Column(String(255), nullable=False)
    timestamp = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    details = Column(String, nullable=True)

    taxpayer = relationship("TaxpayerData", back_populates="audit_logs")

    def __repr__(self) -> str:
        return f"<AuditLog id={self.id} action={self.action}>"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Integer, default=1)
    is_superuser = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    deleted_at = Column(DateTime, nullable=True)
    last_login = Column(DateTime, nullable=True)
    failed_login_attempts = Column(Integer, default=0)
    last_failed_login = Column(DateTime, nullable=True)
    password_reset_token = Column(String, nullable=True)
    password_reset_token_expires = Column(DateTime, nullable=True)

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username}>"
