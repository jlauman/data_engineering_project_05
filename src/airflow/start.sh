#!/usr/bin/env bash

PGPASSWORD=airflow43914 psql --host=airflow-db --dbname=airflow --username=airflow --command='select count(*) from connection;'
AIRFLOW_INITDB=$?
echo "AIRFLOW_INITDB=$AIRFLOW_INITDB"

if [ $AIRFLOW_INITDB -eq 1 ]; then
    airflow initdb
fi

mkdir -p /home/airflow/supervisord

supervisord --configuration /etc/supervisor/conf.d/supervisord.conf
