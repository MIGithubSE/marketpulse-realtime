# 🚀 MarketPulse – Real-Time Stock Analytics Pipeline

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Kafka](https://img.shields.io/badge/Kafka-Streaming-black)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![Airflow](https://img.shields.io/badge/Airflow-Orchestration-red)
![Spark](https://img.shields.io/badge/Spark-Big%20Data-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![Docker](https://img.shields.io/badge/Docker-Containerization-blue)

---

# 📌 Overview

MarketPulse is a production-style real-time stock analytics pipeline that ingests, processes, analyzes, monitors, and visualizes live market data.

The project demonstrates how modern real-time data engineering systems combine:

* ⚡ Real-time streaming
* 🧠 Machine learning
* 🔄 Workflow orchestration
* 📊 Big data processing
* 📈 Interactive monitoring dashboards

---

# 🏗️ Architecture

```text
        ┌──────────────┐
        │  Kafka       │
        │  Producer    │
        └──────┬───────┘
               ↓
        ┌──────────────┐
        │   Kafka      │
        │  Consumer    │
        └──────┬───────┘
               ↓
        ┌──────────────┐
        │ PostgreSQL   │
        │ (Raw Data)   │
        └──────┬───────┘
               ↓
        ┌──────────────┐
        │   Airflow    │
        │ Orchestration│
        └──────┬───────┘
               ↓
   ┌───────────┼───────────┐
   ↓           ↓           ↓
Analysis   AI Models    Monitoring
   ↓           ↓           ↓
        ┌──────────────┐
        │   Spark      │
        │ Aggregation  │
        └──────┬───────┘
               ↓
        ┌──────────────┐
        │ PostgreSQL   │
        │ (Insights)   │
        └──────┬───────┘
               ↓
        ┌──────────────┐
        │ Streamlit    │
        │ Dashboard    │
        └──────────────┘
```

---

# ⚙️ Key Features

## ⚡ Real-Time Streaming

* Kafka producer simulates real stock market ingestion
* Kafka consumer writes directly into PostgreSQL
* Continuous streaming architecture

---

## 🗄️ Data Storage

PostgreSQL stores:

* raw stock data
* trend signals
* AI predictions
* monitoring metrics
* Spark aggregates

---

## 🧠 AI & Machine Learning

### Trend Detection

* Bullish / Bearish classification
* Moving average analysis
* Confidence scoring

### Price Prediction

* Predicts next close price
* Calculates:

  * predicted change
  * predicted direction

---

## 📊 Big Data Processing (Spark)

Spark aggregation pipeline calculates:

* Average close price
* Maximum close price
* Minimum close price
* Average trading volume
* Total records per symbol

---

## 🔄 Workflow Orchestration (Airflow)

Apache Airflow orchestrates:

* AI trend detection
* price prediction
* Spark processing
* monitoring checks

### Stable Manual-Only Workflow

The DAG is intentionally configured in manual-only mode for stability and controlled execution.

Features include:

* `schedule=None`
* single active DAG run
* reduced Airflow parallelism
* example DAGs disabled
* successful manual DAG execution verified

---

# 📈 Interactive Streamlit Dashboard

## Dashboard Features

* Real-time stock charts
* AI prediction tables
* Spark aggregated insights
* Pipeline monitoring section
* Smart freshness indicators
* Auto-refresh every 30 seconds
* Safe PostgreSQL loading logic
* Empty-table handling
* Improved dashboard stability

## Current Dashboard Status

* ✅ Stable
* ✅ Auto-refreshing
* ✅ Connected to PostgreSQL
* ✅ Displays live pipeline metrics
* ✅ Manual Airflow runs reflected correctly

---

# 📡 Monitoring System

Pipeline monitoring tracks:

* total stock rows
* total symbols
* latest stock insert
* trend freshness
* prediction freshness
* pipeline health state

Status types:

* 🟢 Healthy
* 🟠 Warning
* 🔴 Stale

The monitoring system validates that:

* Kafka ingestion is active
* PostgreSQL is updating correctly
* AI analysis modules are producing fresh results
* Spark aggregation tables exist and remain updated
* Dashboard metrics reflect current pipeline activity

The MarketPulse project now behaves like a production-style real-time analytics pipeline with controlled manual orchestration and stable dashboard monitoring.

---

# 🧪 Example Output

| Symbol | Avg Price | Max Price | Min Price | Avg Volume |
| ------ | --------- | --------- | --------- | ---------- |
| AAPL   | 277.18    | 287.40    | 269.50    | 2055.53    |
| TSLA   | 387.26    | 397.30    | 377.60    | 2320.11    |
| IBM    | 232.09    | 233.00    | 226.00    | 4594.45    |
| MSFT   | 416.65    | 428.44    | 408.65    | 717.97     |

---

# 🛠️ Tech Stack

| Layer            | Technology     |
| ---------------- | -------------- |
| Language         | Python         |
| Streaming        | Apache Kafka   |
| Database         | PostgreSQL     |
| Workflow         | Apache Airflow |
| Big Data         | Apache Spark   |
| Dashboard        | Streamlit      |
| Containerization | Docker         |

---

# 🚀 Getting Started

## 1. Clone the Repository

```bash
git clone https://github.com/MIGithubSE/marketpulse-realtime.git
cd marketpulse-realtime
```

---

## 2. Start Infrastructure

```bash
sudo service postgresql stop
docker compose up -d
docker ps
```

---

## 3. Activate Virtual Environment

```bash
source venv/bin/activate
```

---

## 4. Start Kafka Consumer

```bash
python app/consumer/postgres_consumer.py
```

---

## 5. Start Kafka Producer

```bash
python app/producer/stock_producer.py
```

---

## 6. Run Streamlit Dashboard

```bash
streamlit cache clear
streamlit run app/dashboard/dashboard.py
```

Open:

```text
http://localhost:8501
```

---

## 7. Start Airflow (Manual Mode)

```bash
AIRFLOW__CORE__PARALLELISM=2 \
AIRFLOW__CORE__MAX_ACTIVE_TASKS_PER_DAG=1 \
airflow standalone
```

Open:

```text
http://localhost:8080
```

---

# ⚠️ Current Stable Runtime Workflow

The project currently runs most reliably using a controlled manual execution flow.

## Recommended Startup Order

Start Docker services first:

```bash
sudo service postgresql stop
docker compose up -d
docker ps
```

Activate the virtual environment:

```bash
source venv/bin/activate
```

Run the Kafka consumer:

```bash
python app/consumer/postgres_consumer.py
```

In another terminal, run the producer:

```bash
python app/producer/stock_producer.py
```

Run analytics modules manually:

```bash
python app/ai_trend_detection.py
python app/price_prediction.py
python app/spark_processing.py
python app/pipeline_monitoring.py
```

Launch the dashboard:

```bash
streamlit cache clear
streamlit run app/dashboard/dashboard.py
```

---

# 🔄 Airflow Status

Airflow integration is currently configured for manual DAG execution only.

Current DAG configuration:

```python
schedule=None
```

This prevents automatic scheduling conflicts during development and testing.

The DAG can still be triggered manually through:

* Airflow UI
* CLI commands

Example:

```bash
airflow dags trigger marketpulse_stock_pipeline
```

---

# ✅ Verified Working Components

The following components are confirmed operational:

✅ Kafka Producer
✅ Kafka Consumer
✅ PostgreSQL Integration
✅ Spark Aggregation Pipeline
✅ AI Trend Detection
✅ Price Prediction Module
✅ Pipeline Monitoring
✅ Streamlit Dashboard
✅ Manual Airflow DAG Execution
✅ GitHub Integration

---

# 🛠️ Troubleshooting

## Dashboard Freeze / Infinite Loading

If the dashboard hangs on:

```python
load_data(...)
```

Run the Spark aggregation manually:

```bash
python app/spark_processing.py
```

Then restart Streamlit:

```bash
streamlit cache clear
streamlit run app/dashboard/dashboard.py
```

---

## PostgreSQL Connection Refused

If PostgreSQL fails to connect:

```text
connection refused
```

Run:

```bash
sudo service postgresql stop
docker compose up -d
docker ps
```

---

## PostgreSQL Table Missing

Error:

```text
psycopg2.errors.UndefinedTable:
relation "spark_stock_aggregates" does not exist
```

Fix:

```bash
python app/spark_processing.py
```

---

## GitHub SSH Permission Error

If Git push fails with:

```text
Permission denied (publickey)
```

Run:

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/marketpulse_github
ssh -T git@github.com
```

Then retry:

```bash
git push
```

---

# 📊 Pipeline Flow

1. Kafka streams stock data
2. Consumer writes to PostgreSQL
3. Airflow manually triggers:

   * AI trend detection
   * price prediction
   * Spark aggregation
   * pipeline monitoring
4. Results written back to PostgreSQL
5. Streamlit dashboard visualizes live analytics

---

# 📈 Future Improvements

* Real-time Spark Streaming
* Live Kafka ingestion counters
* Smarter dashboard status badges
* Auto-refresh countdown timers
* Advanced ML forecasting
* News sentiment analysis
* Anomaly detection
* React frontend
* Cloud deployment

---

# 👨‍💻 Author

**Mohammed Idriss**

GitHub:
https://github.com/MIGithubSE

---

# ⭐ Why This Project Stands Out

This project demonstrates:

* End-to-end real-time data pipelines
* Production-style orchestration
* Machine learning integration
* Big data processing with Spark
* Real-time monitoring dashboards
* Stream processing architecture
* Dockerized infrastructure
* Airflow workflow management

It reflects systems commonly used in:

* fintech
* analytics platforms
* AI-driven applications
* streaming data engineering
* real-time monitoring systems

