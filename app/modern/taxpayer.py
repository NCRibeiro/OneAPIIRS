# modern/taxpayer.py

from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from modern.base import Base


class Taxpayer(Base):
    __tablename__ = "taxpayers"

    taxpayer_id = Column(String(50), primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    registered_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    status = Column(String(20), server_default="ACTIVE", nullable=False, index=True)

    # Relacionamentos com registros modernos e legados
    legacy_records = relationship(
        "LegacyRecord", back_populates="taxpayer", cascade="all, delete-orphan"
    )
    modern_records = relationship(
        "ModernRecord", back_populates="taxpayer", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Taxpayer {self.name} ({self.taxpayer_id})>"
