from enterprise_ai_data_assistant.services.retrieval_service import retrieve_chunks
from enterprise_ai_data_assistant.services.llm_service import generate_grounded_answer


def generate_answer(question: str) -> str:
    chunks = retrieve_chunks(question)

    answer = generate_grounded_answer(question, chunks=chunks)
    return {"answer": answer, "sources": chunks}
