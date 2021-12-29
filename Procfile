release: python manage.py migrate
web: gunicorn trade_core.wsgi
worker: python manage.py qcluster