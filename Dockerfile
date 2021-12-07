FROM python:3.8-slim-buster as stage1

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set a directory for the app
WORKDIR /usr/src/app

# install dependencies
RUN apt-get update \
  && apt-get install -y --no-install-recommends apache2 apache2-dev postgresql-client python3-venv libxslt1-dev libxml2-dev python-libxml2 python3-dev python-setuptools unixodbc-dev \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# install Python requirements
COPY requirements.txt /usr/src/app/
RUN pip3 install --no-cache-dir -r requirements.txt

# fix permisions on binary_database_fiels migration
RUN chmod -R 777 /usr/local/lib/python3.8/site-packages/binary_database_files/migrations/


# copy all the files to the container
COPY . /usr/src/app/
RUN chown -R www-data:www-data .
RUN chmod u+x startup.sh

FROM stage1
# run as an unprivileged user
USER www-data

#RUN touch db.sqlite3
#RUN python3 manage.py makemigrations admin ssp
#RUN python3 manage.py migrate admin
#RUN python3 manage.py migrate ssp
#RUN python3 manage.py loaddata admin_user.json fixture_information_type.json fixture_status.json fixture_user_function.json fixture_user_privilege.json fixture_user_role.json
#RUN python3 manage.py collectstatic --noinput
#RUN chown -R www-data:www-data .


# use -p 8000:8000 with `docker run` to access the service
EXPOSE 8000

ENV log_level DEBUG

# CMD ["mod_wsgi-express", "start-server", "--user", "www-data", "--group", "www-data", "opal/wsgi.py"]
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ./startup.sh
