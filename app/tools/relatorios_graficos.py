#!/usr/bin/env python

"""
tools/relatorio_graficos.py — Geração de relatórios e gráficos fiscais
Uso:
    python tools/relatorio_graficos.py
"""
import pandas as pd
import numpy as np
import plotly.express as px
from fpdf import FPDF
from sqlalchemy import create_engine
from core.settings import settings
from dotenv import load_dotenv
import logging

# Carrega variáveis de ambiente e configurações
load_dotenv()

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("relatorio_graficos")

# Usa URL síncrona (remove +asyncpg se presente)
sync_url = str(settings.DATABASE_URL).replace("+asyncpg", "")
engine = create_engine(sync_url, echo=False, future=True)


def fetch_taxpayer_data() -> pd.DataFrame:
    """
    Busca dados de contribuintes diretamente do banco.
    Retorna DataFrame com colunas: 'cpf', 'amount_due', 'amount_paid'.
    """
    query = (
        "SELECT tax_id AS cpf, amount_due AS amount_due, "
        "amount_paid AS amount_paid "
        "FROM taxpayer_data"  # Split long line
    )
    df = pd.read_sql(query, engine)
    return df


def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Valida o DataFrame, removendo valores negativos e nulos.
    """
    df = df[(df["amount_due"] >= 0) & (df["amount_paid"] >= 0)]
    df = df.dropna(subset=["cpf", "amount_due", "amount_paid"])
    return df


def create_graphs(df: pd.DataFrame):
    """
    Gera e salva quatro gráficos principais:
    1. Inconsistências por contribuinte
    2. Distribuição de valores pagos
    3. Evolução do pagamento ao longo do tempo
    4. Proporção de inconsistências
    """
    # Marca inconsistências quando valor devido != valor pago
    df["Inconsistência"] = np.where(df["amount_due"] != df["amount_paid"], "Sim", "Não")

    # Adiciona coluna de mês aleatório para simulação de evolução
    df["Mes"] = np.random.choice(
        ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun"],
        size=len(df),
    )

    # Gráfico 1: Inconsistências por contribuinte
    graf1 = px.bar(
        df,
        x="cpf",
        color="Inconsistência",
        title="Inconsistências por Contribuinte",
    )
    graf1.write_image("grafico_inconsistencia.png")

    # Gráfico 2: Distribuição de Valores Pagos
    graf2 = px.histogram(df, x="amount_paid", title="Distribuição de Valores Pagos")
    graf2.write_image("grafico_distribuicao_pago.png")

    # Gráfico 3: Evolução do Pagamento de Impostos
    df_month = df.groupby("Mes").sum().reset_index()
    graf3 = px.line(
        df_month,
        x="Mes",
        y="amount_paid",
        title="Evolução do Pagamento de Impostos",
    )
    graf3.write_image("grafico_evolucao.png")

    # Gráfico 4: Proporção de Inconsistências
    graf4 = px.pie(df, names="Inconsistência", title="Proporção de Inconsistências")
    graf4.write_image("grafico_status_inconsistencia.png")

    return graf1, graf2, graf3, graf4


def export_to_excel(df: pd.DataFrame):
    """
    Exporta dados validados para Excel com formatação condicional.
    """
    with pd.ExcelWriter("relatorio_fiscal.xlsx", engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Dados Fiscais")
        worksheet = writer.sheets["Dados Fiscais"]
        # Formato para valores altos.
        # Fixed: Added a period at the end of the comment.
        fmt = writer.book.add_format({"bold": True, "font_color": "red"})
        worksheet.conditional_format(
            "B2:B{}".format(len(df) + 1),
            {
                "type": "cell",
                "criteria": ">",
                "value": 10000,
                "format": fmt,
            },
        )


def create_pdf():
    """
    Gera um PDF agregando o gráfico de inconsistências.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Relatório Fiscal Simulado", 0, 1, "C")

    # Insere o gráfico de inconsistências
    pdf.ln(10)
    pdf.image("grafico_inconsistencia.png", x=10, y=30, w=180)
    pdf.ln(100)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(
        0,
        10,
        "O gráfico acima mostra as inconsistências identificadas nos "
        "valores declarados vs pagos.",
    )  # Fixed: Split long line

    pdf.output("relatorio_fiscal.pdf")


# Função principal
def main():
    logger.info("Iniciando geração de relatório fiscal...")
    df = fetch_taxpayer_data()
    df = validate_data(df)
    create_graphs(df)
    export_to_excel(df)
    create_pdf()
    logger.info("Relatório gerado com sucesso.")


if __name__ == "__main__":
    main()
