FROM python:3.7-slim-stretch

# NOTE: psql client requies manual page directories
RUN apt-get update &&\
    apt-get install -y build-essential &&\
    pip install --upgrade pip

RUN mkdir -p /usr/share/man/man1 /usr/share/man/man7 &&\
    apt-get install -y postgresql-client

RUN apt-get install -y ack supervisor

RUN pip install apache-airflow[celery,postgres,s3] &&\
    pip uninstall --yes flask &&\
    pip install flask==1.0.4

ENV AIRFLOW_HOME=/home/airflow

RUN useradd -ms /bin/bash airflow
USER airflow
WORKDIR /home/airflow

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY airflow.cfg /home/airflow
COPY start.sh /home/airflow

CMD [ "/bin/bash", "start.sh" ]
