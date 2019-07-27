#!/usr/bin/env bash
set -e

# docker pull apache/airflow:v1-10-test-python3.6-ci-slim

SCRIPT_DIR=$(dirname "$0")
PROJECT_DIR=$(cd ${SCRIPT_DIR}/../; pwd)

docker build --tag airflow --file "${PROJECT_DIR}/src/airflow/Dockerfile" "${PROJECT_DIR}/src/airflow"
