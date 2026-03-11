from fastapi import APIRouter, Request
from pydantic import BaseModel, EmailStr
# from monagent.core.models import 
# from monagent.modules.generator.service import 

router = APIRouter()

class Generator(BaseModel):
    models: list[str]
    name: str

@router.post("generator")
def create_generator(payload: Generator, request: Request):
    pass
    # return {"created": True, "generator_id": generator["id"]}
