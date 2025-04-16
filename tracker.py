import pandas as pd, os, datetime as dt
F="tracker.csv"; COLS=["date","item","platform","bought","sold","roi%"]

def _load(): return pd.read_csv(F) if os.path.exists(F) else pd.DataFrame(columns=COLS)

def log_sale(item,bought,sold,platform):
    roi=round(((sold-bought)/bought*100) if bought else 0,1)
    row={"date":dt.date.today().isoformat(),"item":item,"platform":platform,
         "bought":bought,"sold":sold,"roi%":roi}
    pd.concat([_load(),pd.DataFrame([row])]).to_csv(F,index=False)

def get_log(): return _load()

def monthly_summary():
    df=_load()
    if df.empty: return df
    df["date"]=pd.to_datetime(df["date"])
    return (df.groupby(df["date"].dt.to_period("M"))
             .agg(total_profit=("roi%", "sum"), flips=("item","count"))
             .reset_index().rename(columns={"month":"date"}))
