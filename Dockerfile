FROM python:3.8-slim-buster as stage1

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set a directory for the app
WORKDIR /usr/src/app

# install dependencies
RUN apt update && apt-get upgrade -y
RUN apt install -y --no-install-recommends postgresql-client postgresql-contrib libpq-dev build-essential pkg-config libxml2-dev libxmlsec1-dev libxmlsec1-openssl apache2 apache2-dev
# RUN apt install -y --no-install-recommends apache2 apache2-dev python3-venv libxslt1-dev libxml2-dev python-libxml2 python3-dev python-setuptools unixodbc-dev
# To include support for postgres
# RUN apt install -y --no-install-recommends python-pip python-dev libpq-dev postgresql-client postgresql-contrib
# To include support for SAML
# RUN apt install -y python3-pip xmlsec libssl-dev libsasl2-dev
RUN apt clean
RUN rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /usr/src/app
# install Python requirements
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir mod-wsgi

# Create Service account
RUN useradd -r -u 1001 opal

# copy all the files to the container
COPY . /usr/src/app/

# set ownership to service account and execute bit for statup script
RUN chown -R opal:opal .
RUN chmod u+x startup.sh

FROM stage1 as stage2
# run as an unprivileged user
USER opal

# use -p 8000:8000 with `docker run` to access the service
EXPOSE 8000

CMD ./startup.sh

