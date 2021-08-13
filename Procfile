release: python3 manage.py migrate
web: gunicorn rss_restart.wsgi --preload --log-file -
