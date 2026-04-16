import os, pandas as pd
from base_pipeline import upload_to_hf, log

def clean_for_ai(df):
    if df.empty: return df
    df = df.drop_duplicates(subset=['text'])
    df = df[df['text'].str.len() > 250] # Solo testi lunghi e di qualità
    return df

if __name__ == "__main__":
    # Esempio: Carica dati da EUR-Lex o Gazzetta Ufficiale
    df_raw = pd.DataFrame({"text": ["Lungo testo giuridico di esempio...", "Altro testo medico..."], "source": ["GU", "ISS"]})
    df = clean_for_ai(df_raw)
    upload_to_hf(df, os.environ["HF_REPO_AI_TEXT"], "it_ai_corpus", "# Corpus AI Italiano")
