import cloudscraper, statistics, json, re, urllib.parse

scraper = cloudscraper.create_scraper(
    browser={"browser": "chrome", "platform": "windows", "mobile": False}
)
RX = re.compile(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', re.S)

def _stats(prices):
    return {"low": min(prices),"median": statistics.median(prices),
            "high": max(prices),"count": len(prices)} if prices else            {"low":0,"median":0,"high":0,"count":0}

def vinted_price_stats(q:str, n:int=50):
    api = ( "https://www.vinted.co.uk/api/v2/catalog/items?"
            f"search_text={urllib.parse.quote_plus(q)}&per_page={n}" )
    r = scraper.get(api, timeout=15)
    if r.status_code==200:
        prices=[float(i["price"]) for i in r.json().get("items",[]) if i.get("price")]
        if prices: return _stats(prices)
    html=scraper.get(f"https://www.vinted.co.uk/catalog?search_text={urllib.parse.quote_plus(q)}",timeout=15).text
    m=RX.search(html)
    if not m: return _stats([])
    try:
        items=json.loads(m.group(1))["props"]["pageProps"]["items"]["catalogItems"]["items"][:n]
        prices=[float(i["price"]) for i in items if i.get("price")]
    except Exception:
        prices=[]
    return _stats(prices)
