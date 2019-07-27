#!/usr/bin/env bash
set -e

SCRIPT_DIR=$(dirname "$0")
PROJECT_DIR=$(cd ${SCRIPT_DIR}/../; pwd)

PG_USER=$(cat ${PROJECT_DIR}/run/secrets/postgres-user)
PG_PASSWORD=$(cat ${PROJECT_DIR}/run/secrets/postgres-pass)

VOLUMES_DIR="${PROJECT_DIR}/run/volumes/postgres"

if [ -d ${VOLUMES_DIR} ]; then
    rm -rf ${VOLUMES_DIR}
fi
mkdir -p ${VOLUMES_DIR}
# turn into an absolute path for docker run
VOLUMES_DIR=$(cd ${VOLUMES_DIR}; pwd)
# echo "VOLUMES_DIR=${VOLUMES_DIR}"

NETWORK_EXISTS=$(docker network ls | grep airflow-network | wc -l | tr -d " ")

if [ "$NETWORK_EXISTS" -eq "0" ]; then
   docker network create -d bridge --subnet 192.168.42.0/24 --gateway 192.168.42.1 airflow-network
fi

CONTAINER_EXISTS=$(docker ps | grep "airflow-db$" | wc -l | tr -d " ")

if [ "$CONTAINER_EXISTS" -eq "1" ]; then
   docker kill airflow-db
   sleep 5
fi

docker run \
    --name airflow-db \
    --network airflow-network \
    --publish 5432:5432 \
    --mount type=bind,source="${VOLUMES_DIR}",target=/var/lib/postgresql/data \
    --env POSTGRES_USER=$PG_USER \
    --env POSTGRES_PASSWORD=$PG_PASSWORD \
    --rm --detach \
    postgres-11.3


docker logs -f airflow-db
