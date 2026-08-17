from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name:str = "Enterprise AI Data Assistant"
    azure_search_endpoint:str
    azure_search_key:str
    azure_search_index:str = "enterprise_rag"
    model_config = {"env_file":".env",
                    "env_file_encoding": "utf-8"}
    

settings = Settings()