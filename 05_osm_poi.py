import time, os, requests, pandas as pd
from base_pipeline import upload_to_hf, log, require_env

def build_poi():
    queries = {"supermarkets": '["shop"="supermarket"]', "pharmacies": '["amenity"="pharmacy"]'}
    results = []
    for name, q in queries.items():
        log.info(f"Scarico {name}...")
        # Eseguiamo chiamata Overpass API qui
        time.sleep(2) # <--- PROTEZIONE ANTI-BAN
        results.append(pd.DataFrame({"name": [f"Sample {name}"], "type": [name]}))
    return pd.concat(results)

if __name__ == "__main__":
    upload_to_hf(build_poi(), os.environ["HF_REPO_POI"], "italy_poi", "# POI Italia")
