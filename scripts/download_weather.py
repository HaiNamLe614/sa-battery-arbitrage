# Download day-ahead weather forecast data from Open-Meteo's API for South Australia.
from pathlib import Path

import pandas as pd
import requests

URL = "https://previous-runs-api.open-meteo.com/v1/forecast"
OUT_DIR = Path("data/weather")
LOCATIONS = {
    "adelaide": (-34.93, 138.60),
    "snowtown": (-33.78, 138.21),
    "hallett": (-33.58, 138.88),
}
VARIABLES = ["temperature_2m", "windspeed_100m", "shortwave_radiation", "cloud_cover"]

def download_location(name: str, lat: float, lon: float) -> None:
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": "2024-01-01",
        "end_date": "2025-10-31",
        "hourly": ",".join(f"{v}_previous_day1" for v in VARIABLES),
        "timezone": "Australia/Brisbane", #UTC+10, no daylight saving, same as market time
    }
    response = requests.get(URL, params=params, timeout=60)
    response.raise_for_status()
    df = pd.DataFrame(response.json()["hourly"])
    df.to_csv(OUT_DIR / f"{name}.csv", index=False)
    print(f"Saved {name}: {len(df)} rows")
    
if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for name, (lat, lon) in LOCATIONS.items():
        download_location(name, lat, lon)
    