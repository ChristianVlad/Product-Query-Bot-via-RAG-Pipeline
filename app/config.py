# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    LLM_MODEL: str = "gpt-3.5-turbo"
    TOP_K: int = 3
    EMBEDDING_MODEL: str = "openai"
    
    class Config:
        env_file = ".env"

settings = Settings()