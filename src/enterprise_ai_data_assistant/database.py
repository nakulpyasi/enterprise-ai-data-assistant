from sqlalchemy import create_engine
from enterprise_ai_data_assistant.config import settings

engine = create_engine(settings.database_url)
