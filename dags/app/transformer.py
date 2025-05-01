import boto3
import pandas as pd
import pyarrow.parquet as pq
import s3fs
import pyarrow
import os
import re
from io import BytesIO
from datetime import datetime

AWS_ACCESS_KEY_ID=os.environ.get('aws_access_key_id')
AWS_SECRET_ACCESS_KEY=os.environ.get('aws_secret_access_key')
AWS_REGION=os.environ.get('aws_region')


def process_bronze_to_silver():
    print("Initializing data transformation from Bronze to Silver")
    
    s3_client = boto3.client(
       's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION
    )
    BUCKET_NAME = 'dnc-desafio8'
    directory_path = 'clientes/bronze/'
    
    response = s3_client.list_objects_v2(
        Bucket=BUCKET_NAME,
        Prefix=directory_path
    )
    
    dfs = []
    
    for obj in response.get('Contents', []):
        file_key = obj["Key"]
        
        if ".parquet" in file_key:
            response = s3_client.get_object(Bucket=BUCKET_NAME, Key=file_key)
            parquet_file = BytesIO(response["Body"].read())
            
            df = pq.read_table(parquet_file).to_pandas()
            
            dfs.append(df)
            
            
    combined_df = pd.concat(dfs, ignore_index=True)
    
    print("combined_df", combined_df.info())
    
    print("Removing Null Values")
    df_droped = combined_df.dropna(axis=0)
    
    ## corrigir formato do e-mail
    print("Correcting Email Format")
    def corrigir_email(email):
    # Regex para validar e-mails
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(regex, email):
            return email
        else:
            # Corrigir e-mail (exemplo simples: adicionar '.com' se faltar)
            if '@' in email and '.' not in email.split('@')[1]:
                return email + '.com'
            else:
                return 'email_invalido'

    # Aplicar a função ao DataFrame
    df_droped['emails_corrigidos'] = df_droped['email'].apply(corrigir_email)

    ## calcular idade dos usuários
    print("Calculating the age of users")
    # Converter a coluna de data de nascimento para datetime
    df_droped['date_of_birth'] = pd.to_datetime(df_droped['date_of_birth'])

    # Calcular a idade
    hoje = pd.Timestamp(datetime.now())
    df_droped['idade'] = (hoje - df['date_of_birth']).astype('<m8[Y]')

    print("Saving Data Into Silver Layer")
    pq.write_to_dataset(
        pyarrow.Table.from_pandas(df_droped),
        "dnc-desafio8/clientes/silver/fact_table",
        filesystem=s3fs.S3FileSystem()
    )

def process_silver_to_gold():
    print("Initializing data transformation from Silver to Gold")
    
    s3_client = boto3.client(
       's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION
    )
    BUCKET_NAME = 'dnc-desafio8'
    directory_path = 'clientes/silver/'
    
    response = s3_client.list_objects_v2(
        Bucket=BUCKET_NAME,
        Prefix=directory_path
    )
    
    dfs = []
    
    for obj in response.get('Contents', []):
        file_key = obj["Key"]
        
        if ".parquet" in file_key:
            response = s3_client.get_object(Bucket=BUCKET_NAME, Key=file_key)
            parquet_file = BytesIO(response["Body"].read())
            
            df = pq.read_table(parquet_file).to_pandas()
            
            dfs.append(df)
            
            
    combined_df = pd.concat(dfs, ignore_index=True)
    
    print("combined_df", combined_df.info())

    print("Aggregating data by age group and status")
    # Definir faixas etárias
    bins = [0, 10, 11, 20, 21, 30]
    labels = ['0-10', '11-20', '21-30']
    combined_df = ['faixa_etaria'] = pd.cut(df['idade'], bins=bins, labels=labels, right=False)

    # Agregar dados por faixa etária e status
    combined_df = df.groupby(['faixa_etaria', 'status']).size().reset_index(name='contagem')

    print("Users by age group and status")

    # Criar DataFrame
    df = pd.DataFrame(combined_df)

    # Definir faixas etárias
    bins = [0, 18, 30, 40, 50, 60, 100]
    labels = ['0-18', '19-30', '31-40', '41-50', '51-60', '61+']
    df['faixa_etaria'] = pd.cut(df['idade'], bins=bins, labels=labels, right=False)

    # Contar número de usuários por faixa etária e status
    df = df.groupby(['faixa_etaria', 'status']).size().unstack(fill_value=0)

  




 






