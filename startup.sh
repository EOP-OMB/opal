#!/bin/bash

python3 manage.py makemigrations --noinput admin auth contenttypes sessions ssp common catalog
python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput

mod_wsgi-express start-server opal/wsgi.py