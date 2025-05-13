# tools/gerar_dados_fiscais.py

"""
Script de geração e inserção de dados fiscais simulados.
Uso:
    python tools/gerar_dados_fiscais.py
"""
import logging
from datetime import datetime

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Importa configurações e modelos do projeto
from core.settings import settings
from app.db.models import TaxpayerData, LegacyData, AuditLog

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("gerar_dados_fiscais")

# URL síncrona (retira +asyncpg se presente)
sync_url = str(settings.DATABASE_URL).replace(
    "+asyncpg",
    "",
)  # Convert to string

# Cria engine e sessão
engine = create_engine(sync_url, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def generate_dataframe(n: int = 100) -> pd.DataFrame:
    """Gera um DataFrame com transações fiscais simuladas."""
    np.random.seed(42)  # Fixed: Removed trailing comma
    tipos_imposto = ["ICMS", "IPI", "ISS"]
    status_auditoria = [
        "Concluída",
        "Em Auditoria",
        "Sem Auditoria",
        "Inconsistência",
    ]  # noqa: E501

    df = pd.DataFrame(
        {
            "id_transacao": np.arange(1, n + 1),
            "tipo_imposto": np.random.choice(tipos_imposto, size=n),
            "valor_declarado": np.round(np.random.uniform(500, 10000, size=n), 2),
            "valor_pago": np.round(np.random.uniform(500, 10000, size=n), 2),
            "status_auditoria": np.random.choice(
                status_auditoria, size=n
            ),  # noqa: E501
        }
    )
    df["inconsistencia"] = df["valor_declarado"] != df["valor_pago"]
    return df


def insert_simulated_data(df: pd.DataFrame) -> None:
    """Insere os dados do DataFrame no banco de dados."""
    db = SessionLocal()
    try:  # noqa: E501
        for _, row in df.iterrows():
            # Cria entrada de contribuinte moderno
            taxpayer = TaxpayerData(
                name=f"Contribuinte {int(row['id_transacao'])}",
                tax_id=str(np.random.randint(100000000, 999999999)),
                region="BR-SP",
                payment_status=(
                    "Paid" if row["valor_pago"] >= row["valor_declarado"] else "Unpaid"
                ),
                # noqa: E501
                amount_due=row["valor_declarado"],
                amount_paid=row["valor_pago"],
            )

            db.add(taxpayer)
            db.flush()  # Garante que 'id' seja preenchido

            # Cria registro legado
            legacy = LegacyData(
                record_data=f"Transação {row['tipo_imposto']}",
                # noqa: E501
                taxpayer_id=taxpayer.id,
            )
            db.add(legacy)

            # Cria log de auditoria
            log = AuditLog(
                # noqa: E501
                taxpayer_id=taxpayer.id,
                action="Transação Registrada",
                timestamp=datetime.utcnow(),
                details=(
                    f"Tipo: {row['tipo_imposto']}, "  # noqa: E501
                    f"Declarado: {row['valor_declarado']}, "  # noqa: E501
                    f"Pago: {row['valor_pago']}"  # noqa: E501
                ),
            )
            db.add(log)

        db.commit()
        logger.info("Todos os dados inseridos com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao inserir dados: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    logger.info("Iniciando geração de dados simulados...")
    df = generate_dataframe(n=100)
    insert_simulated_data(df)
    logger.info("Script concluído.")
