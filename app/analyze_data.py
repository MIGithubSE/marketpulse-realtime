import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD")
)

query = """
SELECT *
FROM stock_prices
ORDER BY timestamp DESC
LIMIT 100;
"""

df = pd.read_sql(query, conn)

print(df.head())
print("\nSummary:")
print(df.describe())
