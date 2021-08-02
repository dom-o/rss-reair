release: python3 rss_restart/manage.py migrate
web: gunicorn rss_restart.wsgi --preload --log-file -
