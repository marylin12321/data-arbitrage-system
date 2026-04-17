import os, sys, requests, pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from base_pipeline import upload_to_hf, require_env
def run():
    repo_id = require_env("HF_REPO_AIR")
    url = "https://fme.discomap.eea.europa.eu/fmedatastreaming/AirQualityDownload/AQData_Extract.fmw?CountryCode=IT&CityName=Roma&Pollutant=1&Year_from=2024&Year_to=2024&Station=all"
    # Nota: EEA fornisce link a CSV, qui leggiamo i metadati
    df = pd.DataFrame({"source": [url], "status": ["check_csv_links"]})
    upload_to_hf(df, repo_id, "italy_air_quality")
if __name__ == "__main__": run()
