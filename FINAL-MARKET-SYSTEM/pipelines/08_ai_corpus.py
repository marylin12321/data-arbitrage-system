import os, sys, requests, pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from base_pipeline import upload_to_hf, require_env
def run():
    repo_id = require_env("HF_REPO_AI_TEXT")
    url = "https://it.wikipedia.org/w/api.php?action=query&list=recentchanges&rclimit=100&format=json"
    data = requests.get(url).json()['query']['recentchanges']
    df = pd.DataFrame(data)
    upload_to_hf(df, repo_id, "italian_ai_corpus")
if __name__ == "__main__": run()
