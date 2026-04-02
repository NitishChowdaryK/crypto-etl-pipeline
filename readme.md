# Crypto ETL Pipeline

An automated Python-based ETL pipeline that ingests live cryptocurrency market data from the CoinGecko public REST API, applies transformation and data quality logic, and loads structured records into a local SQLite database.

---

## Tech Stack
- **Language:** Python 3.11
- **Libraries:** Requests, Pandas, SQLite3
- **Database:** SQLite
- **Tools:** VS Code

---

## Architecture

```
CoinGecko REST API → Extract → Transform → Load → SQLite (crypto.db)
```

---

## Key Steps

1. **Extract** — Fetches top 20 cryptocurrencies by market cap from the CoinGecko `/coins/markets` endpoint
2. **Transform** — Selects relevant columns, renames fields, drops null records, and appends an ingestion timestamp
3. **Load** — Upserts clean records into a SQLite database table with a composite primary key `(coin_id, ingested_at)` to prevent duplicates

---

## Project Structure

```
crypto-etl-pipeline/
├── etl.py          # Main ETL script
├── crypto.db       # SQLite database (auto-generated on run)
└── README.md
```

---

## How to Run

```bash
# 1. Clone the repo
git clone https://github.com/NitishChowdaryK/crypto-etl-pipeline.git
cd crypto-etl-pipeline

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# 3. Install dependencies
pip install requests pandas

# 4. Run the pipeline
python etl.py
```

---

## Sample Output

```
2026-04-02 [INFO] Extracting data from CoinGecko API...
2026-04-02 [INFO] Fetched 20 records.
2026-04-02 [INFO] Transforming data...
2026-04-02 [INFO] Transformed 20 clean records.
2026-04-02 [INFO] Loading data into SQLite: crypto.db
2026-04-02 [INFO] Data loaded successfully.

   coin_id symbol     name  price_usd    market_cap  ...
0  bitcoin    btc  Bitcoin   66398.00  1.328945e+12  ...
1  ethereum    eth  Ethereum   2050.97  2.474929e+11  ...
```

---

## Skills Demonstrated
- REST API data ingestion
- ETL pipeline design (Extract → Transform → Load)
- Data cleaning and transformation with Pandas
- SQLite database design with upsert logic
- Python logging and error handling