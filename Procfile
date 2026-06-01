web: gunicorn school.wsgi --log-file -
release: python manage.py migrate --noinput && python manage.py add_demo_data --noinput
