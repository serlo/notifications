FROM python:3.8-alpine

WORKDIR /usr/src/app
RUN apk update && apk add librdkafka-dev gcc musl-dev postgresql-dev
COPY docker/server/requirements.lock .
RUN pip install --upgrade pip
RUN pip install --requirement requirements.lock
COPY docker/worker/run.sh /tmp/run.sh

EXPOSE 8000
CMD ["sh", "/tmp/run.sh"]
