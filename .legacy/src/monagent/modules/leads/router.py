from fastapi import APIRouter, Request
from pydantic import BaseModel, EmailStr
from monagent.core.supabase_client import supabase_service
from monagent.modules.leads.service import insert_lead

router = APIRouter()

class LeadCreate(BaseModel):
    email: EmailStr
    name: str | None = None
    company: str | None = None
    pain: str | None = None

    source: str | None = None
    campaign: str | None = None
    medium: str | None = None
    content: str | None = None
    term: str | None = None

@router.post("")
def create_lead(payload: LeadCreate, request: Request):
    sb = supabase_service()

    ip = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")

    lead = insert_lead(
        sb,
        {
            **payload.model_dump(),
            "ip": ip,
            "user_agent": user_agent,
        },
    )
    return {"created": True, "lead_id": lead["id"]}
