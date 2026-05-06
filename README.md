# 🚀 MarketPulse – Real-Time Stock Analytics Pipeline

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Kafka](https://img.shields.io/badge/Kafka-Streaming-black)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![Airflow](https://img.shields.io/badge/Airflow-Orchestration-red)
![Spark](https://img.shields.io/badge/Spark-Big%20Data-orange)
![Docker](https://img.shields.io/badge/Docker-Containerization-blue)

---

## 📌 Overview

MarketPulse is a **production-style real-time data pipeline** that ingests, processes, analyzes, and monitors stock market data.

It demonstrates how modern data systems combine:

* ⚡ Real-time streaming
* 🧠 Machine learning
* 🔄 Workflow orchestration
* 📊 Big data processing

---

## 🏗️ Architecture

```
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
        └──────────────┘
```

---

## ⚙️ Key Features

### ⚡ Real-Time Streaming

* Kafka producer simulates stock market data
* Kafka consumer writes directly into PostgreSQL

### 🗄️ Data Storage

* PostgreSQL stores structured stock data
* Optimized for analytics queries

### 🧠 AI & Machine Learning

* Trend detection
* Price prediction models

### 📊 Big Data Processing (Spark)

* Aggregates:

  * Average price
  * Min / Max price
  * Volume insights
* Writes results back to database

### 🔄 Workflow Orchestration

* Apache Airflow DAG automates the entire pipeline
* Modular task execution

### 📡 Monitoring

* Pipeline health checks
* Data freshness validation

---

## 🧪 Example Output

| Symbol | Avg Price | Max Price | Min Price | Avg Volume |
| ------ | --------- | --------- | --------- | ---------- |
| AAPL   | 269.68    | 269.79    | 269.50    | 387.65     |
| TSLA   | 377.79    | 377.93    | 377.60    | 1803.75    |
| IBM    | 232.18    | 233.00    | 227.96    | 9247.14    |
| MSFT   | 428.23    | 428.44    | 428.00    | 848.75     |

---

## 🛠️ Tech Stack

| Layer            | Technology     |
| ---------------- | -------------- |
| Language         | Python         |
| Streaming        | Apache Kafka   |
| Database         | PostgreSQL     |
| Orchestration    | Apache Airflow |
| Big Data         | Apache Spark   |
| Containerization | Docker         |

---

## 🚀 Getting Started

### 1. Clone the repo

```
git clone https://github.com/MIGithubSE/marketpulse-realtime.git
cd marketpulse-realtime
```

### 2. Start services

```
docker compose up -d
```

### 3. Activate environment

```
source venv/bin/activate
```

### 4. Run Airflow

```
airflow standalone
```

Open:

```
http://localhost:8080
```

---


## ⚠️ Current Stable Runtime Workflow

The project currently runs most reliably using a controlled manual execution flow.

### Recommended Startup Order

Start Docker services first:

```bash
docker compose up -d
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

## 📊 Dashboard Features

The Streamlit dashboard currently provides:

- Real-time stock monitoring
- Spark aggregation insights
- AI trend detection
- Price prediction outputs
- Pipeline health monitoring
- Data freshness tracking

---

## 🔄 Airflow Status

Airflow integration is currently configured for manual DAG execution only.

Current DAG configuration:

```python
schedule=None
```

This prevents automatic scheduling conflicts during development and testing.

The DAG can still be triggered manually through:

- Airflow UI
- CLI commands

Example:

```bash
airflow dags trigger marketpulse_stock_pipeline
```

---

## 🧪 Verified Working Components

The following components are confirmed operational:

✅ Kafka Producer  
✅ Kafka Consumer  
✅ PostgreSQL Integration  
✅ Spark Aggregation Pipeline  
✅ AI Trend Detection  
✅ Price Prediction Module  
✅ Pipeline Monitoring  
✅ Streamlit Dashboard  
✅ GitHub CI Workflow (Manual Push)

---

## 🛠️ Troubleshooting

### Dashboard Freeze / Infinite Loading

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

### PostgreSQL Table Missing

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

### GitHub SSH Permission Error

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



## 📊 Pipeline Flow

1. Kafka streams stock data
2. Consumer writes to PostgreSQL
3. Airflow triggers:

   * Data analysis
   * AI trend detection
   * Price prediction
   * Monitoring checks
   * Spark aggregation
4. Results stored back in PostgreSQL

---

## 📈 Future Improvements

* Real-time Spark Streaming
* Interactive dashboard (Streamlit / React)
* Advanced ML models
* Anomaly detection
* News sentiment analysis

---

## 👨‍💻 Author

**Mohammed Idriss**
GitHub: https://github.com/MIGithubSE

---

## ⭐ Why This Project Stands Out

This project showcases:

* End-to-end data pipeline design
* Real-time data engineering
* Machine learning integration
* Big data processing with Spark
* Production-style architecture

It reflects real-world systems used in **fintech, analytics, and AI-driven platforms**.

