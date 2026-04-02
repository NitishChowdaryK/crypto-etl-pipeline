import requests
import pandas as pd
import sqlite3
import logging
from datetime import datetime

# --- Config ---
DB_NAME = "crypto.db"
TABLE_NAME = "crypto_prices"
API_URL = (
    "https://api.coingecko.com/api/v3/coins/markets"
    "?vs_currency=usd&order=market_cap_desc&per_page=20&page=1"
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# --- Extract ---
def extract():
    logging.info("Extracting data from CoinGecko API...")
    r = requests.get(API_URL, timeout=10)
    r.raise_for_status()
    data = r.json()
    logging.info(f"Fetched {len(data)} records.")
    return data

# --- Transform ---
def transform(data):
    logging.info("Transforming data...")
    df = pd.DataFrame(data)
    df = df[[
        "id", "symbol", "name",
        "current_price", "market_cap",
        "total_volume", "price_change_percentage_24h",
        "circulating_supply"
    ]]
    df.rename(columns={
        "id": "coin_id",
        "current_price": "price_usd",
        "price_change_percentage_24h": "change_24h_pct"
    }, inplace=True)
    df.dropna(subset=["price_usd", "market_cap"], inplace=True)
    df["ingested_at"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"Transformed {len(df)} clean records.")
    return df

# --- Load (upsert) ---
def load(df):
    logging.info(f"Loading data into SQLite: {DB_NAME}")
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            coin_id TEXT,
            symbol TEXT,
            name TEXT,
            price_usd REAL,
            market_cap REAL,
            total_volume REAL,
            change_24h_pct REAL,
            circulating_supply REAL,
            ingested_at TEXT,
            PRIMARY KEY (coin_id, ingested_at)
        )
    """)
    df.to_sql(TABLE_NAME, conn, if_exists="append", index=False)
    conn.commit()
    conn.close()
    logging.info("Data loaded successfully.")

# --- Run ---
if __name__ == "__main__":
    raw = extract()
    clean = transform(raw)
    load(clean)
    print(clean.head())