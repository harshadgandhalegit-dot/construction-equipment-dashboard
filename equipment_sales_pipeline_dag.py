"""
equipment_sales_pipeline_dag.py
--------------------------------
Apache Airflow DAG that orchestrates the Construction Equipment
Division Performance Dashboard data pipeline:

  1. Extract raw sales data (CSV source)
  2. Run Python cleaning/transformation (data_cleaning.py)
  3. Load cleaned data + division summary into SQL tables
  4. Run data quality checks
  5. Notify on success/failure

Schedule: Daily at 6:00 AM IST
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "harshad_gandhale",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="equipment_sales_pipeline",
    description="ETL pipeline for Construction Equipment Division Performance Dashboard",
    default_args=default_args,
    schedule_interval="0 6 * * *",  # daily at 6 AM
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["power-bi", "etl", "construction-equipment"],
) as dag:

    extract_task = BashOperator(
        task_id="extract_raw_data",
        bash_command="echo 'Extracting raw equipment_sales_sample.csv from source folder'",
    )

    def run_data_cleaning():
        import subprocess
        subprocess.run(["python", "python/data_cleaning.py"], check=True)

    clean_transform_task = PythonOperator(
        task_id="clean_and_transform_data",
        python_callable=run_data_cleaning,
    )

    load_sql_task = BashOperator(
        task_id="load_into_sql",
        bash_command=(
            "echo 'Loading equipment_sales_cleaned.csv and division_summary.csv "
            "into SQL tables via sql/queries.sql views'"
        ),
    )

    def run_quality_checks():
        import pandas as pd
        df = pd.read_csv("data/equipment_sales_cleaned.csv")
        assert (df["Units_Sold"] > 0).all(), "Data quality check failed: zero/negative units"
        assert (df["Revenue_INR"] >= df["Cost_INR"]).all(), "Data quality check failed: cost > revenue"
        print("Data quality checks passed.")

    quality_check_task = PythonOperator(
        task_id="data_quality_checks",
        python_callable=run_quality_checks,
    )

    refresh_powerbi_task = BashOperator(
        task_id="trigger_powerbi_refresh",
        bash_command="echo 'Triggering Power BI dataset refresh via Power BI REST API'",
    )

    extract_task >> clean_transform_task >> load_sql_task >> quality_check_task >> refresh_powerbi_task
