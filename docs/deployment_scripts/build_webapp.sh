#!/usr/bin/env bash

VER_NUM=$(git describe --tags --always | cut -d "-" -f3)

# If container is running, stop and delete it
docker stop $(docker ps | grep opal | cut -f1 -d " ")
docker rm $(docker ps -a | grep opal | cut -f1 -d " ")


docker build -t opal:$VER_NUM ../../.
docker run --rm -it --name opal -p 8000:8000 -e LOG_LEVEL=WARNING opal:$VER_NUM