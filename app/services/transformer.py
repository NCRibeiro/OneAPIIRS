# app/services/transformer.py

"""
Funções para transformar dados legados em estruturas modernas.
"""

import re
from datetime import datetime, date

from app.schemas.legacy import LegacyEntry
from app.schemas.modern import ModernRead


def cobol_to_json(cobol_string: str) -> dict[str, str]:
    """
    Converte string estilo COBOL para dicionário JSON moderno.
    Exemplo de entrada:
      "NOME: JOHN DOE   NASC: 1960-05-15   REND: $45000.00"
    """
    field_map = {
        "nome": "name",
        "nasc": "birth_date",
        "rend": "income",
    }
    result: dict[str, str] = {}

    tokens = re.findall(r"(\w+):\s*([^:]+)", cobol_string)
    for raw_key, raw_val in tokens:
        key = raw_key.strip().lower()
        val = raw_val.strip()
        if key not in field_map:
            continue

        json_key = field_map[key]
        if key == "nasc":
            try:
                parsed = datetime.strptime(val, "%Y-%m-%d").date()
                result[json_key] = parsed.isoformat()
            except ValueError:
                return {"erro": f"Formato de data inválido: {val}"}
        elif key == "nome":
            result[json_key] = val.title()
        elif key == "rend":
            result[json_key] = val.replace("$", "").replace(",", "")

    if set(result.keys()) != set(field_map.values()):
        return {"erro": "Campos esperados (nome, nasc, rend) não encontrados."}
    return result


def transform_legacy_to_modern(entry: LegacyEntry) -> ModernRead:
    """
    Converte um LegacyEntry em um ModernRead padronizado.
    - Nome em Title Case
    - CPF convertido para formato mock SSN
    - Mantém impostos pagos, status e timestamp
    """
    # Garante que birth_date seja do tipo date
    birth_date_obj: date = (
        entry.birth_date.date() if isinstance(entry.birth_date, datetime) else entry.birth_date
    )

    # Limpa CPF e formata como SSN mock
    clean_cpf = entry.cpf.replace(".", "").replace("-", "")
    if len(clean_cpf) == 11:
        ssn = f"{clean_cpf[:3]}-{clean_cpf[3:5]}-{clean_cpf[5:]}"
    else:
        ssn = clean_cpf  # fallback se o CPF estiver mal formatado

    return ModernRead(
        full_name=entry.name.title(),
        cpf=ssn,
        birth_date=birth_date_obj,
        income=entry.gross_income,
        taxes=entry.tax_paid,
        status="Ativo",  # Ou poderia mapear de entry.status se existir
        timestamp=entry.timestamp,
    )
