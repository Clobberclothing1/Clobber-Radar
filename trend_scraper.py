"""
Grabs the current trending tags / brands from Vinted's public endpoint.
Returns a pandas Series (ranked list).
"""
import cloudscraper, pandas as pd

scraper = cloudscraper.create_scraper(
    browser={"browser": "chrome", "platform": "windows", "mobile": False}
)

API = "https://www.vinted.co.uk/api/v2/trends"

def vinted_trending(max_items: int = 20) -> pd.Series:
    try:
        js = scraper.get(API, timeout=10).json()
        tags = [t["name"] for t in js.get("trends", [])][:max_items]
        return pd.Series(tags, name="Trending now")
    except Exception:
        # Fallback: empty series
        return pd.Series([], name="Trending now")
