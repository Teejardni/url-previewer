import httpx
import gzip
import brotli
from . import parse
from ..core.settings import settings
from typing import Optional
import logging
from urllib.parse import urlparse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ALLOWED_CONTENT_TYPES = {"text/html", "application/xhtml+xml"}

async def decompress_content(content: bytes, content_encoding: Optional[str]) -> bytes:
    """Decompress content if encoded with gzip or brotli."""
    if content_encoding == 'gzip':
        try:
            return gzip.decompress(content)
        except Exception as e:
            logger.error(f"Gzip decompression failed: {e}")
    elif content_encoding == 'br':
        try:
            return brotli.decompress(content)
        except Exception as e:
            logger.error(f"Brotli decompression failed: {e}")
    return content

async def fetch_html(url: str) -> str:
    # Determine user agent based on blocked sites
    clean_url = urlparse(url).hostname or url
    user_agent = settings.USER_AGENT_TWITTERBOT
    if any(site in clean_url for site in settings.BLOCKED_SITES):
        user_agent = settings.USER_AGENT_GENERIC
        logger.info(f"Using Generic user agent for blocked site: {clean_url}")
    else:
        logger.info(f"Using Twitterbot user agent for: {clean_url}")

    headers = {
        "User-Agent": user_agent,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0",
    }
    limits = httpx.Limits(max_connections=10, max_keepalive_connections=10)
    timeout = httpx.Timeout(settings.HTTP_TIMEOUT_SECONDS)

    async with httpx.AsyncClient(headers=headers, follow_redirects=True, limits=limits, timeout=timeout) as client:
        async with client.stream("GET", url) as resp:
            resp.raise_for_status()

            ctype = resp.headers.get("content-type", "").split(";")[0].strip()
            if ctype and not any(ctype.startswith(t) for t in ALLOWED_CONTENT_TYPES):
                if "html" not in ctype:
                    raise httpx.HTTPError(f"Unsupported content-type: {ctype}")

            total = 0
            chunks = []
            async for chunk in resp.aiter_bytes():
                total += len(chunk)
                if total > settings.MAX_BYTES:
                    raise httpx.HTTPError("Response too large")
                chunks.append(chunk)
            
            content = b"".join(chunks)
            content_encoding = resp.headers.get('Content-Encoding')
            decompressed_content = await decompress_content(content, content_encoding)
            return decompressed_content.decode(errors="replace")

async def preview_from_url(url: str) -> dict:
    html = await fetch_html(url)
    # Process HTML before metadata extraction
    processed_html = parse.process_html_content(url, html)
    return parse.extract_metadata(url, processed_html)