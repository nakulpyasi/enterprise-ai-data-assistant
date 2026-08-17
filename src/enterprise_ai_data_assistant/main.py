from fastapi import FastAPI
from enterprise_ai_data_assistant.config import settings
from enterprise_ai_data_assistant.api.routes.health import router as health_router
from enterprise_ai_data_assistant.api.routes.ask import router as ask_router

app = FastAPI(title=settings.app_name)
app.include_router(health_router)
app.include_router(ask_router)


@app.get("/")
def root():
    return {"message": "Enterprise AI Data Assistant is running"}
