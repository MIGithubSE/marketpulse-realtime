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

