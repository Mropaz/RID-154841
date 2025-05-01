FROM apache/airflow:3.0.0
RUN pip install s3fs pyarrow
