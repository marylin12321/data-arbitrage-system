import os, requests, pandas as pd
from base_pipeline import upload_to_hf, log

def build_fuel():
    url = "https://www.mase.gov.it/sites/default/files/archivio/comunicati/dgerm/carburanti/prezzo_alle_8.csv"
    # Nota: richiede bypass certificato SSL spesso su siti gov
    try:
        df = pd.read_csv(url, sep=";", skiprows=1)
        return df
    except: return pd.DataFrame()

if __name__ == "__main__":
    upload_to_hf(build_fuel(), os.environ["HF_REPO_FUEL"], "italy_fuel", "# Carburanti Italia")
