import os

PROJECT_DIR = os.path.dirname(__file__)

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3"}}

ROOT_URLCONF = "binary_database_files.urls"

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "binary_database_files",
    "binary_database_files.tests",
]

MEDIA_ROOT = os.path.join(PROJECT_DIR, "media")

USE_TZ = True

SECRET_KEY = "secret"

AUTH_USER_MODEL = "auth.User"

SITE_ID = 1

BASE_SECURE_URL = "https://localhost"

BASE_URL = "http://localhost"

MIDDLEWARE_CLASSES = (
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    # 'django.middleware.transaction.TransactionMiddleware',
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.locale.LocaleMiddleware",
)
