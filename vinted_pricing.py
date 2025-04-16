
import requests, bs4, statistics

HEADERS = {"User-Agent": "Mozilla/5.0"}

def vinted_price_stats(query:str):
    url = f"https://www.vinted.co.uk/catalog?search_text={query.replace(' ','%20')}"
    html = requests.get(url, headers=HEADERS, timeout=10).text
    soup = bs4.BeautifulSoup(html, "html.parser")
    price_elems = soup.select("div.Tile__price")
    prices = []
    for p in price_elems:
        txt = p.get_text(strip=True).replace("£","").split()[0]
        try:
            prices.append(float(txt))
        except ValueError:
            continue
    if not prices:
        return {"low":0,"median":0,"high":0,"count":0}
    return {
        "low": min(prices),
        "median": statistics.median(prices),
        "high": max(prices),
        "count": len(prices)
    }
