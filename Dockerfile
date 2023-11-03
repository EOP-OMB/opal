FROM python:3.11-slim AS base_os
#FROM python:3.12.0a3-slim as base_os
#FROM registry.access.redhat.com/ubi9/python-39:1-90.1669637098 as base_os

USER root

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set a directory for the app
WORKDIR /usr/src/app

# install dependencies
RUN apt update
RUN apt upgrade -y
RUN apt install -y --no-install-recommends postgresql-client postgresql-contrib libpq-dev build-essential pkg-config libxml2-dev libxmlsec1-dev libxmlsec1-openssl apache2 apache2-dev
RUN apt clean
RUN rm -rf /var/lib/apt/lists/*

#RUN yum -y install --disableplugin=subscription-manager \
#  libxml2-devel xmlsec1 \
#  && yum --disableplugin=subscription-manager clean all


# Create Service account
RUN useradd -M -u 1001 opal
RUN chown -R opal:opal .

FROM base_os AS package_installer

#USER opal
WORKDIR /usr/src/app
#ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

COPY ./requirements.txt /usr/src/app
# install Python requirements
RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir -r requirements.txt --upgrade
RUN python -m pip install --no-cache-dir mod-wsgi

FROM package_installer AS app_installer

USER root
WORKDIR /usr/src/app

# copy all the files to the container
COPY . /usr/src/app/

# set permisions and execute bit for startup script
RUN chmod -R ugo+rX,ugo-w .
RUN chmod +x startup.sh
RUN chown -R opal:opal .

# grant write permisions on the static driectory
RUN mkdir -p /usr/src/app/static
RUN chmod 744 /usr/src/app/static
RUN chown -R opal:opal ./static

# grant write permisions on the static driectory
RUN mkdir -p /usr/src/app/media
RUN chmod 744 /usr/src/app/media
RUN chown -R opal:opal ./media

#Create a logs directory if needed
RUN mkdir -p /usr/src/logs
RUN chmod 740 /usr/src/logs
RUN chown -R opal:opal /usr/src/logs

#Create a data directory if needed
RUN mkdir -p /usr/src/data
RUN chmod 740 /usr/src/data
RUN chown -R opal:opal /usr/src/data


FROM app_installer AS final_stage
# run as an unprivileged user
USER opal
WORKDIR /usr/src/app

# use -p 8000:8000 with `docker run` to access the service
EXPOSE 8000

CMD ./startup.sh