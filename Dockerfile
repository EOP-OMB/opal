FROM python:3.8-buster
# set a directory for the app
WORKDIR /usr/src/app

# copy all the files to the container
COPY . .

# install dependencies
RUN apt update && apt install -y python3-venv apache2 apache2-dev libxslt1-dev libxml2-dev python-libxml2 python3-dev python-setuptools unixodbc-dev python3-pip
# install dependencies for PostGRESQL DB
# RUN apt install -y libpq-dev postgresql postgresql-contrib
RUN mv opal/local_settings.py.docker opal/local_settings.py
RUN pip3 install -r requirements.txt
RUN touch db.sqlite3
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
RUN python3 manage.py loaddata admin_user.json fixture_information_type.json fixture_status.json fixture_user_function.json fixture_user_privilege.json fixture_user_role.json
RUN python3 manage.py collectstatic --noinput
RUN chown -R www-data:www-data *

EXPOSE 8000

CMD python3 manage.py runserver