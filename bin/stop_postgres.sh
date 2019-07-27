#!/usr/bin/env bash
set -e

SCRIPT_DIR=$(dirname "$0")

PROJECT_DIR=$(cd ${SCRIPT_DIR}/../; pwd)

CONTAINER_EXISTS=$(docker ps | grep "airflow-db$" | wc -l | tr -d " ")

if [ "$CONTAINER_EXISTS" -eq "1" ]; then
   docker kill airflow-db
   sleep 5
fi
