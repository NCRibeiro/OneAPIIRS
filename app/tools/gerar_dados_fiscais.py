import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import TaxpayerData, LegacyData, AuditLog  # Importando os modelos definidos


# Configuração do banco de dados PostgreSQL com SQLAlchemy
DATABASE_URL = "postgresql://postgres:senha@localhost:5432/ape_fiscal_db"  # Substitua 'senha' pela sua senha
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Gerando dados simulados de transações fiscais
np.random.seed(42)

# Definindo variáveis
n_transacoes = 100  # número de transações
tipos_imposto = ['ICMS', 'IPI', 'ISS']
status_auditoria = ['Auditoria Concluída', 'Em Auditoria', 'Sem Auditoria', 'Inconsistência Detectada']

# Criando um DataFrame com dados simulados
df_transacoes = pd.DataFrame({
    'ID Transação': range(1, n_transacoes + 1),
    'Tipo de Imposto': np.random.choice(tipos_imposto, size=n_transacoes),
    'Valor Declarado': np.round(np.random.uniform(500, 10000, size=n_transacoes), 2),
    'Valor Pago': np.round(np.random.uniform(500, 10000, size=n_transacoes), 2),
    'Status Auditoria': np.random.choice(status_auditoria, size=n_transacoes)
})

# Adicionando uma coluna de inconsistências para simular problemas de auditoria
df_transacoes['Inconsistência'] = np.where(df_transacoes['Valor Declarado'] != df_transacoes['Valor Pago'], 'Sim', 'Não')

# Exibindo as primeiras linhas do DataFrame
print(df_transacoes.head())

# Função para inserir os dados no banco de dados
def insert_taxpayer_data():
    db = SessionLocal()  # Cria uma sessão para interagir com o banco

    try:
        for _, row in df_transacoes.iterrows():
            # Criando um contribuinte moderno
            taxpayer = TaxpayerData(
                name=f"Contribuinte {row['ID Transação']}",
                tax_id=str(np.random.randint(100000000, 999999999)),
                region="São Paulo",  # Definindo a região como exemplo
                payment_status="Paid" if row['Valor Pago'] >= row['Valor Declarado'] else "Unpaid",
                amount_due=row['Valor Declarado'],
                amount_paid=row['Valor Pago']
            )
            
            db.add(taxpayer)
            db.commit()
            db.refresh(taxpayer)  # Atualiza o objeto com o ID gerado no banco

            # Adicionando dados legados para o contribuinte
            legacy_data = LegacyData(
                record_data=f"Histórico de transação de {row['Tipo de Imposto']}",
                taxpayer_id=taxpayer.id
            )

            db.add(legacy_data)
            db.commit()  # Salva os dados legados

            # Adicionando registro de auditoria
            audit_log = AuditLog(
                taxpayer_id=taxpayer.id,
                action="Transação Registrada",
                timestamp=pd.Timestamp.now(),
                details=f"Transação de {row['Tipo de Imposto']} registrada com valor de {row['Valor Declarado']}"
            )
            db.add(audit_log)
            db.commit()  # Salva o log de auditoria

    except Exception as e:
        print(f"Erro ao inserir dados: {e}")
        db.rollback()  # Reverte em caso de erro
    finally:
        db.close()  # Fecha a sessão

# Chama a função para inserir os dados no banco de dados
insert_taxpayer_data()

