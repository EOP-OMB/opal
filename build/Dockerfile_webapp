FROM python:3.11-slim AS base_os
#FROM python:3.12.0a3-slim as base_os
#FROM registry.access.redhat.com/ubi9/python-39:1-90.1669637098 as base_os

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set a directory for the app
WORKDIR /usr/src/app

# copy all the files to the container
COPY . /usr/src/app/

RUN pip install ansible
RUN ansible-playbook playbook.yml

FROM base_os AS final_stage
# run as an unprivileged user
USER opal
WORKDIR /usr/src/app

# use -p 8000:8000 with `docker run` to access the service
EXPOSE 8000

CMD ./startup.sh