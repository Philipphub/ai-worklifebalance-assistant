from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Manages application settings and environment variables."""

    AZURE_AI_API_KEY: str = "YOUR_KEY_HERE"
    AZURE_AI_ENDPOINT: str = "YOUR_ENDPOINT_HERE"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
