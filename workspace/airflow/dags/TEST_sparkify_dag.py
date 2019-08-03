import os
from datetime import datetime, timedelta
from pprint import pprint

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

from helpers import SqlCreates
from helpers import SqlQueries
from airflow.operators import PrepareRedshiftOperator
from airflow.operators import StageToRedshiftOperator
from airflow.operators import (LoadFactOperator, LoadDimensionOperator)
from airflow.operators import DataQualityOperator


def done_operator(**kwargs):
    print('done!')
    return True


args = {
    'owner': 'jlauman',
    'start_date': datetime(2019, 8, 3)
}

dag = DAG(
    dag_id='TEST_sparkify_dag',
    default_args=args,
    schedule_interval='@once',
    dagrun_timeout=timedelta(minutes=60),
)

start_task = DummyOperator(
    task_id='start',
    dag=dag
)

done_task = PythonOperator(
    task_id='done',
    python_callable=done_operator,
    dag=dag
)

prepare_redshift_task = PrepareRedshiftOperator(
    task_id='prepare_redshift',
    params={
        'redshift_connection_id': 'REDSHIFT_SPARKIFY',
        'sql_helper': SqlCreates,
    },
    dag=dag
)

stage_events_to_redshift_task = StageToRedshiftOperator(
    task_id='stage_events_to_redshift',
    params={
        'bucket': 'udacity-dend',
        'prefix': 'log_data',
        'redshift_connection_id': 'REDSHIFT_SPARKIFY',
    },
    dag=dag
)

stage_songs_to_redshift_task = StageToRedshiftOperator(
    task_id='stage_songs_to_redshift',
    params={
        'bucket': 'udacity-dend',
        'prefix': 'song_data',
        'redshift_connection_id': 'REDSHIFT_SPARKIFY',
    },
    dag=dag
)

# dependencies
start_task >> prepare_redshift_task >> [stage_events_to_redshift_task, stage_songs_to_redshift_task] >> done_task


if __name__ == "__main__":
    dag.cli()