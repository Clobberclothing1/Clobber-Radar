"""
CSV‑based profit tracker with a bonus monthly_summary() helper.
"""
import pandas as pd, os, datetime as dt

FILE = "tracker.csv"
COLUMNS = ["date", "item", "platform", "bought", "sold", "roi_percent"]

def _load() -> pd.DataFrame:
    if os.path.exists(FILE):
        return pd.read_csv(FILE)
    return pd.DataFrame(columns=COLUMNS)

def log_sale(item: str, bought: float, sold: float, platform: str):
    roi = (sold - bought) / bought * 100 if bought else 0
    row = {
        "date": dt.date.today().isoformat(),
        "item": item,
        "platform": platform,
        "bought": bought,
        "sold": sold,
        "roi_percent": round(roi, 1),
    }
    df = pd.concat([_load(), pd.DataFrame([row])], ignore_index=True)
    df.to_csv(FILE, index=False)

def get_log() -> pd.DataFrame:
    return _load()

def monthly_summary() -> pd.DataFrame:
    df = _load()
    if df.empty:
        return df
    df["date"] = pd.to_datetime(df["date"])
    summary = (
        df.groupby(df["date"].dt.to_period("M"))
          .agg(total_profit=("roi_percent", "sum"),
               flips=("item", "count"))
          .reset_index()
          .rename(columns={"date": "month"})
    )
    return summary
