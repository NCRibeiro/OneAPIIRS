# app/services/auditor.py
"""
services/auditor.py – Regras de auditoria para dados legados.
"""
from datetime import datetime
from collections import Counter
from typing import List

from app.schemas.audit import AuditReport, SuspiciousRecord, AuditSummary
from app.schemas.legacy import LegacyEntry


def run_audit(data: List[LegacyEntry]) -> AuditReport:
    """
    Executa regras de auditoria em uma lista de registros legados.

    Regras:
    1) CPF duplicado
    2) Renda acima de 1.000.000
    3) Menor de 18 anos com renda
    """
    suspicious: List[SuspiciousRecord] = []

    # Contagem de ocorrências de CPF para detectar duplicados
    cpf_counts = Counter(entry.cpf for entry in data)

    for entry in data:
        # Regra 1: CPF duplicado
        if cpf_counts[entry.cpf] > 1:
            suspicious.append(
                SuspiciousRecord(
                    id=str(entry.id),
                    name=entry.name,
                    cpf=entry.cpf,
                    reason="CPF duplicado",
                )
            )
            continue

        # Regra 2: Renda acima de 1 milhão
        if entry.income > 1_000_000:
            suspicious.append(
                SuspiciousRecord(
                    id=str(entry.id),
                    name=entry.name,
                    cpf=entry.cpf,
                    reason="Renda acima do esperado",
                )
            )
            continue

        # Regra 3: Menor de idade com renda
        birth = entry.birth_date
        age_years = (datetime.utcnow().date() - birth.date()).days // 365
        if age_years < 18 and entry.income > 0:
            suspicious.append(
                SuspiciousRecord(
                    id=str(entry.id),
                    name=entry.name,
                    cpf=entry.cpf,
                    reason="Menor de idade com renda",
                )
            )

    # Construção do resumo da auditoria
    summary = AuditSummary(
        total_records=len(data),
        suspicious_count=len(suspicious),
        timestamp=datetime.utcnow().isoformat() + "Z",
    )

    return AuditReport(summary=summary, suspicious=suspicious)
