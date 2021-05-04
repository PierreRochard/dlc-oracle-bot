FROM python:3

COPY ./database_schema.sh /database_schema.sh
RUN ["chmod", "+x", "/database_schema.sh"]

ENV PYTHONPATH="${PYTHONPATH}:/usr/src/"

WORKDIR /usr/src/dlc_oracle_bot

