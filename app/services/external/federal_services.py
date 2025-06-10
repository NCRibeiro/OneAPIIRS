# app/services/external/federal_services.py

"""
Serviços simulados para validação de CPF, score de renda e checagem de dívidas.
Integrações fictícias com sistemas federais externos.
"""

import random
import re


def validate_cpf_externally(cpf: str) -> bool:
    """
    Simula a verificação de validade de um CPF em sistema federal externo.
    Retorna True se o CPF parecer válido (formato correto) e for aceito na simulação.
    """
    pattern = r"^\d{3}\.\d{3}\.\d{3}-\d{2}$"
    if not re.match(pattern, cpf):
        return False
    return random.choices([True, False], weights=[70, 30])[0]


def fetch_income_score(cpf: str) -> int:
    """
    Retorna um score de renda entre 0 e 999 com base nos dígitos do CPF.
    """
    soma = sum(int(d) for d in re.findall(r"\d", cpf))
    return soma % 1000


def check_debts(cpf: str) -> bool:
    """
    Simula a existência de dívidas no CPF.
    Retorna True em aproximadamente 30% dos casos.
    """
    return random.random() < 0.3
