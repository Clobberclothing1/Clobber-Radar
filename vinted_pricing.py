"""
vinted_pricing.py  ·  Fetches listing prices with Cloudflare handled by
'cloudscraper' (no browser needed, works on Streamlit Cloud).
"""
import cloudscraper, re, json, statistics, urllib.parse

# Regex to grab the big JSON blob from the HTML
SCRIPT_RX = re.compile(
    r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', re.S
)

# Single, reusable Cloudflare‑aware session
scraper = cloudscraper.create_scraper(
    browser={"browser": "chrome", "platform": "windows", "mobile": False}
)

def vinted_price_stats(search: str, max_items: int = 48):
    """
    Return low / median / high price + count of active Vinted listings
    matching `search`.
    """
    url = (
        "https://www.vinted.co.uk/catalog?"
        f"search_text={urllib.parse.quote_plus(search)}"
    )

    try:
        html = scraper.get(url, timeout=15).text
    except Exception:
        return {"low": 0, "median": 0, "high": 0, "count": 0}

    m = SCRIPT_RX.search(html)
    if not m:
        return {"low": 0, "median": 0, "high": 0, "count": 0}

    try:
        data = json.loads(m.group(1))
        items = data["props"]["pageProps"]["items"]["catalogItems"]["items"][:max_items]
    except (KeyError, json.JSONDecodeError):
        return {"low": 0, "median": 0, "high": 0, "count": 0}

    prices = [float(i["price"]) for i in items if i.get("price")]
    if not prices:
        return {"low": 0, "median": 0, "high": 0, "count": 0}

    return {
        "low": min(prices),
        "median": statistics.median(prices),
        "high": max(prices),
        "count": len(prices),
    }
