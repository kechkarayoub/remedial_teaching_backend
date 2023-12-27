"""
Django common settings for remedial_teaching project.

Contains common settings between prod, dev and test environments.
"""
from django.utils.translation import gettext_lazy as _
from pathlib import Path
import os

from os.path import abspath, dirname, join
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# allowed hosts
ALLOWED_HOSTS = []

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Auth user model
AUTH_USER_MODEL = "user.User"

# CORS origin
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = []


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Fixture directories
FIXTURE_DIRS = [
    os.path.join(BASE_DIR, 'user/fixtures'),
]

# Installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'establishment',
    'user',
    'i18n_switcher',
    'home',
    'utils',
    'after_response',
    'colorfield',
    'gdstorage',
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/
LANGUAGES = [
    ('ar', _('Arabic')),
    ('en', _('English')),
    ('fr', _('French'))
]
LANGUAGE_CODE = 'fr'
LANGUAGES_DICT = {
    "ar": _("Arabic"),
    "en": _("English"),
    "fr": _("French")
}

# LOGGING_CONFIG = None
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'main_formatter': {
            'format': '[{asctime} - {levelname} - {module} - {filename} - {lineno}]: {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/main_log.log',
            'formatter': 'main_formatter',
            'level': 'WARNING',
            'backupCount': 10,  # keep at most 10 log files
            'maxBytes': 5242880,  # 5*1024*1024 bytes (5MB)
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'main_formatter',
            'level': 'WARNING',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}

# Middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Rest framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    # 'DEFAULT_PERMISSION_CLASSES': (
    #     'rest_framework.permissions.IsAuthenticated',
    # )
}

# Urls
ROOT_URLCONF = 'remedial_teaching.urls'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-^r4$od(nr7ihnl9e%0rw*2fxei2@_f*e+l33c#m^1k=%%mt63d'

# Site nane
SITE_NAME = "Remedial teaching"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'user/templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/
TIME_ZONE = 'Africa/Casablanca'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# WSGI application
WSGI_APPLICATION = 'remedial_teaching.wsgi.application'
