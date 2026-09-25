from enterprise_ai_data_assistant.exceptions import (
    FoundryResponseError,
    FoundryTimeoutError,
    FoundryUnavailableError,
    DatabaseQueryError,
    DatabaseUnavailableError,
    DatabaseTimeoutError,
    UnsafeSQLQueryError,
)
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
import logging
import uuid
from enterprise_ai_data_assistant.config import settings
from enterprise_ai_data_assistant.api.routes.health import router as health_router
from enterprise_ai_data_assistant.api.routes.ask import router as ask_router
from enterprise_ai_data_assistant.api.routes.sql import router as sql_router
from fastapi.middleware.cors import CORSMiddleware

logger = logging.getLogger("uvicorn.error")

app = FastAPI(title=settings.app_name)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://purple-sea-085e43810.5.azurestaticapps.net",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID"],
)


@app.middleware("http")
async def add_request_id_header(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    logger.info(f"Request ID: {request_id} - {request.method} {request.url.path}")
    try:
        response = await call_next(request)
    except Exception as e:
        logger.exception(
            "request_failed request_id=%s method=%s path=%s",
            request_id,
            request.method,
            request.url.path,
        )
        raise
    response.headers["X-Request-ID"] = request_id
    logger.info(
        f"Response ID: {request_id} - {request.method} {request.url.path} - Status: {response.status_code}"
    )
    return response


@app.exception_handler(FoundryTimeoutError)
async def handle_foundry_timeout(request: Request, error: FoundryTimeoutError):
    request_id = getattr(request.state, "request_id", "unknown")
    logger.error("found_timeout request_id = %s", request_id, exc_info=error)
    return JSONResponse(
        status_code=status.HTTP_504_GATEWAY_TIMEOUT,
        content={
            "error": "The AI service took too long to respond",
            "request_id": request_id,
        },
    )


@app.exception_handler(FoundryUnavailableError)
async def handle_foundry_unavailable(request: Request, error: FoundryUnavailableError):
    request_id = getattr(request.state, "request_id", "unknown")
    logger.error("foundry unavailable request_id = %s", request_id, exc_info=error)
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "error": "The AI service is temporarily unavailable.",
            "request_id": request_id,
        },
    )


@app.exception_handler(FoundryResponseError)
async def handle_foundry_response_error(
    request: Request,
    error: FoundryResponseError,
):
    """Return a safe response when Foundry returns unusable data."""
    request_id = getattr(request.state, "request_id", "unknown")
    logger.error(
        "foundry_invalid_response request_id=%s",
        request_id,
        exc_info=error,
    )
    return JSONResponse(
        status_code=status.HTTP_502_BAD_GATEWAY,
        content={
            "error": "The AI service returned an invalid response.",
            "request_id": request_id,
        },
    )


@app.exception_handler(UnsafeSQLQueryError)
async def handle_unsafe_sql(request: Request, error: UnsafeSQLQueryError):
    """Handle sql that fails the applications saftey validation"""
    request_id = getattr(request.state, "request_id", "unknown")
    logger.error("unsafe sql request_id=%s", request_id, exc_info=error)

    return JSONResponse(
        status_code=status.HTTP_502_BAD_GATEWAY,
        content={
            "error": "The AI generated a query that cannot be safely executed.",
            "request_id": request_id,
        },
    )


@app.exception_handler(DatabaseTimeoutError)
async def handle_database_timeout(
    request: Request,
    error: DatabaseTimeoutError,
):
    """Handle queries cancelled by the PostgreSQL timeout."""

    request_id = getattr(request.state, "request_id", "unknown")

    logger.error(
        "database_timeout request_id=%s",
        request_id,
        exc_info=error,
    )

    return JSONResponse(
        status_code=status.HTTP_504_GATEWAY_TIMEOUT,
        content={
            "error": "The database query took too long to complete.",
            "request_id": request_id,
        },
    )


@app.exception_handler(DatabaseUnavailableError)
async def handle_database_unavailable(
    request: Request,
    error: DatabaseUnavailableError,
):
    """Handle database connection and availability failures."""

    request_id = getattr(request.state, "request_id", "unknown")

    logger.error(
        "database_unavailable request_id=%s",
        request_id,
        exc_info=error,
    )

    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "error": "The database is temporarily unavailable.",
            "request_id": request_id,
        },
    )


@app.exception_handler(DatabaseQueryError)
async def handle_database_query_error(
    request: Request,
    error: DatabaseQueryError,
):
    """Handle SQL that PostgreSQL cannot execute."""

    request_id = getattr(request.state, "request_id", "unknown")

    logger.error(
        "database_query_failed request_id=%s",
        request_id,
        exc_info=error,
    )

    return JSONResponse(
        status_code=status.HTTP_502_BAD_GATEWAY,
        content={
            "error": "The database could not execute the generated query.",
            "request_id": request_id,
        },
    )


app.include_router(health_router)
app.include_router(ask_router)
app.include_router(sql_router)


@app.get("/")
def root():
    return {"message": "Enterprise AI Data Assistant is running"}
