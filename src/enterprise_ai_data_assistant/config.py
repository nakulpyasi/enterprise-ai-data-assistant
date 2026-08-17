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


settings = Settings()
