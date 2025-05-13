#!/usr/bin/env python
"""
tools/visualizar_dados.py — Visualização interativa de dados fiscais
Uso:
    python tools/visualizar_dados.py
"""
import logging

import numpy as np
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
from sqlalchemy import create_engine

from core.settings import settings

# Carrega .env e configurações
load_dotenv()

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s %(message)s",
)
logger = logging.getLogger("visualizar_dados")

# Conexão síncrona ao banco (remove +asyncpg se presente)
sync_url = str(settings.DATABASE_URL).replace("+asyncpg", "")
engine = create_engine(sync_url, echo=False, future=True)


def fetch_data() -> pd.DataFrame:
    """
    Recupera dados de contribuintes do banco.
    Colunas: 'cpf', 'amount_due', 'amount_paid'.
    """
    query = "SELECT tax_id AS cpf, amount_due, amount_paid " "FROM taxpayer_data"
    df = pd.read_sql(query, engine)
    return df


def prepare_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adiciona colunas de inconsistência e mês para visualização.
    """
    df = df.copy()
    # Marca inconsistências
    df["Inconsistência"] = np.where(df["amount_due"] != df["amount_paid"], "Sim", "Não")
    # Adiciona coluna de mês aleatório para simulação de séries temporais
    df["Mes"] = np.random.choice(
        ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun"], size=len(df)
    )
    return df


def plot_inconsistencias(df: pd.DataFrame):
    """
    Exibe um gráfico de barras de inconsistências por contribuinte.
    """
    fig = px.bar(
        df, x="cpf", color="Inconsistência", title="Inconsistências por Contribuinte"
    )
    fig.show()


def plot_distribuicao(df: pd.DataFrame):
    """
    Exibe um histograma de valores pagos.
    """
    fig = px.histogram(
        df,
        x="amount_paid",
        nbins=30,
        title="Distribuição de Valores Pagos",
    )
    fig.show()


def plot_evolucao(df: pd.DataFrame):
    """
    Exibe evolução dos pagamentos por mês.
    """
    df_month = df.groupby("Mes").sum().reset_index()
    fig = px.line(
        df_month,
        x="Mes",
        y="amount_paid",
        title="Evolução do Pagamento de Impostos",
    )
    fig.show()


def plot_proporcao(df: pd.DataFrame):
    """
    Exibe proporção de inconsistências.
    """
    fig = px.pie(
        df,
        names="Inconsistência",
        title="Proporção de Inconsistências",
    )
    fig.show()


def main():
    logger.info("Buscando dados de contribuintes...")
    df = fetch_data()
    df = prepare_dataframe(df)

    logger.info("Gerando visualizações...")
    plot_inconsistencias(df)
    plot_distribuicao(df)
    plot_evolucao(df)
    plot_proporcao(df)
    logger.info("Visualizações concluídas.")


if __name__ == "__main__":
    main()
