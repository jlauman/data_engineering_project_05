import os, time
from pprint import pprint

from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

import boto3
from botocore import UNSIGNED
from botocore.config import Config


class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'

    @apply_defaults
    def __init__(self, *args, **kwargs):
        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        params = kwargs['params']
        self.log.info('StageToRedshiftOperator.__init__: params={}'.format(params))
        self.s3_bucket = params['bucket']
        self.s3_prefix = params['prefix']

    def execute(self, context):
        object_paths = self.read_s3_bucket_paths(self.s3_bucket, self.s3_prefix)
        self.log.info('StageToRedshiftOperator.execute: object_paths...')
        self.log.info(object_paths)
        self.log.info('StageToRedshiftOperator.execute: done')

    def read_s3_bucket_paths(self, bucket, prefix):
        s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))
        object_paths = self.get_object_paths(s3, bucket, prefix)
        return object_paths

    def get_object_paths(self, s3, bucket, prefix):
        """List objects in S3 bucket with given prefix.
        Uses paginator to ensure a complete list of object paths is returned.
        """
        object_paths = []
        paginator = s3.get_paginator('list_objects')
        pages = paginator.paginate(Bucket=bucket, Prefix=prefix)
        for page in pages:
            # print("len(page['Contents'])=" + str(len(page['Contents'])))
            r1 = list(map(lambda obj: obj['Key'], page['Contents']))
            r2 = list(filter(lambda str: str.endswith('.json'), r1))
            object_paths.extend(r2)
        self.log.info('StageToRedshiftOperator.get_object_paths: %s/%s total object paths = %d' % (bucket, prefix, len(object_paths)))
        time.sleep(2)
        return object_paths
