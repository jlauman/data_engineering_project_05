
# these come from container environment
export PGUSER=$POSTGRES_USER
export PGPASSWORD=$POSTGRES_PASSWORD

psql --dbname=template1 --command="create extension if not exists \"pgcrypto\";"

psql --dbname=postgres --command "create role airflow login encrypted password 'airflow43914'";

psql --dbname=postgres --command "create database \"airflow\" with owner airflow";
