#!/bin/bash -x

set -e

python manage.py migrate --noinput
python manage.py collectstatic --noinput

#mod_wsgi-express start-server opal/wsgi.py
#mod_wsgi-express start-server --url-alias /static static  --url-alias /media media opal/wsgi.py
gunicorn opal.wsgi:application --bind 0.0.0.0:8000
