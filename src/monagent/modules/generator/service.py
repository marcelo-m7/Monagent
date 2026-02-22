from supabase import Client
from monagent.core.settings.models import settings

def insert_lead(sb: Client, data: dict) -> dict:
    # sb = supabase_service()
    resp = sb.schema(settings.SUPABASE_SCHEMA).table("leads").insert(data).execute()
    if not resp.data:
        # resp pode trazer info em resp.error em algumas versões
        raise RuntimeError("Failed to insert lead")
    return resp.data[0]
