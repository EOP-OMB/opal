#!/usr/bin/env bash

docker stop $(docker ps | grep opaldb | cut -f1 -d " ")
docker rm $(docker ps -a | grep opaldb | cut -f1 -d " ")

docker volume rm postgresql_data

docker build -t opal-db ../postgres/.
docker volume create postgresql_data
docker run -it -d -p 5432:5432 --name opaldb  -v postgresql_data:/var/lib/postgresql/data -e POSTGRES_PASSWORD=use_a_secure_password_here -e POSTGRES_OPAL_PASSWORD=password opal-db