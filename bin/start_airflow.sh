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
    --mount type=bind,source="${PROJECT_DIR}/workspace/airflow/dags",target=/home/airflow/dags \
    --mount type=bind,source="${PROJECT_DIR}/workspace/airflow/plugins",target=/home/airflow/plugins \
    --rm --detach \
    airflow

docker logs -f airflow
