import os, requests, pandas as pd
from datetime import datetime, timedelta
from base_pipeline import upload_to_hf, get_last_date, log, TODAY, require_env

require_env("HF_TOKEN", "HF_REPO_WEATHER")
REPO = os.environ["HF_REPO_WEATHER"]
STATIONS = {"Milano":"ITE00100550","Roma":"ITE00100501","Napoli":"ITE00100566"}

def fetch_weather():
    last = get_last_date(REPO)
    start = (datetime.strptime(last, "%Y-%m-%d") - timedelta(days=2)).strftime("%Y-%m-%d") if last else "1994-01-01"
    all_data = []
    for city, sid in STATIONS.items():
        log.info(f"Meteo {city}...")
        r = requests.get(f"https://www.ncei.noaa.gov/access/services/data/v1?dataset=daily-summaries&stations={sid}&startDate={start}&endDate={TODAY}&format=json&units=metric")
        if r.status_code == 200: 
            df = pd.DataFrame(r.json())
            df['city'] = city
            all_data.append(df)
    return pd.concat(all_data) if all_data else pd.DataFrame()

if __name__ == "__main__":
    df = fetch_weather()
    upload_to_hf(df, REPO, "italy_weather", "# Dataset Meteo Storico Italia")
