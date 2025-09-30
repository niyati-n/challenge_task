from typing import Dict
from fastapi import APIRouter
from app.services.chat_service import get_chat_completion

router = APIRouter()

# POST /v1/chat/completions
@router.post("/completions")
async def chat_completions(payload: Dict):
    response = get_chat_completion(payload)
    return response
