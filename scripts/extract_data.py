# extract_data.py
import requests, json
from pathlib import Path
DATA_DIR = Path(__file__).resolve().parents[1] / 'data'
DATA_DIR.mkdir(parents=True, exist_ok=True)
RAW_FILE = DATA_DIR / 'raw_products.json'
API_URL = 'https://fakestoreapi.com/products'
def fetch_products():
    resp = requests.get(API_URL, timeout=15)
    resp.raise_for_status()
    return resp.json()
if __name__=='__main__':
    products = fetch_products()
    RAW_FILE.write_text(json.dumps(products, indent=2))
