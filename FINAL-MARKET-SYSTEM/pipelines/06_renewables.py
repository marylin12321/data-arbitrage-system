import os, sys, requests, pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from base_pipeline import upload_to_hf, require_env
def run():
    repo_id = require_env("HF_REPO_RENEWABLES")
    url = "https://api.energy-charts.info/production?country=it"
    df = pd.DataFrame(requests.get(url).json())
    upload_to_hf(df, repo_id, "italy_renewables_production")
if __name__ == "__main__": run()
