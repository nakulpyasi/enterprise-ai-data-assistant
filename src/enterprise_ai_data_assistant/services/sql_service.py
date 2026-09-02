from sqlalchemy import text
from enterprise_ai_data_assistant.database import engine
from enterprise_ai_data_assistant.services.llm_service import (
    generate_sql,
    generate_sql_answer,
)


def get_all_support_tickets() -> list[dict]:
    with engine.connect() as connection:
        result = connection.execute(text("select * from support_tickets;"))

        return [dict(row._mapping) for row in result]


def validate_read_only_query(query: str):
    normalized = query.strip().lower()

    if not normalized.startswith("select"):
        raise ValueError("Only select queries are allowed")


def execute_read_only_query(query: str):
    validate_read_only_query(query)
    with engine.connect() as connection:
        result = connection.execute(text(query))

        return [dict(row._mapping) for row in result]


def answer_from_sql(question: str) -> dict:
    sql = generate_sql(question)
    rows = execute_read_only_query(sql)
    answer = generate_sql_answer(question, sql, rows)

    return {"answer": answer, "sql": sql, "data": rows}
