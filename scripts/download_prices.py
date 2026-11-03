from pathlib import Path

import requests

BASE_URL = "http://aemo.com.au/aemo/data/nem/priceanddemand"
OUT_DIR = Path("data/raw")
MONTHS = ["202508", "202509", "202510"]
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def download_month(month: str, region: str = "SA1") -> None:
    filename = f"PRICE_AND_DEMAND_{month}_{region}.csv"
    response = requests.get(f"{BASE_URL}/{filename}", headers=HEADERS, timeout=30)
    response.raise_for_status()
    (OUT_DIR / filename).write_bytes(response.content)
    print(f"Saved {filename} to {OUT_DIR}")
    
if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for month in MONTHS:
        download_month(month)