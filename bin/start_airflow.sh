#!/usr/bin/env bash
set -e

SCRIPT_DIR=$(dirname "$0")
PROJECT_DIR=$(cd ${SCRIPT_DIR}/../; pwd)

NETWORK_EXISTS=$(docker network ls | grep airflow-network | wc -l | tr -d " ")

if [ "$NETWORK_EXISTS" -eq "0" ]; then
   docker network create -d bridge --subnet 192.168.42.0/24 --gateway 192.168.42.1 airflow-network
fi

CONTAINER_EXISTS=$(docker ps | grep "airflow$" | wc -l | tr -d " ")

if [ "$CONTAINER_EXISTS" -eq "1" ]; then
   docker kill airflow
fi

docker run \
    --name airflow \
    --network airflow-network \
    --publish 8080:8080 \
    --rm --detach \
    airflow

docker logs -f airflow


# docker run \
#     --name airflow \
#     --publish 8033:8033 \
#     --mount type=bind,source="${PROJECT_DIR}/src",target=/app \
#     --env DB_HOST=jms-db \
#     --env DB_PORT=5432 \
#     --env DB_DB=journal_message_store \
#     --env DB_USER=$DB_USER \
#     --env DB_PASS=$DB_PASS \
#     --env NPM_TOKEN=$NPM_TOKEN \
#     --rm --detach \
#     jms-api-node-11
