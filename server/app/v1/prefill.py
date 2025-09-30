from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.prefill_service import extract_and_save_payment_info

router = APIRouter()

class PrefillRequest(BaseModel):
    email_text: str
    model: str

# POST /v1/prefill
@router.post("/prefill")
async def prefill(request: PrefillRequest):
    try:
        extract_and_save_payment_info(request.email_text, request.model)
        return {"success": True, "message": "data extracted and written"}
    except Exception as e:
        return {"success": False, "message": str(e)}
