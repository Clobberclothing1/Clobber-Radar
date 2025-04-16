# vinted_pricing.py  – JSON‑based price grabber
import requests, statistics, urllib.parse

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

def vinted_price_stats(query: str, max_items: int = 50):
    """
    Returns low / median / high price and count for the first `max_items`
    active Vinted listings that match `query`.
    """
    q = urllib.parse.quote_plus(query)
    url = (
        "https://www.vinted.co.uk/api/v2/catalog/items?"
        f"search_text={q}&per_page={max_items}"
    )

    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
    except requests.RequestException:
        return {"low": 0, "median": 0, "high": 0, "count": 0}

    items = resp.json().get("items", [])
    prices = [float(it.get("price", 0)) for it in items if it.get("price")]

    if not prices:
        return {"low": 0, "median": 0, "high": 0, "count": 0}

    return {
        "low": min(prices),
        "median": statistics.median(prices),
        "high": max(prices),
        "count": len(prices),
    }
