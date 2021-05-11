FROM python:3

COPY ./oracle/announcer.sh /announcer.sh
RUN ["chmod", "+x", "/announcer.sh"]

ENV PYTHONPATH="${PYTHONPATH}:/usr/src/"

WORKDIR /usr/src/dlc_oracle_bot

