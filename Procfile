web: python manage.py migrate api --noinput && python manage.py migrate --noinput && python manage.py seeddata && gunicorn academia.wsgi --bind 0.0.0.0:$PORT
