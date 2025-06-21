# app/services/bigquery_service.py
from core.settings import settings


def query_rows(sql: str) -> list[dict]:
    """
    Executa a query SQL no BigQuery e retorna lista de dicionários.
    """
    job = settings._bq_client.query(sql)
    result = job.result()  # bloquear até completar
    return [dict(row) for row in result]
