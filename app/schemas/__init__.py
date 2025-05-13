"""
Schemas centralizados para validação e serialização de dados do APE.
Agrupa todos os modelos utilizados na aplicação.
"""

from .auth import Token, TokenData
from .user import UserCreate, UserRead, UserInDB, RoleEnum
from .taxpayer import TaxpayerCreate, TaxpayerRead, TaxpayerBatchResponse
from .legacy import LegacyEntry, LegacyResponse, LegacyBatchResponse
from .modern import (
    ModernEntry,
    ModernCreate,
    ModernRead,
    ModernResponse,
    ModernBatchResponse,
)
from .transform import RawCOBOLInput, TransformedResponse
from .external import ExternalCheckResult, SupportedBank, BanksResponse
from .analytics import (
    AnalyticsSummary,
    MonthlyRecord,
    MonthlyBreakdown,
    AuditError,
    AuditErrorList,
)
from .audit import SuspiciousRecord, AuditSummary, AuditReport

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
