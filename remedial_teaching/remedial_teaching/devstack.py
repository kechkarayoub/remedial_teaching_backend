"""
Django's settings for remedial_teaching project.

Contains settings for development environment
"""

from django.utils.translation import gettext_lazy as _
# Import common settings from .common.py
from .common import *  # pylint: disable=import-error,wildcard-import

# allowed hosts
ALLOWED_HOSTS = ["*"]

# Email configuration
CONTACT_EMAIL = "contact@example.com"

# CORS origin
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = ["http://localhost:3000"]

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': os.path.join(BASE_DIR, 'my.cnf'),
        },
    }
}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    },
}

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Development mode
DEVELOPMENT_MODE = "dev"

# Email configuration
EMAIL_CONFIRMATION_KEY_EXPIRATION_MINUTES = 60
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_SMTP_PROVIDER = "sendgrid"
EMAIL_USE_TLS = True

# Site urls
FRONTEND_URL = "http://localhost:3000"

# google storage config
GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE = join(dirname(abspath(__file__)), 'dev_mafatih/remedial_teachingdev_drive_storage.json')  # path to private json key file obtained by Google.
GOOGLE_DRIVE_STORAGE_SERVICE_EMAIL = "remedial_teachingdev@gmail.com"


# Test settings
TEST_SETTINGS = False


## This code must be in .private file for production:
# RSS api key
RSS2JSON_API_KEY = 'qk5dc4otajoyz1ljbpxhrbcm7gfzs0cuo9dxokcy'
# sendgrid django setting
SENDGRID_API_KEY = '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'
EMAIL_HOST_USER = 'apikey' # this is exactly the value 'apikey'
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
EMAIL_FROM_ADDRESS = 'edxkls2019@gmail.com'
# Site urls
BACKEND_URL = "http://localhost:8000"
FRONT_URL = "http://localhost:3000"
## End .private code
