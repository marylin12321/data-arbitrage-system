import os, sys, requests, pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from base_pipeline import upload_to_hf, require_env, log

def run():
    repo_id = require_env("HF_REPO_AI_TEXT")
    try:
        if "italian_ai_corpus" == "italy_poi":
            q = '[out:json];area["name"="Italia"]->.a;(node["amenity"~"restaurant|hotel"](area.a););out 100;'
            r = requests.post("https://it.wikipedia.org/w/api.php?action=query&list=recentchanges&rclimit=100&format=json", data={'data': q})
            df = pd.DataFrame(r.json()['elements'])
        elif "italian_ai_corpus" == "italy_fuel":
            df = pd.read_csv("https://it.wikipedia.org/w/api.php?action=query&list=recentchanges&rclimit=100&format=json", sep=";", skiprows=1).head(500)
        else:
            r = requests.get("https://it.wikipedia.org/w/api.php?action=query&list=recentchanges&rclimit=100&format=json")
            data = r.json()
            df = pd.DataFrame(data['features'] if 'features' in data else (data if isinstance(data, list) else [data]))
        
        upload_to_hf(df, repo_id, "italian_ai_corpus")
    except Exception as e: log.error(f"Errore in italian_ai_corpus: {e}")

if __name__ == "__main__": run()