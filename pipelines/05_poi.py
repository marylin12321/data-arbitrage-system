import os, sys, requests, pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from base_pipeline import upload_to_hf, require_env, log

def run():
    repo_id = require_env("HF_REPO_POI")
    try:
        if "italy_poi" == "italy_poi":
            q = '[out:json];area["name"="Italia"]->.a;(node["amenity"~"restaurant|hotel"](area.a););out 100;'
            r = requests.post("https://overpass-api.de/api/interpreter", data={'data': q})
            df = pd.DataFrame(r.json()['elements'])
        elif "italy_poi" == "italy_fuel":
            df = pd.read_csv("https://overpass-api.de/api/interpreter", sep=";", skiprows=1).head(500)
        else:
            r = requests.get("https://overpass-api.de/api/interpreter")
            data = r.json()
            df = pd.DataFrame(data['features'] if 'features' in data else (data if isinstance(data, list) else [data]))
        
        upload_to_hf(df, repo_id, "italy_poi")
    except Exception as e: log.error(f"Errore in italy_poi: {e}")

if __name__ == "__main__": run()