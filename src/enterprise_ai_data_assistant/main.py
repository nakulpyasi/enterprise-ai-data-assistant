from fastapi import FastAPI
from enterprise_ai_data_assistant.config import settings
from enterprise_ai_data_assistant.schemas import AskRequest

app = FastAPI(title= settings.app_name)

@app.get("/")
def root():
    return {"message": "Enterprise AI Data Assistant is running"}

@app.get("/health")
def health_check():
    return {"status":"ok"}

@app.post("/ask")
def ask(request: AskRequest):
    return {"answer": f"You asked: {request.question}"}