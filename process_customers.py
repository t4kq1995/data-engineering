#!/usr/bin/env python
# coding: utf-8
from datetime import datetime, timedelta
from airflow import DAG
from airflow.contrib.operators.gcs_to_bq import GoogleCloudStorageToBigQueryOperator
from airflow.contrib.operators.bigquery_operator import BigQueryOperator
from airflow.operators.python_operator import PythonOperator

# -----------------------------------------------------------------------------
# --- Default DAG settings ---
# -----------------------------------------------------------------------------
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2022, 8, 1),
    'end_date': datetime(2022, 8, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'catchup': True,
    'max_active_runs': 1
}


def pass_ds_day_to_xcom(ds, **kwargs):
    ds_day = kwargs['execution_date'].strftime('%Y-%m-%-d')
    return ds_day


def get_ds_day_from_xcom(**kwargs):
    ti = kwargs['ti']
    ds_day = ti.xcom_pull(task_ids='pass_ds_day_to_xcom')
    return ds_day


# -----------------------------------------------------------------------------
# --- Define the DAG ---
# -----------------------------------------------------------------------------
dag = DAG(
    'process_customers',
    default_args=default_args,
    description='DAG to send data from bucket to Big Query',
    user_defined_macros={
        'ds_day': '{{ execution_date.strftime("%Y-%m-%-d") }}'
    }
)

# -----------------------------------------------------------------------------
# --- Convert ds variable ---
# -----------------------------------------------------------------------------
pass_ds_day_task = PythonOperator(
    task_id='pass_ds_day_to_xcom',
    python_callable=pass_ds_day_to_xcom,
    provide_context=True,
    dag=dag
)


get_ds_day_task = PythonOperator(
    task_id='get_ds_day_from_xcom',
    python_callable=get_ds_day_from_xcom,
    provide_context=True,
    dag=dag
)

# -----------------------------------------------------------------------------
# --- Copy data from GCP to BigQuery ---
# -----------------------------------------------------------------------------
copy_files_to_bronze = GoogleCloudStorageToBigQueryOperator(
    task_id='copy_files_to_bronze_bigquery',
    bucket='raw-data-de',
    source_objects=[
        'customers/'
        '{{ ti.xcom_pull(task_ids="get_ds_day_from_xcom") }}/'
        '{{ ti.xcom_pull(task_ids="get_ds_day_from_xcom") }}'
        '_part1__customers.csv'
    ],
    destination_project_dataset_table='de2023-vlad-nebesniuk.bronze.customers',
    write_disposition='WRITE_TRUNCATE',
    schema_fields=[
        {'name': 'Id', 'type': 'STRING', 'mode': 'NULLABLE'},
        {'name': 'FirstName', 'type': 'STRING', 'mode': 'NULLABLE'},
        {'name': 'LastName', 'type': 'STRING', 'mode': 'NULLABLE'},
        {'name': 'Email', 'type': 'STRING', 'mode': 'NULLABLE'},
        {'name': 'RegistrationDate', 'type': 'STRING', 'mode': 'NULLABLE'},
        {'name': 'State', 'type': 'STRING', 'mode': 'NULLABLE'}
    ],
    dag=dag
)

# -----------------------------------------------------------------------------
# --- Modify data to silver table ---
# -----------------------------------------------------------------------------
sql_query = """
CREATE OR REPLACE TABLE `de2023-vlad-nebesniuk.silver.customers`
    AS
    SELECT
        Id as client_id,
        FirstName as first_name,
        LastName as last_name,
        Email as email,
        RegistrationDate as registration_date,
        State as state
    FROM
        `de2023-vlad-nebesniuk.bronze.customers`
"""

# Define a task to execute the SQL query
execute_sql_task = BigQueryOperator(
    task_id='execute_sql_task',
    sql=sql_query,
    use_legacy_sql=False,
    dag=dag
)

pass_ds_day_task >> get_ds_day_task >> copy_files_to_bronze >> execute_sql_task
