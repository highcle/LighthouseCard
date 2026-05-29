import httpx
from bs4 import BeautifulSoup
from typing import Optional


def scrape_jcg_lighthouse_page(url: str) -> dict[str, Optional[str]]:
    try:
        response = httpx.get(url, timeout=10, follow_redirects=True)
        response.raise_for_status()
    except Exception:
        return {"name": None, "card_image_url": None}

    soup = BeautifulSoup(response.text, "html.parser")
    name: Optional[str] = None
    card_image_url: Optional[str] = None

    asset_body = soup.find("div", class_="asset-body")
    if asset_body:
        h3 = asset_body.find("h3")
        if h3:
            name = h3.get_text(strip=True)

        img_link = asset_body.find("a", href=lambda x: x and x.startswith("image/"))
        if img_link:
            base = url.rsplit("/", 1)[0]
            card_image_url = f"{base}/{img_link['href']}"

    return {"name": name, "card_image_url": card_image_url}
