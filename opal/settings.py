"""
Django settings for opal project.

Generated by 'django-admin startproject' using Django 4.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import logging
import secrets
from pathlib import Path
import os
import environ
import subprocess

from django.urls import reverse

import opal
from logging.handlers import RotatingFileHandler

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
# Build paths inside the project like this: BASE_DIR / 'subdir'.


BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'vendor')]

env = environ.Env()
if str(BASE_DIR) + "/opal/.env":
    environ.Env.read_env()

# Load environment variables and set defaults
default_secret_key = secrets.token_urlsafe()

ENVIRONMENT = os.getenv("ENVIRONMENT", default="development")
ASYNC = os.getenv("ASYNC", default=False)
BROKER = os.getenv("BROKER", default='')
HOST_NAME = os.getenv("HOST_NAME", default="http://localhost:8000")
# set SSL active to True if you are using https
SSL_ACTIVE = os.getenv("SSL_ACTIVE", default=False)
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("OPAL_SECRET_KEY", default=default_secret_key)
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", default="False")
LOG_LEVEL = os.getenv("LOG_LEVEL", default="INFO")
LOG_FILE = os.getenv("LOG_FILE", default=os.path.join(BASE_DIR,"debug.log"))
# Set proxy servers if needed. This will be used when the app attempts to download catalog files from the internet
HTTP_PROXY = os.getenv("HTTP_PROXY", default=False)
HTTPS_PROXY = os.getenv("HTTPS_PROXY", default=False)
USE_X_FORWARDED_HOST = os.getenv("USE_X_FORWARDED_HOST", default=True)
# Database settings
DATABASE = os.getenv("DATABASE", default="sqlite")
DB_NAME = os.getenv("DB_NAME", default="db.sqlite3")
# These can be blank if using sqlite
DB_PASSWORD = os.getenv("DB_PASSWORD", default="")
DB_USER = os.getenv("DB_USER", default="opal")
DB_HOST = os.getenv("DB_HOST", default="localhost")
DB_PORT = os.getenv("DB_PORT", default="5432")
# The next 2 variables are used with the django-require-login module
LOGIN_URL = os.getenv("LOGIN_URL", default="common:auth_view")
LOGOUT_URL = os.getenv("LOGOUT_URL", default="common:auth_view")
LOGIN_REDIRECT_URL = os.getenv("LOGIN_REDIRECT_URL", default="/")
LOGOUT_REDIRECT_URL = os.getenv("LOGOUT_REDIRECT_URL", default="/")
ENABLE_DJANGO_AUTH = os.getenv("ENABLE_DJANGO_AUTH", default=True)
# SAML settings
ENABLE_SAML = os.getenv("ENABLE_SAML", default=True)
SAML_HTTPS = os.getenv("SAML_HTTPS", default=False)  # Acceptable values are "True" or "False"
SAML_HTTP_HOST = os.getenv("SAML_HTTP_HOST", default=False)
SAML_SCRIPT_NAME = os.getenv("SAML_SCRIPT_NAME", default=False)  # should be the path to the acs function
SAML_SERVER_PORT = os.getenv("SAML_SERVER_PORT", default=False)
# SAML_PROVIDERS must be a comma seperated list of idp stubs that will be used in the application
SAML_PROVIDERS = os.getenv("SAML_PROVIDERS", default="stub")
SP_PREPARE_REQUEST = "common.auth_functions.prepare_request"
# Handling allowed hosts a little different since we have to turn it into a list.
# If providing a value, you just need to provide a comma separated string of hosts
# You don't need to quote anything or add [] yourself.
if SSL_ACTIVE:
    protocol = "https://"
else:
    protocol = "http://"

if env.__contains__("ALLOWED_HOSTS"):
    ALLOWED_HOSTS = env("ALLOWED_HOSTS").split(',')
    CSRF_TRUSTED_ORIGINS = []
    for host in ALLOWED_HOSTS:
        CSRF_TRUSTED_ORIGINS.append(protocol + host)
else:
    ALLOWED_HOSTS = ['*']
    CSRF_TRUSTED_ORIGINS = [protocol + '*.localhost', protocol + '*.127.0.0.1']

# Other Variables
DATA_UPLOAD_MAX_NUMBER_FIELDS = 2048
ROOT_URLCONF = 'opal.urls'
WSGI_APPLICATION = 'opal.wsgi.application'
ROOT_URLCONF = 'opal.urls'

# Version Numbering
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

try:
    opal.__build__ = subprocess.check_output(["git", "describe", "--tags", "--always"], cwd=BASE_DIR).decode('utf-8').strip()
except:
    opal.__build__ = opal.__version__ + " ?"

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR + '/templates'],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': ['django.template.context_processors.debug', 'django.template.context_processors.request',
                               'django.contrib.auth.context_processors.auth',
                               'django.contrib.messages.context_processors.messages', ],
        },
    }, ]


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        }
    }

if ENVIRONMENT == "production":
    SECURE_SSL_REDIRECT = True
else:
    print("Running in Development mode!")
    for k, v in sorted(os.environ.items()):
        print(k + ':', v)

# Application definition

# These are the applications defined in opal and map to OSCAL models.
# We track them separately here because we use this list for some functions
# that have to cycle through all apps
USER_APPS = ['common', 'catalog', 'ctrl_profile', 'component', 'ssp', ]

INSTALLED_APPS = ['django.contrib.admin', 'django.contrib.contenttypes','django.contrib.auth','django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles', "bootstrap5", 'celery_progress', 'extra_views', 'ckeditor']

# Auth apps defined separately so that they can be selectively disabled in the future
AUTHENTICATION_BACKENDS = []
if ENABLE_SAML:
    INSTALLED_APPS.append('sp')
    AUTHENTICATION_BACKENDS.append('sp.backends.SAMLAuthenticationBackend')
    REQUIRE_LOGIN_PUBLIC_NAMED_URLS = (LOGIN_URL, LOGOUT_URL,'admin:login')
    REQUIRE_LOGIN_PUBLIC_URLS = ()
    # SAML_PROVIDERS must be a comma seperated list of idp stubs that will be used in the application
    saml_provider_list = SAML_PROVIDERS.split(",")
    for idp in saml_provider_list:
        saml_urls = ['/sso/idp/', '/sso/idp/login/', '/sso/idp/test/', '/sso/idp/verify/', '/sso/idp/acs/']
        for url in saml_urls:
            REQUIRE_LOGIN_PUBLIC_URLS += (url.replace('idp',idp),)
if ENABLE_DJANGO_AUTH:
    AUTHENTICATION_BACKENDS.append('django.contrib.auth.backends.ModelBackend')

DEV_APPS = ['django_extensions', ]

# Add the user defined applications to INSTALLED_APPS
INSTALLED_APPS.extend(USER_APPS)

if ENVIRONMENT == "development":
    INSTALLED_APPS.extend(DEV_APPS)

MIDDLEWARE = ['django.middleware.security.SecurityMiddleware',
              'django.contrib.sessions.middleware.SessionMiddleware',
              'django.middleware.common.CommonMiddleware',
              'django.middleware.csrf.CsrfViewMiddleware',
              'django.contrib.auth.middleware.AuthenticationMiddleware',
              'django.contrib.messages.middleware.MessageMiddleware',
              'django.middleware.clickjacking.XFrameOptionsMiddleware',
              ]

if ENVIRONMENT != 'development':
    MIDDLEWARE.append("django_require_login.middleware.LoginRequiredMiddleware")


# To enable sitewide caching
# MIDDLEWARE_FOR_CACHE = ['django.middleware.cache.UpdateCacheMiddleware', 'django.middleware.common.CommonMiddleware', 'django.middleware.cache.FetchFromCacheMiddleware',]
# MIDDLEWARE.extend(MIDDLEWARE_FOR_CACHE)

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators


AUTH_PASSWORD_VALIDATORS = [{
    'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    }, {
    'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    }, {
    'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    }, {
    'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    }, ]

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
if DATABASE == "postgres":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', 'NAME': env('DB_NAME'), 'USER': env('DB_USER'),
            'PASSWORD': env('DB_PASSWORD'), 'HOST': env('DB_HOST'), 'PORT': env('DB_PORT'),
            }
        }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3', 'NAME': os.path.join(BASE_DIR, DB_NAME),
            }
        }

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


class auto_reload_filter(logging.Filter):
    """
    This is a filter which removes autoreload.py messages
    """

    def filter(self, record):
        if record.filename == 'autoreload.py':
            return False
        else:
            return True


# Logging Information
LOGGING = {
    'version': 1,
    # Version of logging
    'disable_existing_loggers': False,
    # disable logging
    # Formatters ###########################################################
    'formatters': {
        'verbose': {
            'format': '{levelname} : {asctime} : {filename} line {lineno} in function {funcName} : {message}',
            'style': '{',
            },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
            },
        },
    # Filters ####################################################################
    'filters': {
        'autoreload': {
            '()': auto_reload_filter,
            },
        },
    # Handlers #############################################################
    'handlers': {
        # 'file': {
        #     'level': LOG_LEVEL,
        #     'class': 'logging.FileHandler',
        #     'filename': LOG_FILE,
        #     'formatter': 'verbose',
        #     'filters': ['autoreload']
        #     },
        'console': {
            'class': 'logging.StreamHandler',
            'level': LOG_LEVEL,
            'formatter': 'verbose',
            'filters': ['autoreload']
            },
        },
    # Loggers ####################################################################
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': LOG_LEVEL
            },
        # 'debug': {
        #     'handlers': ['console'],
        #     'propagate': True,
        #     'level': 'DEBUG'
        #     },
        # 'werkzeug': {
        #     'handlers': ['console'],
        #     'level': 'DEBUG',
        #     'propagate': True,
        #     },
        },
    }
