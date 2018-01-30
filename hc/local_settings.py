import os
import dj_database_url

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME':   './hc.sqlite',
    }
}

if os.getenv('DATABASE_URL'):
    db_from_env = dj_database_url.config()
    STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
    DATABASES['default'].update(db_from_env)


SLACK_CLIENT_ID = os.getenv('SLACK_CLIENT_ID')
SLACK_CLIENT_SECRET = os.getenv('SLACK_CLIENT_SECRET')
