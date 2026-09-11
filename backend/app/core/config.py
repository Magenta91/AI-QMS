from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "AIVOA Complaint Management System"
    environment: str = "development"
    database_url: str
    groq_api_key: str
    groq_model: str = "gemma2-9b-it"
    api_host: str = "127.0.0.1"
    api_port: int = 8000
    frontend_url: str = "http://localhost:5173"
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
