"""
app/services/auditor.py

Serviço de auditoria para detectar inconsistências e possíveis fraudes em dados legados.
"""

from collections import Counter
from datetime import datetime, date
from typing import Annotated, List

from app.schemas.legacy import LegacyEntry
from app.schemas.audit import AuditReport, SuspiciousRecord, AuditSummary


def run_audit(data: Annotated[List[LegacyEntry], ...]) -> Annotated[AuditReport, ...]:
    """
    Executa auditoria fiscal com base em múltiplas regras:
    - CPF duplicado
    - Pessoa menor de idade com renda
    - Renda acima de R$ 1.000.000
    - Campos obrigatórios ausentes
    """

    suspicious: List[Annotated[SuspiciousRecord, ...]] = []

    # Conta CPFs duplicados
    cpf_counts: Counter[str] = Counter(entry.cpf for entry in data)

    for entry in data:
        if _is_cpf_duplicado(entry, cpf_counts):
            suspicious.append(_suspicious(entry, "CPF duplicado"))

        if _is_menor_de_idade_com_renda(entry):
            suspicious.append(_suspicious(entry, "Menor de idade com renda"))

        if _is_renda_acima_do_limite(entry):
            suspicious.append(_suspicious(entry, "Renda acima de R$ 1.000.000"))

        if _tem_campos_vazios(entry):
            suspicious.append(_suspicious(entry, "Campos obrigatórios ausentes"))

    summary = AuditSummary(
        total_checked=len(data),
        suspicious_count=len(suspicious),
        audit_date=datetime.today().date()
    )

    return AuditReport(
        id="audit-001",
        total_records=len(data),
        total_suspect=len(suspicious),
        suspicious=suspicious,
        summary=summary
    )


# ───── Funções auxiliares ─────

def _suspicious(entry: LegacyEntry, reason: str) -> SuspiciousRecord:
    return SuspiciousRecord(
        id=str(entry.id),
        name=entry.name or "Desconhecido",
        cpf=entry.cpf or "Desconhecido",
        taxpayer_id=entry.taxpayer_id,
        reason=reason,
    )


def _is_cpf_duplicado(entry: LegacyEntry, cpf_counts: Counter[str]) -> bool:
    return cpf_counts.get(entry.cpf, 0) > 1


def _is_menor_de_idade_com_renda(entry: LegacyEntry) -> bool:
    try:
        birth = (
            entry.birth_date if isinstance(entry.birth_date, date)
            else datetime.strptime(entry.birth_date, "%Y-%m-%d").date()
        )
        idade = (datetime.today().date() - birth).days // 365
        return idade < 18 and float(entry.gross_income) > 0
    except Exception:
        return True  # Data malformada é considerada suspeita


def _is_renda_acima_do_limite(entry: LegacyEntry) -> bool:
    try:
        return float(entry.gross_income) > 1_000_000
    except ValueError:
        return True


def _tem_campos_vazios(entry: LegacyEntry) -> bool:
    return not all([entry.name, entry.cpf, entry.birth_date, entry.gross_income])
