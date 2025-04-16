from PIL import Image
import pytesseract, re

BRANDS = [
    "adidas","armani","balenciaga","burberry","carhartt","chanel","converse",
    "dior","fila","ganni","gap","gucci","lacoste","levis","louis vuitton",
    "moncler","nike","north face","off white","prada","reebok","supreme",
    "tommy hilfiger","under armour","valentino","versace","vans","ralph lauren",
]
PAT = re.compile(r"\b(" + "|".join(re.escape(b) for b in BRANDS) + r")\b", re.I)

def detect_brand(file) -> str:
    if not file: return ""
    try:
        text = pytesseract.image_to_string(Image.open(file).convert("RGB")).lower()
        m = PAT.search(text)
        return m.group(1).title() if m else ""
    except Exception:
        return ""
