from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

from app.extractor_loader import upload_raw_data_to_bronze
from app.transformer import process_bronze_to_silver
from app.transformer import process_silver_to_gold

default_args = {
    'owner': 'dnc',
    'retries': 5,
    'retry_delay': timedelta(seconds=5)
}

with DAG(
    dag_id='clientes_dag',
    default_args=default_args,
    description='data pipeline dos clientes',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
    catchup=False
) as dag:
    task_1 = PythonOperator(
        task_id="extractor_loader",
        python_callable=upload_raw_data_to_bronze
    )
    
    task_2 = PythonOperator(
        task_id="Transformer_Bronze_to_Silver",
        python_callable=process_bronze_to_silver
    )
        
    task_3 = PythonOperator(
        task_id="Transformer_Silver_to_Gold",
        python_callable=process_silver_to_gold
    )
    
    task_1 >> task_2 >> task_3