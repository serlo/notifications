#!/bin/sh
RETRIES=30

until psql --host $DATABASE_HOST --user $DATABASE_USER --database $DATABASE_NAME --command "select 1" > /dev/null 2>&1 || [ $RETRIES -eq 0 ]; do
  echo "Waiting for postgres server, $((RETRIES--)) remaining attempts…"
  sleep 1
done

python manage.py migrate
python manage.py runserver 0.0.0.0:8000
