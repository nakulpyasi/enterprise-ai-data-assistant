from enterprise_ai_data_assistant.services.retrieval_service import retrieve_chunks


def generate_answer(question: str) -> str:
    chunks = retrieve_chunks(question)
    return {"question": question, "sources": chunks}
