from sqlalchemy import text
from sqlalchemy.exc import DBAPIError, OperationalError
from enterprise_ai_data_assistant.database import engine
from enterprise_ai_data_assistant.services.llm_service import (
    generate_sql,
    generate_sql_answer,
)
from sqlglot import exp, parse
from sqlglot.errors import ParseError
from enterprise_ai_data_assistant.exceptions import (
    DatabaseQueryError,
    DatabaseTimeoutError,
    DatabaseUnavailableError,
    UnsafeSQLQueryError,
)

ALLOWED_TABLES = {"support_tickets"}

MAX_QUERY_ROWS = 100

DATABASE_STATEMENT_TIMEOUT_MS = 5_000

FORBIDDEN_SQL_OPERATIONS = {
    "insert",
    "update",
    "alter",
    "delete",
    "merge",
    "create",
    "truncate",
    "grant",
    "revoke",
    "into",
}


def get_all_support_tickets() -> list[dict]:
    with engine.connect() as connection:
        result = connection.execute(text("select * from support_tickets;"))

        return [dict(row._mapping) for row in result]


def validate_read_only_query(query: str) -> None:
    "Allow one read-only select against approved application tables"
    if not isinstance(query, str) or not query.strip():
        raise UnsafeSQLQueryError("SQL query cannot be empty")
    try:
        statements = [
            statement
            for statement in parse(query, read="postgres")
            if statement is not None
        ]
    except ParseError as error:
        raise UnsafeSQLQueryError("Generated SQL is not valid PostgreSQL") from error

    if len(statements) != 1:
        raise UnsafeSQLQueryError("Only one SQL statement is allowed")

    statement = statements[0]

    if not isinstance(statement, exp.Select):
        raise UnsafeSQLQueryError("Only SELECT statements are allowed")

    forbidden_operations_found = {
        node.key for node in statement.walk() if node.key in FORBIDDEN_SQL_OPERATIONS
    }

    if forbidden_operations_found:
        operations = ", ".join(sorted(forbidden_operations_found))
        raise UnsafeSQLQueryError(f"SQL contains forbidden operations: {operations}")

    cte_names = {
        cte.alias_or_name.lower()
        for cte in statement.find_all(exp.CTE)
        if cte.alias_or_name
    }

    referenced_tables = {
        table.name.lower()
        for table in statement.find_all(exp.Table)
        if table.name and table.name.lower() not in cte_names
    }

    if not referenced_tables:
        raise UnsafeSQLQueryError("SQL must reference an approved table")

    disallowed_tables = referenced_tables - ALLOWED_TABLES

    if disallowed_tables:
        tables = ", ".join(sorted(disallowed_tables))
        raise UnsafeSQLQueryError(f"SQL references disallowed tables: {tables}")


def execute_read_only_query(query: str) -> list[dict]:
    validate_read_only_query(query)
    query_without_semicolon = query.strip().rstrip(";")

    limited_query = f"""select * from ({query_without_semicolon}) as validated_query limit {MAX_QUERY_ROWS}"""

    try:
        with engine.connect() as connection:
            with connection.begin():
                connection.execute(text("SET TRANSACTION READ ONLY"))

                connection.execute(
                    text("""
                        SELECT set_config(
                            'statement_timeout',
                            :timeout_ms,
                            true
                        )
                        """),
                    {"timeout_ms": str(DATABASE_STATEMENT_TIMEOUT_MS)},
                )
                result = connection.execute(text(limited_query))
                return [dict(row._mapping) for row in result]
    except OperationalError as error:
        # PostgreSQL uses SQLSTATE 57014 when it cancels a statement,
        # error.orig is the original PostgreSQL driver exception.
        sqlstate = getattr(error.orig, "pgcode", None)
        if sqlstate == "57014":
            raise DatabaseTimeoutError("The database exceeded the configured timeout.")

        raise DatabaseUnavailableError(
            "The application could not reach the database"
        ) from error

    except DBAPIError as error:
        # the database was reachable but the query was rejected
        raise DatabaseQueryError(
            "Postgresql could not execute the generated query"
        ) from error


def answer_from_sql(question: str) -> dict:
    sql = generate_sql(question)
    rows = execute_read_only_query(sql)
    answer = generate_sql_answer(question, sql, rows)

    return {"answer": answer, "sql": sql, "data": rows}
