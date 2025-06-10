from datetime import datetime
from typing import Dict, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class RawCOBOLInput(BaseModel):
    """Entrada bruta em formato legado COBOL."""
    raw_data: str = Field(
        ...,
        description="Texto bruto no estilo COBOL com dados fiscais antigos.",
    )


class TransformedResponse(BaseModel):
    """Resposta após transformação COBOL → JSON."""
    id: UUID = Field(..., description="UUID único da transformação")
    timestamp: datetime = Field(..., description="Data e hora do processamento (UTC)")
    parsed_data: Dict[str, str] = Field(
        ..., description="Dados convertidos para JSON moderno"
    )
    preview: Optional[str] = Field(
        None,
        description="Prévia dos primeiros 100 caracteres da entrada original",
    )
