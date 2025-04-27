import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash.dash import no_update
import io
import base64
from fpdf import FPDF

# Inicializando o app Dash com o tema do Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Gerando dados simulados de transações fiscais
np.random.seed(42)
n_transacoes = 100
tipos_imposto = ['ICMS', 'IPI', 'ISS']
status_auditoria = ['Auditoria Concluída', 'Em Auditoria', 'Sem Auditoria', 'Inconsistência Detectada']

df_transacoes = pd.DataFrame({
    'ID Transação': range(1, n_transacoes + 1),
    'Tipo de Imposto': np.random.choice(tipos_imposto, size=n_transacoes),
    'Valor Declarado': np.round(np.random.uniform(500, 10000, size=n_transacoes), 2),
    'Valor Pago': np.round(np.random.uniform(500, 10000, size=n_transacoes), 2),
    'Status Auditoria': np.random.choice(status_auditoria, size=n_transacoes)
})

df_transacoes['Inconsistência'] = np.where(df_transacoes['Valor Declarado'] != df_transacoes['Valor Pago'], 'Sim', 'Não')
df_transacoes['Mes'] = np.random.choice(['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'], size=n_transacoes)

# Gráficos
grafico_inconsistencia = px.bar(df_transacoes, x='Tipo de Imposto', color='Inconsistência', title="Inconsistências por Tipo de Imposto")
grafico_distribuicao_pago = px.histogram(df_transacoes, x='Valor Pago', title="Distribuição de Valores Pagos")
grafico_evolucao = px.line(df_transacoes.groupby('Mes').sum().reset_index(), x='Mes', y='Valor Pago', title="Evolução do Pagamento de Impostos")
grafico_status_auditoria = px.pie(df_transacoes, names='Status Auditoria', title="Status de Auditoria das Transações")

# Layout do Dash com filtros e download
app.layout = html.Div([
    html.H1("Dashboard Fiscal Interativo", style={'text-align': 'center'}),
    
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='dropdown-imposto',
                options=[{'label': tipo, 'value': tipo} for tipo in tipos_imposto],
                value='ICMS',
                multi=False,
                style={'width': '100%'}
            )
        ], width=4),
        dbc.Col([
            dcc.Dropdown(
                id='dropdown-mes',
                options=[{'label': mes, 'value': mes} for mes in ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun']],
                value='Jan',
                multi=False,
                style={'width': '100%'}
            )
        ], width=4),
    ], style={'margin-bottom': '20px'}),

    dbc.Row([
        dbc.Col(dcc.Graph(figure=grafico_inconsistencia), width=6),
        dbc.Col(dcc.Graph(figure=grafico_distribuicao_pago), width=6),
    ]),

    dbc.Row([
        dbc.Col(dcc.Graph(figure=grafico_evolucao), width=6),
        dbc.Col(dcc.Graph(figure=grafico_status_auditoria), width=6),
    ]),

    html.Br(),
    
    # Botão de download
    dbc.Button("Baixar Relatório (PDF)", id="btn-download-pdf", color="primary", style={'width': '100%', 'margin-bottom': '20px'}),

    dcc.Download(id="download-pdf"),
    dcc.Download(id="download-excel"),
])

# Callback para atualizar gráficos com filtros
@app.callback(
    [Output('grafico_inconsistencia', 'figure'),
     Output('grafico_distribuicao_pago', 'figure'),
     Output('grafico_evolucao', 'figure'),
     Output('grafico_status_auditoria', 'figure')],
    [Input('dropdown-imposto', 'value'),
     Input('dropdown-mes', 'value')]
)
def atualizar_graficos(imposto_selecionado, mes_selecionado):
    # Filtrar dados com base nos filtros selecionados
    df_filtrado = df_transacoes[(df_transacoes['Tipo de Imposto'] == imposto_selecionado) & 
                                (df_transacoes['Mes'] == mes_selecionado)]
    
    grafico_inconsistencia = px.bar(df_filtrado, x='Tipo de Imposto', color='Inconsistência', title="Inconsistências por Tipo de Imposto")
    grafico_distribuicao_pago = px.histogram(df_filtrado, x='Valor Pago', title="Distribuição de Valores Pagos")
    grafico_evolucao = px.line(df_filtrado.groupby('Mes').sum().reset_index(), x='Mes', y='Valor Pago', title="Evolução do Pagamento de Impostos")
    grafico_status_auditoria = px.pie(df_filtrado, names='Status Auditoria', title="Status de Auditoria das Transações")
    
    return grafico_inconsistencia, grafico_distribuicao_pago, grafico_evolucao, grafico_status_auditoria

# Função para gerar PDF
def gerar_pdf(df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Relatório Fiscal Simulado", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt="Este é um relatório fiscal simulado com base nos dados gerados para fins de auditoria.")
    pdf.output("relatorio_fiscal.pdf")

    return "relatorio_fiscal.pdf"

# Função para exportar Excel
def gerar_excel(df):
    excel_file = df.to_excel(index=False)
    return excel_file

# Callback para download do PDF
@app.callback(
    Output("download-pdf", "data"),
    Input("btn-download-pdf", "n_clicks"),
    prevent_initial_call=True
)
def gerar_relatorio_pdf(n_clicks):
    if n_clicks is None:
        return no_update
    pdf_file = gerar_pdf(df_transacoes)
    return dcc.send_file(pdf_file)

# Callback para download do Excel
@app.callback(
    Output("download-excel", "data"),
    Input("btn-download-pdf", "n_clicks"),
    prevent_initial_call=True
)
def gerar_relatorio_excel(n_clicks):
    if n_clicks is None:
        return no_update
    excel_file = gerar_excel(df_transacoes)
    return dcc.send_data_frame(excel_file, "relatorio_fiscal.xlsx")

# Rodando o servidor
if __name__ == '__main__':
    app.run_server(debug=True)
