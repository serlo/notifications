FROM python:3.8-alpine
WORKDIR /usr/src/app

# Install Alpine packages
RUN apk update && apk add gcc musl-dev postgresql-dev

# Install Python packages
COPY docker/server/requirements.lock .
RUN pip install --upgrade pip
RUN pip install --requirement requirements.lock

# Add application code
COPY app app
RUN rm app/settings.py
COPY notifications notifications
COPY manage.py .

# Add entrypoint script
COPY docker/server/docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh
ENTRYPOINT ["docker-entrypoint.sh"]

EXPOSE 8000
CMD []
