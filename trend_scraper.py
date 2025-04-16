
import requests, bs4, pandas as pd

def vinted_trending():
    url = "https://www.vinted.co.uk/vinted-trending"
    html = requests.get(url, timeout=10).text
    soup = bs4.BeautifulSoup(html, "html.parser")
    tags = [t.get_text(strip=True) for t in soup.select("a.TrendsItem")]
    return pd.Series(tags, name="Trending Now")
