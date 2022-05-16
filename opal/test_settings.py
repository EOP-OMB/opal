from opal.settings import *

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3', 'NAME': os.path.join(BASE_DIR, DB_NAME),
            }
        }