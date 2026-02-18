from fastapi import APIRouter
from pydantic import BaseModel, EmailStr

router = APIRouter()

class LeadCreate(BaseModel):
    email: EmailStr
    name: str | None = None
    company: str | None = None
    pain: str | None = None  # dor principal

@router.post("")
def create_lead(payload: LeadCreate):
    # MVP: só retorna. Depois pluga Supabase/DB/CRM/Resend/Stripe etc.
    return {"created": True, "lead": payload.model_dump()}
