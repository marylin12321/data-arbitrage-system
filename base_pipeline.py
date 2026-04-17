import os, logging, tempfile, pandas as pd
from datetime import datetime
from huggingface_hub import HfApi

HF_TOKEN = os.environ.get("HF_TOKEN")
TODAY = datetime.now().strftime("%Y-%m-%d")

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

def require_env(name):
    val = os.environ.get(name)
    if not val: raise ValueError(f"Manca Secret: {name}")
    return val

def upload_to_hf(df, repo_id, filename):
    if df is None or df.empty: return False
    api = HfApi(token=HF_TOKEN)
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, f"{filename}_{TODAY}.parquet")
        df.to_parquet(path, index=False)
        with open(os.path.join(tmp, "README.md"), "w", encoding="utf-8") as rm:
            rm.write(f"# {filename}\nUpdated: {TODAY}\nProvider: GabrieleCorsoIT")
        try:
            api.upload_file(path_or_fileobj=path, path_in_repo=f"data/{filename}_{TODAY}.parquet", repo_id=repo_id, repo_type="dataset")
            api.upload_file(path_or_fileobj=os.path.join(tmp, "README.md"), path_in_repo="README.md", repo_id=repo_id, repo_type="dataset")
            log.info(f"✅ Caricato con successo")
            return True
        except Exception as e:
            log.error(f"Errore caricamento: {e}")
            return False