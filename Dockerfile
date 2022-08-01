FROM python:3.8-slim-buster as stage1

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set a directory for the app
WORKDIR /usr/src/app

# install dependencies
RUN apt update
RUN apt-get upgrade -y
RUN apt install -y --no-install-recommends postgresql-client postgresql-contrib libpq-dev build-essential pkg-config libxml2-dev libxmlsec1-dev libxmlsec1-openssl apache2 apache2-dev git
RUN apt clean
RUN rm -rf /var/lib/apt/lists/*

# Create Service account
RUN useradd -r -u 1001 opal

FROM stage1 as stage2

USER opal

RUN python -m venv venv
RUN source venv/bin/activate

COPY ./requirements.txt /usr/src/app
# install Python requirements
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
# RUN python -m pip install git+https://github.com/cs4p/django-saml-sp.git
RUN pip install --no-cache-dir mod-wsgi

# copy all the files to the container
COPY . /usr/src/app/

# set ownership to service account and execute bit for statup script
RUN chown -R opal:opal .
RUN chmod u+x startup.sh

FROM stage2 as stage3
# run as an unprivileged user
USER opal

RUN source venv/bin/activate

# use -p 8000:8000 with `docker run` to access the service
EXPOSE 8000

CMD ./startup.sh