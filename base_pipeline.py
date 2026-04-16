import os
import logging
import tempfile
import smtplib
import pandas as pd
from email.mime.text import MIMEText
from datetime import datetime
from huggingface_hub import HfApi, hf_hub_download

# Configurazione Automatica
HF_TOKEN = os.environ.get("HF_TOKEN")
TODAY = datetime.now().strftime("%Y-%m-%d")
ALERT_EMAIL = "corsogabriele92@gmail.com"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

def send_alert(subject, body):
    pw = os.environ.get("GMAIL_APP_PASSWORD")
    if not pw: return
    try:
        msg = MIMEText(body)
        msg["Subject"] = f"[DATA SYSTEM] {subject}"
        msg["From"], msg["To"] = ALERT_EMAIL, ALERT_EMAIL
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
            s.login(ALERT_EMAIL, pw)
            s.send_message(msg)
    except Exception as e: log.warning(f"Email fallita: {e}")

def get_last_date(repo_id):
    try:
        path = hf_hub_download(repo_id=repo_id, filename="last_update.txt", repo_type="dataset", token=HF_TOKEN)
        with open(path, "r") as f: return f.read().strip()
    except: return None

def upload_to_hf(df, repo_id, dataset_name, readme):
    if df is None or df.empty:
        log.warning(f"Nessun dato per {dataset_name}")
        return False
    
    api = HfApi(token=HF_TOKEN)
    with tempfile.TemporaryDirectory() as tmp:
        pq_path = f"{tmp}/{dataset_name}_{TODAY}.parquet"
        df.to_parquet(pq_path, index=False)
        with open(f"{tmp}/README.md", "w", encoding="utf-8") as f: f.write(readme)
        
        try:
            api.upload_file(path_or_fileobj=pq_path, path_in_repo=f"data/{dataset_name}_{TODAY}.parquet", repo_id=repo_id, repo_type="dataset")
            api.upload_file(path_or_fileobj=f"{tmp}/README.md", path_in_repo="README.md", repo_id=repo_id, repo_type="dataset")
            
            # Aggiorna la data solo se l'upload è riuscito
            with open(f"{tmp}/last_update.txt", "w") as f: f.write(TODAY)
            api.upload_file(path_or_fileobj=f"{tmp}/last_update.txt", path_in_repo="last_update.txt", repo_id=repo_id, repo_type="dataset")
            log.info(f"✅ {dataset_name} caricato.")
            return True
        except Exception as e:
            send_alert(f"ERRORE {dataset_name}", str(e))
            return False
