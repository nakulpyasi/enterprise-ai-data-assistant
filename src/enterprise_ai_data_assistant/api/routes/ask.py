from fastapi import APIRouter
from enterprise_ai_data_assistant.schemas import AskRequest
from enterprise_ai_data_assistant.services.ask_service import generate_answer

router = APIRouter()

@router.post("/ask")
def ask(request:AskRequest):
    return {"answer": generate_answer(request.question)}