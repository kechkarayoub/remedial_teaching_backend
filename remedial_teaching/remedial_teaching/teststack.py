"""
Django's settings for remedial_teaching project.

Contains settings for test environment
"""

# Import common settings from .common.py
# from .common import *  # pylint: disable=import-error,wildcard-import


# Import devstack settings from .common.py
from .devstack import *  # pylint: disable=import-error,wildcard-import


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'user/emails_test')
# Test settings
TEST_SETTINGS = True

# Remove console from  LOGGING loggers handlers
LOGGING['loggers']['django']['handlers'] = ['file']
LOGGING['handlers']['file']['filename'] = 'log/main_log_test.log'

try:
    url_file_to_remove = os.path.join(BASE_DIR, 'log/main_log_test.log')
    os.remove(url_file_to_remove)
except:
    pass

