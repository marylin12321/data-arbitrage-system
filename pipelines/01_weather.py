import os, sys, requests, pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from base_pipeline import upload_to_hf, require_env, log

def run():
    repo_id = require_env("HF_REPO_WEATHER")
    try:
        if "italy_weather" == "italy_poi":
            q = '[out:json];area["name"="Italia"]->.a;(node["amenity"~"restaurant|hotel"](area.a););out 100;'
            r = requests.post("https://www.ncei.noaa.gov/access/services/data/v1?dataset=daily-summaries&stations=GMM00010384&startDate=2024-01-01&format=json", data={'data': q})
            df = pd.DataFrame(r.json()['elements'])
        elif "italy_weather" == "italy_fuel":
            df = pd.read_csv("https://www.ncei.noaa.gov/access/services/data/v1?dataset=daily-summaries&stations=GMM00010384&startDate=2024-01-01&format=json", sep=";", skiprows=1).head(500)
        else:
            r = requests.get("https://www.ncei.noaa.gov/access/services/data/v1?dataset=daily-summaries&stations=GMM00010384&startDate=2024-01-01&format=json")
            data = r.json()
            df = pd.DataFrame(data['features'] if 'features' in data else (data if isinstance(data, list) else [data]))
        
        upload_to_hf(df, repo_id, "italy_weather")
    except Exception as e: log.error(f"Errore in italy_weather: {e}")

if __name__ == "__main__": run()