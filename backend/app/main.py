from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .schemas import PreviewRequest, PreviewResponse, ErrorResponse
from .services.fetch import preview_from_url
from .core.settings import settings
import httpx

app = FastAPI(title="URL Previewer API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/preview", response_model=PreviewResponse, responses={400: {"model": ErrorResponse}, 504: {"model": ErrorResponse}})
async def preview(payload: PreviewRequest):
    try:
        data = await preview_from_url(str(payload.url))
        return PreviewResponse(**data)
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Upstream fetch timed out")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=400, detail=f"Upstream returned {e.response.status_code}")
    except httpx.HTTPError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to fetch or parse the URL")