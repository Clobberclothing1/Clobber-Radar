import cloudscraper, pandas as pd
scraper = cloudscraper.create_scraper(browser={"browser":"chrome","platform":"windows"})

def vinted_trending():
    try:
        js = scraper.get("https://www.vinted.co.uk/api/v2/trends", timeout=10).json()
        tags = [t["name"] for t in js.get("trends", [])][:20]
        return pd.Series(tags, name="Trending")
    except Exception:
        return pd.Series([], name="Trending")
