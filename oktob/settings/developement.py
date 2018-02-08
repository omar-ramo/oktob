from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'rx1c8zbn#d=y@4z)&_@&8wi%3tv@p!(@p=ckhq7p#n+-9nh=(q'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['testserver', 'localhost']


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}