FROM python:3.8-slim-buster as base_os

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set a directory for the app
WORKDIR /usr/src/app

# install dependencies
RUN apt update
RUN apt upgrade -y
RUN apt install -y --no-install-recommends postgresql-client postgresql-contrib libpq-dev build-essential pkg-config libxml2-dev libxmlsec1-dev libxmlsec1-openssl apache2 apache2-dev git
RUN apt clean
RUN rm -rf /var/lib/apt/lists/*

# Create Service account
RUN useradd -u 1001 opal
RUN mkdir /home/opal
RUN chown -R opal:opal .
RUN chown -R opal:opal /home/opal

FROM base_os as package_installer

#USER opal
WORKDIR /usr/src/app
#ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

COPY ./requirements.txt /usr/src/app
# install Python requirements
RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir -r requirements.txt
RUN python -m pip install --no-cache-dir mod-wsgi

FROM package_installer as app_installer

USER root
WORKDIR /usr/src/app

# copy all the files to the container
COPY . /usr/src/app/

# set ownership to service account and execute bit for statup script
RUN chmod -R 705 .
RUN chown -R opal:opal ./static
#RUN chmod +x startup.sh

FROM app_installer as final_stage
# run as an unprivileged user
USER opal
WORKDIR /usr/src/app

# use -p 8000:8000 with `docker run` to access the service
EXPOSE 8000

CMD ./startup.sh