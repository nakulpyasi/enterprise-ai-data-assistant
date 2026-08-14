from enterprise_ai_data_assistant.services.ask_service import generate_answer


def test_generate_answer():
    assert generate_answer("What is RAG?.") == "You asked: What is RAG?."
    
    