from airflow.hooks.base_hook import BaseHook
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):
    """Load dimension table using SQL INSERT+SELECT query.

    Parameter keys are: redshift_connection_id, sql

    load_artist_dimension_table_task = LoadDimensionOperator(
        task_id='load_artist_dimension_table',
        params={
            'redshift_connection_id': 'REDSHIFT_SPARKIFY',
            'sql': SqlQueries.artist_table_insert
        },
        dag=dag
    )
    """
    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self, *args, **kwargs):
        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        params = kwargs['params']
        self.log.info('LoadDimensionOperator.__init__: params={}'.format(params))
        self.redshift_connection_id = params['redshift_connection_id']
        self.sql = params['sql']

    def execute(self, context):
        connection_info = BaseHook.get_connection(self.redshift_connection_id)
        self.log.info('LoadDimensionOperator.execute: redshift_connection_id={}'.format(connection_info))
        pg_hook = PostgresHook(self.redshift_connection_id)
        pg_hook.run(self.sql, autocommit=True)
