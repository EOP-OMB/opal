FROM python:3.11-slim as base_os
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
RUN useradd opal
RUN chown -R opal:opal .

FROM base_os as package_installer

#USER opal
WORKDIR /usr/src/app
#ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

COPY ./requirements.txt /usr/src/app
# install Python requirements
RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir -r requirements.txt --upgrade
RUN python -m pip install --no-cache-dir mod-wsgi

FROM package_installer as app_installer

USER root
WORKDIR /usr/src/app

# copy all the files to the container
COPY . /usr/src/app/

# set permisions and execute bit for statup script
RUN chmod -R o+r .
RUN chmod +x startup.sh
RUN mkdir -p /usr/src/logs
RUN mkdir -p /usr/src/app/static
RUN chmod 777 /usr/src/logs
RUN chmod 777 /usr/src/app/static
RUN chown -R opal:opal ./static
RUN chown -R opal:opal /usr/src/logs


FROM app_installer as final_stage
# run as an unprivileged user
USER opal
WORKDIR /usr/src/app

# use -p 8000:8000 with `docker run` to access the service
EXPOSE 8000

CMD ./startup.sh