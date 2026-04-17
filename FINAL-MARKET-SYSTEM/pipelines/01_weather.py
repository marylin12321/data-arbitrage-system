import os, sys, requests, pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from base_pipeline import upload_to_hf, require_env, TODAY
def run():
    repo_id = require_env("HF_REPO_WEATHER")
    # Stazione Roma Urbe
    url = f"https://www.ncei.noaa.gov/access/services/data/v1?dataset=daily-summaries&stations=GMM00010384&startDate=2024-01-01&endDate={TODAY}&format=json"
    df = pd.DataFrame(requests.get(url).json())
    upload_to_hf(df, repo_id, "italy_weather")
if __name__ == "__main__": run()
