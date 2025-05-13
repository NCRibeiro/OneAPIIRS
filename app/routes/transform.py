# app/routers/transform.py

import re
from datetime import datetime
from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, Body, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.dependencies import get_current_user
from app.services.transformer import cobol_to_json
from core.settings import settings

router = APIRouter(
    prefix=f"{settings.api_prefix}/transform",
    tags=["Transformador"],
    dependencies=[Depends(get_current_user)],
)


# Entrada
class RawCOBOLInput(BaseModel):
    raw_data: str = Field(
        ...,
        min_length=10,
        description="Texto bruto estilo COBOL com dados fiscais antigos.",
    )


# Saída
class TransformedResponse(BaseModel):
    id: str = Field(..., description="UUID da transformação")
    timestamp: str = Field(..., description="Timestamp UTC do processamento")
    parsed_data: dict = Field(..., description="Dados transformados para JSON moderno")
    preview: Optional[str] = Field(
        None,
        description="Prévia dos primeiros 100 caracteres da entrada original",
    )


@router.post(
    "/",
    response_model=TransformedResponse,
    status_code=status.HTTP_200_OK,
    summary="Transforma string estilo COBOL em JSON moderno",
)
async def transform_data(
    payload: RawCOBOLInput = Body(...), user: str = Depends(get_current_user)
):
    """
    Transforma uma string estilo COBOL em JSON moderno. A resposta inclui:
    - ID de rastreamento único
    - Timestamp UTC do processamento
    - Dados parseados
    - Pré-visualização opcional da string original
    """
    raw = payload.raw_data.strip()

    # Validação do padrão COBOL
    pattern = r"NOME:\s+.+?\s+NASC:\s+\d{4}-\d{2}-\d{2}\s+REND:\s+\$\d+\.\d+"
    if not re.search(pattern, raw):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Formato da string não corresponde ao estilo COBOL "
                "esperado. Ex: 'NOME: JOHN DOE NASC: 1960-05-15 REND: "
                "$45000.00'"
            ),
        )

    # Transformação
    transformed = cobol_to_json(raw)
    if not transformed or "erro" in transformed:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=transformed.get("erro", "Erro desconhecido ao transformar dados."),
        )

    return TransformedResponse(
        id=str(uuid4()),
        timestamp=datetime.utcnow().isoformat() + "Z",
        parsed_data=transformed,
        preview=(raw[:100] + "..." if len(raw) > 100 else raw),
    )
