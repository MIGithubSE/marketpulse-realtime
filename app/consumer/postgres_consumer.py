import os
import json
import psycopg2
from dotenv import load_dotenv
from kafka import KafkaConsumer

load_dotenv()

TOPIC = os.getenv("KAFKA_TOPIC", "stock_prices")
BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD")
)

cursor = conn.cursor()

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=BOOTSTRAP_SERVERS,
    auto_offset_reset="latest",
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

insert_query = """
INSERT INTO stock_prices (
    symbol,
    timestamp,
    open_price,
    high_price,
    low_price,
    close_price,
    volume
)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

print("Listening for Kafka messages...")

for message in consumer:
    record = message.value

    cursor.execute(
        insert_query,
        (
            record["symbol"],
            record["timestamp"],
            record["open_price"],
            record["high_price"],
            record["low_price"],
            record["close_price"],
            record["volume"]
        )
    )

    conn.commit()
    print("Inserted into PostgreSQL:", record)
