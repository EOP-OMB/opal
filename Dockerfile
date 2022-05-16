FROM python:3.8-slim-buster as stage1

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set a directory for the app
WORKDIR /usr/src/app

# install dependencies
RUN apt-get update && apt-get upgrade -y\
  && apt-get install -y --no-install-recommends apache2 apache2-dev python3-venv libxslt1-dev libxml2-dev python-libxml2 python3-dev python-setuptools unixodbc-dev \
  # To include support for postgres
  && apt-get install -y --no-install-recommends python-pip python-dev libpq-dev postgresql-client postgresql-contrib \
  # To include support for SAML
  && apt-get install -y libxml2-dev libxmlsec1-dev libxmlsec1-openssl \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*


# install Python requirements
COPY requirements.txt /usr/src/app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir mod-wsgi
# To include support for postgres
RUN pip install --no-cache-dir psycopg2

# Create Service account
RUN useradd -r -u 1001 opal

# copy all the files to the container
COPY . /usr/src/app/
RUN chown -R opal:opal .
RUN chmod u+x startup.sh

FROM stage1
# run as an unprivileged user
USER opal

# use -p 8000:8000 with `docker run` to access the service
EXPOSE 8000

CMD ./startup.sh
