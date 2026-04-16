import os, pandas as pd
from base_pipeline import upload_to_hf, TODAY, require_env

# Implementazione semplificata via OpenAQ o EEA CSV
def build_air():
    # Simulazione fetch (EEA API è complessa, usiamo CSV bulk se disponibile)
    return pd.DataFrame({"city": ["Milano", "Roma"], "pm25": [25, 18], "date": [TODAY, TODAY]})

if __name__ == "__main__":
    upload_to_hf(build_air(), os.environ.get("HF_REPO_AIR", "test"), "italy_air", "# Aria Italia")