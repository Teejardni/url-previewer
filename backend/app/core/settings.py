from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
from pydantic import field_validator
import json
from pathlib import Path

class Settings(BaseSettings):
    PORT: int = 8000
    ALLOWED_ORIGINS: List[str] = ["http://localhost:5173"]
    USER_AGENT_TWITTERBOT: str = "Twitterbot/1.0"
    USER_AGENT_GENERIC: str = "Mozilla/5.0 (PlayStation; PlayStation 5/6.50) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
    HTTP_TIMEOUT_SECONDS: float = 12.0
    MAX_BYTES: int = 3_145_728  # ~3 MB
    BLOCKED_SITES_FILE: str = "app/blocked_sites.txt"
    ENABLE_OTEL: bool = False

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_allowed_origins(cls, value):
        if not value:
            return []
        
        if isinstance(value, str):
            # Handle JSON array
            if value.strip().startswith("["):
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    raise ValueError(f"Invalid JSON array: {value}")
            
            # Handle comma-separated or single value
            return [x.strip() for x in value.split(",") if x.strip()]
        
        return value

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False,
        env_nested_delimiter='__'
    )

    @property
    def BLOCKED_SITES(self) -> List[str]:
        """Load blocked sites from file or return empty list if not found."""
        try:
            with open(self.BLOCKED_SITES_FILE, 'r', encoding='utf-8') as file:
                return [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            print(f"Warning: {self.BLOCKED_SITES_FILE} not found. No sites will be treated as blocked.")
            return []
        except IOError as e:
            print(f"Error reading {self.BLOCKED_SITES_FILE}: {e}")
            return []

settings = Settings()