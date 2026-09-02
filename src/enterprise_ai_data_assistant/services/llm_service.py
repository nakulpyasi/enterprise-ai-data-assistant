from openai import AzureOpenAI
from enterprise_ai_data_assistant.config import settings

client = AzureOpenAI(
    api_version="2024-12-01-preview",
    azure_endpoint=settings.azure_openai_endpoint,
    api_key=settings.azure_openai_api_key,
)

SUPPORT_TICKETS_SCHEMA = """
Table: support_tickets

Columns:
- id: integer
- product: varchar
- status: varchar
- severity: varchar
- created_at: timestamp
"""


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


def generate_sql(question: str) -> str:
    response = client.chat.completions.create(
        model=settings.azure_openai_model,
        messages=[
            {
                "role": "system",
                "content": f"""
        You convert natural-language questions into PostgreSQL SELECT queries.

        Use only this schema:

        {SUPPORT_TICKETS_SCHEMA}

        Rules:
        - Return only SQL.
        - Generate only SELECT queries.
        - Do not use INSERT, UPDATE, DELETE, DROP, ALTER, or TRUNCATE.
        - Do not invent tables or columns.
        """,
            },
            {
                "role": "user",
                "content": question,
            },
        ],
    )

    sql = response.choices[0].message.content.strip()
    sql = sql.replace("```sql", "").replace("```", "").strip()
    return sql


def generate_sql_answer(
    question: str,
    sql: str,
    rows: list[dict],
) -> str:
    response = client.chat.completions.create(
        model=settings.azure_openai_model,
        messages=[
            {
                "role": "system",
                "content": (
                    "Answer the user's question using only the SQL query result. "
                    "Be concise. Do not invent information."
                ),
            },
            {
                "role": "user",
                "content": f"""
Question:
{question}

SQL:
{sql}

Result:
{rows}
""",
            },
        ],
    )

    return response.choices[0].message.content.strip()
