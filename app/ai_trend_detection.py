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

def detect_trends():
    query = """
    WITH deduplicated_prices AS (
        SELECT DISTINCT ON (symbol, timestamp)
            symbol,
            timestamp,
            close_price
        FROM stock_prices
        ORDER BY symbol, timestamp, created_at DESC
    )
    SELECT symbol, timestamp, close_price
    FROM deduplicated_prices
    ORDER BY symbol, timestamp;
    """

    df = pd.read_sql(query, conn)

    if df.empty:
        print("No stock data found.")
        return

    cursor = conn.cursor()

    for symbol in df["symbol"].unique():
        stock_df = df[df["symbol"] == symbol].copy()

        if len(stock_df) < 10:
            print(f"Not enough unique timestamp data for {symbol}")
            continue

        stock_df["short_ma"] = stock_df["close_price"].rolling(window=3).mean()
        stock_df["long_ma"] = stock_df["close_price"].rolling(window=10).mean()

        latest = stock_df.dropna().iloc[-1]

        short_ma = float(latest["short_ma"])
        long_ma = float(latest["long_ma"])
        latest_close = float(latest["close_price"])

        if short_ma > long_ma:
            trend_signal = "Bullish"
        elif short_ma < long_ma:
            trend_signal = "Bearish"
        else:
            trend_signal = "Neutral"

        confidence_score = abs(short_ma - long_ma) / latest_close * 100

        insert_query = """
        INSERT INTO stock_trends (
            symbol,
            latest_timestamp,
            latest_close,
            short_ma,
            long_ma,
            trend_signal,
            confidence_score
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """

        cursor.execute(
            insert_query,
            (
                symbol,
                latest["timestamp"],
                latest_close,
                short_ma,
                long_ma,
                trend_signal,
                confidence_score
            )
        )

        conn.commit()

        print(
            f"{symbol}: {trend_signal} | "
            f"Unique Rows={len(stock_df)} | "
            f"Close={latest_close:.2f} | "
            f"Short MA={short_ma:.2f} | "
            f"Long MA={long_ma:.2f} | "
            f"Confidence={confidence_score:.4f}%"
        )

    cursor.close()

if __name__ == "__main__":
    detect_trends()
    conn.close()
