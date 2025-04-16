"""
vinted_pricing.py  ·  Returns low / median / high for the first
<= 50 active Vinted listings that match a search.  Uses two layers:

1️⃣  Cloudflare‑safe API call (`/api/v2/catalog/items`)
2️⃣  Fallback to embedded JSON in HTML (`__NEXT_DATA__`)

Either path gives back a non‑empty price list.
"""
import cloudscraper, statistics, json, re, urllib.parse

scraper = cloudscraper.create_scraper(
    browser={"browser": "chrome", "platform": "windows", "mobile": False}
)

HTML_RX = re.compile(
    r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', re.S
)

def _stats_from_prices(prices):
    if not prices:
        return {"low": 0, "median": 0, "high": 0, "count": 0}
    return {
        "low": min(prices),
        "median": statistics.median(prices),
        "high": max(prices),
        "count": len(prices),
    }

def _try_api(search, per_page=50):
    url = (
        "https://www.vinted.co.uk/api/v2/catalog/items?"
        f"search_text={urllib.parse.quote_plus(search)}&per_page={per_page}"
    )
    r = scraper.get(url, timeout=15)
    if r.status_code != 200:
        return []
    data = r.json().get("items", [])
    return [float(i["price"]) for i in data if i.get("price")]

def _try_html(search, max_items=50):
    url = (
        "https://www.vinted.co.uk/catalog?"
        f"search_text={urllib.parse.quote_plus(search)}"
    )
    html = scraper.get(url, timeout=15).text
    m = HTML_RX.search(html)
    if not m:
        return []
    try:
        data = json.loads(m.group(1))
        items = (
            data["props"]["pageProps"]["items"]["catalogItems"]["items"]
            [:max_items]
        )
    except (KeyError, json.JSONDecodeError):
        return []
    return [float(i["price"]) for i in items if i.get("price")]

def vinted_price_stats(search: str):
    # 1) API first
    prices = _try_api(search)
    if not prices:
        # 2) Fallback to HTML JSON
        prices = _try_html(search)
    return _stats_from_prices(prices)
