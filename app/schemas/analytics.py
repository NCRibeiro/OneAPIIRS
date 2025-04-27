from pydantic import BaseModel
from typing import List, Dict

class AnalyticsSummary(BaseModel):
    total_taxpayers: int
    total_legacy_records: int
    total_modern_records: int
    error_rate_percent: float

class MonthlyRecord(BaseModel):
    month: str
    count: int

class MonthlyBreakdown(BaseModel):
    records_by_month: List[MonthlyRecord]

class AuditError(BaseModel):
    taxpayer_id: str
    issue: str

class AuditErrorList(BaseModel):
    errors: List[AuditError]
