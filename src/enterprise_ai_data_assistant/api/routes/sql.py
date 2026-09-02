from fastapi import APIRouter
from enterprise_ai_data_assistant.services.sql_service import answer_from_sql
from enterprise_ai_data_assistant.schemas import AskRequest

router = APIRouter()


@router.post("/ask-sql")
def ask_sql(request: AskRequest):
    return answer_from_sql(request.question)
