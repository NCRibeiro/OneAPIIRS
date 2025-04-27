from fastapi import APIRouter, HTTPException, status, Query
from app.schemas.external import ExternalCheckResult
from app.services.external.federal_services import validate_cpf_externally, fetch_income_score, check_debts

router = APIRouter(
    prefix="/external", 
    tags=["external integrations"]
)

@router.get("/check", response_model=ExternalCheckResult)
async def external_check(cpf: str = Query(..., min_length=14, max_length=14, description="CPF no formato XXX.XXX.XXX-XX")):
    return ExternalCheckResult(
        cpf=cpf,
        is_valid=validate_cpf_externally(cpf),
        income_score=fetch_income_score(cpf),
        has_debts=check_debts(cpf)
    )

@router.get("/banks")
async def get_supported_banks():
    return {
        "banks": [
            {"name": "Bank of Mars", "code": "001"},
            {"name": "Lunar Savings", "code": "002"},
            {"name": "Intergalatic Credit Union", "code": "003"}
        ]
    }