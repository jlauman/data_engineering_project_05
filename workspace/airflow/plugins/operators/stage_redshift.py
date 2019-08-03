import hashlib, json, os, time
from pprint import pprint

import pandas as pd

from airflow import AirflowException
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
        self.redshift_connection_id = params['redshift_connection_id']

    def execute(self, context):
        self.log.info('StageToRedshiftOperator.execute: s3_bucket={}, s3_prefix={}'.format(self.s3_bucket, self.s3_prefix))
        # object_paths = self.read_s3_bucket_paths(self.s3_bucket, self.s3_prefix)
        # self.log.info(object_paths)
        if self.s3_prefix == 'log_data':
            self.load_staging_events_data(self.s3_bucket, self.s3_prefix, self.redshift_connection_id)
        elif self.s3_prefix == 'song_data':
            self.load_staging_song_data(self.s3_bucket, self.s3_prefix, self.redshift_connection_id)
        else:
            # self.log.error('invalid s3_prefix={}'.format(self.s3_prefix))
            raise AirflowException('invalid s3_prefix={}'.format(self.s3_prefix))
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

    def load_staging_events_data(self, bucket, prefix, redshift_connection_id):
        """Load song-play event records into s_songplay_event table.
        """
        # import pdb; pdb.set_trace()
        # load log_data (events) into s_event table
        staging_events_insert = ("""
            insert into staging_events (
                artist,
                auth,
                firstname,
                gender,
                iteminsession,
                lastname,
                length,
                level,
                location,
                method,
                page,
                registration,
                sessionid,
                song,
                status,
                ts,
                useragent,
                userid
                ) values
        """)
        pg_hook = PostgresHook(redshift_connection_id)
        s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))
        file_paths = self.get_object_paths(s3, bucket, prefix)
        # self.log.info(file_paths)
        for file_path in file_paths:
            sql = str(staging_events_insert)
            self.log.info('log_data: %s' % file_path)
            obj1 = s3.get_object(Bucket=bucket, Key=file_path)
            str1 = obj1['Body'].read().decode('utf-8').strip()
            df = pd.read_json(str1, lines=True)
            df = df[df.page == 'NextSong']
            # pprint(df)
            for index, row in df.iterrows():
                # pprint(row)
                str1 = ("(" +
                    "'" + row.artist.replace("'", "''") + "', " +
                    "'" + row.auth + "', " +
                    "'" + row.firstName.replace("'", "''") + "', " +
                    "'" + 'unknown' + "', " +
                    "" + str(row.itemInSession) + ", " +
                    "'" + row.lastName.replace("'", "''") + "', " +
                    "" + str(row.length) + ", " +
                    "'" + row.level + "', " +
                    "'" + row.location.replace("'", "''") + "', " +
                    "'" + row.method + "', " +
                    "'" + row.page + "', " +
                    "" + str(row.registration) + ", " +
                    "" + str(row.sessionId) + ", " +
                    "'" + row.song.replace("'", "''") + "', " +
                    "" + str(row.status) + ", " +
                    "" + str(row.ts) + ", " +
                    "'" + row.userAgent.replace("'", "''") + "', " +
                    "" + str(row.userId) + "" +
                    "),\n")
                sql += str1
            sql = ''.join(sql).strip()[:-1] + ';'
            # print(sql)
            pg_hook.run(sql, autocommit=True)

    def load_staging_song_data(self, bucket, prefix, redshift_connection_id):
        """Load song records into s_song staging table.
        """
        staging_songs_insert = ("""
            insert into staging_songs (
                num_songs,
                artist_id,
                artist_name,
                artist_latitude,
                artist_longitude,
                artist_location,
                song_id,
                title,
                duration,
                year
                ) values
        """)
        pg_hook = PostgresHook(redshift_connection_id)
        s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))
        file_paths = self.get_object_paths(s3, bucket, prefix)
        # pprint(file_paths)
        sql = str(staging_songs_insert)
        for file_path in file_paths:
            self.log.info('song_data: %s' % file_path)
            obj1 = s3.get_object(Bucket=bucket, Key=file_path)
            str1 = obj1['Body'].read().decode('utf-8').strip()
            data = json.loads(str1)
            if data['year'] == 0: data['year'] = None
            # fix link string...
            if str(data['artist_location']).startswith('<a'): data['artist_location'] = None
            # pprint(data)
            str2 = ("(" +
                "" + str(data['num_songs']) + ", " +
                "'" + data['artist_id'] + "', " +
                "'" + str(data['artist_name']).replace("'", "''") + "', " +
                "" + (str(data['artist_latitude']) if not data['artist_latitude'] == None else 'null') + ", " +
                "" + (str(data['artist_longitude']) if not data['artist_longitude'] == None else 'null') + ", " +
                "'" + str(data['artist_location']).replace("'", "''") + "', " +
                "'" + data['song_id'] + "', " +
                "'" + str(data['title']).replace("'", "''") + "', " +
                "" + str(data['duration']) + ", " +
                "" + (str(data['year']) if not data['year'] == None else 'null') + "" +
                "),\n")
            sql += str2
            # print(str2)
            # batch inserts at 8k character threshold
            if len(sql) > 8192:
                self.log.info('  8k insert...')
                sql = ''.join(sql).strip()[:-1] + ';'
                pg_hook.run(sql, autocommit=True)
                sql = str(staging_songs_insert)
        self.log.info('last insert...')
        sql = ''.join(sql).strip()[:-1] + ';'
        pg_hook.run(sql, autocommit=True)
