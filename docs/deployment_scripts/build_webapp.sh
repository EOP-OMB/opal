#!/usr/bin/env bash

docker stop $(docker ps | grep opal | cut -f1 -d " ")
docker rm $(docker ps -a | grep opal | cut -f1 -d " ")

docker build -t opal ../../.
docker run --rm -it --name opal -p 8000:8000 -e LOG_LEVEL=WARNING opal