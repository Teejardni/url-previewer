import httpx
from . import parse
from ..core.settings import settings
from typing import Optional

ALLOWED_CONTENT_TYPES = {"text/html", "application/xhtml+xml"}

async def fetch_html(url: str) -> str:
    headers = {"User-Agent": settings.USER_AGENT}
    limits = httpx.Limits(max_connections=10, max_keepalive_connections=10)
    timeout = httpx.Timeout(settings.HTTP_TIMEOUT_SECONDS)

    async with httpx.AsyncClient(headers=headers, follow_redirects=True, limits=limits, timeout=timeout) as client:
        # Stream to enforce MAX_BYTES
        async with client.stream("GET", url) as resp:
            resp.raise_for_status()

            ctype = resp.headers.get("content-type", "").split(";")[0].strip()
            if ctype and not any(ctype.startswith(t) for t in ALLOWED_CONTENT_TYPES):
                # Still allow if it looks like HTML without an explicit type
                if "html" not in ctype:
                    raise httpx.HTTPError(f"Unsupported content-type: {ctype}")

            total = 0
            chunks = []
            async for chunk in resp.aiter_bytes():
                total += len(chunk)
                if total > settings.MAX_BYTES:
                    raise httpx.HTTPError("Response too large")
                chunks.append(chunk)
            return b"".join(chunks).decode(errors="replace")

async def preview_from_url(url: str) -> dict:
    html = await fetch_html(url)
    return parse.extract_metadata(url, html)