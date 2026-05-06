import os
from datetime import datetime

import pandas as pd
import plotly.express as px
import psycopg2
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="MarketPulse Dashboard",
    page_icon="📈",
    layout="wide",
)

# Auto-refresh every 30 seconds
st.markdown(
    """
    <meta http-equiv="refresh" content="30">
    """,
    unsafe_allow_html=True,
)

st.title("🚀 MarketPulse Real-Time Stock Analytics Dashboard")

conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST", "localhost"),
    port=os.getenv("POSTGRES_PORT", "5432"),
    dbname=os.getenv("POSTGRES_DB", "marketpulse"),
    user=os.getenv("POSTGRES_USER", "marketpulse_user"),
    password=os.getenv("POSTGRES_PASSWORD", "marketpulse_pass"),
)


@st.cache_data(ttl=20)
def load_data(query: str) -> pd.DataFrame:
    return pd.read_sql(query, conn)


stock_df = load_data(
    """
    SELECT symbol, timestamp, close_price, volume, created_at
    FROM stock_prices
    ORDER BY created_at DESC
    LIMIT 5000;
    """
)

trend_df = load_data(
    """
    SELECT DISTINCT ON (symbol)
        symbol,
        trend_signal,
        ROUND(confidence_score::numeric, 4) AS confidence_score,
        created_at
    FROM stock_trends
    ORDER BY symbol, created_at DESC;
    """
)

prediction_df = load_data(
    """
    SELECT DISTINCT ON (symbol)
        symbol,
        latest_close,
        predicted_next_close,
        predicted_change,
        predicted_direction,
        created_at
    FROM stock_predictions
    ORDER BY symbol, created_at DESC;
    """
)

monitor_df = load_data(
    """
    SELECT pipeline_status, notes, total_stock_rows, total_symbols, created_at
    FROM pipeline_monitoring
    ORDER BY created_at DESC
    LIMIT 5;
    """
)

spark_df = load_data(
    """
    SELECT symbol, total_records, avg_close_price, max_close_price, min_close_price, avg_volume
    FROM spark_stock_aggregates
    ORDER BY symbol;
    """
)

if stock_df.empty:
    st.error("No stock data found in PostgreSQL.")
    st.stop()

stock_df["created_at"] = pd.to_datetime(stock_df["created_at"])
stock_df["timestamp"] = pd.to_datetime(stock_df["timestamp"])

latest_monitor = monitor_df.iloc[0] if not monitor_df.empty else None
latest_stock_time = stock_df["created_at"].max()
seconds_since_latest = (pd.Timestamp.now() - latest_stock_time).total_seconds()

if seconds_since_latest <= 600:
    live_status = "🟢 Fresh"
elif seconds_since_latest <= 21600:  # 6 hours
    live_status = "🟠 Delayed"
else:
    live_status = "🔴 Stale"

total_rows = int(latest_monitor["total_stock_rows"]) if latest_monitor is not None else len(stock_df)
total_symbols = int(latest_monitor["total_symbols"]) if latest_monitor is not None else stock_df["symbol"].nunique()
pipeline_status = latest_monitor["pipeline_status"] if latest_monitor is not None else "Unknown"

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Rows", f"{total_rows:,}")
col2.metric("Symbols", total_symbols)
col3.metric("Pipeline Status", pipeline_status)
col4.metric("Data Freshness", live_status)
col5.metric("Loaded Rows", f"{len(stock_df):,}")

st.caption(f"Latest stock insert: {latest_stock_time}")

st.divider()

symbols = sorted(stock_df["symbol"].unique())
selected_symbols = st.multiselect(
    "Select symbols",
    symbols,
    default=symbols,
)

filtered_df = stock_df[stock_df["symbol"].isin(selected_symbols)].copy()

st.subheader("📈 Stock Price Movement")

fig = px.line(
    filtered_df.sort_values("created_at"),
    x="created_at",
    y="close_price",
    color="symbol",
    title="Close Price Over Time",
)

fig.update_layout(
    height=520,
    legend_title_text="Symbol",
    xaxis_title="Time",
    yaxis_title="Close Price",
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("🤖 Latest AI Trend Detection")
    st.dataframe(
        trend_df,
        use_container_width=True,
        hide_index=True,
    )

with right:
    st.subheader("🔮 Latest Price Predictions")
    st.dataframe(
        prediction_df,
        use_container_width=True,
        hide_index=True,
    )

st.divider()

st.subheader("⚡ Spark Aggregated Insights")
st.dataframe(
    spark_df,
    use_container_width=True,
    hide_index=True,
)

st.divider()

st.subheader("📡 Pipeline Monitoring")
st.dataframe(
    monitor_df,
    use_container_width=True,
    hide_index=True,
)

if latest_monitor is not None:
    notes = latest_monitor["notes"]
    if pipeline_status.lower() == "healthy":
        st.success(notes)
    else:
        st.warning(notes)

st.caption("MarketPulse dashboard reads from PostgreSQL and does not modify pipeline data.")
