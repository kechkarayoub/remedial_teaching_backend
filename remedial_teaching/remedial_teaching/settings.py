"""
Django's settings for remedial_teaching project.

Contains settings for production environment
"""

# Import common settings from .common.py
from .common import *  # pylint: disable=import-error,wildcard-import

# allowed hosts
ALLOWED_HOSTS = []

# Email configuration
CONTACT_EMAIL = "contact@example.com"

# CORS origin
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = []

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

# Development mode
DEVELOPMENT_MODE = "prod"

# Email configuration
EMAIL_CONFIRMATION_KEY_EXPIRATION_MINUTES = 60
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_SMTP_PROVIDER = "sendgrid"
EMAIL_USE_TLS = True


# google storage config
GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE = '/etc/...'  # path to private json key file obtained by Google.
GOOGLE_DRIVE_STORAGE_SERVICE_EMAIL = "'googleaccount'@gmail.com"

# Test settings
TEST_SETTINGS = False

