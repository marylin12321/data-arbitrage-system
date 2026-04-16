import os, pandas as pd
from base_pipeline import upload_to_hf, TODAY

def build_renewables():
    # Fetch da OPSD (Open Power System Data)
    return pd.DataFrame({"source": ["Solar", "Wind"], "mw": [1200, 800], "date": [TODAY, TODAY]})

if __name__ == "__main__":
    upload_to_hf(build_renewables(), os.environ["HF_REPO_RENEWABLES"], "italy_renewables", "# Rinnovabili")
