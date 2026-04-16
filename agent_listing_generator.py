"""
agent_listing_generator.py
Genera e pubblica listing Gumroad per ogni dataset automaticamente.
Esegui manualmente dopo ogni nuovo dataset.
Richiede: GUMROAD_TOKEN (da app.gumroad.com/settings/applications)
"""

import os
import json
import requests
from datetime import datetime

GUMROAD_TOKEN = os.environ.get("GUMROAD_TOKEN", "")
TODAY = datetime.now().strftime("%Y-%m-%d")

# ── DEFINIZIONE PRODOTTI ─────────────────────────────────────────────────────
# Per ogni dataset: nome HF repo, prezzo, descrizione ottimizzata

PRODUCTS = [
    {
        "name": "Italy Daily Weather Data — 8 Cities, 30 Years | CSV + Parquet",
        "price_cents": 2900,
        "description": """**Clean, analysis-ready daily weather data for 8 major Italian cities.**

📍 Cities: Milano, Roma, Napoli, Palermo, Torino, Bologna, Firenze, Bari  
📅 Coverage: ~30 years rolling (updated weekly)  
📊 Variables: Max/min temperature (°C), precipitation (mm), snow depth, wind speed  
🗂️ Formats: CSV + Parquet (both included)  
📜 Source: NOAA GHCND (US Government, public domain)  
🔄 Updates: Weekly via automated pipeline  

**What you get:**
- Single clean file, no preprocessing needed
- Consistent column names and types across all cities and years
- Both CSV (Excel/R compatible) and Parquet (Python/Spark optimized)
- README with schema, load examples, and use case guidance

**Ideal for:**
- ML weather feature engineering for demand forecasting
- Insurance municipal risk modeling
- Agricultural yield prediction inputs
- Energy consumption weather normalization
- Climate trend analysis

**Load in 2 lines:**
```python
import pandas as pd
df = pd.read_parquet("italy_weather.parquet")
```

*Source data is public domain (US Gov). This product provides cleaning, structuring, and convenience.*""",
        "tags": ["weather", "italy", "climate", "machine-learning", "data", "parquet"],
        "hf_repo": "italy-weather-noaa",
    },
    {
        "name": "Italy Electricity Prices — Day-Ahead Market | 10 Years Hourly",
        "price_cents": 4900,
        "description": """**Hourly day-ahead electricity prices for Italy — 10 years of clean data.**

🏭 Market: Italian MGP (Mercato del Giorno Prima) day-ahead  
📅 Coverage: ~10 years hourly (updated daily)  
💶 Unit: €/MWh  
🗂️ Formats: CSV + Parquet  
📜 Source: ENTSO-E / Open Power System Data (CC BY 4.0)  

**Schema:** datetime_utc, price_eur_mwh, date, hour, year, month

**Ideal for:**
- Energy price forecasting models
- Renewable asset valuation and PPA pricing
- Industrial energy cost optimization
- ESG fund energy transition analysis
- Algorithmic power trading backtesting""",
        "tags": ["energy", "electricity", "italy", "prices", "time-series"],
        "hf_repo": "italy-energy-prices",
    },
    {
        "name": "Italy Air Quality — PM2.5, NO2, O3 | 5 Years | All Monitoring Stations",
        "price_cents": 2900,
        "description": """**Official Italian air quality monitoring data — all stations, all pollutants.**

🌍 Coverage: All Italian EEA monitoring stations  
📅 Period: ~5 years rolling hourly data  
☁️ Pollutants: PM2.5, PM10, NO2, O3, CO  
📜 Source: European Environment Agency (CC BY 4.0)  

**Ideal for:**
- Real estate air quality premium/discount modeling
- Insurance health risk scoring by municipality
- ESG scoring for real estate and infrastructure portfolios
- Urban planning and public health research""",
        "tags": ["air-quality", "pollution", "italy", "health", "environment"],
        "hf_repo": "italy-air-quality",
    },
    {
        "name": "Italy Seismic Data — 500K+ Events Since 1985 | INGV Official",
        "price_cents": 3900,
        "description": """**Complete seismic catalog for Italy — official INGV data since 1985.**

🌋 Coverage: All events Mw ≥ 1.5 within Italian territory  
📅 Period: 1985 to present (updated monthly)  
📊 Fields: Datetime, coordinates, depth, magnitude, location  
📜 Source: INGV — Istituto Nazionale di Geofisica e Vulcanologia (CC BY 4.0)  

**Ideal for:**
- Catastrophe (CAT) modeling for insurance and reinsurance
- Structural engineering seismic risk assessment
- Real estate seismic exposure analysis
- Infrastructure investment risk""",
        "tags": ["seismic", "earthquake", "italy", "risk", "insurance"],
        "hf_repo": "italy-seismic-ingv",
    },
    {
        "name": "Italy Points of Interest — 14 Categories | OpenStreetMap | 200K+ POI",
        "price_cents": 4900,
        "description": """**Comprehensive POI dataset for Italy — ready for location intelligence.**

📍 200,000+ POIs across 14 categories  
🏪 Categories: Supermarkets, Pharmacies, Hospitals, Schools, Banks, Restaurants, Hotels, Gas Stations, EV Charging, Train Stations, Airports, Shopping Malls, Gyms, Universities  
📊 Fields: Coordinates, name, brand, address, postcode, phone, website, opening hours  
📜 Source: OpenStreetMap (ODbL — commercial use OK with attribution)  

**Ideal for:**
- Retail site selection and competitor proximity analysis
- Delivery and logistics network optimization
- Real estate walkability scoring
- Location intelligence SaaS products""",
        "tags": ["poi", "location", "italy", "openstreetmap", "retail", "geospatial"],
        "hf_repo": "italy-poi-osm",
    },
    {
        "name": "Italian Text Corpus for AI Training — Legal, Medical, News | CC BY 4.0",
        "price_cents": 9900,
        "description": """**High-quality Italian text for LLM fine-tuning and NLP research.**

📚 Sources: EUR-Lex (EU law in Italian), Gazzetta Ufficiale, Wikipedia IT  
🏛️ Domains: Legal, Medical, Government, Encyclopedia, News  
✅ License: CC BY 4.0 / Public Domain — safe for commercial AI training  
🔄 Updated: Monthly  

**Why this matters:**
Italian is severely under-represented in open AI training corpora. Most available Italian  
text is either low-quality web crawl or legally ambiguous. This corpus provides clean,  
domain-specific, commercially licensed Italian text.

**Ideal for:**
- LLM fine-tuning for Italian language models
- Legal NLP for Italian jurisdiction
- Medical NLP for Italian healthcare
- Named Entity Recognition (NER) benchmarks
- RAG knowledge bases in Italian""",
        "tags": ["nlp", "italian", "ai-training", "llm", "legal", "text-corpus"],
        "hf_repo": "italian-text-ai-corpus",
    },
]


def create_gumroad_product(product: dict) -> dict:
    """Crea un prodotto su Gumroad via API."""
    url = "https://api.gumroad.com/v2/products"
    payload = {
        "access_token":  GUMROAD_TOKEN,
        "name":          product["name"],
        "description":   product["description"],
        "price":         product["price_cents"],
        "published":     False,  # Pubblica manualmente dopo review
    }
    r = requests.post(url, data=payload, timeout=30)
    return r.json()


def generate_listings_json() -> str:
    """
    Genera file JSON con tutti i listing pronti.
    Usa questo per incollare manualmente su Gumroad se preferisci.
    """
    listings = []
    for p in PRODUCTS:
        listings.append({
            "platform": "Gumroad",
            "name": p["name"],
            "price_usd": p["price_cents"] / 100,
            "tags": p["tags"],
            "hf_sample": f"https://huggingface.co/datasets/YOURNAME/{p['hf_repo']}",
            "description_preview": p["description"][:200] + "...",
        })
    return json.dumps(listings, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    if not GUMROAD_TOKEN:
        print("GUMROAD_TOKEN non impostato — salvo listing in JSON per upload manuale.")
        with open("listings_ready.json", "w", encoding="utf-8") as f:
            f.write(generate_listings_json())
        print("Salvato: listings_ready.json")
    else:
        print(f"Creazione {len(PRODUCTS)} prodotti su Gumroad...")
        for p in PRODUCTS:
            result = create_gumroad_product(p)
            if result.get("success"):
                pid = result["product"]["id"]
                print(f"✓ {p['name'][:50]}... → ID: {pid}")
            else:
                print(f"✗ {p['name'][:50]}... → {result.get('message')}")
