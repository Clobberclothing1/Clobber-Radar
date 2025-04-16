"""
vinted_pricing.py – fetches active‑listing prices even when Cloudflare
blocks normal requests, by using a headless real browser.
"""
import statistics, json, re, urllib.parse, time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

SCRIPT_RX = re.compile(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', re.S)

def _fetch_html(url: str) -> str:
    opts = uc.ChromeOptions()
    opts.add_argument("--headless=new")
    driver = uc.Chrome(options=opts)
    driver.get(url)
    time.sleep(2)            # wait for Cloudflare JS & page render
    html = driver.page_source
    driver.quit()
    return html

def vinted_price_stats(search: str, max_items: int = 48):
    url = (
        "https://www.vinted.co.uk/catalog?"
        f"search_text={urllib.parse.quote_plus(search)}"
    )
    html = _fetch_html(url)
    m = SCRIPT_RX.search(html)
    if not m:
        return {"low": 0, "median": 0, "high": 0, "count": 0}

    try:
        data = json.loads(m.group(1))
        items = data["props"]["pageProps"]["items"]["catalogItems"]["items"][:max_items]
    except (KeyError, json.JSONDecodeError):
        return {"low": 0, "median": 0, "high": 0, "count": 0}

    prices = [float(it["price"]) for it in items if it.get("price")]
    if not prices:
        return {"low": 0, "median": 0, "high": 0, "count": 0}

    return {
        "low": min(prices),
        "median": statistics.median(prices),
        "high": max(prices),
        "count": len(prices),
    }
