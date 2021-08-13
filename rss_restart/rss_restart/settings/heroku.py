## Heroku production settings

import environ
from rss_restart.settings1.base import *

env = environ.Env(
    DEBUG=(bool, False)
)

DEBUG = env('DEBUG')

SECRET_KEY = env('SECRET_KEY')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

DATABASES = {
    'default': env.db(),
}
