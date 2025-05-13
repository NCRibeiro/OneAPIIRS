# app/services/transformer.py

"""
Funções para transformar dados legados em estruturas modernas.
"""

import re
from datetime import date, datetime
from typing import Dict, Union

from app.schemas.legacy import LegacyEntry
from app.schemas.modern import ModernEntry


def cobol_to_json(cobol_string: str) -> Union[Dict[str, str], Dict[str, str]]:
    """
    Converte uma string estilo COBOL para um dicionário JSON moderno.

    Espera um formato como:
        "NOME: JOHN DOE   NASC: 1960-05-15   REND: $45000.00"

    Retorna:
        dict com chaves (
            'name',
            'birth_date',
            'income' ou {'erro': ...}
            em caso de falha e valores correspondentes)

    """

    field_map = {
        "nome": "name",
        "nasc": "birth_date",
        "rend": "income",
    }
    result: Dict[str, str] = {}

    try:
        # Extrai pares campo: valor
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
                # Remove '$' and ',' then convert to float
                val = val.replace("$", "").replace(",", "")
                result[json_key] = val

        expected_fields = set(field_map.values())
        actual_fields = set(result.keys())
        if actual_fields != expected_fields:
            return {"erro": "Campos esperados (nome, nasc, rend) não encontrados."}

        return result
    except Exception as e:
        return {"erro": f"Falha na transformação: {e}"}


def transform_legacy_to_modern(entry: LegacyEntry) -> ModernEntry:
    """
    Converte um LegacyEntry em um ModernEntry.

    - Mantém o mesmo ID legado.
    - Formata o nome para Title Case.
    - Ajusta o CPF como SSN no formato 000-00-0000.
    - Converte birth_date para date.
    """
    bd: date = (
        entry.birth_date.date()
        if isinstance(entry.birth_date, datetime)
        else entry.birth_date
    )

    # Ajusta o SSN para o formato 000-00-0000 a partir do CPF (exemplo).
    # Formatação real dependeria das regras do país de origem dos
    # dados legados.

    clean_cpf = entry.cpf.replace(".", "").replace("-", "")
    ssn_formatted = f"{clean_cpf[:3]}-{clean_cpf[3:5]}-{clean_cpf[5:9]}"

    return ModernEntry(
        full_name=entry.name.title(),
        ssn=ssn_formatted,
        annual_income=entry.income,
        birth_date=bd,
    )


__author__ = "Nívea C. Ribeiro"
__license__ = "MIT"
__copyright__ = "Copyright 2023 Nívea C. Ribeiro"
__url__ = "https://github.com/NCRibeiro"
__description__ = "OneAPIIRS — APE Project"
__long_description__ = __doc__
__long_description_content_type__ = "text/markdown"
__maintainer__ = "Nívea C. Ribeiro"
__email__ = "contato@nivea.dev"
__github_username__ = "NCRibeiro"
__status__ = "Development"
__title__ = "OneAPIIRS — APE Project"
__version__ = "1.0.0"
__all__ = [
    "cobol_to_json",
    "transform_legacy_to_modern",
]
