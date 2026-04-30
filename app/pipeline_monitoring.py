import os
import psycopg2
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD")
)

def get_single_value(cursor, query):
    cursor.execute(query)
    return cursor.fetchone()[0]

def monitor_pipeline():
    cursor = conn.cursor()

    total_stock_rows = get_single_value(cursor, "SELECT COUNT(*) FROM stock_prices;")
    total_symbols = get_single_value(cursor, "SELECT COUNT(DISTINCT symbol) FROM stock_prices;")
    latest_stock_insert = get_single_value(cursor, "SELECT MAX(created_at) FROM stock_prices;")

    total_trend_rows = get_single_value(cursor, "SELECT COUNT(*) FROM stock_trends;")
    latest_trend_run = get_single_value(cursor, "SELECT MAX(created_at) FROM stock_trends;")

    total_prediction_rows = get_single_value(cursor, "SELECT COUNT(*) FROM stock_predictions;")
    latest_prediction_run = get_single_value(cursor, "SELECT MAX(created_at) FROM stock_predictions;")

    now = get_single_value(cursor, "SELECT CURRENT_TIMESTAMP;").replace(tzinfo=None)

    notes = []

    if latest_stock_insert is None:
        notes.append("No stock data found.")
    elif latest_stock_insert < now - timedelta(minutes=10):
        notes.append("Stock data is stale.")

    if latest_trend_run is None:
        notes.append("No trend detection runs found.")
    elif latest_trend_run < now - timedelta(minutes=10):
        notes.append("Trend detection is stale.")

    if latest_prediction_run is None:
        notes.append("No prediction runs found.")
    elif latest_prediction_run < now - timedelta(minutes=10):
        notes.append("Price prediction is stale.")

    if total_symbols < 4:
        notes.append("Expected at least 4 stock symbols.")

    pipeline_status = "Healthy" if not notes else "Warning"
    notes_text = " | ".join(notes) if notes else "Pipeline operating normally."

    insert_query = """
    INSERT INTO pipeline_monitoring (
        total_stock_rows,
        total_symbols,
        latest_stock_insert,
        total_trend_rows,
        latest_trend_run,
        total_prediction_rows,
        latest_prediction_run,
        pipeline_status,
        notes
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    cursor.execute(
        insert_query,
        (
            total_stock_rows,
            total_symbols,
            latest_stock_insert,
            total_trend_rows,
            latest_trend_run,
            total_prediction_rows,
            latest_prediction_run,
            pipeline_status,
            notes_text
        )
    )

    conn.commit()

    print("Pipeline Monitoring Report")
    print("--------------------------")
    print(f"Total stock rows: {total_stock_rows}")
    print(f"Total symbols: {total_symbols}")
    print(f"Latest stock insert: {latest_stock_insert}")
    print(f"Total trend rows: {total_trend_rows}")
    print(f"Latest trend run: {latest_trend_run}")
    print(f"Total prediction rows: {total_prediction_rows}")
    print(f"Latest prediction run: {latest_prediction_run}")
    print(f"Status: {pipeline_status}")
    print(f"Notes: {notes_text}")

    cursor.close()

if __name__ == "__main__":
    monitor_pipeline()
    conn.close()
