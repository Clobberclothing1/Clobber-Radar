
import pandas as pd, os, datetime

CSV_FILE = "tracker.csv"

def log_sale(item,bought,sold,platform):
    roi = (sold - bought) / bought if bought else 0
    row = {
        "date": datetime.date.today().isoformat(),
        "item": item,
        "platform": platform,
        "bought": bought,
        "sold": sold,
        "roi_percent": round(roi*100,1)
    }
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        df = pd.concat([df,pd.DataFrame([row])], ignore_index=True)
    else:
        df = pd.DataFrame([row])
    df.to_csv(CSV_FILE,index=False)

def get_log():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    return pd.DataFrame(columns=["date","item","platform","bought","sold","roi_percent"])
