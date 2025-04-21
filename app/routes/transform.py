from fastapi import APIRouter, Body, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional
from uuid import uuid4
from datetime import datetime
import re

from app.core.security import get_current_user
from app.services.transformer import cobol_to_json

router = APIRouter(
    prefix="/transform",
    tags=["Transformador"]
)

# Entrada
class RawCOBOLInput(BaseModel):
    """
    Payload de entrada com string estilo COBOL para transformação.
    """
    raw_data: str = Field(..., min_length=10, description="Texto bruto no estilo COBOL com dados fiscais antigos.")

# Saída
class TransformedResponse(BaseModel):
    """
    Estrutura da resposta da transformação com metadados para rastreamento.
    """
    id: str = Field(..., description="Identificador único da transformação (UUID)")
    timestamp: str = Field(..., description="Data e hora do processamento")
    parsed_data: dict = Field(..., description="Dados transformados em estrutura JSON moderna")
    preview: Optional[str] = Field(None, description="Resumo da entrada bruta")

@router.post("/", response_model=TransformedResponse, status_code=status.HTTP_200_OK)
def transform_data(
    payload: RawCOBOLInput = Body(...),
    user: str = Depends(get_current_user)
):
    """
    Transforma uma string estilo COBOL em JSON moderno. A resposta inclui:
    - ID de rastreamento único
    - Timestamp UTC do processamento
    - Dados parseados
    - Pré-visualização opcional da string original
    """
    raw = payload.raw_data.strip()

    # Validação de padrão COBOL-style aprimorado
    if not re.search(r"NOME:\s+.+?\s+NASC:\s+\d{4}-\d{2}-\d{2}\s+REND:\s+\$\d+", raw):
        raise HTTPException(
            status_code=400,
            detail="Formato da string não parece estilo COBOL esperado. Ex: 'NOME: JOHN DOE NASC: 1960-05-15 REND: $45000.00'"
        )

    # Transformação
    transformed = cobol_to_json(raw)
    if not transformed or "erro" in transformed:
        raise HTTPException(
            status_code=422,
            detail=transformed.get("erro", "Erro desconhecido ao transformar dados.")
        )

    return TransformedResponse(
        id=str(uuid4()),
        timestamp=datetime.utcnow().isoformat() + "Z",
        parsed_data=transformed,
        preview=raw[:100] + ("..." if len(raw) > 100 else "")
    )
