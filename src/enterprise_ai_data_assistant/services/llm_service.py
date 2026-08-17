from openai import AzureOpenAI
from enterprise_ai_data_assistant.config import settings

client = AzureOpenAI(
    api_version="2024-12-01-preview",
    azure_endpoint=settings.azure_openai_endpoint,
    api_key=settings.azure_openai_api_key,
)


def generate_grounded_answer(question: str, chunks: list[dict]) -> str:
    context = "\n\n".join(chunk["chunk"] for chunk in chunks)

    response = client.chat.completions.create(
        model=settings.azure_openai_model,
        messages=[
            {
                "role": "system",
                "content": (
                    "Answer only from the provided context. "
                    "If the answer is not in the context, say you don't know."
                ),
            },
            {
                "role": "user",
                "content": f"""
Context:
{context}

Question:
{question}
""",
            },
        ],
    )

    return response.choices[0].message.content
