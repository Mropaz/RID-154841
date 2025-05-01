import boto3
import pandas as pd
import pyarrow.parquet as pq
import s3fs
import pyarrow
import os
from functools import partial
from airflow import DAG

AWS_ACCESS_KEY_ID=os.environ.get('aws_access_key_id')
AWS_SECRET_ACCESS_KEY=os.environ.get('aws_secret_access_key')
AWS_REGION=os.environ.get('aws_region')

def upload_raw_data_to_bronze():
    print("Initializing data upload from Raw Folder")
    
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION
    )
    
    BUCKET_NAME = 'dnc-desafio8'
    FILE_KEY = 'clientes/raw/cadastro.csv'
    
    response = s3_client.get_object(Bucket=BUCKET_NAME, Key=FILE_KEY)
    
    df = pd.read_csv(response["Body"])
    
    print("Dataframe Clientes", df.info())
    
    print("Saving Data into Bronze Layer")
    
    pq.write_to_dataset(
        pyarrow.Table.from_pandas(df),
        'dnc-desafio8/clientes/bronze',
        filesystem=s3fs.S3FileSystem()
    )

 