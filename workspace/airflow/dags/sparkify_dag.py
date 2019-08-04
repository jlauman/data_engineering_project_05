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


def done_function():
    print('done!')
    return True

default_args = {
    'owner': 'jlauman',
    'description': 'Load fact and dimension tables from S3 bucket with log_data and song_data.',
    'start_date': datetime(2010, 1, 1),
    'catchup': True,
    'schedule_interval': '@hourly',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    dag_id='sparkify_dag',
    default_args=default_args,
    dagrun_timeout=timedelta(minutes=60),
)

start_task = DummyOperator(
    task_id='start',
    dag=dag
)

done_task = PythonOperator(
    task_id='done',
    python_callable=done_function,
    dag=dag
)

prepare_redshift_task = PrepareRedshiftOperator(
    task_id='prepare_redshift',
    params={
        'redshift_connection_id': 'REDSHIFT_SPARKIFY',
        'sql_class': SqlCreates,
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

load_songplays_fact_table_task = LoadFactOperator(
    task_id='load_songplays_fact_table',
    params={
        'redshift_connection_id': 'REDSHIFT_SPARKIFY',
        'sql': SqlQueries.songplay_table_insert
    },
    dag=dag
)

load_user_dimension_table_task = LoadDimensionOperator(
    task_id='load_user_dimension_table',
    params={
        'redshift_connection_id': 'REDSHIFT_SPARKIFY',
        'sql': SqlQueries.user_table_insert
    },
    dag=dag
)

load_song_dimension_table_task = LoadDimensionOperator(
    task_id='load_song_dimension_table',
    params={
        'redshift_connection_id': 'REDSHIFT_SPARKIFY',
        'sql': SqlQueries.song_table_insert
    },
    dag=dag
)

load_artist_dimension_table_task = LoadDimensionOperator(
    task_id='load_artist_dimension_table',
    params={
        'redshift_connection_id': 'REDSHIFT_SPARKIFY',
        'sql': SqlQueries.artist_table_insert
    },
    dag=dag
)

load_time_dimension_table_task = LoadDimensionOperator(
    task_id='load_time_dimension_table',
    params={
        'redshift_connection_id': 'REDSHIFT_SPARKIFY',
        'sql': SqlQueries.time_table_insert
    },
    dag=dag
)

data_quality_checks_task = DataQualityOperator(
    task_id='data_quality_checks',
    params={
        'redshift_connection_id': 'REDSHIFT_SPARKIFY',
        'sql': SqlQueries.data_quality_check
    },
    dag=dag
)

# dependencies
start_task >> prepare_redshift_task >> \
    [stage_events_to_redshift_task, stage_songs_to_redshift_task] >> \
    load_songplays_fact_table_task >> \
    [load_user_dimension_table_task, load_song_dimension_table_task, load_artist_dimension_table_task, load_time_dimension_table_task] >> \
    data_quality_checks_task >> \
    done_task


if __name__ == "__main__":
    dag.cli()