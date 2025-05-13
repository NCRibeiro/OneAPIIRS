"""
Schemas centralizados para validação e serialização de dados do APE.
Agrupa todos os modelos utilizados na aplicação.
"""

from .analytics import (AnalyticsSummary, AuditError, AuditErrorList,
                        MonthlyBreakdown, MonthlyRecord)
from .audit import AuditReport, AuditSummary, SuspiciousRecord
from .auth import Token, TokenData
from .external import BanksResponse, ExternalCheckResult, SupportedBank
from .legacy import LegacyBatchResponse, LegacyEntry, LegacyResponse
from .modern import (ModernBatchResponse, ModernCreate, ModernEntry,
                     ModernRead, ModernResponse)
from .taxpayer import TaxpayerBatchResponse, TaxpayerCreate, TaxpayerRead
from .transform import RawCOBOLInput, TransformedResponse
from .user import RoleEnum, UserCreate, UserInDB, UserRead

__all__ = [
    # Auth
    "Token",
    "TokenData",
    # Users
    "UserCreate",
    "UserRead",
    "UserInDB",
    "RoleEnum",
    # Taxpayers
    "TaxpayerCreate",
    "TaxpayerRead",
    "TaxpayerBatchResponse",
    # Legacy
    "LegacyEntry",
    "LegacyResponse",
    "LegacyBatchResponse",
    # Modern
    "ModernEntry",
    "ModernCreate",
    "ModernRead",
    "ModernResponse",
    "ModernBatchResponse",
    # Transform
    "RawCOBOLInput",
    "TransformedResponse",
    # External
    "ExternalCheckResult",
    "SupportedBank",
    "BanksResponse",
    # Analytics
    "AnalyticsSummary",
    "MonthlyRecord",
    "MonthlyBreakdown",
    "AuditError",
    "AuditErrorList",
    # Audit
    "SuspiciousRecord",
    "AuditSummary",
    "AuditReport",
]
