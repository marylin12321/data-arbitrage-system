import os, sys, requests, pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from base_pipeline import upload_to_hf, require_env
def run():
    repo_id = require_env("HF_REPO_FUEL")
    # Download diretto CSV Osservaprezzi Carburanti
    url = "https://www.mise.gov.it/images/stories/carburanti/prezzo_alle_pompe.csv"
    try:
        df = pd.read_csv(url, sep=";", skiprows=1)
        upload_to_hf(df, repo_id, "italy_fuel_prices")
    except: pass
if __name__ == "__main__": run()
