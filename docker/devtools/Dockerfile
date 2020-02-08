FROM python:3.8-alpine

WORKDIR /usr/src/app
RUN apk update && apk add gcc musl-dev postgresql-dev
COPY docker/devtools/requirements.lock .
RUN pip install --upgrade pip
RUN pip install --requirement requirements.lock
