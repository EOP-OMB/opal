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

#RUN python3 -m venv /usr/src/app/venv
#RUN source venv/bin/activate

# install Python requirements
COPY requirements.txt /usr/src/app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir mod-wsgi

# Create Service account
RUN useradd -r opal

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
