# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'rx1c8zbn#d=y@4z)&_@&8wi%3tv@p!(@p=ckhq7p#n+-9nh=(q' #Get it from somewhere

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['localhost']


# Database
# Use postgresql or don't -_-

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}