## Production settings

import environ
from rss_restart.settings.base import *

env = environ.Env(
    DEBUG=(bool, False)
)

environ.Env.read_env()

DEBUG = env('DEBUG')

SECRET_KEY = env('SECRET_KEY')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
STATIC_URL = '/rss-restart/static/'

DATABASES = {
    'default': env.db(),
}
