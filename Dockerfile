FROM python:3.9-alpine

COPY ./compound /app/compound
COPY ./requirements.txt /app
WORKDIR /app
RUN pip install -r requirements.txt

ENTRYPOINT /bin/sh
