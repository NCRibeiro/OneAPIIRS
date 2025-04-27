# === services/auditor.py ===
from datetime import datetime
from typing import List
from app.schemas.audit import AuditReport, SuspiciousRecord, AuditSummary
from app.schemas.legacy import LegacyEntry


def run_audit(data: List[LegacyEntry]) -> AuditReport:
    suspicious = []

    for entry in data:
        # Regra 1: CPF duplicado
        cpf_occurrences = [e for e in data if e.cpf == entry.cpf]
        if len(cpf_occurrences) > 1:
            suspicious.append(SuspiciousRecord(
                id=str(entry.id),
                name=entry.name,
                cpf=entry.cpf,
                reason="CPF duplicado"
            ))
            continue

        # Regra 2: Renda acima de 1 milhão
        if entry.income > 1_000_000:
            suspicious.append(SuspiciousRecord(
                id=str(entry.id),
                name=entry.name,
                cpf=entry.cpf,
                reason="Renda acima do esperado"
            ))
            continue

        # Regra 3: Menor de idade com renda
        age = (datetime.utcnow().date() - entry.birth_date.date()).days // 365
        if age < 18 and entry.income > 0:
            suspicious.append(SuspiciousRecord(
                id=str(entry.id),
                name=entry.name,
                cpf=entry.cpf,
                reason="Menor de idade com renda"
            ))

    summary = AuditSummary(
        total_records=len(data),
        suspicious_count=len(suspicious),
        timestamp=datetime.utcnow().isoformat() + "Z"
    )

    return AuditReport(summary=summary, suspicious=suspicious)
