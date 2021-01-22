FROM python:3.8-buster
# set a directory for the app
WORKDIR /usr/src/app

# copy all the files to the container
COPY . .

# install dependencies
RUN apt update && apt install -y python3-venv apache2 apache2-dev libxslt1-dev libxml2-dev python-libxml2 python3-dev python-setuptools unixodbc-dev python3-pip
# install dependencies for PostGRESQL DB
RUN sudo apt-get install libpq-dev postgresql postgresql-contrib
RUN pip3 install -r requirements.txt
# mod-wsgi is used in the docker container but if deployed on a real server use apache instead
RUN pip3 install mod-wsgi
RUN touch db.sqlite3
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
RUN python3 manage.py loaddata admin_user.json
RUN python3 manage.py collectstatic --noinput
RUN chown -R www-data:www-data *

EXPOSE 80

CMD python3 manage.py runmodwsgi --user www-data --group www-data