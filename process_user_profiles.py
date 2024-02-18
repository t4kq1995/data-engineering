#!/usr/bin/env python
# coding: utf-8
from datetime import timedelta
from airflow import DAG
from airflow.contrib.operators.gcs_to_bq import GoogleCloudStorageToBigQueryOperator
from airflow.contrib.operators.bigquery_operator import BigQueryOperator

# -----------------------------------------------------------------------------
# --- Default DAG settings ---
# -----------------------------------------------------------------------------
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'catchup': True,
    'max_active_runs': 1
}


# -----------------------------------------------------------------------------
# --- Define the DAG ---
# -----------------------------------------------------------------------------
dag = DAG(
    'process_user_profiles',
    default_args=default_args,
    description='DAG to send data from bucket to Big Query',
)

# -----------------------------------------------------------------------------
# --- Copy data from GCP to BigQuery ---
# -----------------------------------------------------------------------------
copy_files_to_bronze = GoogleCloudStorageToBigQueryOperator(
    task_id='copy_files_to_bronze_bigquery',
    bucket='raw-data-de',
    source_objects=['user_profiles/user_profiles.json'],
    source_format='NEWLINE_DELIMITED_JSON',
    destination_project_dataset_table='de2023-vlad-nebesniuk.bronze.user_profiles',
    write_disposition='WRITE_TRUNCATE',
    schema_fields=[
        {'name': 'email', 'type': 'STRING', 'mode': 'NULLABLE'},
        {'name': 'full_name', 'type': 'STRING', 'mode': 'NULLABLE'},
        {'name': 'state', 'type': 'STRING', 'mode': 'NULLABLE'},
        {'name': 'birth_date', 'type': 'STRING', 'mode': 'NULLABLE'},
        {'name': 'phone_number', 'type': 'STRING', 'mode': 'NULLABLE'}
    ],
    dag=dag
)

# -----------------------------------------------------------------------------
# --- Modify data to silver table ---
# -----------------------------------------------------------------------------
sql_query = """
CREATE OR REPLACE TABLE `de2023-vlad-nebesniuk.silver.user_profiles`
    AS
    WITH normalized_phone_numbers AS (
        SELECT
            email, REGEXP_REPLACE(phone_number, r'\D', '') AS phone_number
        FROM
            `de2023-vlad-nebesniuk.bronze.user_profiles`
    ),
    formatted_phone_number AS (
        SELECT
            email,
            CONCAT('+', SUBSTR(npn.phone_number, 1, 1), '-', SUBSTR(npn.phone_number, 2, 3), '-', SUBSTR(npn.phone_number, 5, 3), '-', SUBSTR(npn.phone_number, 8, 4)) AS phone_number
        FROM
            normalized_phone_numbers as npn
    )
    SELECT `de2023-vlad-nebesniuk.bronze.user_profiles`.email, 
      SPLIT(full_name, " ")[safe_ordinal(1)] AS first_name, 
      SPLIT(full_name, " ")[safe_ordinal(2)] AS last_name, 
      state,
      birth_date, 
      fpn.phone_number AS phone_number 
    FROM `de2023-vlad-nebesniuk.bronze.user_profiles`
    LEFT JOIN formatted_phone_number AS fpn ON fpn.email = `de2023-vlad-nebesniuk.bronze.user_profiles`.email;
"""

# Define a task to execute the SQL query
execute_sql_task = BigQueryOperator(
    task_id='execute_sql_task',
    sql=sql_query,
    use_legacy_sql=False,
    dag=dag
)

copy_files_to_bronze
