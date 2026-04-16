import os, pandas as pd
from base_pipeline import upload_to_hf, log, TODAY, require_env

require_env("HF_REPO_ENERGY")
URL = "https://data.open-power-system-data.org/time_series/latest/time_series_60min_singleindex.csv"

def build_energy():
    log.info("Download dati energia...")
    df = pd.read_csv(URL, usecols=["utc_timestamp","IT_price_day_ahead"])
    df = df.dropna().rename(columns={"IT_price_day_ahead":"price_eur_mwh"})
    df["price_spike"] = (df["price_eur_mwh"] > df["price_eur_mwh"].quantile(0.95)).astype(int)
    return df

if __name__ == "__main__":
    df = build_energy()
    upload_to_hf(df, os.environ["HF_REPO_ENERGY"], "italy_energy", "# Prezzi Energia Italia")
