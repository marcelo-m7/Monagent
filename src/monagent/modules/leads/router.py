from fastapi import APIRouter
from pydantic import BaseModel, EmailStr

router = APIRouter()

class BaseLead(BaseModel):
    email: EmailStr
    name: str | None = None
    company: str | None = None
    revenue: int | None = None
    pain: str | None = None  # dor principal
    json_data: dict | None = None  # campo genérico para dados adicionais

@router.post("/base-lead")
def create_lead(payload: BaseLead):
    # MVP: só retorna. Depois pluga Supabase/DB/CRM/Resend/Stripe etc.
    return {"created": True, "lead": payload.model_dump()}

