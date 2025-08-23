from pydantic import BaseModel, HttpUrl
from typing import Optional

class PreviewRequest(BaseModel):
    url: HttpUrl

class PreviewResponse(BaseModel):
    title: Optional[str]
    description: Optional[str]
    imageUrl: Optional[str]
    siteName: Optional[str]
    articleContent: Optional[str] = None  # New field for full article HTML

class ErrorResponse(BaseModel):
    detail: str