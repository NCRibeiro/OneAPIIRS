from pydantic import BaseModel, Field
from typing import Dict

class RawCOBOLInput(BaseModel):
    raw_data: str = Field(..., description="Dados brutos no formato COBOL")

class TransformedResponse(BaseModel):
    parsed_data: Dict[str, str] = Field(..., description="Dados transformados e estruturados")
