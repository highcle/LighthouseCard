import httpx
from bs4 import BeautifulSoup
from typing import Optional

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ja,en-US;q=0.9",
}


def scrape_jcg_lighthouse_page(url: str) -> dict[str, Optional[str]]:
    try:
        response = httpx.get(url, timeout=15, follow_redirects=True, headers=_HEADERS)
        response.raise_for_status()
    except Exception as e:
        print(f"[scraper] fetch failed: {e}")
        return {"name": None, "card_image_url": None}

    soup = BeautifulSoup(response.text, "html.parser")
    name: Optional[str] = None
    card_image_url: Optional[str] = None

    asset_body = soup.find("div", class_="asset-body")
    if not asset_body:
        print("[scraper] asset-body not found")
        return {"name": None, "card_image_url": None}

    h3 = asset_body.find("h3")
    if h3:
        name = h3.get_text(strip=True)
        print(f"[scraper] name: {name}")

    # フルサイズ画像リンク（href が image/ で始まるもの）
    img_link = asset_body.find("a", href=lambda x: x and x.startswith("image/"))
    if img_link:
        base = url.rsplit("/", 1)[0]
        card_image_url = f"{base}/{img_link['href']}"
        print(f"[scraper] card_image_url: {card_image_url}")

    return {"name": name, "card_image_url": card_image_url}
