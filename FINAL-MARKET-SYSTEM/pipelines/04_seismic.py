import os, sys, requests, pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from base_pipeline import upload_to_hf, require_env, TODAY
def run():
    repo_id = require_env("HF_REPO_SEISMIC")
    url = f"https://webservices.ingv.it/fdsnws/event/1/query?format=json&starttime=2024-01-01&endtime={TODAY}"
    data = requests.get(url).json()['features']
    df = pd.DataFrame([f['properties'] for f in data])
    upload_to_hf(df, repo_id, "italy_seismic_events")
if __name__ == "__main__": run()
