from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    PORT: int = 8000
    ALLOWED_ORIGINS: List[str] = ["http://localhost:5173"]

    USER_AGENT: str = "URLPreviewerBot/1.0"
    HTTP_TIMEOUT_SECONDS: float = 12.0
    MAX_BYTES: int = 3_145_728  # ~3 MB

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', case_sensitive=False)

settings = Settings()