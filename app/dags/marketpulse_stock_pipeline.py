from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

PROJECT_DIR = "/home/mo/projects/marketpulse-realtime"

default_args = {
    "owner": "mohammed",
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="marketpulse_stock_pipeline",
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule_interval="*/5 * * * *",
    catchup=False,
    description="MarketPulse real-time stock data pipeline"
) as dag:

    fetch_stock_data = BashOperator(
        task_id="fetch_stock_data_to_kafka",
        bash_command=f"cd {PROJECT_DIR} && source venv/bin/activate && python app/producer/stock_producer.py"
    )

    fetch_stock_data
