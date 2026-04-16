import os, requests, pandas as pd
from datetime import datetime, timedelta
from base_pipeline import upload_to_hf, get_last_date, log, TODAY

def build_seismic():
    last = get_last_date(os.environ["HF_REPO_SEISMIC"])
    start = (datetime.strptime(last, "%Y-%m-%d") - timedelta(days=3)).strftime("%Y-%m-%d") if last else "2020-01-01"
    url = f"https://webservices.ingv.it/fdsnws/event/1/query?starttime={start}&endtime={TODAY}&minmag=1.5&format=text"
    r = requests.get(url)
    # Parsing testo INGV...
    return pd.DataFrame([x.split('|') for x in r.text.split('\n')[1:] if '|' in x])

if __name__ == "__main__":
    upload_to_hf(build_seismic(), os.environ["HF_REPO_SEISMIC"], "italy_seismic", "# Sismicità Italia")
