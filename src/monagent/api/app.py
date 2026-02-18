from fastapi import FastAPI
from monagent.modules.leads.router import router as leads_router

app = FastAPI(
    title="Monagent",
    version="0.1.0",
    description="Monynha API for leads now, integrations + AI later.",
)

app.include_router(leads_router, prefix="/leads", tags=["leads"])

@app.get("/health")
def health():
    return {"data": "Hi World! :D s2",
            "status": "ok"}