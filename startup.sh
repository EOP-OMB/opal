#!/bin/bash

python3 manage.py makemigrations --noinput admin auth binary_database_files contenttypes sessions ssp
python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput

mod_wsgi-express start-server opal/wsgi.py