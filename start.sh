#!/bin/bash
python manage.py migrate api --noinput
python manage.py migrate --noinput
python manage.py seeddata
exec gunicorn academia.wsgi --bind 0.0.0.0:$PORT
