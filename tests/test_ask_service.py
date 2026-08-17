from unittest.mock import patch

from enterprise_ai_data_assistant.services.ask_service import generate_answer


@patch("enterprise_ai_data_assistant.services.ask_service.retrieve_chunks")
def test_generate_answer(mock_retrieve_chunks):
    mock_retrieve_chunks.return_value = [
        {
            "chunk_id": "1",
            "title": "sample.pdf",
            "chunk": "Product A has a 2-year warranty.",
        }
    ]

    result = generate_answer("What is the warranty for Product A?")

    assert result["question"] == "What is the warranty for Product A?"
    assert len(result["sources"]) == 1
    assert result["sources"][0]["title"] == "sample.pdf"
