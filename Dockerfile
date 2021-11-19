FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set a directory for the app
WORKDIR /usr/src/app

# install dependencies
RUN apt-get update \
  && apt-get install -y --no-install-recommends apache2 apache2-dev python3-venv libxslt1-dev libxml2-dev python-libxml2 python3-dev python-setuptools unixodbc-dev \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# install dependencies for PostGRESQL DB
# RUN apt-get install -y --no-install-recommends libpq-dev postgresql postgresql-contrib && apt-get clean && rm -rf /var/lib/apt/lists/*

# install Python requirements
COPY requirements.txt /usr/src/app/
RUN pip3 install --no-cache-dir -r requirements.txt

# copy all the files to the container
COPY . /usr/src/app/

RUN touch db.sqlite3 \
  && python3 manage.py makemigrations \
  && python3 manage.py migrate \
  && python3 manage.py loaddata admin_user.json fixture_information_type.json fixture_status.json fixture_user_function.json fixture_user_privilege.json fixture_user_role.json \
  && python3 manage.py collectstatic --noinput \
  && chown -R www-data:www-data .

# run as an unprivileged user
# USER www-data

# use -p 8000:8000 with `docker run` to access the service
EXPOSE 8000

CMD ["mod_wsgi-express", "start-server", "--user", "www-data", "--group", "www-data", "opal/wsgi.py"]
