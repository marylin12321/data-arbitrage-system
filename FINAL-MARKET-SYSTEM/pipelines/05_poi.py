import os, sys, requests, pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from base_pipeline import upload_to_hf, require_env
def run():
    repo_id = require_env("HF_REPO_POI")
    q = '[out:json];area["name"="Italia"]->.a;(node["amenity"~"restaurant|hotel"](area.a););out 500;'
    df = pd.DataFrame(requests.post("https://overpass-api.de/api/interpreter", data={'data': q}).json()['elements'])
    upload_to_hf(df, repo_id, "italy_poi")
if __name__ == "__main__": run()
