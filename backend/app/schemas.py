from pydantic import BaseModel, AnyHttpUrl, field_validator
from typing import Optional
from urllib.parse import urlparse

class PreviewRequest(BaseModel):
    url: AnyHttpUrl

    @field_validator('url')
    @classmethod
    def only_http_https(cls, v: AnyHttpUrl) -> AnyHttpUrl:
        if v.scheme not in {"http", "https"}:
            raise ValueError("Only http/https URLs are allowed")
        return v

class PreviewResponse(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    imageUrl: Optional[str] = None
    siteName: Optional[str] = None

class ErrorResponse(BaseModel):
    detail: str