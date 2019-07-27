#!/usr/bin/env bash
set -e

SCRIPT_DIR=$(dirname "$0")
PROJECT_DIR=$(cd ${SCRIPT_DIR}/../; pwd)

docker build --tag postgres-11.3 --file "${PROJECT_DIR}/src/postgres/Dockerfile" "${PROJECT_DIR}/src/postgres"
