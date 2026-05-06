import os
import pandas as pd
import psycopg2
import streamlit as st
import plotly.express as px
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="MarketPulse Dashboard",
    page_icon="📈",
    layout="wide"
)

conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST", "localhost"),
    port=os.getenv("POSTGRES_PORT", "5432"),
    dbname=os.getenv("POSTGRES_DB", "marketpulse"),
    user=os.getenv("POSTGRES_USER", "marketpulse_user"),
    password=os.getenv("POSTGRES_PASSWORD", "marketpulse_pass")
)

@st.cache_data(ttl=30)
def load_table(query):
    return pd.read_sql(query, conn)

st.title("🚀 MarketPulse Real-Time Stock Analytics Dashboard")

stock_df = load_table("""
    SELECT symbol, timestamp, close_price, volume, created_at
    FROM stock_prices
    ORDER BY created_at DESC
    LIMIT 5000;
""")

trend_df = load_table("""
    SELECT symbol, trend_signal, confidence_score, created_at
    FROM stock_trends
    ORDER BY created_at DESC
    LIMIT 20;
""")

prediction_df = load_table("""
    SELECT symbol, latest_close, predicted_next_close, predicted_change, predicted_direction, created_at
    FROM stock_predictions
    ORDER BY created_at DESC
    LIMIT 20;
""")

monitor_df = load_table("""
    SELECT pipeline_status, notes, total_stock_rows, total_symbols, created_at
    FROM pipeline_monitoring
    ORDER BY created_at DESC
    LIMIT 5;
""")

spark_df = load_table("""
    SELECT symbol, total_records, avg_close_price, max_close_price, min_close_price, avg_volume
    FROM spark_stock_aggregates;
""")

latest_monitor = monitor_df.iloc[0] if not monitor_df.empty else None

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Rows", int(latest_monitor["total_stock_rows"]) if latest_monitor is not None else 0)
col2.metric("Symbols", int(latest_monitor["total_symbols"]) if latest_monitor is not None else 0)
col3.metric("Pipeline Status", latest_monitor["pipeline_status"] if latest_monitor is not None else "Unknown")
col4.metric("Latest Records Loaded", len(stock_df))

st.divider()

symbols = sorted(stock_df["symbol"].unique())
selected_symbols = st.multiselect("Select symbols", symbols, default=symbols)

filtered_df = stock_df[stock_df["symbol"].isin(selected_symbols)].copy()
filtered_df["created_at"] = pd.to_datetime(filtered_df["created_at"])

st.subheader("📈 Stock Price Movement")

fig = px.line(
    filtered_df.sort_values("created_at"),
    x="created_at",
    y="close_price",
    color="symbol",
    title="Close Price Over Time"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("🤖 Latest AI Trend Detection")
st.dataframe(trend_df, use_container_width=True)

st.subheader("🔮 Latest Price Predictions")
st.dataframe(prediction_df, use_container_width=True)

st.subheader("⚡ Spark Aggregated Insights")
st.dataframe(spark_df, use_container_width=True)

st.subheader("📡 Pipeline Monitoring")
st.dataframe(monitor_df, use_container_width=True)

st.caption("MarketPulse dashboard reads from PostgreSQL and does not modify pipeline data.")
