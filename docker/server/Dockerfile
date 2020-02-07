FROM python:3.8-alpine

WORKDIR /usr/src/app
RUN apk update && apk add librdkafka-dev postgresql-libs gcc musl-dev postgresql-dev
COPY requirements.txt .
RUN pip install --requirement requirements.txt
COPY docker/server/run.sh /tmp/run.sh

EXPOSE 8000
CMD ["sh", "/tmp/run.sh"]
