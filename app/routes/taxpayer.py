from fastapi import APIRouter, Body, Depends, HTTPException, status
from pydantic import BaseModel
from app.core.security import get_current_user
from app.services.transformer import cobol_to_json

router = APIRouter(
    prefix="/transform",
    tags=["Transformador"]
)

class RawCOBOLInput(BaseModel):
    raw_data: str

@router.post("/", status_code=status.HTTP_200_OK)
def transform_data(
    payload: RawCOBOLInput,
    user: str = Depends(get_current_user)
):
    """
    Transforma uma string de dados estilo COBOL em JSON moderno.
    
    Exemplo de entrada:
    "NOME: JOHN DOE   NASC: 1960-05-15  REND: $45000.00"
    """
    if not payload.raw_data or len(payload.raw_data.strip()) < 10:
        raise HTTPException(
            status_code=400,
            detail="Entrada inválida. Certifique-se de enviar uma string COBOL-style válida."
        )

    transformed = cobol_to_json(payload.raw_data)

    if "erro" in transformed:
        raise HTTPException(status_code=422, detail=transformed["erro"])

    return transformed
