FROM python:3

COPY ./database_schema.sh /database_schema.sh
RUN ["chmod", "+x", "/database_schema.sh"]

COPY ./external_rate_services/cryptowatch_rates.sh /cryptowatch_rates.sh
RUN ["chmod", "+x", "/cryptowatch_rates.sh"]

ENV PYTHONPATH="${PYTHONPATH}:/usr/src/"

WORKDIR /usr/src/dlc_oracle_bot

