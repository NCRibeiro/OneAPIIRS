import os
from typing import Any, Sequence
import dash
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.express as px
from dash import dcc, html
from dash.dependencies import Input, Output
from fpdf import FPDF
from pandas import DataFrame

from dash.dcc import send_file  # type: ignore
from dash.dcc import send_data_frame  # type: ignore

# --- Inicialização ---
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# --- Dados simulados ---
rng = np.random.default_rng(42)  # Generator moderno, evita warnings SonarQube
n = 100
tipos = ["ICMS", "IPI", "ISS"]
status = [
    "Auditoria Concluída",
    "Em Auditoria",
    "Sem Auditoria",
    "Inconsistência Detectada",
]

df = pd.DataFrame(
    {
        "ID": range(1, n + 1),
        "Tipo": rng.choice(tipos, n),
        "Declarado": np.round(rng.uniform(500, 10000, n), 2),
        "Pago": np.round(rng.uniform(500, 10000, n), 2),
        "Status": rng.choice(status, n),
    }
)
df["Inconsistência"] = np.where(df["Declarado"] != df["Pago"], "Sim", "Não")
df["Mês"] = rng.choice(["Jan", "Fev", "Mar", "Abr", "Mai", "Jun"], n)


# --- Funções auxiliares ---
def get_dropdown_options(values: list[str]) -> Sequence[dict[str, Any]]:
    return [{"label": v, "value": v} for v in values]


# --- Layout ---
app.layout = html.Div(
    [
        html.H1("Dashboard Fiscal Interativo", style={"textAlign": "center"}),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                        id="dropdown-imposto",
                        options=[{"label": t, "value": t} for t in tipos],  # type: ignore
                        value=tipos[0],
                        clearable=False,
                    ),
                    width=4,
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id="dropdown-mes",
                        options=[{"label": str(m), "value": str(m)} for m in df["Mês"].unique()],  # type: ignore
                        value=df["Mês"].iloc[0],
                        clearable=False,
                    ),
                    width=4,
                ),
            ],
            style={"marginBottom": "20px"},
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="grafico_inconsistencia"), width=6),
                dbc.Col(dcc.Graph(id="grafico_distribuicao_pago"), width=6),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="grafico_evolucao"), width=6),
                dbc.Col(dcc.Graph(id="grafico_status"), width=6),
            ]
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button("Baixar PDF", id="btn-pdf", color="primary", className="d-grid"),
                    width=3,
                ),
                dbc.Col(
                    dbc.Button("Baixar Excel", id="btn-excel", color="secondary", className="d-grid"),
                    width=3,
                ),
            ],
            justify="start",
            style={"marginBottom": "20px"},
        ),
        dcc.Download(id="download-pdf"),
        dcc.Download(id="download-excel"),
    ]
)


# --- Callback de atualização de gráficos ---
@app.callback(
    Output("grafico_inconsistencia", "figure"),
    Output("grafico_distribuicao_pago", "figure"),
    Output("grafico_evolucao", "figure"),
    Output("grafico_status", "figure"),
    Input("dropdown-imposto", "value"),
    Input("dropdown-mes", "value"),
)
def atualizar(imposto: str, mes: str) -> tuple[Any, Any, Any, Any]:
    dff = df[(df["Tipo"] == imposto) & (df["Mês"] == mes)]
    f1 = px.bar(dff, x="Tipo", color="Inconsistência", title="Inconsistências")
    f2 = px.histogram(dff, x="Pago", title="Distribuição de Valores Pagos")
    sum_mes = dff.groupby("Mês")["Pago"].sum().reset_index()
    f3 = px.line(sum_mes, x="Mês", y="Pago", title="Evolução de Pagamentos")
    f4 = px.pie(dff, names="Status", title="Status Auditoria")
    return f1, f2, f3, f4


# --- Geração de PDF em disco (cleanup após envio) ---
def criar_pdf(dataframe: DataFrame) -> str:
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "relatorio.pdf")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Relatório Fiscal Simulado", ln=1, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 8, "Este relatório foi gerado dinamicamente.")
    pdf.output(path)
    return path


@app.callback(
    Output("download-pdf", "data"),
    Input("btn-pdf", "n_clicks"),
    prevent_initial_call=True,
)
def baixar_pdf(n: int) -> Any:
    return send_file(criar_pdf(df))  # type: ignore


@app.callback(
    Output("download-excel", "data"),
    Input("btn-excel", "n_clicks"),
    prevent_initial_call=True,
)
def baixar_excel(n: int) -> Any:
    return send_data_frame(df.to_excel, "relatorio.xlsx", sheet_name="Dados", index=False)  # type: ignore


# --- Run ---
if __name__ == "__main__":
    app.run_server(debug=True)
