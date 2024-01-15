#!/usr/bin/env python
# coding: utf-8
import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator

# -----------------------------------------------------------------------------
# --- GCP Credentials ---
# -----------------------------------------------------------------------------
GCS_BUCKET_NAME = 'data-engineering-practice-2024'
SRC = "/".join(
    [
        '/'.join(os.getcwd().split('/')[:-1]),
        'lesson2/file_storage/stg/sales',
        '{{ ds }}/sales_{{ ds }}.avro'
    ]
)
DST = "src1/sales/v1/"


# -----------------------------------------------------------------------------
# --- Custom functions ---
# -----------------------------------------------------------------------------
def format_ds(ds, **kwargs):
    return ds.replace('-', '/')


# -----------------------------------------------------------------------------
# --- Default DAG settings ---
# -----------------------------------------------------------------------------
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2022, 8, 9),
    'end_date': datetime(2022, 8, 10),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'catchup': True,
    'max_active_runs': 1
}

# -----------------------------------------------------------------------------
# --- Define the DAG ---
# -----------------------------------------------------------------------------
dag = DAG(
    'upload_to_gcs',
    default_args=default_args,
    description='DAG to upload data to GCS',
)

# -----------------------------------------------------------------------------
# --- Upload ---
# -----------------------------------------------------------------------------
format_ds_task = PythonOperator(
    task_id='format_ds_task',
    python_callable=format_ds,
    provide_context=True,
    dag=dag,
)

upload_task = LocalFilesystemToGCSOperator(
   task_id="upload_to_gcs_task",
   src=SRC,
   dst="".join(
       [
           DST,
           "{{ task_instance.xcom_pull(task_ids='format_ds_task') }}"
           "/sales_{{ ds }}.avro"
       ]
   ),
   bucket=GCS_BUCKET_NAME,
   dag=dag
)

# -----------------------------------------------------------------------------
# --- Define the task dependencies ---
# -----------------------------------------------------------------------------
format_ds_task >> upload_task
