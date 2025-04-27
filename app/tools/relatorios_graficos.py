import pandas as pd
import numpy as np
import plotly.express as px
from fpdf import FPDF
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Carregar as variáveis de ambiente
load_dotenv()

# ============================
# Conexão com o Banco de Dados
# ============================
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

# Função para buscar os dados fiscais
def fetch_taxpayer_data():
    query = "SELECT * FROM taxpayer_data;"  # Ajuste conforme necessário
    df = pd.read_sql(query, engine)
    return df

# Função para validar os dados
def validate_data(df):
    # Garantir que 'Valor Declarado' e 'Valor Pago' não sejam negativos
    df = df[df['Valor Declarado'] >= 0]
    df = df[df['Valor Pago'] >= 0]
    
    # Garantir que não haja valores ausentes
    df = df.dropna(subset=['Tipo de Imposto', 'Valor Declarado', 'Valor Pago', 'Status Auditoria', 'Mes'])
    
    return df

# Função para gerar gráficos
def create_graphs(df):
    # Gráfico 1: Inconsistências por Tipo de Imposto
    grafico_inconsistencia = px.bar(
        df, x='Tipo de Imposto', color='Inconsistência', title="Inconsistências por Tipo de Imposto"
    )

    # Gráfico 2: Distribuição de Valores Pagos
    grafico_distribuicao_pago = px.histogram(
        df, x='Valor Pago', title="Distribuição de Valores Pagos"
    )

    # Gráfico 3: Evolução do Pagamento de Impostos
    grafico_evolucao = px.line(
        df.groupby('Mes').sum().reset_index(), x='Mes', y='Valor Pago', title="Evolução do Pagamento de Impostos"
    )

    # Gráfico 4: Status de Auditoria
    grafico_status_auditoria = px.pie(
        df, names='Status Auditoria', title="Status de Auditoria das Transações"
    )

    # Salvando os gráficos como imagens
    grafico_inconsistencia.write_image("grafico_inconsistencia.png")
    grafico_distribuicao_pago.write_image("grafico_distribuicao_pago.png")
    grafico_evolucao.write_image("grafico_evolucao.png")
    grafico_status_auditoria.write_image("grafico_status_auditoria.png")
    
    return grafico_inconsistencia, grafico_distribuicao_pago, grafico_evolucao, grafico_status_auditoria

# Função para exportar dados para Excel
def export_to_excel(df):
    with pd.ExcelWriter("relatorio_fiscal.xlsx", engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Dados Fiscais")
        
        # Obtendo o objeto de planilha
        worksheet = writer.sheets["Dados Fiscais"]
        
        # Aplicando formatação condicional
        worksheet.conditional_format('C2:C101', {'type': 'cell', 'criteria': '>', 'value': 10000, 'format': {'bold': True, 'font_color': 'red'}})

# Função para gerar o PDF
def create_pdf():
    pdf = FPDF()
    pdf.add_page()

    # Título
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Relatório Fiscal Simulado", ln=True, align="C")

    # Adicionando gráficos ao PDF
    pdf.ln(10)
    pdf.image("grafico_inconsistencia.png", x=10, y=30, w=180)
    pdf.ln(100)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt="O gráfico acima mostra as inconsistências por tipo de imposto.")

    # Salvando o PDF
    pdf.output("relatorio_fiscal.pdf")

# Função principal
def main():
    # Carregando os dados
    df_transacoes = fetch_taxpayer_data()

    # Validando os dados
    df_transacoes = validate_data(df_transacoes)

    # Adicionando a coluna de inconsistência
    df_transacoes['Inconsistência'] = np.where(df_transacoes['Valor Declarado'] != df_transacoes['Valor Pago'], 'Sim', 'Não')
    df_transacoes['Mes'] = np.random.choice(['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'], size=len(df_transacoes))

    # Criando os gráficos
    create_graphs(df_transacoes)

    # Exportando para Excel
    export_to_excel(df_transacoes)

    # Criando o PDF
    create_pdf()

# Rodar o script principal
if __name__ == "__main__":
    main()
