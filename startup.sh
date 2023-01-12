#!/bin/bash

set -e

python manage.py migrate --noinput
python manage.py bootstrap --noinput
python manage.py collectstatic --noinput

#mod_wsgi-express start-server opal/wsgi.py
mod_wsgi-express start-server --url-alias /static static opal/wsgi.py
