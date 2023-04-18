import uuid

from opal.settings import *


DB_NAME = str(uuid.uuid4()) + '.testdb'

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3', 'NAME': os.path.join(BASE_DIR, DB_NAME),
            }
        }

print("Using database %s" % os.path.join(BASE_DIR, DB_NAME))