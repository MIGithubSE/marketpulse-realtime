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

def predict_prices():
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

        if len(stock_df) < 5:
            print(f"Not enough data for {symbol}")
            continue

        stock_df["close_price"] = stock_df["close_price"].astype(float)
        stock_df["price_change"] = stock_df["close_price"].diff()

        recent_changes = stock_df["price_change"].dropna().tail(5)

        if recent_changes.empty:
            print(f"Not enough price changes for {symbol}")
            continue

        latest_row = stock_df.iloc[-1]
        latest_close = float(latest_row["close_price"])
        average_change = float(recent_changes.mean())

        predicted_next_close = latest_close + average_change
        predicted_change = predicted_next_close - latest_close

        if predicted_change > 0:
            predicted_direction = "Up"
        elif predicted_change < 0:
            predicted_direction = "Down"
        else:
            predicted_direction = "Flat"

        insert_query = """
        INSERT INTO stock_predictions (
            symbol,
            latest_timestamp,
            latest_close,
            predicted_next_close,
            predicted_change,
            predicted_direction,
            model_type
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """

        cursor.execute(
            insert_query,
            (
                symbol,
                latest_row["timestamp"],
                latest_close,
                predicted_next_close,
                predicted_change,
                predicted_direction,
                "Rolling Average Price Change"
            )
        )

        conn.commit()

        print(
            f"{symbol}: Latest={latest_close:.2f} | "
            f"Predicted={predicted_next_close:.2f} | "
            f"Change={predicted_change:.4f} | "
            f"Direction={predicted_direction}"
        )

    cursor.close()

if __name__ == "__main__":
    predict_prices()
    conn.close()
