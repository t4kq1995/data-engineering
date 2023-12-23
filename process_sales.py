#!/usr/bin/env python
# coding: utf-8
import json
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.http_operator import SimpleHttpOperator

# -----------------------------------------------------------------------------
# --- Default DAG settings ---
# -----------------------------------------------------------------------------
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2022, 8, 9),
    'end_date': datetime(2022, 8, 12),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'catchup': True,
    'max_active_runs': 1
}

# -----------------------------------------------------------------------------
# --- Define the DAG ---
# -----------------------------------------------------------------------------
dag = DAG(
    'process_sales',
    default_args=default_args,
    description='DAG to send requests to an API',
    schedule_interval='0 1 * * *',  # Schedule every day at 1 AM UTC
)

# -----------------------------------------------------------------------------
# --- Task 1 ---
# -----------------------------------------------------------------------------
extract_data_from_api_task = SimpleHttpOperator(
    task_id='extract_data_from_api',
    http_conn_id='extract_data_from_api',
    endpoint='/',
    headers={'Content-Type': 'application/json'},
    method='POST',
    data=json.dumps({
        "date": "{{ ds }}",
        "raw_dir": "/file_storage/raw/sales/{{ ds }}"
    }),
    response_check=lambda response: response.status_code == 201,
    dag=dag,
)

# -----------------------------------------------------------------------------
# --- Task 2 ---
# -----------------------------------------------------------------------------
convert_to_avro_task = SimpleHttpOperator(
    task_id='convert_to_avro',
    http_conn_id='convert_to_avro',
    endpoint='/',
    headers={'Content-Type': 'application/json'},
    method='POST',
    data=json.dumps({
        "stg_dir": "/file_storage/stg/sales/{{ ds }}",
        "raw_dir": "/file_storage/raw/sales/{{ ds }}"
    }),
    response_check=lambda response: response.status_code == 201,
    dag=dag,
)

# -----------------------------------------------------------------------------
# --- Define the task dependencies ---
# -----------------------------------------------------------------------------
extract_data_from_api_task >> convert_to_avro_task
