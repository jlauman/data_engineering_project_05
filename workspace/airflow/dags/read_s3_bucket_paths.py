import configparser, os, glob, csv, json, hashlib, time
from datetime import datetime, timedelta
from pprint import pprint

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator



import boto3
from botocore import UNSIGNED
from botocore.config import Config


def get_object_paths(s3, bucket, prefix):
    """List objects in S3 bucket with given prefix.
    Uses paginator to ensure a complete list of object paths is returned.
    """
    # r1 = s3.list_objects(Bucket=DEND_BUCKET, Prefix=prefix)
    # r2 = list(map(lambda obj: obj['Key'], r1['Contents']))
    # r3 = list(filter(lambda str: str.endswith('.json'), r2))
    # s3 client does not need to be closed
    object_paths = []
    paginator = s3.get_paginator('list_objects')
    pages = paginator.paginate(Bucket=bucket, Prefix=prefix)
    for page in pages:
        # print("len(page['Contents'])=" + str(len(page['Contents'])))
        r1 = list(map(lambda obj: obj['Key'], page['Contents']))
        r2 = list(filter(lambda str: str.endswith('.json'), r1))
        object_paths.extend(r2)
    print('%s/%s total object paths = %d' % (bucket, prefix, len(object_paths)))
    time.sleep(2)
    return object_paths


def read_s3_bucket_paths(**context):
    s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))
    object_paths = get_object_paths(s3, 'udacity-dend', 'log_data')
    pprint(object_paths)
    task_instance = context['task_instance']
    task_instance.xcom_push(key='s3_object_paths', value=object_paths)
    return True

def do_xcom_pull(**context):
    task_instance = context['task_instance']
    object_paths = task_instance.xcom_pull(key='s3_object_paths')
    pprint(object_paths)


args = {
    'owner': 'jlauman',
    'start_date': datetime(2019, 7, 29)
}

dag = DAG(
    dag_id='read_s3_bucket_paths',
    default_args=args,
    schedule_interval='@once',
    dagrun_timeout=timedelta(minutes=60),
)

run_this_last_task = PythonOperator(
    task_id='run_this_last',
    python_callable=do_xcom_pull,
    provide_context=True,
    dag=dag,
)

start_task = DummyOperator(
    task_id='start',
    dag=dag
)

read_s3_bucket_path_task = PythonOperator(
    task_id='read_s3_bucket_path',
    python_callable=read_s3_bucket_paths,
    provide_context=True,
    dag=dag,
)

# dependencies
start_task >> read_s3_bucket_path_task >> run_this_last_task


if __name__ == "__main__":
    dag.cli()