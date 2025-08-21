from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from typing import Optional, Dict

META_NAME_MAP = {
    'og:title': 'title',
    'twitter:title': 'title',
    'og:description': 'description',
    'twitter:description': 'description',
    'description': 'description',
    'og:image': 'imageUrl',
    'twitter:image': 'imageUrl',
    'og:site_name': 'siteName',
}

PRIORITY_TITLE = ['og:title', 'twitter:title']
PRIORITY_DESC = ['og:description', 'twitter:description', 'description']
PRIORITY_IMAGE = ['og:image', 'twitter:image']
PRIORITY_SITENAME = ['og:site_name']


def _meta_content(tag) -> Optional[str]:
    if not tag:
        return None
    # Support <meta name|property=... content=...>
    return tag.get('content') or tag.get('value')


def absolutize(base: str, url: Optional[str]) -> Optional[str]:
    if not url:
        return None
    return urljoin(base, url)


def extract_metadata(base_url: str, html: str) -> Dict[str, Optional[str]]:
    soup = BeautifulSoup(html, 'lxml')

    # Build lookup for name/property metas
    metas = {}
    for m in soup.find_all('meta'):
        key = m.get('property') or m.get('name')
        if not key:
            continue
        key = key.strip().lower()
        val = _meta_content(m)
        if val:
            metas.setdefault(key, val)

    def pick(keys):
        for k in keys:
            if k in metas and metas[k].strip():
                return metas[k].strip()
        return None

    title = pick(PRIORITY_TITLE) or (soup.title.string.strip() if soup.title and soup.title.string else None)
    description = pick(PRIORITY_DESC)
    image = pick(PRIORITY_IMAGE)
    site_name = pick(PRIORITY_SITENAME)

    if not site_name:
        try:
            site_name = urlparse(base_url).hostname
        except Exception:
            site_name = None

    image = absolutize(base_url, image)

    return {
        'title': title or None,
        'description': description or None,
        'imageUrl': image or None,
        'siteName': site_name or None,
    }