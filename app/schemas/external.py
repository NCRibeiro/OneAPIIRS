from pydantic import BaseModel, Field

class ExternalCheckResult(BaseModel):
    cpf: str = Field(..., description="CPF consultado")
    is_valid: bool = Field(..., description="Se o CPF é válido no sistema federal")
    income_score: int = Field(..., description="Score financeiro (simulado)")
    has_debts: bool = Field(..., description="Indica se há pendências financeiras")
