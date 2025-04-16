# vinted_pricing.py
"""
Grabs the first ~48 active Vinted listings for a search term by
parsing the JSON blob embedded in the catalog HTML.  Works even when
the API endpoint blocks cloud hosts.
"""
import requests, re, json, statistics, urllib.parse

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

SCRIPT_RE = re.compile(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', re.S)

def vinted_price_stats(search: str, max_items: int = 48):
    url = (
        "https://www.vinted.co.uk/catalog?"
        f"search_text={urllib.parse.quote_plus(search)}"
    )

    try:
        html = requests.get(url, headers=HEADERS, timeout=10).text
    except requests.RequestException:
        return {"low": 0, "median": 0, "high": 0, "count": 0}

    m = SCRIPT_RE.search(html)
    if not m:
        return {"low": 0, "median": 0, "high": 0, "count": 0}

    try:
        data = json.loads(m.group(1))
        items = (
            data["props"]["pageProps"]["items"]["catalogItems"]["items"][:max_items]
        )
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
