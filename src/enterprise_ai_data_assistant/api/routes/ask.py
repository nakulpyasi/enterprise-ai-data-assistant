from fastapi import APIRouter
from enterprise_ai_data_assistant.schemas import AskRequest
from enterprise_ai_data_assistant.services.orchestration_service import orchestrate

router = APIRouter()


@router.post("/ask")
async def ask(request: AskRequest):
    answer = await orchestrate(request.question)
    return {"answer": answer}
