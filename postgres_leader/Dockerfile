FROM postgres:12-alpine

COPY ./setup-leader.sh /docker-entrypoint-initdb.d/setup-leader.sh

RUN chmod 0666 /docker-entrypoint-initdb.d/setup-leader.sh
