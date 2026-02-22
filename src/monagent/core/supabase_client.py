from supabase import create_client, Client
from monagent.core.settings import settings

def supabase_anon() -> Client:
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)

def supabase_service() -> Client:
    # Use APENAS no backend (server-to-server)
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)
