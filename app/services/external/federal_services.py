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
    """
    cpf_pattern = r"\d{3}\.\d{3}\.\d{3}-\d{2}"
    if not re.match(cpf_pattern, cpf):
        return False
    # Maior probabilidade de ser válido
    return random.choice([True, True, False])


def fetch_income_score(cpf: str) -> int:
    """
    Retorna um score de renda baseado em uma lógica simulada.
    """
    base = sum(int(ch) for ch in re.findall(r"\d", cpf))
    return base % 1000  # Score entre 0 e 999


def check_debts(cpf: str) -> bool:
    """
    Verifica se há pendências financeiras ativas para o CPF.
    Simula 30% de chance de dívida.
    """

    return random.random() < 0.3
