import re
from datetime import datetime
from app.schemas.legacy import LegacyEntry
from app.schemas.modern import ModernEntry


def cobol_to_json(cobol_string: str) -> dict:
    """
    Converte uma string estilo COBOL para um dicionário JSON moderno.

    Espera um formato como:
    "NOME: JOHN DOE   NASC: 1960-05-15   REND: $45000.00"

    Saída:
    {
        "name": "John Doe",
        "birth_date": "1960-05-15",
        "income": "$45000.00"
    }
    """
    try:
        field_map = {
            "nome": "name",
            "nasc": "birth_date",
            "rend": "income"
        }

        result = {}
        campos = re.findall(r"(\w+):\s*([^:]+)", cobol_string)

        for chave_bruta, valor in campos:
            chave = chave_bruta.strip().lower()
            valor = valor.strip()

            if chave not in field_map:
                continue

            json_key = field_map[chave]

            if chave == "nasc":
                try:
                    parsed_date = datetime.strptime(valor, "%Y-%m-%d")
                    valor = parsed_date.date().isoformat()
                except ValueError:
                    raise ValueError(f"Formato de data inválido: {valor}")

            elif chave == "nome":
                valor = valor.title()

            result[json_key] = valor

        if len(result) != len(field_map):
            return {
                "erro": "Nem todos os campos esperados foram encontrados. Esperado: nome, nasc, rend."
            }

        return result

    except Exception as e:
        return {"erro": f"Falha na transformação: {str(e)}"}


def transform_legacy_to_modern(entry: LegacyEntry) -> ModernEntry:
    """
    Converte um LegacyEntry para um ModernEntry com novos campos derivados.
    """
    birth_date = entry.birth_date
    today = datetime.utcnow()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    income_usd = round(entry.income / 5.0, 2)  # Conversão simbólica de BRL para USD

    return ModernEntry(
        id=entry.id,
        full_name=entry.name.upper(),
        cpf=entry.cpf,
        birth_date=entry.birth_date,
        age=age,
        income_brl=entry.income,
        income_usd=income_usd,
        registered_at=today.isoformat()
    )
