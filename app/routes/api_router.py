# app/routes/api_router.py

import os
import shutil
import json
from typing import Any, List, Dict
from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from core.settings import settings

# Importa todos os módulos de rota existentes
from app.routes import (
    auth,
    taxpayer,
    legacy,
    modern_routes,
    audit,
    external,
    analytics,
)

# importe seus serviços
from app.services.bigquery_service import query_rows
from app.services.storage_service import upload_file
from app.services.pubsub_service import pubsub_message

# roteador principal, já montado sob o prefixo de versão da API
api_router = APIRouter(prefix=settings.API_PREFIX)

# —————————————————————————————————————————————————————————————————————————————
# Rotas existentes
# —————————————————————————————————————————————————————————————————————————————

# autenticação / login / tokens
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Auth"],
)

# rotas de contribuinte (taxpayer)
api_router.include_router(
    taxpayer.router,
    prefix="/taxpayer",
    tags=["Taxpayer"],
)

# rotas legadas (legacy)
api_router.include_router(
    legacy.router,
    prefix="/legacy",
    tags=["Legacy"],
)

# rotas modernas (modern_routes)
api_router.include_router(
    modern_routes.router,
    prefix="/modern",
    tags=["Modern"],
)

# auditoria fiscal (audit)
api_router.include_router(
    audit.router,
    prefix="/audit",
    tags=["Audit"],
)

# integrações externas (external)
api_router.include_router(
    external.router,
    prefix="/external",
    tags=["External"],
)

# análises e relatórios (analytics)
api_router.include_router(
    analytics.router,
    prefix="/analytics",
    tags=["Analytics"],
)

# —————————————————————————————————————————————————————————————————————————————
# Novas rotas de Serviço
# —————————————————————————————————————————————————————————————————————————————


# Modelo para requisição de BigQuery
class QueryRequest(BaseModel):
    sql: str


@api_router.post(
    "/bigquery",
    summary="Executa uma consulta SQL no BigQuery",
    tags=["Serviços Externos"]
)
async def run_bigquery(req: QueryRequest) -> Dict[str, List[Dict[str, Any]]]:
    try:
        resultados = query_rows(req.sql)
        return {"rows": resultados}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no BigQuery: {e}")


# Upload de arquivo para Cloud Storage
@api_router.post(
    "/upload",
    summary="Faz upload de um arquivo para o bucket",
    tags=["Serviços Externos"]
)
async def upload_endpoint(file: UploadFile = File(...)) -> Dict[str, str]:
    # salva temporariamente no /tmp dentro do container
    tmp_path = f"/tmp/{file.filename}"
    with open(tmp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    try:
        public_url = upload_file(tmp_path, file.filename if file.filename else "uploaded_file")
        # remove o arquivo temporário
        os.remove(tmp_path)
        return {"url": public_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no Storage: {e}")


# Modelo para requisição de Pub/Sub
class PublishRequest(BaseModel):
    data: Dict[str, Any]


@api_router.post(
    "/publish",
    summary="Publica uma mensagem no Pub/Sub",
    tags=["Serviços Externos"]
)
async def publish_endpoint(req: PublishRequest) -> Dict[str, str]:
    try:
        message_id = pubsub_message(req.data)  # Chamada com o nome padronizado
        return {"message_id": message_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no Pub/Sub: {e}")
