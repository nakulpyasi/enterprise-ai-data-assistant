from fastapi import APIRouter
from enterprise_ai_data_assistant.schemas import AskRequest, AskResponse
from enterprise_ai_data_assistant.services.orchestration_service import orchestrate

router = APIRouter()


@router.post("/ask", response_model=AskResponse)
async def ask(request: AskRequest):
    result = await orchestrate(request.question)
    return result
