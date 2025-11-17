# clean_data.py
import json, pandas as pd
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
RAW=BASE/'data/raw_products.json'
CLEAN=BASE/'data/cleaned_products.json'
df=pd.json_normalize(json.loads(RAW.read_text()))
df.to_json(CLEAN, orient='records', indent=2)
