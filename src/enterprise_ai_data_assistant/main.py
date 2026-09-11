from fastapi import FastAPI
from enterprise_ai_data_assistant.config import settings
from enterprise_ai_data_assistant.api.routes.health import router as health_router
from enterprise_ai_data_assistant.api.routes.ask import router as ask_router
from enterprise_ai_data_assistant.api.routes.sql import router as sql_router
from fastapi.middleware.cors import CORSMiddleware

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
)
app.include_router(health_router)
app.include_router(ask_router)
app.include_router(sql_router)


@app.get("/")
def root():
    return {"message": "Enterprise AI Data Assistant is running"}
