from fastapi import APIRouter, Depends, HTTPException, Query, status

from dependencies import get_current_user
from app.schemas.external import ExternalCheckResult
from app.services.external import (
    check_debts,
    fetch_income_score,
    validate_cpf_externally,
)
from core.settings import settings

router = APIRouter(
    prefix=f"{settings.API_PREFIX}/external",
    tags=["External Integrations"],
    dependencies=[Depends(get_current_user)],
)


@router.get(
    "/check",
    response_model=ExternalCheckResult,
    status_code=status.HTTP_200_OK,
    summary="Valida CPF e retorna score e dívidas",
)
async def external_check(
    cpf: str = Query(
        ..., min_length=14, max_length=14, description="CPF no formato XXX.XXX.XXX-XX"
    ),
) -> ExternalCheckResult:
    try:
        valid = await validate_cpf_externally(cpf)
        score = await fetch_income_score(cpf)
        debts = await check_debts(cpf)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Erro ao consultar serviço externo: {e}",
        )
    return ExternalCheckResult(
        cpf=cpf, is_valid=valid, income_score=score, has_debts=debts
    )


@router.get(
    "/banks",
    status_code=status.HTTP_200_OK,
    summary="Lista bancos suportados (mock)",
)
async def get_supported_banks():
    return {
        "banks": [
            {"name": "Bank of Mars", "code": "001"},
            {"name": "Lunar Savings", "code": "002"},
            {"name": "Intergalactic Credit Union", "code": "003"},
        ]
    }
