release: python manage.py migrate
release: python manage.py ensuretriggers & python manage.py sendalerts
web: gunicorn hc.wsgi --log-file -