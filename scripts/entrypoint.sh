#!/bin/sh

set -e

python manage.py collectstatic --noinput
./manage.py makemigrations
./manage.py migrate

uwsgi --socket :8000 --master --enable-threads --module app.wsgi