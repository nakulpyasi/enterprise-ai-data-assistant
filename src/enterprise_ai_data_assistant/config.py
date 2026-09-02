from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Enterprise AI Data Assistant"
    azure_search_endpoint: str
    azure_search_key: str
    azure_search_index: str = "enterprise_rag"

    azure_openai_endpoint: str
    azure_openai_api_key: str
    azure_openai_model: str
    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    database_url: str

    foundry_project_endpoint: str
    foundry_rag_agent_name: str
    foundry_rag_agent_version: str

    foundry_sql_agent_name: str
    foundry_sql_agent_version: str


settings = Settings()
