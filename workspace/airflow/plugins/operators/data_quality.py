from airflow.hooks.base_hook import BaseHook
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):
    """Use SQL query to return fact and dimension table counts.

    Parameter keys are: redshift_connection_id, sql

    data_quality_checks_task = DataQualityOperator(
        task_id='data_quality_checks',
        params={
            'redshift_connection_id': 'REDSHIFT_SPARKIFY',
            'sql': SqlQueries.data_quality_check
        },
        dag=dag
    )
    """
    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self, *args, **kwargs):
        super(DataQualityOperator, self).__init__(*args, **kwargs)
        params = kwargs['params']
        self.log.info('LoadDimensionOperator.__init__: params={}'.format(params))
        self.redshift_connection_id = params['redshift_connection_id']
        self.sql = params['sql']

    def execute(self, context):
        connection_info = BaseHook.get_connection(self.redshift_connection_id)
        self.log.info('LoadDimensionOperator.execute: redshift_connection_id={}'.format(connection_info))
        pg_hook = PostgresHook(self.redshift_connection_id)
        df = pg_hook.get_pandas_df(self.sql)
        print(df)
        return df
