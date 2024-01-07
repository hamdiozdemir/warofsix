#!/bin/sh

python manage.py wait_for_db
python manage.py makemigrations
python manage.py migrate

gunicorn warofsix.wsgi:application --bind 0.0.0.0:8000

