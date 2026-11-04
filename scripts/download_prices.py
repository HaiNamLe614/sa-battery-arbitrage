# Download price and demand data from AEMO for SA1.
import time
from pathlib import Path

import pandas as pd
import requests

BASE_URL = "http://aemo.com.au/aemo/data/nem/priceanddemand"
OUT_DIR = Path("data/raw")
MONTHS = [p.strftime("%Y%m") for p in pd.date_range("2023-11", "2025-10", freq="ME")]
HEADERS = {"User-Agent": "Mozilla/5.0"}

def download_month(month: str, region: str = "SA1") -> None:
    filename = f"PRICE_AND_DEMAND_{month}_{region}.csv"
    path = OUT_DIR / filename
    if path.exists():
        print(f"{filename} already exists, skipping download.")
        return
    response = requests.get(f"{BASE_URL}/{filename}", headers=HEADERS, timeout=30)
    response.raise_for_status()
    path.write_bytes(response.content)
    print(f"Saved {filename}")
    time.sleep(1)  # Be polite and avoid overwhelming the server
    
if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for month in MONTHS:
        download_month(month)