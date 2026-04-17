# Italy Data Arbitrage System 🇮🇹📊

Automated pipeline for extracting, processing, and delivering high-value Italian datasets.

## 🚀 Overview
This system runs daily via GitHub Actions to collect fragmented data from institutional Italian sources, cleans it, and uploads analysis-ready Parquet files to Hugging Face Datasets.

## 📁 Datasets included:
- **01 Weather**: 30 years of historical data for 8 Italian cities.
- **02 Energy**: Real-time GME electricity prices (PUN).
- **04 Seismic**: INGV seismic events monitoring.
- **08 AI Corpus**: Cleaned Italian text for LLM training.

## 🛠️ Tech Stack
- **Language**: Python 3.11
- **Automation**: GitHub Actions (Cron schedule)
- **Storage**: Hugging Face Datasets (Parquet format)
- **Monitoring**: Automated Gmail alerts for pipeline failures.

## ⚙️ Setup
1. Clone the repo.
2. Set up GitHub Secrets: `HF_TOKEN`, `GMAIL_APP_PASSWORD`, `NOAA_TOKEN`.
3. The workflows will trigger automatically or can be started via 'Workflow Dispatch'.
