from enterprise_ai_data_assistant.services.sql_service import answer_from_sql


def query_enterprise_database(question: str):
    """Answer a question using the enterprise SQL DB"""
    return answer_from_sql(question)
