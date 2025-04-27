import plotly.express as px
import pandas as pd
import numpy as np

# Usando os mesmos dados do exemplo anterior
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

# Criando um gráfico de barras de inconsistências por tipo de imposto
fig = px.bar(df_transacoes, x='Tipo de Imposto', color='Inconsistência', title="Inconsistências por Tipo de Imposto")
fig.show()
