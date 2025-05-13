# app/schemas/transform.py

from datetime import datetime
from typing import Dict, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class RawCOBOLInput(BaseModel):
    raw_data: str = Field(
        ...,
        description="Texto bruto no estilo COBOL com dados fiscais antigos.",
    )


class TransformedResponse(BaseModel):
    id: UUID = Field(..., description="UUID único da transformação")
    timestamp: datetime = Field(..., description="Data e hora do processamento (UTC)")
    parsed_data: Dict[str, str] = Field(
        ..., description="Dados convertidos para JSON moderno"
    )
    preview: Optional[str] = Field(
        None, description="Prévia dos primeiros 100 caracteres da entrada"
    )

    class Config:
        orm_mode = True
