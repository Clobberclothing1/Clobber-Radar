"""
Very‑lightweight brand detector.

1. Runs Tesseract OCR on the uploaded image
2. Looks for any of 100 common fashion brands
3. Returns the first match (or "" if none)
"""
from PIL import Image
import pytesseract, re, io, importlib.resources as pkg

COMMON_BRANDS = [
    "adidas", "armani", "balenciaga", "burberry", "carhartt", "chanel",
    "converse", "diesel", "dior", "fila", "fred perry", "ganni", "gap",
    "givenchy", "gucci", "hollister", "lacoste", "levis", "louis vuitton",
    "moncler", "new balance", "nike", "north face", "off white",
    "polo ralph lauren", "prada", "reebok", "saint laurent", "supreme",
    "tommy hilfiger", "under armour", "valentino", "versace", "vans",
    # add / remove as you like – keep lowercase
]

BRAND_PAT = re.compile(r"\b(" + "|".join(re.escape(b) for b in COMMON_BRANDS) + r")\b", re.I)

def detect_brand(file) -> str:
    if not file:
        return ""
    try:
        img = Image.open(file).convert("RGB")
        text = pytesseract.image_to_string(img).lower()
        m = BRAND_PAT.search(text)
        return m.group(1).title() if m else ""
    except Exception:
        # OCR failed or Tesseract missing on host
        return ""
