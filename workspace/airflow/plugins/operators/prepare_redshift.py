import os, time
from pprint import pprint

from airflow.hooks.base_hook import BaseHook
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

import boto3
from botocore import UNSIGNED
from botocore.config import Config


class PrepareRedshiftOperator(BaseOperator):
    """Create and truncate fact and dimension tables.

    Parameter keys are: redshift_connection_id, sql_class

    The sql_class parameter is a python class used as a dict
    to store SQL statements.

    prepare_redshift_task = PrepareRedshiftOperator(
        task_id='prepare_redshift',
        params={
            'redshift_connection_id': 'REDSHIFT_SPARKIFY',
            'sql_class': SqlCreates,
        },
        dag=dag
    )
    """
    ui_color = '#358140'

    @apply_defaults
    def __init__(self, *args, **kwargs):
        super(PrepareRedshiftOperator, self).__init__(*args, **kwargs)
        params = kwargs['params']
        self.log.info('PrepareRedshiftOperator.__init__: params={}'.format(params))
        self.redshift_connection_id = params['redshift_connection_id']
        self.sql_class = params['sql_class']

    def execute(self, context):
        connection_info = BaseHook.get_connection(self.redshift_connection_id)
        self.log.info('PrepareRedshiftOperator.execute: redshift_connection_id={}'.format(connection_info))
        pg_hook = PostgresHook(self.redshift_connection_id)
        keys = [k for k in self.sql_class.__dict__.keys() if not k.startswith('__')]
        keys.sort()
        for key in keys:
            print('query={}'.format(key))
            sql = self.sql_class.__dict__[key]
            pg_hook.run(sql, autocommit=True)
        self.log.info('PrepareRedshiftOperator.execute: done')
