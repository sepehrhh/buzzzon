#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

cd avalon/
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --no-input --clear
gunicorn avalon.wsgi:application --bind 0.0.0.0:8000 --workers 3 --max-requests 10 --max-requests-jitter 20 --timeout 120

exec "$@"
