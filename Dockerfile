FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY README.md ./
COPY src ./src

RUN pip install uv

RUN uv sync --frozen --no-dev

ENV PYTHONPATH=/app/src

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "enterprise_ai_data_assistant.main:app", "--host", "0.0.0.0", "--port", "8000"]