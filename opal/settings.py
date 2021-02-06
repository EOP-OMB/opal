"""
Django settings for opal project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os

#Path variables for application
BASE_DIR = str(Path(__file__).resolve(strict=True).parent.parent)
STATIC_ROOT = BASE_DIR + '/static'
MEDIA_ROOT = BASE_DIR + '/uploads'
MEDIA_URL = '/uploads/'
IMPORTED_CATALOGS_DIR = 'catalogs/'

#Set reasonable defaults for environment values
env_defaults = {
    "env" : "development",
    "opal_secret_key" : "klchwf98p23hd81&*^*&D(Hohdqp98yphP97gp:GF2837189YB12;O",
    "debug" : "False",
    "allowed_hosts" : ["*"],
    "database" : "sqlite",
    "db_name" : "opal_prod",
    "db_user" : "opal",
    "db_password" : "use_a_strong_password",
    "db_host" : "localhost",
    "db_port" : ""
}

from opal.local_settings import env

for k in env_defaults:
    if k not in env:
        env[k] = env_defaults[k]
        print("No value found for variable ",k," using default value of " + str(env_defaults[k]))
    else:
        print("Value found for variable ",k," (",str(env[k]),")")

if env["env"] == "development":
    print("Running in Development mode!")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env["opal_secret_key"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env["debug"]
ALLOWED_HOSTS = env["allowed_hosts"]


# Application definition

INSTALLED_APPS = [
    'django_auth_adfs',
    'dal',
    'dal_select2',
    'dal_queryset_sequence',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tinymce',
    'ssp.apps.ssp',
    'django_extensions',
    'fixture_magic',
    'rest_framework',
    'rest_framework_tricks',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',]

if env["env"] == "production":
    # With this you can force a user to login without using
    # the LoginRequiredMixin on every view class
    #
    # You can specify URLs for which login is not enforced by
    # specifying them in the LOGIN_EXEMPT_URLS setting.
    MIDDLEWARE.append('django_auth_adfs.middleware.LoginRequiredMiddleware',)

ROOT_URLCONF = 'opal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'opal.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases


if env["database"] == "sqlite":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR + '/db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': env['db_name'],
            'USER': env['db_user'],
            'PASSWORD': env["db_password"],
            'HOST': env["db_host"],
            'PORT': env["db_port"],
        }
    }

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'rest_framework_json_api.exceptions.exception_handler',
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework_json_api.pagination.JsonApiPageNumberPagination',
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework_json_api.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework_json_api.renderers.JSONRenderer',
        # If you're performance testing, you will want to use the browseable API
        # without forms, as the forms can generate their own queries.
        # If performance testing, enable:
        # 'example.utils.BrowsableAPIRendererWithoutForms',
        # Otherwise, to play around with the browseable API, enable:
        'rest_framework.renderers.BrowsableAPIRenderer'
    ),
    'DEFAULT_METADATA_CLASS': 'rest_framework_json_api.metadata.JSONAPIMetadata',
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework_json_api.filters.QueryParameterValidationFilter',
        'rest_framework_json_api.filters.OrderingFilter',
        'rest_framework_json_api.django_filters.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
    ),
    'SEARCH_PARAM': 'filter[search]',
    'TEST_REQUEST_RENDERER_CLASSES': (
        'rest_framework_json_api.renderers.JSONRenderer',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'vnd.api+json'
}


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'EST'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
DATA_UPLOAD_MAX_NUMBER_FIELDS = 2048


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    )

if env["env"] == "production":
    AUTHENTICATION_BACKENDS = (
    'django_auth_adfs.backend.AdfsAuthCodeBackend',
    )

# checkout the documentation for more settings
AUTH_ADFS = {
    "SERVER": "adfs.omb.gov",
    "CLIENT_ID": "3fbddfb7-bb0a-4eb8-9b8d-756a52e4e6b7",
    "RELYING_PARTY_ID": "3fbddfb7-bb0a-4eb8-9b8d-756a52e4e6b7",
    # Make sure to read the documentation about the AUDIENCE setting
    # when you configured the identifier as a URL!
    "AUDIENCE": "microsoft:identityserver:3fbddfb7-bb0a-4eb8-9b8d-756a52e4e6b7",
    # "CA_BUNDLE": "/path/to/ca-bundle.pem",
    "CLAIM_MAPPING": {"first_name": "given_name",
                      "last_name": "family_name",
                      "email": "email"},
    "USERNAME_CLAIM": "upn",
    "GROUP_CLAIM": "group"
    }

if env["env"] == "production":
    # Configure django to redirect users to the right URL for login
    LOGIN_URL = "django_auth_adfs:login"
    LOGIN_REDIRECT_URL = "/"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR + '/debug.log',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file','console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
