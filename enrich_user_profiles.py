#!/usr/bin/env python
# coding: utf-8
from datetime import timedelta
from airflow import DAG
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
    'enrich_user_profiles',
    default_args=default_args,
    description='DAG to create final gold state with data',
)

# -----------------------------------------------------------------------------
# --- Insert final data in gold table ---
# -----------------------------------------------------------------------------
sql_query = """
CREATE OR REPLACE TABLE `de2023-vlad-nebesniuk.gold.user_profiles_enriched`
    AS
    SELECT CAST(c.client_id AS INTEGER) AS client_id, 
      up.first_name, up.last_name, c.email, 
      CAST(c.registration_date AS DATE) AS registration_date, 
      up.state, 
      CAST(up.birth_date AS DATE) AS birth_date, 
      up.phone_number
    FROM `de2023-vlad-nebesniuk.silver.customers` AS c
    LEFT JOIN `de2023-vlad-nebesniuk.silver.user_profiles` AS up ON up.email = c.email;
"""

# Define a task to execute the SQL query
execute_sql_task = BigQueryOperator(
    task_id='execute_sql_task',
    sql=sql_query,
    use_legacy_sql=False,
    dag=dag
)

execute_sql_task
